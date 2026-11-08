import os
import stat

import pytest
from fastapi.testclient import TestClient

from kedayam import family as fam
from kedayam.app import app
from kedayam.i18n import UI

SCAM = "Scan this QR code to receive Rs 4000 for your sofa."


@pytest.fixture
def client():
    with TestClient(app) as c:
        yield c


def setup_family(client, **over):
    data = {"lang": "en", "parent_lang": "ta", "name": "Ravi", "phone": "+91 70000 11111", "bank": "Indian Bank", "bank_phone": "1800 000 2222"}
    data.update(over)
    return client.post("/family", data=data, follow_redirects=False)


def test_validation():
    assert fam.validate("ta", "Ravi", "70000 11111") is not None
    assert fam.validate("ta", "", "70000 11111") is None
    assert fam.validate("ta", "Ravi", "12") is None
    assert fam.validate("ta", "Ravi", "call me maybe") is None
    assert fam.validate("xx", "Ravi", "70000 11111") is None
    assert fam.validate("en", "Ravi", "70000 11111", bank_phone="abc") is None
    assert fam.validate("en", "R" * 100, "70000 11111").name == "R" * 40


def test_save_load_clear_and_private_file():
    f = fam.validate("hi", "Meena", "7000022222")
    fam.save(f)
    assert fam.load() == f
    assert stat.S_IMODE(os.stat(fam.path()).st_mode) == 0o600
    fam.clear()
    assert fam.load() is None


def test_corrupt_file_is_ignored():
    fam.data_dir().mkdir(parents=True, exist_ok=True)
    fam.path().write_text("{not json")
    assert fam.load() is None


def test_setup_then_warning_shows_family_call(client):
    r = setup_family(client)
    assert r.status_code == 303
    assert fam.load().lang == "ta"
    # Home page now opens in the parent's language.
    home = client.get("/")
    assert '<html lang="ta">' in home.text
    res = client.post("/check", data={"text": SCAM, "lang": "ta"})
    assert UI["ta"]["family_call"].format(name="Ravi", phone="+91 70000 11111") in res.text
    assert "1800 000 2222" in res.text


def test_no_pattern_result_suggests_calling_family(client):
    setup_family(client, parent_lang="en")
    res = client.post("/check", data={"text": "Hi Amma, reached home.", "lang": "en"})
    assert UI["en"]["family_unsure"].format(name="Ravi", phone="+91 70000 11111") in res.text


def test_invalid_setup_keeps_form_and_explains(client):
    r = setup_family(client, phone="12", lang="hi")
    assert r.status_code == 400
    assert UI["hi"]["family_invalid"] in r.text
    assert 'value="Ravi"' in r.text
    assert fam.load() is None


def test_remove(client):
    setup_family(client)
    r = client.post("/family/remove", data={"lang": "en"}, follow_redirects=True)
    assert UI["en"]["family_removed"] in r.text
    assert fam.load() is None


def test_card_prints_numbers(client):
    setup_family(client, parent_lang="hi")
    r = client.get("/family/card")
    assert UI["hi"]["card_title"] in r.text
    assert UI["hi"]["card_call"].format(name="Ravi", phone="+91 70000 11111") in r.text


def test_cross_site_post_refused(client):
    r = client.post(
        "/family",
        data={"lang": "en", "parent_lang": "en", "name": "Scammer", "phone": "7000099999"},
        headers={"Origin": "https://evil.example"},
    )
    assert r.status_code == 403
    assert fam.load() is None
    r = client.post("/family/remove", data={"lang": "en"}, headers={"Origin": "null"})
    assert r.status_code == 403


def test_same_origin_post_allowed(client):
    r = client.post(
        "/family",
        data={"lang": "en", "parent_lang": "en", "name": "Ravi", "phone": "7000011111"},
        headers={"Origin": "http://testserver"},
        follow_redirects=False,
    )
    assert r.status_code == 303


def test_other_host_names_refused(client):
    r = client.get("/", headers={"Host": "attacker.example"})
    assert r.status_code == 400


def test_family_names_are_escaped(client):
    setup_family(client, name="<b>Ravi</b>", parent_lang="en")
    res = client.post("/check", data={"text": SCAM, "lang": "en"})
    assert "<b>Ravi</b>" not in res.text
    assert "&lt;b&gt;Ravi&lt;/b&gt;" in res.text


def test_hosted_family_is_per_browser_and_in_memory(monkeypatch):
    from kedayam import app as app_module, i18n

    monkeypatch.setattr(fam, "HOSTED", True)
    monkeypatch.setattr(app_module, "HOSTED", True)
    monkeypatch.setattr(i18n, "HOSTED", True)
    monkeypatch.setattr(fam, "_memory", type(fam._memory)())
    with TestClient(app, base_url="https://testserver") as a, TestClient(app, base_url="https://testserver") as b:
        assert "public demo" in a.get("/?lang=en").text
        assert setup_family(a).status_code == 303
        assert not fam.path().exists()
        warn_a = a.post("/check", data={"text": SCAM, "lang": "en"}).text
        warn_b = b.post("/check", data={"text": SCAM, "lang": "en"}).text
        assert "Ravi" in warn_a and "Ravi" not in warn_b
        assert "Modal" in a.get("/about?lang=en").text
        a.post("/family/remove", data={"lang": "en"})
        assert "Ravi" not in a.post("/check", data={"text": SCAM, "lang": "en"}).text
