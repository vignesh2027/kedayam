"""Every rule has at least one message it must catch and one it must not.

These dev examples are separate from data/handwritten/holdout.jsonl, which
is only used by the evaluation script.
"""

import pytest

from kedayam.rules import RULES, RULES_BY_ID, brand_in, is_official
from kedayam.textutil import parse

CASES = {
    "pin_to_receive": (
        [
            "Your cashback of Rs 750 is ready. Enter UPI PIN to receive it in your account.",
            "To get the refund amount, please type your MPIN on the next screen.",
            "कैशबैक पाने के लिए अपना पिन डालें।",
            "கேஷ்பேக் பெற உங்கள் பின் நம்பர் உள்ளிடவும்.",
        ],
        [
            "Never enter your UPI PIN to receive money.",
            "You do not need to enter a PIN to receive money.",
            "Rs 750 received in your account from Suresh via UPI.",
        ],
    ),
    "qr_to_receive": (
        ["Please scan the QR I sent to receive the advance for your bike."],
        ["Scan the QR code at the counter to pay for your order.", "Do not scan any QR code to receive money."],
    ),
    "collect_request_lure": (
        [
            "A collect request for your Diwali bonus has been sent. Approve it now.",
            "Accept the request in GPay to claim your reward of Rs 999.",
        ],
        ["Your request for a duplicate passbook has been received.", "You have a payment request from Kumar for Rs 300 for dinner."],
    ),
    "otp_request": (
        [
            "Please send the OTP you received to this number to verify.",
            "Sir, read out the 6 digit code that just came on your phone.",
            "आपके फोन पर आया ओटीपी बताओ जल्दी।",
            "உங்களுக்கு வந்த OTP யை சொல்லுங்கள்.",
        ],
        [
            "Your OTP is 849302. Do not share it with anyone.",
            "Never share your OTP with anyone, the bank will never ask for it.",
            "आपका OTP 1234 है। इसे किसी के साथ शेयर न करें।",
        ],
    ),
    "secret_details_request": (
        [
            "Kindly share your card number and CVV to stop the charge.",
            "Verify your net banking password at the link below.",
        ],
        ["We will never ask for your CVV or password.", "Your card number ending 1234 was used at a shop.", "Should I send you my account number for the gift?"],
    ),
    "screen_share_app": (
        ["Download TeamViewer so our engineer can fix your bank app.", "Please start screen sharing so I can guide you."],
        ["Never install AnyDesk when a caller asks you to.", "The team is viewing the new house tomorrow."],
    ),
    "apk_link": (
        ["Install the new KYC app: http://example-kyc.top/update.apk"],
        ["Install the app from the Play Store.", "Read the apkallu poem tonight."],
    ),
    "digital_arrest": (
        [
            "You are under digital arrest. Stay on this call.",
            "CBI officer will join the video call. Keep your camera on.",
        ],
        ["Join the family video call at 7 pm.", "We will discuss the case study on a video call."],
    ),
    "advance_fee": (
        [
            "Your loan of Rs 2 lakh is approved. Pay processing fee of Rs 1,999 to get it.",
            "You are selected for the job. Pay security deposit of Rs 3000 to confirm.",
        ],
        ["The school fee is due next week.", "Processing fee waived on your home loan, as discussed at the branch."],
    ),
    "wrong_transfer": (
        ["I transferred 3000 to you by mistake, please return it to my number."],
        ["I sent the wrong photo by mistake, sorry!", "Please return the book when you are done."],
    ),
    "lookalike_upi_id": (
        [
            "Pay the fine to sbi.recovery@ybl today.",
            "Send Rs 10 to refund.desk@paytm to receive your refund.",
            "Pay at tnebbill@okaxis",
        ],
        ["Pay to murugan.stores@okaxis for the vegetables.", "My UPI is ramesh1972@oksbi"],
    ),
    "lookalike_link": (
        ["Login at hdfc-netbanking-verify.com to continue.", "Visit amaz0n-offers.in for the prize."],
        ["Pay at https://www.hdfcbank.com today.", "Check your status at incometax.gov.in", "See onlinesbi.sbi"],
    ),
    "suspicious_link": (
        ["Check details at tinyurl.com/x8kq2", "Open http://198.51.100.7/pay", "Visit offer-zone.xyz now"],
        ["Read the notice at rbi.org.in", "Our new menu is at sangeetha-veg.com"],
    ),
    "fake_security_alert": (
        [
            "We noticed unusual activity on your net banking. Verify at http://secure-netbank-verify.top now",
            "Transaction of Rs 9,999 on your card. If this was not you, click https://cancel-txn.in/x",
        ],
        [
            "Rs 9,999 spent on your card. If not done by you, call 1800 000 1111. -Bank",
            "Unusual login on your account? Check at https://www.icicibank.com",
        ],
    ),
    "parcel_problem_link": (
        [
            "India Post: your parcel could not be delivered due to incomplete address. Update: http://indpost-track.top/a",
            "Courier delivery failed. Call 7000012345 to re-schedule.",
        ],
        ["Your parcel will be delivered today by 6 pm.", "Delivery failed, we will try again tomorrow. -Amazon"],
    ),
    "reward_link": (
        ["Your Rs 2,000 refund is ready. Claim it at http://refund-desk.online/claim", "Claim your Diwali gift: bit.ly/gift-ab"],
        ["Your refund of Rs 499 has been processed.", "Gift ideas for Diwali at https://www.amazon.in/diwali"],
    ),
    "account_block_threat": (
        [
            "Your PAN card will be deactivated tonight. Update at once.",
            "आपका KYC ब्लॉक हो गया है।",
            "WE WILL HOLD YOUR WALLET AMOUNT, COMPLETE YOUR KYC",
            "WE WILL HOLD YOUR PAYTM AMOUNT AFTER SOMETIME COMPLETE YOUR PAYTM KYC",
            "Your ATM card has just been De-Activated. To activate call customer care.",
            "Your account will be suspended today. Log in to avoid suspension.",
        ],
        [
            "Please complete your KYC at the branch at your convenience.",
            "The road is blocked near the temple.",
            "Your debit card ending 4321 has been blocked as per your request.",
        ],
    ),
    "utility_disconnection": (
        ["Your power supply will be disconnected today. Call 7000011111.", "बिजली कट जाएगी, तुरंत अधिकारी से संपर्क करें।"],
        ["Pay your electricity bill by the due date to avoid disconnection.", "Power cut in our area from 10 to 2 for maintenance."],
    ),
    "authority_threat": (
        ["Customs has seized your parcel with illegal items.", "पुलिस ने आपके खिलाफ वारंट जारी किया है।"],
        ["Police verification for your tenant is complete.", "The court near our house has a new canteen."],
    ),
    "prize_lottery": (
        [
            "Congratulations, you have won an iPhone in our lucky draw!",
            "आपने लॉटरी जीती है।",
            "You have W0N a guaranteed cash prize of Rs.5,00,000. FL1PKART TEAM",
            "You are awarded with a Rs.2,00,000 Bonus Prize, call now",
        ],
        [
            "Congratulations on your daughter's wedding!",
            "We did not win the cricket match today.",
            "You won't believe how big the grandchildren have grown.",
        ],
    ),
    "easy_money_job": (
        ["Earn Rs 5000 daily by rating hotels online.", "घर बैठे कमाएँ हज़ारों रुपये।"],
        ["My son started his new job in Pune.", "Daily walk at 6 am in the park.", "She had a part time job and tuition before."],
    ),
    "family_money_request": (
        [
            "Appa this is my new number. Please send 15,000 now, I will explain.",
            "I had an accident, send money to this account fast.",
        ],
        ["Amma, my new number is saved? Call me when free.", "Visited grandma in hospital, she is fine now."],
    ),
    "sender_is_mobile_number": (
        [("Your SBI account is on hold. Contact branch.", "+91 70000 12345")],
        [("Your SBI account is on hold. Contact branch.", "AX-SBIINB-S"), ("Reached home safely.", "7000012345")],
    ),
    "urgency": (
        ["Reply immediately or lose your benefit.", "உடனே பதில் அனுப்புங்கள்", "तुरंत जवाब दें"],
        ["See you next week at the wedding.", "I will call you tomorrow."],
    ),
    "secrecy": (
        ["Do not tell anyone about this offer.", "Keep this confidential until the officer calls."],
        ["Tell everyone the function starts at 6.", "Don't forget to take your medicine."],
    ),
    "call_this_number": (
        ["For help call 7000012345", "WhatsApp us on +91 90000 54321 for details", "KYC OFFICE PH 7000099999"],
        ["Call 1800 000 1111 for help.", "Call me when you reach."],
    ),
    "otp_message": (
        ["458921 is your OTP for login. Do not share it.", "आपका OTP 662211 है।"],
        ["Your order 458921 is shipped.", "Please send the OTP you received."],
    ),
    "has_link": (
        ["Photos are at photos.google.com/share/abc"],
        ["No link here, just a hello."],
    ),
}


def _msg(item):
    if isinstance(item, tuple):
        text, sender = item
        return parse(text, sender)
    return parse(item)


def test_every_rule_has_cases():
    assert set(CASES) == {r.id for r in RULES}


@pytest.mark.parametrize("rule_id,text", [(rid, t) for rid, (pos, _) in CASES.items() for t in pos])
def test_rule_fires(rule_id, text):
    assert RULES_BY_ID[rule_id].check(_msg(text)), f"{rule_id} should fire on: {text}"


@pytest.mark.parametrize("rule_id,text", [(rid, t) for rid, (_, neg) in CASES.items() for t in neg])
def test_rule_quiet(rule_id, text):
    assert not RULES_BY_ID[rule_id].check(_msg(text)), f"{rule_id} should not fire on: {text}"


def test_brand_detection():
    assert brand_in("netf1ix-billing.com") == "netflix"
    assert brand_in("sbikyc") == "sbi"
    assert brand_in("bobby", bait=True) is None
    assert brand_in("rebecca") is None
    assert brand_in("helpdesk.cashback", bait=True) == "cashback" or brand_in("helpdesk.cashback", bait=True) == "helpdesk"


def test_official_domains():
    assert is_official("www.onlinesbi.sbi")
    assert is_official("uidai.gov.in")
    assert is_official("sbi.bank.in")
    assert not is_official("sbi-kyc.online")
    assert not is_official("gov.in.example.xyz")


def test_every_rule_has_text_in_all_languages():
    from kedayam.i18n import ACTION_TEXT, LANGS, RULE_TEXT, SOURCE_LINKS

    for r in RULES:
        assert r.id in RULE_TEXT, r.id
        for lang in LANGS:
            title, why = RULE_TEXT[r.id][lang]
            assert title and why
        for a in r.actions:
            assert all(ACTION_TEXT[a][lang] for lang in LANGS), a
        assert r.source in SOURCE_LINKS, r.source
