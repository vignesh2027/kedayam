"""Family mode: a trusted person's name and number, saved only on this computer.

A son, daughter or carer fills this in once. Warnings then tell the parent
to call that person before acting. The file lives in KEDAYAM_DATA_DIR
(default: the git-ignored `instance/` folder) with owner-only permissions.
"""

from __future__ import annotations

import json
import os
import re
from dataclasses import asdict, dataclass
from pathlib import Path

from .i18n import LANGS

ROOT = Path(__file__).resolve().parents[2]


def data_dir() -> Path:
    return Path(os.environ.get("KEDAYAM_DATA_DIR", ROOT / "instance"))


def path() -> Path:
    return data_dir() / "family.json"


@dataclass
class Family:
    lang: str
    name: str
    phone: str
    bank: str = ""
    bank_phone: str = ""


_PHONE_OK = re.compile(r"^\+?[\d\s-]{6,20}$")


def clean_phone(raw: str) -> str | None:
    raw = (raw or "").strip()
    if not raw:
        return None
    digits = re.sub(r"\D", "", raw)
    if not _PHONE_OK.match(raw) or not 6 <= len(digits) <= 15:
        return None
    return re.sub(r"\s+", " ", raw)


def validate(lang: str, name: str, phone: str, bank: str = "", bank_phone: str = "") -> Family | None:
    name = re.sub(r"\s+", " ", (name or "").strip())[:40]
    bank = re.sub(r"\s+", " ", (bank or "").strip())[:40]
    p = clean_phone(phone)
    bp = clean_phone(bank_phone) if bank_phone.strip() else ""
    if lang not in LANGS or not name or p is None or bp is None:
        return None
    return Family(lang=lang, name=name, phone=p, bank=bank, bank_phone=bp or "")


def load() -> Family | None:
    try:
        data = json.loads(path().read_text(encoding="utf-8"))
        return validate(data["lang"], data["name"], data["phone"], data.get("bank", ""), data.get("bank_phone", ""))
    except (OSError, ValueError, KeyError, TypeError):
        return None


def save(f: Family) -> None:
    d = data_dir()
    d.mkdir(parents=True, exist_ok=True)
    tmp = path().with_suffix(".tmp")
    fd = os.open(tmp, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
    with os.fdopen(fd, "w", encoding="utf-8") as fh:
        json.dump(asdict(f), fh, ensure_ascii=False, indent=1)
    os.replace(tmp, path())


def clear() -> None:
    path().unlink(missing_ok=True)
