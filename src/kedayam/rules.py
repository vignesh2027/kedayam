"""Scam pattern rules.

Each rule is a small, readable function that looks for one known trick and
returns the quoted parts of the message that triggered it. Weights:

* 3 (critical): the pattern is a scam on its own, for example "enter your
  PIN to receive money". One critical hit gives a scam warning.
* 2 (strong): a common scam ingredient that legitimate messages rarely use.
* 1 (weak): pressure tactics such as urgency or secrecy. They only add up.
* 0 (tip): not a warning sign, but worth a safety tip (for example an OTP
  message from a bank: never tell the code to anyone).

Patterns for English and romanised Hindi or Tamil use word boundaries.
Patterns for Tamil and Devanagari script are plain substrings because
Python's \\b does not work across Indic vowel signs.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Callable

from .textutil import IP_HOST_RE, Message, deleet, find, near, snippet

I = re.IGNORECASE


def rx(*parts: str) -> re.Pattern[str]:
    return re.compile("|".join(f"(?:{p})" for p in parts), I)


# ---------------------------------------------------------------- vocabulary

RECEIVE = rx(
    r"\breceiv\w*",
    r"\bget (?:the |your )?(?:money|amount|payment|refund|cashback|prize|reward)",
    r"\bcredit(?:ed)? (?:to|in|into)\b",
    r"\brefund\b",
    r"\bcash ?back\b",
    r"\bprize\b",
    r"\breward\b",
    r"\bclaim\b",
    r"\bmilega\b|\bmilegi\b",
    "प्राप्त",
    "पाने",
    "मिलेगा",
    "मिलेगी",
    "रिफंड",
    "कैशबैक",
    "इनाम",
    "பெற",
    "கிடைக்கும்",
    "பரிசு",
    "கேஷ்பேக்",
    "வரவு",
)
PIN = rx(r"\bupi[ -]?pin\b", r"\bm-?pin\b", r"\bpin\b", "पिन", "பின் நம்பர்", "பின் எண்", "ரகசிய எண்")
ENTER = rx(
    r"\benter\w*",
    r"\btype\b",
    r"\bput\b",
    r"\binput\b",
    r"\bdaal\w*",
    "डालें",
    "डालिए",
    "दर्ज",
    "உள்ளிட",
    "போடவும்",
    "பதிவிட",
)
QR = rx(r"\bqr\b", "क्यूआर", "கியூஆர்")
SCAN = rx(r"\bscan\w*", "स्कैन", "ஸ்கேன்")
OTP = rx(
    r"\botp\b",
    r"\bone[ -]?time[ -]?password\b",
    r"\bverification code\b",
    r"\bsecurity code\b",
    r"\b\d[ -]?digit code\b",
    "ओटीपी",
    "ஓடிபி",
)
SHARE_VERB = rx(
    r"\bshare\b",
    r"\btell\b",
    r"\bsend\b",
    r"\bgive\b",
    r"\bforward\b",
    r"\bprovide\b",
    r"\bread out\b",
    r"\bdisclose\b",
    r"\bbata\w*\b",
    r"\bbhej\w*\b",
    "बताएं",
    "बताइए",
    "बताओ",
    "बता दें",
    "भेजें",
    "भेजो",
    "शेयर",
    "சொல்லுங்கள்",
    "சொல்லவும்",
    "சொல்லு",
    "அனுப்பு",
    "கூறவும்",
    "பகிரவும்",
)
SECRET_DETAIL = rx(
    r"\bcvv\b",
    r"\bcard (?:number|details|no)\b",
    r"\b(?:debit|credit|atm) card details\b",
    r"\bexpiry date\b",
    r"\b(?:net ?banking |login )?password\b",
    r"\batm pin\b",
    r"\bm-?pin\b",
    "कार्ड नंबर",
    "सीवीवी",
    "पासवर्ड",
    "கார்டு எண்",
    "கடவுச்சொல்",
)
ASK_DETAIL = rx(
    r"\bshare\b",
    r"\bsend\b",
    r"\benter\b",
    r"\bupdate\b",
    r"\bverify\b",
    r"\bprovide\b",
    r"\btell\b",
    r"\bsubmit\b",
    r"\bconfirm\b",
    r"\bfill\b",
    "बताएं",
    "भेजें",
    "डालें",
    "அனுப்பவும்",
    "சொல்லுங்கள்",
)
URGENCY = rx(
    r"\bwithin \d+ ?(?:hours?|hrs?|minutes?|mins?|days?)\b",
    r"\bin (?:\d+|next \d+) ?(?:hours?|hrs?|minutes?|mins?)\b",
    r"\btoday\b",
    r"\btonight\b",
    r"\bimmediately\b",
    r"\burgent(?:ly)?\b",
    r"\bright now\b",
    r"\blast (?:chance|warning|reminder)\b",
    r"\basap\b",
    r"\bturant\b",
    r"\bjaldi\b",
    r"\baaj raat\b",
    r"\binniku\b",
    r"\budane\b",
    "तुरंत",
    "आज रात",
    "जल्दी",
    "உடனே",
    "உடனடியாக",
    "இன்று இரவு",
)
AUTHORITY = rx(
    r"\bpolice\b",
    r"\bcbi\b",
    r"\bcustoms?\b",
    r"\bncb\b",
    r"\bnarcotics\b",
    r"\benforcement directorate\b",
    r"\bed officer\b",
    r"\bcourt\b",
    r"\bjudge\b",
    r"\bcyber ?cell\b",
    r"\bcrime branch\b",
    r"\btrai\b",
    r"\bincome tax department\b",
    r"\brbi officer\b",
    "पुलिस",
    "सीबीआई",
    "कस्टम",
    "अदालत",
    "காவல்",
    "போலீஸ்",
    "சுங்க",
    "நீதிமன்ற",
)
THREAT = rx(
    r"\barrest\w*\b",
    r"\bwarrant\b",
    r"\bfir\b",
    r"\bcase (?:has been |is )?(?:registered|filed)\b",
    r"\blegal action\b",
    r"\bseized\b",
    r"\billegal\b",
    r"\bmoney laundering\b",
    r"\bdrugs?\b",
    r"\bmdma\b",
    r"\bde-?activat\w*\b",
    r"\bsuspend\w*\b",
    "गिरफ्तार",
    "वारंट",
    "कानूनी कार्रवाई",
    "कैद",
    "கைது",
    "வழக்கு",
    "சட்ட நடவடிக்கை",
)
VIDEO_CALL = rx(r"\bvideo ?call\b", r"\bskype\b", "वीडियो कॉल", "வீடியோ கால்")
KYC = rx(
    r"\be-?kyc\b",
    r"\bkyc\b",
    r"\bpan(?: card)?\b",
    r"\baadhaar\b",
    r"\byono\b",
    r"\bnet ?banking\b",
    r"\bwallet\b",
    "केवाईसी",
    "पैन",
    "आधार",
    "கேஒய்சி",
    "ஆதார்",
)
BLOCK = rx(
    r"\bexpir\w*\b",
    r"\bblock(?:ed)?\b",
    r"\bsuspend\w*\b",
    r"\bclosed?\b",
    r"\bde-?activat\w*\b",
    r"\bfrozen\b",
    r"\bfreeze\b",
    r"\bon hold\b",
    r"\bhold (?:your|the) (?:\w+ )?(?:amount|money|account|wallet|balance)\b",
    r"\bband\b",
    "बंद",
    "ब्लॉक",
    "निलंबित",
    "முடக்க",
    "காலாவதி",
    "நிறுத்த",
    "ரத்து",
)
UTILITY = rx(
    r"\belectricity\b",
    r"\bpower\b",
    r"\bbijli\b",
    r"\beb\b",
    r"\bcurrent\b",
    r"\bgas connection\b",
    r"\bmeter\b",
    "बिजली",
    "मीटर",
    "மின்",
    "கரண்ட்",
)
CUT = rx(
    r"\bdisconnect\w*\b",
    r"\bcut\b",
    r"\bcutoff\b",
    r"\bkaat\w*\b",
    r"\bkat\b",
    "काट",
    "कट",
    "துண்டி",
    "கட் ",
)
UTILITY_PUSH = rx(
    r"\btonight\b",
    r"\btoday\b",
    r"\bofficer\b",
    r"\badhikari\b",
    r"\bcall\b",
    r"\bcontact\b",
    r"\bsampark\b",
    r"\bnight\b",
    r"\binniku\b",
    "आज रात",
    "अधिकारी",
    "संपर्क",
    "இன்று",
    "அதிகாரி",
    "தொடர்பு",
)
PRIZE = rx(
    r"\b(?:you|u) (?:have |'ve |ve )?won\b(?!')",
    r"\bclaim\b.{0,40}\b(?:prize|cash|reward|voucher|bonus|winnings)\b",
    r"\b(?:million|milion|crore)s?\b.{0,30}\b(?:transfer(?:red)? to you|to your account|unclaimed|bequest|inheritance)\b",
    r"\blucky (?:draw|winner|customer)\b",
    r"\blottery\b",
    r"\bjackpot\b",
    r"\b(?:have |has |u |you )?won (?:a |an |the )?(?:£|rs\.? ?|₹ ?|inr ?|\$|€)[\d,.]+",
    r"\bwon (?:a |an |the )?(?:[\w£₹$€,.*]+ ){0,4}(?:prize|cash|award|holiday|voucher|reward|gift|car|iphone|bonus|crore|lakh)s?\b",
    r"\bawait(?:s|ing)? (?:your )?collection\b",
    r"\b(?:you|u|ur|your mobile(?: no| number)?|your number) (?:have been |has been |are |were |was |is |'ve been |have )?awarded\b",
    r"\b(?:you are|u are|you're|u r) (?:a |the )?(?:lucky )?winner\b",
    r"\blucky day\b",
    r"\bclaim (?:your |ur |the |a )?(?:prize|reward|cash|voucher|gift|bonus|winnings)\b",
    r"\b(?:cash|bonus|guaranteed|mega) (?:prize|award|reward)\b",
    r"\bawarded with\b",
    r"\b(?:a )?winner of\b",
    r"\bselected to (?:receive|win|get)\b",
    r"\b(?:today'?s|recent|lucky|bumper) draw\b",
    r"\bkbc\b",
    r"\bprize money\b",
    r"\bclaim your (?:prize|reward|gift)\b",
    r"\binaam\b",
    "लॉटरी",
    "इनाम",
    "जीती",
    "जीता",
    "லாட்டரி",
    "பரிசு வென்ற",
    "வென்றுள்ளீர்கள்",
)
FEE = rx(
    r"\b(?:processing|registration|clearance|release|gst|tax|transfer|insurance|verification|customs|handling|activation|security)"
    r" (?:fees?|charges?|amount|deposit)\b",
    r"\bfees? (?:of )?(?:rs\.?|₹|inr)",
    "प्रोसेसिंग फीस",
    "रजिस्ट्रेशन फीस",
    "शुल्क",
    "கட்டணம் செலுத்த",
)
FEE_CONTEXT = rx(
    r"\bprize\b",
    r"\blottery\b",
    r"\bwon\b",
    r"\bloan\b",
    r"\bjob\b",
    r"\bselected\b",
    r"\bparcel\b",
    r"\bgift\b",
    r"\brefund\b",
    r"\binaam\b",
    r"\breward\b",
    "लॉटरी",
    "इनाम",
    "लोन",
    "नौकरी",
    "பரிசு",
    "கடன்",
    "வேலை",
)
MISTAKE = rx(
    r"\bby mistake\b",
    r"\bwrongly\b",
    r"\bmistakenly\b",
    r"\baccidentally\b",
    r"\bgalti se\b",
    "गलती से",
    "தவறுதலாக",
    "தவறாக",
)
RETURN = rx(r"\breturn\b", r"\bsend (?:it )?back\b", r"\brefund\b", r"\bwapas\b", "वापस", "திருப்பி")
SCREEN_APP = rx(
    r"\bany ?desk\b",
    r"\bteam ?viewer\b",
    r"\bquick ?support\b",
    r"\brust ?desk\b",
    r"\bair ?droid\b",
    r"\bscreen ?shar\w*\b",
    r"\bremote (?:access|support|desktop)\b",
    "स्क्रीन शेयर",
    "ஸ்கிரீன் ஷேர்",
)
APK = rx(r"\.apk\b", r"\bapk (?:file|download|link)\b")
JOB = rx(
    r"\b(?:part[ -]?time|work from home|wfh|home[ -]based) (?:job|work|income|opportunity)\b"
    r"(?=.{0,80}\b(?:earn\w*|daily|per day|a day|income|salary|telegram|whatsapp|contact|apply|join|investment|rs\.?|₹|\d{3,}))",
    r"\bwork from home\b(?=.{0,80}\b(?:earn\w*|daily|per day|a day|income|salary|telegram|whatsapp|contact|apply|join|investment|rs\.?|₹|\d{3,}))",
    r"\bearn (?:rs\.? ?|₹ ?)?[\d,]+(?: ?- ?[\d,]+)? (?:daily|per day|a day|every day)\b",
    r"\bdaily income\b",
    r"\blik(?:e|ing) (?:youtube )?videos\b",
    r"\brate (?:hotels|products|movies)\b",
    r"\btelegram task\b",
    r"\btask[- ]based\b",
    "घर बैठे",
    "வீட்டிலிருந்தே",
)
NEW_NUMBER = rx(
    r"\b(?:this is )?my new number\b",
    r"\bmy (?:phone|mobile) (?:fell|broke|is broken|got lost|is lost|was stolen)\b",
    r"\bnaya number\b",
    "नया नंबर",
    "புது நம்பர்",
    "புதிய எண்",
)
EMERGENCY = rx(
    r"\baccident\b",
    r"\bhospital\b",
    r"\barrested\b",
    r"\bin trouble\b",
    "अस्पताल",
    "दुर्घटना",
    "விபத்து",
    "மருத்துவமனை",
)
SEND_MONEY = rx(
    r"\bsend (?:me )?(?:rs\.? ?|₹ ?)?[\d,]{3,}",
    r"\bsend (?:the )?money\b",
    r"\btransfer (?:rs\.? ?|₹ ?)?[\d,]{3,}",
    r"\bpaise bhej\w*\b",
    "पैसे भेज",
    "பணம் அனுப்ப",
)
SECRECY = rx(
    r"\b(?:do not|don'?t|dont|never)(?: \w+){0,3} (?:tell|inform)(?: \w+)? (?:anyone|anybody|family|dad|mom|mum|father|mother|husband|wife|son|daughter|police)\b",
    r"\bkeep (?:this|it) (?:a )?(?:secret|confidential)\b",
    r"\bdo not (?:disconnect|cut) the call\b",
    "किसी को मत बताना",
    "किसी को न बताएं",
    "யாரிடமும் சொல்ல வேண்டாம்",
)
CALL = rx(
    r"\bcall\b",
    r"\bdial\b",
    r"\bph(?:one)?\b",
    r"\bmissed call\b",
    r"\bcontact\b",
    r"\bwhats ?app\b",
    r"\bsampark\b",
    r"\bcall pannunga\b",
    "संपर्क",
    "कॉल",
    "தொடர்பு",
    "அழைக்க",
)
MOBILE = re.compile(r"(?<!\d)(?:\+?91[\s-]?)?[6-9]\d{4}[\s-]?\d{5}(?!\d)")
INSTITUTION = rx(
    r"\bbank\b",
    r"\bsbi\b",
    r"\bhdfc\b",
    r"\bicici\b",
    r"\baxis\b",
    r"\bkotak\b",
    r"\bpnb\b",
    r"\bcanara\b",
    r"\bkyc\b",
    r"\bpaytm\b",
    r"\bphonepe\b",
    r"\bamazon\b",
    r"\bflipkart\b",
    r"\belectricity\b",
    r"\bincome tax\b",
    r"\buidai\b",
    r"\baadhaar\b",
    r"\blic\b",
    r"\bcredit card\b",
    "बैंक",
    "வங்கி",
)

# Names a scammer borrows to look official, in a UPI ID or a web address.
BRAND_NAMES = (
    "hdfc", "icici", "kotak", "canara", "paytm", "phonepe", "googlepay", "amazon", "flipkart", "netflix",
    "electricity", "incometax", "aadhaar", "uidai", "pmkisan", "billdesk", "indiapost", "fedex", "bluedart",
    "airtel", "yono", "npci", "tneb", "bses", "bescom", "msedcl", "police", "customs",
    "apple", "icloud", "paypal", "microsoft", "whatsapp", "instagram", "facebook", "google", "youtube",
)
BRAND_TOKENS = {"sbi", "rbi", "lic", "pnb", "bob", "kbc", "kyc", "gov", "govt", "eb", "itr", "gpay", "jio", "dhl", "axis"}
BRAND_PREFIXES = ("sbi", "rbi", "kyc")
# Bait words that only matter inside a UPI ID: nobody needs to pay "refund@..." to get a refund.
BAIT_WORDS = ("refund", "cashback", "reward", "lottery", "prize", "support", "helpdesk", "helpline", "customer", "care", "offer", "bonus")

SHORTENERS = {
    "bit.ly", "tinyurl.com", "cutt.ly", "is.gd", "rb.gy", "shorturl.at", "tiny.cc", "ow.ly", "goo.gl",
    "s.id", "t.ly", "v.gd", "rebrand.ly", "shorte.st", "bitly.com",
}
RISKY_TLDS = {
    "xyz", "top", "online", "site", "live", "click", "icu", "info", "shop", "vip", "buzz", "tk", "ml",
    "ga", "cf", "gq", "rest", "link", "work", "loan", "club", "store",
}
OFFICIAL_DOMAINS = {
    "sbi.co.in", "onlinesbi.sbi", "sbi.bank.in", "hdfcbank.com", "hdfc.bank.in", "icicibank.com", "icici.bank.in",
    "axisbank.com", "axis.bank.in", "kotak.com", "pnbindia.in", "canarabank.com", "paytm.com", "phonepe.com",
    "amazon.in", "amazon.com", "flipkart.com", "netflix.com", "npci.org.in", "rbi.org.in", "licindia.in",
    "google.com", "incometax.gov.in", "uidai.gov.in", "airtel.in", "jio.com", "fedex.com", "bluedart.com",
    "indiapost.gov.in", "cybercrime.gov.in", "sancharsaathi.gov.in",
    "apple.com", "icloud.com", "paypal.com", "microsoft.com", "whatsapp.com", "instagram.com", "facebook.com",
    "youtube.com", "google.co.in",
}
OFFICIAL_SUFFIXES = (".gov.in", ".nic.in", ".bank.in")


def registrable(host: str) -> str:
    parts = host.split(".")
    if len(parts) >= 3 and parts[-2] in {"co", "org", "gov", "nic", "bank", "net", "ac"}:
        return ".".join(parts[-3:])
    return ".".join(parts[-2:])


def is_official(host: str) -> bool:
    host = host.removeprefix("www.")
    return registrable(host) in OFFICIAL_DOMAINS or host.endswith(OFFICIAL_SUFFIXES)


def brand_in(name: str, *, bait: bool = False) -> str | None:
    """Return a borrowed brand (or, for UPI IDs, a bait word) found in a name."""
    flat = deleet(name.lower())
    tokens = [t for t in re.split(r"[^a-z]+", flat) if t]
    for b in BRAND_NAMES:
        if b in flat:
            return b
    for t in tokens:
        if t in BRAND_TOKENS:
            return t
        for pre in BRAND_PREFIXES:
            if t.startswith(pre):
                return pre
    if bait:
        for b in BAIT_WORDS:
            if b in flat:
                return b
    return None


# ---------------------------------------------------------------- rule type


@dataclass(frozen=True)
class Rule:
    id: str
    weight: int
    source: str
    actions: tuple[str, ...]
    check: Callable[[Message], list[str]]


RULES: list[Rule] = []


def rule(id: str, weight: int, source: str, actions: tuple[str, ...]):
    def deco(fn: Callable[[Message], list[str]]):
        RULES.append(Rule(id, weight, source, actions, fn))
        return fn

    return deco


def quotes(m: Message, spans: list[tuple[int, int]], limit: int = 2) -> list[str]:
    seen, out = set(), []
    for s, e in spans:
        q = snippet(m.display, s, e)
        if q not in seen:
            seen.add(q)
            out.append(q)
        if len(out) >= limit:
            break
    return out


# ---------------------------------------------------------------- critical


@rule("pin_to_receive", 3, "NPCI-SAFETY", ("no_pin", "no_pay", "call_bank"))
def pin_to_receive(m: Message) -> list[str]:
    t = m.words
    pin_spans = near(t, ENTER, PIN, 25, allow_negated=False)
    spans = []
    for s, e in pin_spans:
        for r0, r1 in find(RECEIVE, t):
            if max(r0 - e, s - r1, 0) <= 90:
                spans.append((min(s, r0), max(e, r1)))
                break
    return quotes(m, spans)


@rule("qr_to_receive", 3, "NPCI-SAFETY", ("no_qr", "no_pay"))
def qr_to_receive(m: Message) -> list[str]:
    t = m.words
    spans = []
    for s, e in near(t, SCAN, QR, 30, allow_negated=False):
        for r0, r1 in find(RECEIVE, t):
            if max(r0 - e, s - r1, 0) <= 90:
                spans.append((min(s, r0), max(e, r1)))
                break
    return quotes(m, spans)


COLLECT = rx(
    r"\b(?:payment|collect|money) request\b",
    r"\brequest from\b",
    r"\b(?:approve|accept) (?:the |this )?(?:payment )?request\b",
    r"\brequest (?:of|for) (?:rs\.?|₹|inr)",
    "भुगतान अनुरोध",
    "रिक्वेस्ट",
    "கோரிக்கை",
)
LURE = rx(
    r"\bcash ?back\b",
    r"\breward\b",
    r"\brefund\b",
    r"\bprize\b",
    r"\bwon\b",
    r"\blottery\b",
    r"\bbonus\b",
    r"\breceive\b",
    r"\bclaim\b",
    "कैशबैक",
    "इनाम",
    "रिफंड",
    "பரிசு",
    "கேஷ்பேக்",
)


@rule("collect_request_lure", 3, "NPCI-SAFETY", ("no_pin", "no_pay"))
def collect_request_lure(m: Message) -> list[str]:
    return quotes(m, near(m.words, COLLECT, LURE, 90, allow_negated=False))


@rule("otp_request", 3, "RBI-BEAWARE", ("no_otp", "call_bank"))
def otp_request(m: Message) -> list[str]:
    return quotes(m, near(m.words, SHARE_VERB, OTP, 40, allow_negated=False))


@rule("secret_details_request", 3, "RBI-BEAWARE", ("no_details", "no_link", "call_bank"))
def secret_details_request(m: Message) -> list[str]:
    return quotes(m, near(m.words, ASK_DETAIL, SECRET_DETAIL, 40, allow_negated=False))


@rule("screen_share_app", 3, "RBI-BEAWARE", ("no_app", "call_bank"))
def screen_share_app(m: Message) -> list[str]:
    return quotes(m, find(SCREEN_APP, m.words, allow_negated=False))


@rule("apk_link", 3, "RBI-BEAWARE", ("no_app", "no_link"))
def apk_link(m: Message) -> list[str]:
    return quotes(m, find(APK, m.norm))


DIGITAL_ARREST = rx(r"\bdigital(?:ly)? arrest\w*\b", "डिजिटल अरेस्ट", "डिजिटल गिरफ्तारी", "டிஜிட்டல் கைது", "டிஜிட்டல் அரெஸ்ட்")


@rule("digital_arrest", 3, "I4C-DIGITAL-ARREST", ("hang_up", "no_pay", "tell_family"))
def digital_arrest(m: Message) -> list[str]:
    t = m.words
    spans = find(DIGITAL_ARREST, t, allow_negated=False)
    spans += near(t, VIDEO_CALL, THREAT, 120)
    spans += near(t, VIDEO_CALL, AUTHORITY, 120)
    return quotes(m, spans)


PAY = rx(r"\bpay\b", r"\bdeposit\b", r"\bjama\b", r"\btransfer\b", r"\bsend\b", "जमा", "भुगतान करें", "செலுத்த", "கட்டவும்")


@rule("advance_fee", 3, "RBI-BEAWARE", ("no_pay", "tell_family"))
def advance_fee(m: Message) -> list[str]:
    t = m.words
    fee_asks = near(t, FEE, PAY, 40)
    spans = []
    for s, e in fee_asks:
        for c0, c1 in find(FEE_CONTEXT, t):
            if max(c0 - e, s - c1, 0) <= 200:
                spans.append((min(s, c0), max(e, c1)))
                break
    return quotes(m, spans)


@rule("wrong_transfer", 3, "RBI-BEAWARE", ("check_balance", "no_pay", "call_bank"))
def wrong_transfer(m: Message) -> list[str]:
    return quotes(m, near(m.words, MISTAKE, RETURN, 160))


@rule("lookalike_upi_id", 3, "NPCI-SAFETY", ("no_pay", "no_pin", "check_payee"))
def lookalike_upi_id(m: Message) -> list[str]:
    out = []
    for v in m.vpas:
        handle = v.split("@", 1)[0]
        if brand_in(handle, bait=True):
            out.append(v)
    return out[:2]


@rule("lookalike_link", 3, "RBI-BEAWARE", ("no_link", "call_bank"))
def lookalike_link(m: Message) -> list[str]:
    out = []
    for url, host in zip(m.urls, m.hosts):
        if is_official(host) or host in SHORTENERS:
            continue
        if brand_in(host):
            out.append(url)
    return out[:2]


# ---------------------------------------------------------------- strong


@rule("suspicious_link", 2, "RBI-BEAWARE", ("no_link",))
def suspicious_link(m: Message) -> list[str]:
    out = []
    for url, host in zip(m.urls, m.hosts):
        if is_official(host):
            continue
        tld = host.rsplit(".", 1)[-1]
        if host in SHORTENERS or IP_HOST_RE.match(host) or "xn--" in host or tld in RISKY_TLDS or "ngrok" in host:
            out.append(url)
    return out[:2]


ACCOUNT_THING = rx(
    r"\baccount\b",
    r"\b(?:atm|debit|credit)? ?card\b",
    r"\bonline banking\b",
    r"\bapple ?id\b",
    r"\bsim\b",
    r"\bupi(?: id)?\b",
    "खाता",
    "कार्ड",
    "கணக்கு",
    "கார்டு",
)
WILL_BE_BLOCKED = rx(
    r"\b(?:will be|has been|have been|has just been|is being|got|is|are|was) (?:temporarily |permanently |now )?"
    r"(?:blocked|suspended|de-?activated|closed|frozen|locked|disabled|terminated|restricted|on hold)\b",
    r"\bavoid (?:your )?(?:account |card )?(?:suspension|de-?activation|blocking|closure|being blocked)\b",
)
AS_REQUESTED = rx(r"\bas (?:per )?(?:your )?request(?:ed)?\b", r"\bat your request\b", r"\byour request to\b")


ALERT = rx(
    r"\b(?:unusual|suspicious|unauthori[sz]ed|unrecogni[sz]ed|strange) (?:activity|login|log-in|sign-?in|transaction|access|payment|purchase)s?\b",
    r"\bif (?:this|it) (?:was|is|wasn'?t|isn'?t) (?:not )?(?:done by |made by )?you\b",
    r"\bif not (?:done |made )?(?:by )?you\b",
    r"\bnot done by you\b",
    r"\bwas this you\b",
)


def _unofficial_urls(m: Message) -> list[str]:
    return [u for u, h in zip(m.urls, m.hosts) if not is_official(h)]


@rule("fake_security_alert", 3, "RBI-BEAWARE", ("no_link", "call_bank"))
def fake_security_alert(m: Message) -> list[str]:
    """A security alert that sends you to a link that is not the bank's site."""
    urls = _unofficial_urls(m)
    if not urls:
        return []
    hits = find(ALERT, m.words)
    return (quotes(m, hits, limit=1) + urls[:1]) if hits else []


PARCEL = rx(
    r"\bdeliver(?:y|ies)?\b", r"\bparcel\b", r"\bpackage\b", r"\bcourier\b", r"\bshipment\b", r"\bconsignment\b",
    "पार्सल", "डिलीवरी", "பார்சல்", "டெலிவரி",
)
PARCEL_PROBLEM = rx(
    r"\b(?:could not|couldn'?t|unable to|failed to|cannot|can'?t) (?:be )?(?:make a )?deliver\w*",
    r"\bundeliver\w*",
    r"\bdelivery (?:failed|attempt|unsuccessful|was unsuccessful)\b",
    r"\bre-?schedule\b",
    r"\b(?:incomplete|incorrect|wrong|invalid|insufficient) address\b",
    r"\bupdate (?:your )?(?:delivery )?address\b",
    r"\bheld at\b",
    "पता अपडेट",
    "अधूरा पता",
    "முகவரி",
)


@rule("parcel_problem_link", 2, "RBI-BEAWARE", ("no_link", "no_call_number"))
def parcel_problem_link(m: Message) -> list[str]:
    """'Your parcel could not be delivered, update address at this link or call this number.'"""
    if not (_unofficial_urls(m) or m.mobiles):
        return []
    return quotes(m, near(m.words, PARCEL, PARCEL_PROBLEM, 80))


REWARD = rx(r"\brefund\b", r"\breward\b", r"\bprize\b", r"\bgift\b", r"\bbonus\b", r"\bcash ?back\b", "रिफंड", "इनाम", "பரிசு")


@rule("reward_link", 2, "RBI-BEAWARE", ("no_link", "no_details"))
def reward_link(m: Message) -> list[str]:
    """A refund, prize or cashback that you collect through a link that is not an official site."""
    urls = _unofficial_urls(m)
    if not urls or not REWARD.search(m.words):
        return []
    return quotes(m, find(REWARD, m.words), limit=1) + urls[:1]


@rule("account_block_threat", 2, "RBI-BEAWARE", ("no_link", "call_bank"))
def account_block_threat(m: Message) -> list[str]:
    t = m.words
    spans = near(t, KYC, BLOCK, 80)
    if not AS_REQUESTED.search(t):
        spans += near(t, ACCOUNT_THING, WILL_BE_BLOCKED, 60)
    return quotes(m, spans)


@rule("utility_disconnection", 2, "DOT-CHAKSHU", ("no_call_number", "check_bill"))
def utility_disconnection(m: Message) -> list[str]:
    t = m.words
    hits = near(t, UTILITY, CUT, 80)
    if not hits:
        return []
    if find(UTILITY_PUSH, t) or m.mobiles:
        return quotes(m, hits)
    return []


@rule("authority_threat", 2, "I4C-DIGITAL-ARREST", ("hang_up", "tell_family"))
def authority_threat(m: Message) -> list[str]:
    return quotes(m, near(m.words, AUTHORITY, THREAT, 120))


@rule("prize_lottery", 2, "RBI-BEAWARE", ("no_pay", "no_details"))
def prize_lottery(m: Message) -> list[str]:
    return quotes(m, find(PRIZE, m.words, allow_negated=False))


@rule("easy_money_job", 2, "RBI-BEAWARE", ("no_pay", "tell_family"))
def easy_money_job(m: Message) -> list[str]:
    return quotes(m, find(JOB, m.words))


@rule("family_money_request", 2, "RBI-BEAWARE", ("verify_family", "no_pay"))
def family_money_request(m: Message) -> list[str]:
    t = m.words
    spans = near(t, NEW_NUMBER, SEND_MONEY, 160) + near(t, EMERGENCY, SEND_MONEY, 120)
    return quotes(m, spans)


@rule("sender_is_mobile_number", 2, "TRAI-HEADERS", ("call_bank",))
def sender_is_mobile_number(m: Message) -> list[str]:
    digits = re.sub(r"\D", "", m.sender)
    if not m.sender or len(digits) < 10 or re.search(r"[a-z]", m.sender):
        return []
    if not re.fullmatch(r"(?:91)?[6-9]\d{9}", digits):
        return []
    hit = INSTITUTION.search(m.words)
    if not hit:
        return []
    return [m.sender] + quotes(m, [(hit.start(), hit.end())], limit=1)


# ---------------------------------------------------------------- weak


@rule("urgency", 1, "RBI-BEAWARE", ("slow_down",))
def urgency(m: Message) -> list[str]:
    return quotes(m, find(URGENCY, m.words))


@rule("secrecy", 1, "I4C-DIGITAL-ARREST", ("tell_family",))
def secrecy(m: Message) -> list[str]:
    return quotes(m, find(SECRECY, m.words))


@rule("call_this_number", 1, "RBI-BEAWARE", ("no_call_number",))
def call_this_number(m: Message) -> list[str]:
    return quotes(m, near(m.words, CALL, MOBILE, 40))


# ---------------------------------------------------------------- tips


@rule("otp_message", 0, "RBI-BEAWARE", ("no_otp",))
def otp_message(m: Message) -> list[str]:
    t = m.words
    if not OTP.search(t) or not re.search(r"(?<!\d)\d{4,8}(?!\d)", t):
        return []
    if otp_request(m):
        return []
    return quotes(m, find(OTP, t), limit=1)


@rule("has_link", 0, "RBI-BEAWARE", ("no_link",))
def has_link(m: Message) -> list[str]:
    return m.urls[:2]


RULES_BY_ID = {r.id: r for r in RULES}
