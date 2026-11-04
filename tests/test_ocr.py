"""Screenshot reading. Tests that need Tesseract are skipped when it or the
language data is missing (run `uv run kavach-ocr-setup`)."""

import io
import json
import re
from pathlib import Path

import pytest
from fastapi.testclient import TestClient
from PIL import Image

from kavach import ocr
from kavach.app import app
from kavach.engine import analyse
from kavach.i18n import UI

FIX = Path(__file__).parent / "fixtures" / "screenshots"
MANIFEST = json.loads((FIX / "manifest.json").read_text(encoding="utf-8"))
needs_ocr = pytest.mark.skipif(not ocr.available(), reason="tesseract or language data not installed")


def words(text: str) -> list[str]:
    return [w for w in re.split(r"[\s,.!?।:]+", text.lower()) if w]


def test_status_bar_removed_and_wrapped_link_joined():
    raw = "10:42 4G 72%\nBank Helpdesk\nUpdate now: http://sbi-kyc-\nupdate.xyz/login\n"
    out = ocr.clean_ocr_text(raw)
    assert "72%" not in out
    assert "http://sbi-kyc-update.xyz/login" in out


def test_noisy_status_bar_removed_but_real_percentages_kept():
    out = ocr.clean_ocr_text("_ 48 72%\n| 4G 72%\nGet 50% cashback today\nInterest rate 7.5%")
    assert "72%" not in out
    assert "Get 50% cashback today" in out
    assert "Interest rate 7.5%" in out


def test_ordinary_hyphen_lines_not_joined():
    assert ocr.clean_ocr_text("well-\nknown") == "well-\nknown"


def test_tamil_ocr_joiners_do_not_break_rules():
    # Tesseract inserts ZWNJ after Tamil virama; rules must still match.
    text = "உங்கள்‌ மின்‌ இணைப்பு இன்று இரவு துண்டிக்கப்படும்‌. 7000078901"
    assert analyse(text, use_classifier=False).level != "none"


def test_bad_input_is_rejected_without_ocr():
    assert ocr.read_image(b"").error == "ocr_not_image"
    assert ocr.read_image(b"x" * (ocr.MAX_BYTES + 1)).error == "ocr_too_big"


@needs_ocr
def test_not_an_image():
    assert ocr.read_image(b"this is not a picture").error == "ocr_not_image"


@needs_ocr
def test_blank_image_has_no_text():
    buf = io.BytesIO()
    Image.new("RGB", (800, 600), "white").save(buf, "PNG")
    assert ocr.read_image(buf.getvalue()).error == "ocr_no_text"


@needs_ocr
@pytest.mark.parametrize("item", MANIFEST, ids=[m["id"] for m in MANIFEST])
def test_fixture_reads_and_gets_same_result_as_typed_text(item):
    read = ocr.read_image((FIX / item["file"]).read_bytes())
    assert read.error is None
    truth = words(item["text"])
    got = set(words(read.text))
    recall = sum(1 for w in truth if w in got) / len(truth)
    assert recall >= item["min_word_recall"], (recall, read.text)
    assert analyse(read.text).level == item["expected_level"], read.text


def test_uploads_stay_in_memory():
    from starlette.formparsers import MultiPartParser

    assert MultiPartParser.spool_max_size > ocr.MAX_BYTES


@pytest.fixture(scope="module")
def client():
    with TestClient(app) as c:
        yield c


@needs_ocr
def test_home_offers_screenshot_upload(client):
    r = client.get("/?lang=ta")
    assert UI["ta"]["shot_button"] in r.text
    assert 'enctype="multipart/form-data"' in r.text


@needs_ocr
@pytest.mark.parametrize("lang", ["en", "ta", "hi"])
def test_upload_end_to_end(client, lang):
    data = (FIX / "upi_collect_request.png").read_bytes()
    r = client.post(f"/check-image?lang={lang}", data={"lang": lang}, files={"image": ("shot.png", data, "image/png")})
    assert r.status_code == 200
    assert UI[lang]["level_danger"] in r.text
    assert UI[lang]["ocr_read"] in r.text
    assert "rewards.sbi@ybl" in r.text


@needs_ocr
def test_upload_wrong_file_type_friendly(client):
    r = client.post("/check-image", data={"lang": "hi"}, files={"image": ("a.pdf", b"%PDF-1.4 nope", "application/pdf")})
    assert r.status_code == 400
    assert UI["hi"]["ocr_not_image"] in r.text


def test_upload_too_big_refused(client):
    big = b"0" * (ocr.MAX_BYTES + 200_000)
    r = client.post("/check-image", data={"lang": "en"}, files={"image": ("big.png", big, "image/png")})
    assert r.status_code == 413
    assert UI["en"]["ocr_too_big"] in r.text


def test_upload_missing_file(client):
    r = client.post("/check-image", data={"lang": "en"})
    assert r.status_code == 400
