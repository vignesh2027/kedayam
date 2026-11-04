from kedayam.engine import analyse
from kedayam.i18n import UI, LANGS
from kedayam.textutil import defang, negated, normalise


def test_critical_pattern_gives_danger():
    r = analyse("Enter your UPI PIN to receive Rs 5000 cashback.", use_classifier=False)
    assert r.level == "danger"
    assert r.findings[0].id == "pin_to_receive"
    assert "no_pin" in r.actions


def test_weak_signals_alone_do_not_warn():
    r = analyse("Meeting today at 6 pm, come immediately after work.", use_classifier=False)
    assert r.level == "none"


def test_strong_signal_gives_caution():
    r = analyse("Your KYC has expired. Visit your branch.", use_classifier=False)
    assert r.level == "caution"


def test_never_says_safe_and_has_general_advice():
    r = analyse("Hi Amma, reached home.", use_classifier=False)
    assert r.level == "none"
    for lang in LANGS:
        assert "safe" not in UI[lang]["level_none"].lower()


def test_otp_delivery_is_tip_not_warning():
    r = analyse("482913 is your OTP. Do not share it with anyone.", use_classifier=False)
    assert r.level == "none"
    assert [t.id for t in r.tips] == ["otp_message"]
    assert r.actions == []


def test_classifier_skipped_for_non_latin_text():
    r = analyse("அம்மா, நாளை காலை வருகிறேன்.")
    assert r.classifier.used is False


def test_classifier_cannot_lower_a_warning():
    r = analyse("Scan this QR code to receive your payment.")
    assert r.level == "danger"


def test_zero_width_characters_do_not_hide_keywords():
    r = analyse("Enter your U​PI P​IN to rece​ive money", use_classifier=False)
    assert r.level == "danger"


def test_defang():
    assert defang("go to http://bit.ly/x now") == "go to hxxp://bit[.]ly/x now"
    assert defang("visit sbi-kyc.online") == "visit sbi-kyc[.]online"
    assert "@" in defang("pay to kbc.lottery@ybl")


def test_negation():
    t = normalise("Do not share this OTP with anyone")
    i = t.index("share")
    assert negated(t, i, i + 5)


def test_long_text_is_truncated_not_crashing():
    r = analyse("hello " * 5000, use_classifier=False)
    assert r.level == "none"


def test_leetspeak_is_undone_for_keywords_only():
    from kedayam.textutil import parse

    m = parse("You have W0N Rs 5,00,000. Call 7000012345")
    assert "won" in m.words
    assert "5,00,000" in m.words
    assert m.mobiles == ["7000012345"]
    assert len(m.words) == len(m.norm)


def test_classifier_does_not_change_level():
    # A normal bank credit alert that the wording classifier scores high.
    r = analyse("Dear customer, Rs 10,000 credited to your a/c XX4321 by NEFT. Avl bal Rs 45,210. -Axis Bank")
    assert r.level == "none"


def test_quotes_keep_original_case():
    r = analyse("Please enter your UPI PIN to receive the Amazon refund", use_classifier=False)
    assert "UPI PIN" in r.findings[0].evidence[0]
