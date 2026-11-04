"""Kedayam web app: server-rendered pages, no JavaScript, local only.

The server binds to 127.0.0.1 so other devices on the network cannot reach
it. Messages are processed in memory, never written to disk or logs.
"""

from __future__ import annotations

import os
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI, Form, Request
from fastapi.concurrency import run_in_threadpool
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.formparsers import MultiPartParser

from . import classifier as clf
from . import ocr
from .engine import MAX_CHARS, Result, analyse
from .i18n import ACTION_TEXT, LANG_NAMES, LANGS, RULE_TEXT, SOURCE_LINKS, lang_or_default, t
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


@app.middleware("http")
async def security_headers(request: Request, call_next):
    response = await call_next(request)
    response.headers["Content-Security-Policy"] = CSP
    response.headers["Cache-Control"] = "no-store"
    response.headers["Referrer-Policy"] = "no-referrer"
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
    }
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


@app.get("/", response_class=HTMLResponse)
async def home(request: Request, lang: str = "en"):
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


@app.get("/about", response_class=HTMLResponse)
async def about(request: Request, lang: str = "en"):
    meta_path = clf.META_PATH
    meta = None
    if meta_path.exists():
        import json

        meta = json.loads(meta_path.read_text())
    return templates.TemplateResponse(
        request, "about.html", base_context(request, lang, sources=SOURCE_LINKS, meta=meta)
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
