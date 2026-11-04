import pytest
from fastapi.testclient import TestClient

from kedayam.app import app
from kedayam.i18n import LANGS, UI


@pytest.fixture(scope="module")
def client():
    with TestClient(app) as c:
        yield c


def test_ui_strings_complete_in_every_language():
    keys = set(UI["en"])
    for lang in LANGS:
        assert set(UI[lang]) == keys, lang
        assert all(v.strip() for v in UI[lang].values())


@pytest.mark.parametrize("lang", LANGS)
def test_home_renders_in_each_language(client, lang):
    r = client.get(f"/?lang={lang}")
    assert r.status_code == 200
    assert f'<html lang="{lang}">' in r.text
    assert UI[lang]["check"] in r.text


def test_unknown_language_falls_back_to_english(client):
    r = client.get("/?lang=xx")
    assert '<html lang="en">' in r.text


def test_privacy_and_security_headers(client):
    r = client.get("/")
    assert r.headers["cache-control"] == "no-store"
    assert "default-src 'none'" in r.headers["content-security-policy"]
    assert "script-src" not in r.headers["content-security-policy"]
    assert r.headers["referrer-policy"] == "same-origin"
    assert "<script" not in r.text


@pytest.mark.parametrize("lang", LANGS)
def test_scam_gets_warning_with_reasons_and_actions(client, lang):
    r = client.post("/check", data={"text": "Scan this QR code to receive Rs 4000 for your sofa.", "lang": lang})
    assert r.status_code == 200
    assert UI[lang]["level_danger"] in r.text
    assert UI[lang]["report_1930"] in r.text


def test_clean_message_never_called_safe(client):
    r = client.post("/check", data={"text": "Hi Amma, reached home. Will call later.", "lang": "en"})
    assert UI["en"]["level_none"] in r.text
    assert UI["en"]["level_none_sub"] in r.text
    assert "is safe" not in r.text.replace("does not mean the message is safe", "")


def test_links_are_defanged_in_output(client):
    r = client.post("/check", data={"text": "Update KYC now at http://sbi-kyc.online/login", "lang": "en"})
    assert "hxxp://sbi-kyc[.]online/login" in r.text
    assert 'href="http://sbi-kyc' not in r.text


def test_html_in_message_is_escaped(client):
    r = client.post("/check", data={"text": "<script>alert(1)</script> enter your PIN to receive cashback", "lang": "en"})
    assert "<script>alert(1)</script>" not in r.text
    assert "&lt;script&gt;" in r.text


def test_empty_message_shows_friendly_error(client):
    r = client.post("/check", data={"text": "   ", "lang": "ta"})
    assert r.status_code == 400
    assert UI["ta"]["empty"] in r.text


def test_too_long_message(client):
    r = client.post("/check", data={"text": "a" * 5000, "lang": "hi"})
    assert r.status_code == 400
    assert "4000" in r.text


def test_sender_mobile_number_flag(client):
    r = client.post(
        "/check",
        data={"text": "SBI: your account is on hold, visit branch.", "sender": "+91 70000 11223", "lang": "en"},
    )
    assert "came from a mobile number" in r.text


def test_about_page(client):
    r = client.get("/about")
    assert r.status_code == 200
    assert "npci.org.in" in r.text


def test_logo_served_and_old_name_gone(client):
    assert client.get("/static/logo.svg").status_code == 200
    assert client.get("/static/logo-512.png").headers["content-type"] == "image/png"
    for path in ("/?lang=en", "/?lang=ta", "/?lang=hi", "/about"):
        page = client.get(path).text
        assert "Kedayam" in page
        for old in ("Kavach", "கவச்", "कवच"):
            assert old not in page


@pytest.mark.parametrize("lang", LANGS)
def test_about_page_translated(client, lang):
    from kedayam.i18n import ABOUT

    assert set(ABOUT[lang]) == set(ABOUT["en"])
    assert len(ABOUT[lang]["not"]) == len(ABOUT["en"]["not"])
    r = client.get(f"/about?lang={lang}")
    assert ABOUT[lang]["privacy_h"] in r.text
    assert ABOUT[lang]["not"][0].replace('"', "&#34;") in r.text
