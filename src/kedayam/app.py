"""Kedayam web app: server-rendered pages, no JavaScript, local only.

The server binds to 127.0.0.1 so other devices on the network cannot reach
it. Messages are processed in memory, never written to disk or logs.
"""

from __future__ import annotations

import os
import re
import secrets
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI, Form, Request
from fastapi.concurrency import run_in_threadpool
from fastapi.responses import HTMLResponse, PlainTextResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.formparsers import MultiPartParser

from . import classifier as clf
from . import family as fam
from . import ocr
from .engine import MAX_CHARS, Result, analyse
from .i18n import ABOUT, ACTION_TEXT, HOSTED_ABOUT_PRIVACY, LANG_NAMES, LANGS, RULE_TEXT, SOURCE_LINKS, lang_or_default, t
from .textutil import defang

HERE = Path(__file__).resolve().parent
templates = Jinja2Templates(directory=HERE / "templates")

# Keep uploaded screenshots in memory: Starlette would otherwise move uploads
# over 1 MB into a temporary file on disk.
MultiPartParser.spool_max_size = ocr.MAX_BYTES + 1024 * 1024
UPLOAD_LIMIT = ocr.MAX_BYTES + 64 * 1024

CSP = (
    "default-src 'none'; style-src 'self'; img-src 'self' data:; form-action 'self'; "
    "base-uri 'none'; frame-ancestors 'none'"
)


@asynccontextmanager
async def lifespan(_: FastAPI):
    clf.load()  # train or load once, so the first check is quick
    yield


app = FastAPI(title="Kedayam", docs_url=None, redoc_url=None, openapi_url=None, lifespan=lifespan)
app.mount("/static", StaticFiles(directory=HERE / "static"), name="static")


# Kedayam only ever runs on this computer. Refusing other Host names blocks
# DNS rebinding, and refusing cross-site form posts stops a web page you visit
# from silently changing the family contact number.
ALLOWED_HOSTS = {"127.0.0.1", "localhost", "testserver"}
# The public demo (KEDAYAM_HOSTED=1) also accepts its own host name, given in KEDAYAM_ALLOWED_HOSTS.
HOSTED = fam.HOSTED
ALLOWED_HOSTS |= {h.strip().lower() for h in os.environ.get("KEDAYAM_ALLOWED_HOSTS", "").split(",") if h.strip()}
COOKIE = "kedayam_id"


def _host_only(value: str) -> str:
    value = value.strip().lower()
    if value.startswith("["):
        return value.split("]")[0] + "]"
    return value.rsplit(":", 1)[0] if value.count(":") == 1 else value


@app.middleware("http")
async def security_headers(request: Request, call_next):
    host = request.headers.get("host", "")
    if _host_only(host) not in ALLOWED_HOSTS:
        return PlainTextResponse("Kedayam only accepts requests from this computer.", status_code=400)
    if request.method == "POST":
        origin = request.headers.get("origin")
        if origin is not None:
            origin_host = origin.split("://", 1)[-1]
            if origin == "null" or origin_host.lower() != host.lower():
                return PlainTextResponse("Form posts from other websites are not accepted.", status_code=403)
    fresh = False
    if HOSTED:  # each browser gets its own in-memory family setup
        owner = request.cookies.get(COOKIE, "")
        fresh = not re.fullmatch(r"[A-Za-z0-9_-]{16,64}", owner)
        if fresh:
            owner = secrets.token_urlsafe(18)
        token = fam.OWNER.set(owner)
    try:
        response = await call_next(request)
    finally:
        if HOSTED:
            fam.OWNER.reset(token)
    if fresh:
        response.set_cookie(COOKIE, owner, httponly=True, samesite="lax", secure=True, max_age=7 * 24 * 3600)
    response.headers["Content-Security-Policy"] = CSP
    response.headers["Cache-Control"] = "no-store"
    # same-origin, not no-referrer: with no-referrer Chrome sends "Origin: null"
    # on our own form posts, which the cross-site check above would refuse.
    # Other sites still receive no referrer.
    response.headers["Referrer-Policy"] = "same-origin"
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["Permissions-Policy"] = "camera=(), microphone=(), geolocation=()"
    return response


def base_context(request: Request, lang: str, **extra) -> dict:
    lang = lang_or_default(lang)
    ctx = {
        "request": request,
        "lang": lang,
        "langs": LANGS,
        "lang_names": LANG_NAMES,
        "t": lambda key, **kw: t(lang, key, **kw),
        "max_chars": MAX_CHARS,
        "ocr_ready": ocr.available(),
        "family": fam.load(),
    }
    ctx["family_form"] = dict(vars(ctx["family"])) if ctx["family"] else {}
    ctx.update(extra)
    return ctx


def present(result: Result, lang: str) -> dict:
    def finding(f):
        title, why = RULE_TEXT[f.id][lang]
        src_name, src_url = SOURCE_LINKS[f.rule.source]
        return {
            "id": f.id,
            "weight": f.weight,
            "title": title,
            "why": why,
            "evidence": [defang(e) for e in f.evidence],
            "source_name": src_name,
            "source_url": src_url,
        }

    c = result.classifier
    return {
        "level": result.level,
        "findings": [finding(f) for f in result.findings],
        "tips": [finding(f) for f in result.tips],
        "actions": [ACTION_TEXT[a][lang] for a in result.actions],
        "classifier_used": c.used,
        "classifier_pct": None if c.score is None else round(c.score * 100),
        "message_safe": defang(result.message.raw),
        "rule_ids": [f.id for f in result.findings + result.tips],
    }


def default_lang(lang: str | None) -> str:
    if lang:
        return lang_or_default(lang)
    f = fam.load()
    return f.lang if f else "en"


@app.get("/", response_class=HTMLResponse)
async def home(request: Request, lang: str | None = None):
    lang = default_lang(lang)
    return templates.TemplateResponse(request, "index.html", base_context(request, lang))


@app.post("/check", response_class=HTMLResponse)
async def check(request: Request, text: str = Form(""), sender: str = Form(""), lang: str = Form("en")):
    lang = lang_or_default(lang)
    text = text.strip()
    if not text:
        return templates.TemplateResponse(
            request, "index.html", base_context(request, lang, error=t(lang, "empty")), status_code=400
        )
    if len(text) > MAX_CHARS:
        return templates.TemplateResponse(
            request,
            "index.html",
            base_context(request, lang, error=t(lang, "too_long", n=MAX_CHARS), text=text[:MAX_CHARS], sender=sender),
            status_code=400,
        )
    result = analyse(text, sender[:100])
    return templates.TemplateResponse(request, "result.html", base_context(request, lang, r=present(result, lang)))


@app.post("/check-image", response_class=HTMLResponse)
async def check_image(request: Request):
    lang = lang_or_default(request.query_params.get("lang"))

    def fail(key: str, status: int = 400):
        return templates.TemplateResponse(
            request, "index.html", base_context(request, lang, error=t(lang, key)), status_code=status
        )

    try:
        declared = int(request.headers.get("content-length", "0"))
    except ValueError:
        declared = 0
    if declared > UPLOAD_LIMIT:
        return fail("ocr_too_big", 413)
    async with request.form(max_files=1, max_fields=3) as form:
        lang = lang_or_default(str(form.get("lang") or lang))
        upload = form.get("image")
        if upload is None or isinstance(upload, str):
            return fail("ocr_not_image")
        data = await upload.read(UPLOAD_LIMIT + 1)
    if len(data) > ocr.MAX_BYTES:
        return fail("ocr_too_big", 413)
    read = await run_in_threadpool(ocr.read_image, data)
    del data
    if read.error:
        return fail(read.error, 503 if read.error == "ocr_not_setup" else 400)
    result = analyse(read.text)
    little = sum(c.isalpha() for c in read.text) < 40
    return templates.TemplateResponse(
        request,
        "result.html",
        base_context(request, lang, r=present(result, lang), ocr_text=read.text, little_text=little),
    )


@app.get("/family", response_class=HTMLResponse)
async def family_page(request: Request, lang: str | None = None, msg: str | None = None):
    lang = default_lang(lang)
    note = t(lang, msg) if msg in ("family_saved", "family_removed") else None
    return templates.TemplateResponse(request, "family.html", base_context(request, lang, note=note))


@app.post("/family", response_class=HTMLResponse)
async def family_save(
    request: Request,
    lang: str = Form("en"),
    parent_lang: str = Form("en"),
    name: str = Form(""),
    phone: str = Form(""),
    bank: str = Form(""),
    bank_phone: str = Form(""),
):
    lang = lang_or_default(lang)
    f = fam.validate(parent_lang, name, phone, bank, bank_phone)
    if f is None:
        ctx = base_context(request, lang, error=t(lang, "family_invalid"))
        ctx["form"] = {"parent_lang": parent_lang, "name": name, "phone": phone, "bank": bank, "bank_phone": bank_phone}
        return templates.TemplateResponse(request, "family.html", ctx, status_code=400)
    fam.save(f)
    return RedirectResponse(f"/family?lang={f.lang}&msg=family_saved", status_code=303)


@app.post("/family/remove")
async def family_remove(request: Request, lang: str = Form("en")):
    fam.clear()
    return RedirectResponse(f"/family?lang={lang_or_default(lang)}&msg=family_removed", status_code=303)


@app.get("/family/card", response_class=HTMLResponse)
async def family_card(request: Request, lang: str | None = None):
    lang = default_lang(lang)
    return templates.TemplateResponse(request, "card.html", base_context(request, lang))


def about_text(lang: str) -> dict:
    a = ABOUT[lang_or_default(lang)]
    return {**a, "privacy": HOSTED_ABOUT_PRIVACY[lang_or_default(lang)]} if HOSTED else a


@app.get("/about", response_class=HTMLResponse)
async def about(request: Request, lang: str | None = None):
    lang = default_lang(lang)
    meta_path = clf.META_PATH
    meta = None
    if meta_path.exists():
        import json

        meta = json.loads(meta_path.read_text())
    return templates.TemplateResponse(
        request, "about.html", base_context(request, lang, sources=SOURCE_LINKS, meta=meta, a=about_text(lang))
    )


@app.get("/health")
async def health():
    return {"ok": True}


def main() -> None:
    import uvicorn

    import socket
    import sys

    port = int(os.environ.get("KEDAYAM_PORT", "8740"))
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        if s.connect_ex(("127.0.0.1", port)) == 0:
            sys.exit(f"Port {port} is already in use. Start Kedayam on another port, for example: KEDAYAM_PORT={port + 1} uv run kedayam")
    clf.load()
    print(f"Kedayam is running. Open http://127.0.0.1:{port} in your browser. Press Ctrl+C to stop.", flush=True)
    uvicorn.run(app, host="127.0.0.1", port=port, access_log=False, log_level="warning")


if __name__ == "__main__":
    main()
