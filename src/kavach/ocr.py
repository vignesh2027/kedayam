"""Read text from a screenshot with Tesseract (English, Tamil, Hindi).

The image is processed in memory: it is decoded with Pillow, re-encoded as
PNG and passed to the tesseract program on stdin. Nothing is written to
disk. Tesseract language data is downloaded once by `uv run kavach-ocr-setup`
into vendor/tessdata and checked against pinned SHA-256 hashes.
"""

from __future__ import annotations

import hashlib
import io
import re
import shutil
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path

from PIL import Image, ImageOps, UnidentifiedImageError

ROOT = Path(__file__).resolve().parents[2]
TESSDATA = ROOT / "vendor" / "tessdata"
LANGS = "eng+tam+hin"
MAX_BYTES = 8 * 1024 * 1024
MAX_PIXELS = 40_000_000
TIMEOUT_S = 30
MIN_WIDTH = 900

# tessdata_fast models, Apache License 2.0, https://github.com/tesseract-ocr/tessdata_fast
MODELS = {
    "eng": "7d4322bd2a7749724879683fc3912cb542f19906c83bcc1a52132556427170b2",
    "tam": "d02fbec24be4b07e32e80d0ccfc3b6b67a3c5d61c9d0a7c8532677990912c6ec",
    "hin": "4c73ffc59d497c186b19d1e90f5d721d678ea6b2e277b719bee4e2af12271825",
}
MODEL_URL = "https://github.com/tesseract-ocr/tessdata_fast/raw/main/{lang}.traineddata"


@dataclass
class OcrResult:
    text: str = ""
    error: str | None = None  # a key in i18n.UI, for example "ocr_not_image"


def tesseract_bin() -> str | None:
    return shutil.which("tesseract")


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def models_ok() -> bool:
    return all((TESSDATA / f"{lang}.traineddata").exists() for lang in MODELS)


def available() -> bool:
    return tesseract_bin() is not None and models_ok()


# Status bars ("10:42 4G 72%") and similar phone chrome are not part of the message.
_STATUS_BAR = re.compile(r"^.{0,30}\d{1,3}\s?%\s*$")


def _is_status_bar(line: str) -> bool:
    """Clock, network and battery lines: short, end in a percentage, almost no letters."""
    return bool(_STATUS_BAR.match(line)) and sum(c.isalpha() for c in line) <= 4
# A link broken at the end of a line ("http://sbi-kyc-" + "update.xyz/login").
_URLISH = re.compile(r"(?:https?://|www\.|\.[a-z]{2,6}/)\S*$|^\S*https?://\S*$", re.IGNORECASE)


def clean_ocr_text(raw: str) -> str:
    # Tesseract puts zero-width joiners inside Tamil words; they only affect drawing.
    raw = raw.replace("\r", "").replace("\u200c", "").replace("\u200d", "")
    lines = [ln.rstrip() for ln in raw.split("\n")]
    lines = [ln for ln in lines if not _is_status_bar(ln)]
    out: list[str] = []
    for ln in lines:
        if out and out[-1] and ln.strip():
            prev = out[-1]
            last = prev.split()[-1]
            if last[-1] in "-/._=?&" and _URLISH.search(last):
                out[-1] = prev + ln.strip()
                continue
        out.append(ln)
    text = "\n".join(out)
    text = re.sub(r"\n{2,}", "\n", text)
    return text.strip()


def _prepare(data: bytes) -> bytes:
    Image.MAX_IMAGE_PIXELS = MAX_PIXELS
    with Image.open(io.BytesIO(data)) as im:
        im.load()
        im = ImageOps.exif_transpose(im)
        im = im.convert("RGB")
        if im.width < MIN_WIDTH:
            scale = MIN_WIDTH / im.width
            im = im.resize((MIN_WIDTH, max(1, round(im.height * scale))), Image.Resampling.LANCZOS)
        buf = io.BytesIO()
        im.save(buf, format="PNG")
        return buf.getvalue()


def read_image(data: bytes) -> OcrResult:
    if not data:
        return OcrResult(error="ocr_not_image")
    if len(data) > MAX_BYTES:
        return OcrResult(error="ocr_too_big")
    exe = tesseract_bin()
    if exe is None or not models_ok():
        return OcrResult(error="ocr_not_setup")
    try:
        png = _prepare(data)
    except (UnidentifiedImageError, Image.DecompressionBombError, OSError, ValueError):
        return OcrResult(error="ocr_not_image")
    try:
        proc = subprocess.run(
            [exe, "stdin", "stdout", "-l", LANGS, "--psm", "3", "--tessdata-dir", str(TESSDATA)],
            input=png,
            capture_output=True,
            timeout=TIMEOUT_S,
            check=False,
        )
    except subprocess.TimeoutExpired:
        return OcrResult(error="ocr_failed")
    if proc.returncode != 0:
        return OcrResult(error="ocr_failed")
    text = clean_ocr_text(proc.stdout.decode("utf-8", errors="replace"))
    if sum(c.isalpha() for c in text) < 3:
        return OcrResult(error="ocr_no_text")
    return OcrResult(text=text)


def setup_main() -> None:
    """Download and verify the Tesseract language data (run once)."""
    if tesseract_bin() is None:
        print(
            "The tesseract program is not installed.\n"
            "  macOS:          brew install tesseract\n"
            "  Debian/Ubuntu:  sudo apt install tesseract-ocr\n"
            "Then run this command again.",
            file=sys.stderr,
        )
        sys.exit(1)
    curl = shutil.which("curl")
    if curl is None:
        sys.exit("curl is needed to download the language data.")
    TESSDATA.mkdir(parents=True, exist_ok=True)
    for lang, want in MODELS.items():
        dest = TESSDATA / f"{lang}.traineddata"
        if dest.exists() and _sha256(dest) == want:
            print(f"{lang}: already present and verified")
            continue
        tmp = dest.with_suffix(".part")
        print(f"{lang}: downloading...")
        subprocess.run([curl, "-fsSL", "--max-time", "300", "-o", str(tmp), MODEL_URL.format(lang=lang)], check=True)
        got = _sha256(tmp)
        if got != want:
            tmp.unlink(missing_ok=True)
            sys.exit(f"{lang}: checksum mismatch ({got}), not installed.")
        tmp.replace(dest)
        print(f"{lang}: verified")
    print("Screenshot reading is ready (English, Tamil, Hindi).")


if __name__ == "__main__":
    setup_main()
