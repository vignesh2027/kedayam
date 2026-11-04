"""Text helpers: normalisation, extraction of links, UPI IDs and phone numbers,
proximity matching, negation checks and link defanging.

Indian scripts (Tamil, Devanagari) use combining vowel signs that Python's
regex engine does not treat as word characters, so patterns for those
scripts are matched as plain substrings, never with \\b.
"""

from __future__ import annotations

import re
import unicodedata
from dataclasses import dataclass, field

# Invisible characters scammers insert to break up keywords. ZWNJ and ZWJ
# (U+200C, U+200D) are removed too: in Tamil and Devanagari they only change
# how a word is drawn, and OCR inserts them inside Tamil words.
_INVISIBLE = dict.fromkeys(map(ord, "\u200b\u200c\u200d\u2060\ufeff\u00ad"), None)

# Common digit-for-letter swaps used in lookalike names (netf1ix, amaz0n).
_LEET = str.maketrans({"0": "o", "1": "l", "3": "e", "4": "a", "5": "s", "7": "t", "@": "a", "$": "s"})

NEGATION = re.compile(
    r"\b(?:do\s*not|don'?t|dont|never|not\s+to|no\s+need\s+to|not\s+required|will\s+never|does\s+not|doesn'?t)\b"
    r"|न\s*करें|न\s*दें|(?<![ऀ-ॿ])मत(?![ऀ-ॿ])|नहीं"
    r"|வேண்டாம்|தேவையில்லை|கூடாது"
)

_TLDS = (
    "com|in|net|org|xyz|top|online|site|info|live|click|icu|co|ly|me|link|app|io|shop|biz|vip|cc|"
    "tk|ml|ga|cf|gq|buzz|rest|work|loan|club|store|pro|gd|at|id|gy|sbi|bank"
)
URL_RE = re.compile(
    r"(?<![@\w.-])(?:https?://[^\s<>\"']+|(?:www\.)?(?:[a-z0-9-]+\.)+(?:" + _TLDS + r")\b(?!@)(?:/[^\s<>\"']*)?)",
    re.IGNORECASE,
)
IP_HOST_RE = re.compile(r"^\d{1,3}(?:\.\d{1,3}){3}$")
# A UPI ID is handle@psp with no dot after the @ (that would be an email address).
VPA_RE = re.compile(r"(?<![\w.])([a-z0-9][a-z0-9._-]{1,63})@([a-z]{2,20})(?![\w.@-]*\.[a-z])", re.IGNORECASE)
MOBILE_RE = re.compile(r"(?<!\d)(?:\+?91[\s-]?)?[6-9]\d{4}[\s-]?\d{5}(?!\d)")


@dataclass
class Message:
    raw: str
    sender: str = ""
    # Cleaned text with the original letter case, used for quotes.
    display: str = ""
    # Lower-cased, cleaned text. Links, UPI IDs and numbers come from this.
    norm: str = ""
    # Same length as norm, with digit-for-letter swaps undone inside words
    # ("w0n" -> "won", "fl1pkart" -> "flipkart"). Keyword rules match on this.
    words: str = ""
    urls: list[str] = field(default_factory=list)
    hosts: list[str] = field(default_factory=list)
    vpas: list[str] = field(default_factory=list)
    mobiles: list[str] = field(default_factory=list)


def clean(text: str) -> str:
    """NFKC, invisible characters removed, whitespace collapsed. Case kept."""
    text = unicodedata.normalize("NFKC", text or "")
    text = text.translate(_INVISIBLE)
    text = text.replace("’", "'").replace("‘", "'")
    return re.sub(r"\s+", " ", text).strip()


def normalise(text: str) -> str:
    return clean(text).lower()


def deleet(text: str) -> str:
    return text.translate(_LEET)


_MIXED = re.compile(r"\b[a-z0-9]*[a-z][a-z0-9]*\b")


def unleet_words(text: str) -> str:
    """Undo digit-for-letter swaps inside words that are mostly letters.

    Pure numbers, amounts and phone numbers are untouched, and the output has
    exactly the same length as the input so match positions line up.
    """

    def fix(m: re.Match[str]) -> str:
        w = m.group(0)
        letters = sum(c.isalpha() for c in w)
        digits = sum(c.isdigit() for c in w)
        if digits and letters >= 2 and letters >= digits:
            return w.translate(_LEET)
        return w

    return _MIXED.sub(fix, text)


def host_of(url: str) -> str:
    u = re.sub(r"^https?://", "", url.strip().lower())
    host = re.split(r"[/?#:]", u, maxsplit=1)[0]
    return host.rstrip(".")


def parse(text: str, sender: str = "") -> Message:
    display = clean(text)
    norm = display.lower()
    if len(norm) != len(display):  # rare letters whose lower case changes length
        display = norm
    urls = [m.group(0).rstrip(".,;:)!?") for m in URL_RE.finditer(norm)]
    # Drop things like "rs.500" or "a/c" that look odd but are not hosts.
    urls = [u for u in urls if "." in host_of(u)]
    hosts = [host_of(u) for u in urls]
    vpas = [f"{m.group(1)}@{m.group(2)}" for m in VPA_RE.finditer(norm)]
    mobiles = [re.sub(r"\D", "", m.group(0))[-10:] for m in MOBILE_RE.finditer(norm)]
    return Message(raw=text, sender=normalise(sender), display=display, norm=norm, words=unleet_words(norm), urls=urls, hosts=hosts, vpas=vpas, mobiles=mobiles)


def snippet(text: str, start: int, end: int, pad: int = 25) -> str:
    """A short quote around [start, end), cut at word edges where possible."""
    s = max(0, start - pad)
    e = min(len(text), end + pad)
    if s > 0:
        sp = text.find(" ", s, start)
        s = sp + 1 if sp != -1 else s
    if e < len(text):
        sp = text.rfind(" ", end, e)
        e = sp if sp != -1 else e
    out = text[s:e].strip()
    return ("..." if s > 0 else "") + out + ("..." if e < len(text) else "")


def negated(text: str, start: int, end: int, before: int = 30, after: int = 25) -> bool:
    """True if a negation word sits just before or just after a match.

    Hindi and Tamil put the negation after the verb ("साझा न करें",
    "பகிர வேண்டாம்"), English puts it before ("do not share").
    """
    left = text[max(0, start - before) : start]
    right = text[end : end + after]
    # Only look to the right up to the end of the sentence.
    right = re.split(r"[.!?।\n]", right, maxsplit=1)[0]
    left = re.split(r"[.!?।\n]", left)[-1]
    return bool(NEGATION.search(left) or NEGATION.search(right))


def find(pattern: re.Pattern[str], text: str, *, allow_negated: bool = True) -> list[tuple[int, int]]:
    spans = []
    for m in pattern.finditer(text):
        if not allow_negated and negated(text, m.start(), m.end()):
            continue
        spans.append((m.start(), m.end()))
    return spans


def near(
    text: str,
    a: re.Pattern[str],
    b: re.Pattern[str],
    window: int = 80,
    *,
    allow_negated: bool = True,
) -> list[tuple[int, int]]:
    """Spans where a match of `a` and a match of `b` are within `window` chars."""
    out = []
    a_spans = find(a, text, allow_negated=allow_negated)
    if not a_spans:
        return out
    b_spans = find(b, text)
    for a0, a1 in a_spans:
        for b0, b1 in b_spans:
            gap = max(b0 - a1, a0 - b1, 0)
            if gap <= window:
                out.append((min(a0, b0), max(a1, b1)))
                break
    return out


def defang(text: str) -> str:
    """Make links in text non-clickable and visibly marked: hxxp, [.]"""

    def _one(m: re.Match[str]) -> str:
        u = m.group(0)
        u = re.sub(r"^http", "hxxp", u, flags=re.IGNORECASE)
        return u.replace(".", "[.]")

    return URL_RE.sub(_one, text)
