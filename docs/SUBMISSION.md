# Text for the Devpost form

Plain text, ready to paste. Numbers come from `eval/RESULTS.md`; regenerate with `uv run kedayam-eval` and update them here if the rules change.

## Name and pitch

**Kedayam** (Tamil for "shield")

Check before you pay: a local scam checker that explains suspicious UPI and SMS messages to older parents in India, in Tamil, Hindi or English, and never says "safe".

## Links

* Try it live: https://kedayam.140-245-16-129.sslip.io (switch language at the top, and try the example messages in the README). Messages and screenshots are checked in memory and never saved or logged. Family setup is kept in memory for your browser only.
* Source code: [GITHUB REPO LINK]
* Demo video: [YOUTUBE LINK]

## Who it helps, the risk, the improvement

* **User:** a retired parent in India who uses UPI and reads English slowly, and the son or daughter who worries about them.
* **Risk:** messages that push them to enter a UPI PIN "to receive" money, call an "electricity officer", update KYC through a link, install a screen sharing app or share an OTP.
* **Improvement:** before acting, they paste the message or a screenshot and get a plain answer in their language: what the trick is, the words that gave it away, and what to do now, starting with "call your son first".

## One example of the safer outcome

Lakshmi, 67, receives: "உங்கள் மின் இணைப்பு இன்று இரவு 9.30 மணிக்கு துண்டிக்கப்படும். உடனடியாக மின்சார அதிகாரியை தொடர்பு கொள்ளவும் 7000078901" (your electricity will be cut tonight at 9.30, call the officer now). Instead of calling the number, she pastes it into Kedayam. It shows, in Tamil, "Warning: this looks like a scam", explains that electricity boards do not ask you to call an officer's mobile number to stop a disconnection tonight, and lists what to do: call her son Ravi on the number he saved, do not call the number in the message, check the bill on the official app, and call 1930 if money was lost. She calls Ravi, and no money moves.

## One limitation

Kedayam only recognises the tricks it has rules for. In a test set written from recent news reports after the rules were frozen, it flagged 10 of 14 scams but missed WhatsApp "stock tip" investment groups and a "please forward the code I sent you by mistake" WhatsApp hijack. Such messages get "No known scam pattern found", which is why Kedayam never says a message is safe and always shows general advice.

## Evidence

* Public SMS phishing dataset (Mishra and Soni, CC BY 4.0), 876 held out messages: precision 1.000, no false alarms on 726 legitimate messages, 49 of 92 smishing messages flagged.
* 80 hand-written messages from RBI, NPCI, I4C and DoT advisories (committed before the rules): 45 of 45 scams flagged, 0 of 35 false alarms. Same author as the rules, so this shows coverage, not real-world accuracy.
* 20 messages written from news reports after the rules were frozen: 10 of 14 scams flagged, 0 of 6 false alarms.
* 10 synthetic phone screenshots in three languages, including blurred photo-like ones: same result as typed text in 10 of 10.
* The statistical wording model was taken out of the decision after it flagged 16 of 35 normal bank and service messages; the history is in `eval/HISTORY.md`.

## Built during the event and reused

Built during SafeSpace Hacks (from 4 November 2026; see the git history): the rules engine and all 28 rules, the trilingual text, the web app and its design, screenshot handling around Tesseract, family mode, the logo, the hand-written and news-based test sets, the screenshot fixtures, the evaluation and all documentation.

Reused: Tesseract OCR and its tessdata_fast English, Tamil and Hindi models (Apache 2.0); FastAPI, Starlette, Uvicorn, Jinja2, scikit-learn, Pillow, python-multipart, pytest, httpx; the Mishra and Soni SMS Phishing Dataset (CC BY 4.0); scam patterns and advice from public RBI, NPCI, Ministry of Home Affairs (I4C) and DoT advisories.

Hosting for the public demo: an Oracle Cloud Always Free VM (Docker behind Caddy); `modal_app.py` is kept as an alternative host.

[AI-ASSISTANCE CREDITS LINE]

## Technologies

Python 3.12 with uv, FastAPI, Jinja2 server-rendered HTML and CSS (no JavaScript), scikit-learn, Tesseract OCR, pytest. The public demo runs on an Oracle Cloud Always Free VM.

## Challenges and what we learned

* A model with 0.97 precision on its own dataset raised false alarms on almost half of ordinary Indian bank messages, because "normal" in its training data meant personal chat. Testing on messages like the real user's mattered more than the headline score.
* OCR puts invisible joiners inside Tamil words and splits links across lines, which silently broke the rules until we tested with real rendered screenshots.
* A strict "no referrer" privacy header made Chrome mark our own forms as coming from nowhere, which our new anti-forgery check then refused. Only a test in a real browser caught it.
* Writing warnings for an older reader meant shorter sentences, one action per line, and never relying on colour alone.

## Setup for judges

The quickest way is the live demo: https://kedayam.140-245-16-129.sslip.io. It is the same code with `KEDAYAM_HOSTED=1`: it accepts its own host name, keeps family setup in memory per browser, and says on the page that it is a public demo. To run it on your own computer, see the README: `uv sync`, `uv run kedayam`, open http://127.0.0.1:8740. Screenshot checking needs `brew install tesseract` (or `apt install tesseract-ocr`) and `uv run kedayam-ocr-setup` once.
