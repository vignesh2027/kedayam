# Kavach

Kavach ("shield") helps older parents in India check a suspicious SMS or WhatsApp message before acting on it. Paste the message and Kavach says, in plain English, Tamil or Hindi, whether it matches a known UPI or SMS scam pattern, why, and what to do next.

It runs on your own computer. The message is never sent anywhere.

* **Who it is for:** a retired parent who uses UPI and gets messages about refunds, KYC, electricity bills, prizes or "police cases", and the son or daughter who sets it up for them.
* **The safer outcome:** a message like "To receive your refund, accept the request and enter your UPI PIN" gets a clear "Warning: this looks like a scam", the reason in their language ("The UPI PIN is only for sending money"), and the next step (do not enter the PIN, call the bank on the number on your card, call 1930 if money was lost).
* **One limitation:** Kavach only knows the tricks it has rules for. A new scam script that avoids those patterns gets "No known scam pattern found", which is why it never says "safe".

See [DESIGN.md](DESIGN.md) for the user, the harm, how success is measured and the responsible design choices, and [RULES.md](RULES.md) for the hackathon rules this was built to.

## Run it

You need [uv](https://docs.astral.sh/uv/) and macOS or Linux. uv installs Python 3.12 for you if needed.

```sh
git clone <this repository> kavach
cd kavach
uv sync
uv run kavach
```

Then open http://127.0.0.1:8740 in a browser. The first start trains the small wording model from the dataset in `data/` (a few seconds); later starts reuse it. Press Ctrl+C to stop.

If port 8740 is busy, choose another: `KAVACH_PORT=8741 uv run kavach`.

Try these fictional messages:

* `Dear customer, you have a refund of Rs 4,999 pending. To receive the amount please accept the request and enter your UPI PIN.`
* `அன்புள்ள வாடிக்கையாளரே, உங்கள் மின் இணைப்பு இன்று இரவு 9.30 மணிக்கு துண்டிக்கப்படும். உடனடியாக மின்சார அதிகாரியை தொடர்பு கொள்ளவும் 7000078901`
* `आपका SBI खाता KYC अपडेट न होने के कारण आज बंद कर दिया जाएगा। तुरंत इस लिंक पर क्लिक करें: http://sbi-kyc.online`
* `482913 is your OTP for login. Do not share this OTP with anyone.` (a normal message: no warning, plus a safety tip)

## Test and evaluate

```sh
uv run pytest
uv run kavach-eval
```

`pytest` runs a catching case and a non-catching case for every rule, checks that every rule and screen has text in all three languages, and checks the privacy headers, link defanging and HTML escaping.

`kavach-eval` rewrites [eval/RESULTS.md](eval/RESULTS.md). Current results:

| Test set | What it is | Precision | Recall | False alarms |
| --- | --- | --- | --- | --- |
| Hand-written holdout | 45 scam and 35 normal messages in English, Tamil, Hindi and mixed script, based on RBI, NPCI, I4C and DoT advisories | 1.000 | 1.000 | 0 of 35 |
| Public dataset test split | 876 messages from the Mishra and Soni SMS phishing dataset, not used to write rules | 1.000 | 0.180 (smishing 27 of 92, marketing spam 0 of 58) | 0 of 726 |

Read these honestly. The holdout set was committed before any rule existed, but the same person wrote both, so a perfect score shows the rules cover the advisory patterns, not real-world accuracy. On the independent public data, Kavach raised no false alarms but caught under a third of the smishing messages. [eval/HISTORY.md](eval/HISTORY.md) records each run, including why the wording model was removed from the decision: it flagged 16 of 35 normal bank and service messages.

To retrain the wording model by hand: `uv run kavach-train`.

## How it works

* `src/kavach/rules.py`: 25 readable rules, one per scam pattern, each with a weight and a cited public source. One critical pattern (such as "enter PIN to receive") gives a Warning. Weaker signs (urgency, a threat to block the account, a mobile number to call) add up.
* `src/kavach/engine.py`: runs the rules and picks one of three results: "Warning: this looks like a scam", "Be careful", or "No known scam pattern found".
* `src/kavach/classifier.py`: TF-IDF and logistic regression on the public dataset. Shown as a hint for English text only; it does not change the result.
* `src/kavach/app.py` and `templates/`: FastAPI with server-rendered HTML and one stylesheet. No JavaScript.
* `src/kavach/i18n.py`: all text in English, Tamil and Hindi.

## Privacy and safety choices

* The server only listens on 127.0.0.1. Messages are processed in memory and are not saved or logged; access logging is off.
* Pages send `Cache-Control: no-store` and a Content Security Policy that blocks all scripts and outside resources.
* Links in a checked message are shown defanged (`hxxp://sbi-kyc[.]online`) so they cannot be tapped from Kavach.
* Every result has an "I think this result is wrong" section that explains how to verify independently.
* All example messages, phone numbers and UPI IDs are made up.

## Credits and data

* SMS Phishing Dataset for Machine Learning and Pattern Recognition, Sandhya Mishra and Devpriya Soni, Mendeley Data, 2022, doi:10.17632/f45bkkt8pr.1, licensed CC BY 4.0. Included unchanged in `data/smishing/`; see [PROVENANCE.md](data/smishing/PROVENANCE.md) for how it is used.
* Scam patterns and safety advice: RBI BE(A)WARE booklet (2022), NPCI UPI Safety Shield, Ministry of Home Affairs (I4C) on digital arrest scams, DoT Sanchar Saathi Chakshu. Details in [data/handwritten/SOURCES.md](data/handwritten/SOURCES.md).
* Libraries: FastAPI, Starlette, Uvicorn, Jinja2, scikit-learn, joblib, Pillow, python-multipart, pytest, httpx.
* Everything else in this repository was written for SafeSpace Hacks between 4 and 22 November 2026.

## Licence

Code: MIT. The dataset in `data/smishing/` keeps its CC BY 4.0 licence.
