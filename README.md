<img src="src/kedayam/static/logo-512.png" width="112" alt="Kedayam logo, a kolam: one unbroken line looped round four dots, guarding the one in the middle">

# Kedayam

Kedayam (கேடயம், Tamil for "shield") helps older parents in India check a suspicious SMS or WhatsApp message before acting on it. Paste the message and Kedayam says, in plain English, Tamil or Hindi, whether it matches a known UPI or SMS scam pattern, why, and what to do next.

It runs on your own computer. The message is never sent anywhere.

* **Who it is for:** a retired parent who uses UPI and gets messages about refunds, KYC, electricity bills, prizes or "police cases", and the son or daughter who sets it up for them.
* **The safer outcome:** a message like "To receive your refund, accept the request and enter your UPI PIN" gets a clear "Warning: this looks like a scam", the reason in their language ("The UPI PIN is only for sending money"), and the next step (do not enter the PIN, call the bank on the number on your card, call 1930 if money was lost).
* **One limitation:** Kedayam only knows the tricks it has rules for. A new scam script that avoids those patterns gets "No known scam pattern found", which is why it never says "safe".

A two minute demo script is in [docs/DEMO.md](docs/DEMO.md) and ready-to-paste submission text in [docs/SUBMISSION.md](docs/SUBMISSION.md). See [DESIGN.md](DESIGN.md) for the user, the harm, how success is measured and the responsible design choices, and [RULES.md](RULES.md) for the hackathon rules this was built to.

## Run it

You need [uv](https://docs.astral.sh/uv/) and macOS or Linux. uv installs Python 3.12 for you if needed.

```sh
git clone <this repository> kedayam
cd kedayam
uv sync
uv run kedayam
```

Then open http://127.0.0.1:8740 in a browser. The first start trains the small wording model from the dataset in `data/` (a few seconds); later starts reuse it. Press Ctrl+C to stop.

If port 8740 is busy, choose another: `KEDAYAM_PORT=8741 uv run kedayam`.

### Screenshot checking (optional)

To check screenshots as well as pasted text, install the Tesseract OCR program and download its English, Tamil and Hindi language data once:

```sh
brew install tesseract              # macOS
# sudo apt install tesseract-ocr    # Debian or Ubuntu instead
uv run kedayam-ocr-setup
```

`kedayam-ocr-setup` downloads three files (about 8.5 MB) from the tessdata_fast project into `vendor/tessdata/` with curl and checks each against a pinned SHA-256 hash. Restart `uv run kedayam` and an "Or check a screenshot" box appears on the home page. Without this step Kedayam still works for pasted text and hides the screenshot box.

After reading a screenshot, Kedayam shows the text it read above the result, in a box you can correct and check again.

Try these fictional messages:

* `Dear customer, you have a refund of Rs 4,999 pending. To receive the amount please accept the request and enter your UPI PIN.`
* `அன்புள்ள வாடிக்கையாளரே, உங்கள் மின் இணைப்பு இன்று இரவு 9.30 மணிக்கு துண்டிக்கப்படும். உடனடியாக மின்சார அதிகாரியை தொடர்பு கொள்ளவும் 7000078901`
* `आपका SBI खाता KYC अपडेट न होने के कारण आज बंद कर दिया जाएगा। तुरंत इस लिंक पर क्लिक करें: http://sbi-kyc.online`
* `482913 is your OTP for login. Do not share this OTP with anyone.` (a normal message: no warning, plus a safety tip)

Sample screenshots to upload are in `tests/fixtures/screenshots/`.

### Family mode (optional)

A son, daughter or carer can open "Family setup" from the footer (http://127.0.0.1:8740/family) on the parent's computer and enter the parent's language, their own name and phone number, and optionally the bank's helpline from the back of the card. After that:

* Kedayam opens in the parent's language.
* Every warning starts with "Call Ravi on +91 70000 11111 before you do anything", and lists the bank helpline.
* "Print a reminder card" gives a one page card with the key rules and the numbers, to keep near the phone.

This is saved only in `instance/family.json` on that computer (owner-only file permissions, git-ignored; set `KEDAYAM_DATA_DIR` to keep it elsewhere). "Remove family setup" deletes it.

## Test and evaluate

```sh
uv run pytest
uv run kedayam-eval
```

`pytest` runs a catching case and a non-catching case for every rule, checks that every rule and screen has text in all three languages, and checks the privacy headers, link defanging, HTML escaping and screenshot uploads. Screenshot tests that need Tesseract are skipped if it is not set up.

`kedayam-eval` rewrites [eval/RESULTS.md](eval/RESULTS.md). Current results:

| Test set | What it is | Precision | Recall | False alarms |
| --- | --- | --- | --- | --- |
| Hand-written holdout | 45 scam and 35 normal messages in English, Tamil, Hindi and mixed script, based on RBI, NPCI, I4C and DoT advisories | 1.000 | 1.000 | 0 of 35 |
| Public dataset test split | 876 messages from the Mishra and Soni SMS phishing dataset; rules were tuned only on its train and validation splits | 1.000 | 0.333 (smishing 49 of 92, marketing spam 1 of 58) | 0 of 726 |
| News-based synthetic set | 14 scam and 6 normal messages written from news reports of newer scam types after the rules were frozen, committed before the first run | 1.000 | 0.714 | 0 of 6 |

Screenshots: on 10 synthetic phone screenshots (English, Tamil, Hindi; light and dark; 3 made to look like a tilted, blurred phone photo), the result from the screenshot matched the result from typing the text in 10 of 10, with 0.88 to 1.00 of the words read correctly. These are rendered images, not real photos.

Read these honestly. The holdout set was committed before any rule existed, but the same person wrote both, so a perfect score shows the rules cover the advisory patterns, not real-world accuracy. On the public test split, which was not used for tuning, Kedayam raised no false alarms and flagged just over half of the smishing messages, mostly as "Be careful"; it misses much of the UK premium-rate marketing spam in that dataset, which it was not built for. [eval/HISTORY.md](eval/HISTORY.md) records each run, including why the wording model was removed from the decision: it flagged 16 of 35 normal bank and service messages.

To retrain the wording model by hand: `uv run kedayam-train`.

## How it works

* `src/kedayam/rules.py`: 28 readable rules, one per scam pattern, each with a weight and a cited public source. One critical pattern (such as "enter PIN to receive") gives a Warning. Weaker signs (urgency, a threat to block the account, a mobile number to call) add up.
* `src/kedayam/engine.py`: runs the rules and picks one of three results: "Warning: this looks like a scam", "Be careful", or "No known scam pattern found".
* `src/kedayam/classifier.py`: TF-IDF and logistic regression on the public dataset. Shown as a hint for English text only; it does not change the result.
* `src/kedayam/ocr.py`: screenshot reading with Tesseract (English, Tamil and Hindi together). The image is decoded and passed to Tesseract in memory, never written to disk.
* `src/kedayam/app.py` and `templates/`: FastAPI with server-rendered HTML and one stylesheet. No JavaScript.
* `src/kedayam/family.py`: family mode storage and validation.
* `src/kedayam/i18n.py`: all text in English, Tamil and Hindi.

## Privacy and safety choices

* The server only listens on 127.0.0.1. Messages and screenshots are processed in memory and are not saved or logged; access logging is off. Uploads up to 8 MB are kept in memory (larger ones are refused), so a screenshot is never written to a temporary file.
* Pages send `Cache-Control: no-store` and a Content Security Policy that blocks all scripts and outside resources.
* Links in a checked message are shown defanged (`hxxp://sbi-kyc[.]online`) so they cannot be tapped from Kedayam.
* Every result has an "I think this result is wrong" section that explains how to verify independently.
* Kedayam refuses requests addressed to any host name other than 127.0.0.1 or localhost, and refuses form posts from other websites, so a web page you visit cannot quietly change the family contact number.
* All example messages, phone numbers and UPI IDs are made up.

## Credits and data

* SMS Phishing Dataset for Machine Learning and Pattern Recognition, Sandhya Mishra and Devpriya Soni, Mendeley Data, 2022, doi:10.17632/f45bkkt8pr.1, licensed CC BY 4.0. Included unchanged in `data/smishing/`; see [PROVENANCE.md](data/smishing/PROVENANCE.md) for how it is used.
* Scam patterns and safety advice: RBI BE(A)WARE booklet (2022), NPCI UPI Safety Shield, Ministry of Home Affairs (I4C) on digital arrest scams, DoT Sanchar Saathi Chakshu. Details in [data/handwritten/SOURCES.md](data/handwritten/SOURCES.md).
* OCR: Tesseract (Apache 2.0) and the tessdata_fast English, Tamil and Hindi models (Apache 2.0), https://github.com/tesseract-ocr. Downloaded at setup, not included in this repository.
* Libraries: FastAPI, Starlette, Uvicorn, Jinja2, scikit-learn, joblib, Pillow, python-multipart, pytest, httpx.
* Test screenshots in `tests/fixtures/screenshots/` are synthetic: rendered with headless Chrome from the HTML files beside them. They imitate no real app or brand.
* Everything else in this repository was written for SafeSpace Hacks between 4 and 22 November 2026.

## Licence

Code: MIT. The dataset in `data/smishing/` keeps its CC BY 4.0 licence.
