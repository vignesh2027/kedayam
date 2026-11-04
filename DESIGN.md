# Kavach design

Kavach means "shield" in Sanskrit, and the word is used the same way in Tamil and Hindi.

## The user

A retired parent in India, usually over 60, who has a smartphone with UPI (Google Pay, PhonePe, Paytm or a bank app) and gets SMS and WhatsApp messages in English, Tamil or Hindi. They are careful, but they were not raised with digital payments, and they often read English slowly. When a message worries them, their usual option today is to call a son or daughter, who may be at work or in another city.

A second user is that son or daughter, who wants to set things up once so the parent can check a message alone.

## The situation and the harm

The moment Kavach is built for: a message arrives that says the electricity will be cut tonight, or that a refund is waiting, or that the KYC has expired, or that a parcel was seized by customs. It asks the reader to tap a link, call a number, scan a QR code, approve a request, install an app or tell an OTP. The person has a few minutes of doubt.

The harm is direct money loss through UPI, card or net banking, and often loss of savings. The core trick in many UPI scams is simple: the victim is told they will receive money, but the action they are asked to take (entering the UPI PIN, scanning a QR code, approving a collect request) sends money instead. NPCI's own guidance is that the UPI PIN is only entered to send money and is never needed to receive it.

## What Kavach does

1. The person pastes or forwards the message text, or uploads a screenshot.
2. Kavach checks it on the same computer against a list of known scam patterns drawn from public advisories by RBI, NPCI, I4C (Ministry of Home Affairs) and the Department of Telecommunications.
3. It shows one of three results, in large text, in the language the person picked:
   * **Warning: this looks like a scam.** At least one strong pattern was found (for example "enter your PIN to receive money").
   * **Be careful.** Some warning signs were found, but not a definite scam pattern.
   * **No known scam pattern found.** Kavach never says a message is safe. It says what it checked and gives general advice.
4. Under the result it lists each reason in plain words, quotes the part of the message that triggered it, and says what to do: do not enter the PIN, do not tap the link, call the bank on the number printed on the card or passbook, and if money was lost, call 1930 or report at cybercrime.gov.in at once.

## How success is measured

* **Recall on scam patterns that matter.** On a hand-written set of realistic Indian scam messages based on public advisories, what share does Kavach flag as "Warning" or "Be careful"?
* **False alarms on ordinary messages.** On real legitimate messages (bank debit alerts, OTP messages, bill reminders, family chat), how often does Kavach raise a warning? A tool that cries wolf trains people to ignore it.
* **Classifier precision and recall** on a held-out split of a public, openly licensed SMS phishing dataset, reported honestly with its limits (it is mostly English and not Indian UPI specific).
* **Usability.** Can a person who reads slowly get from "I have a message" to "I know what to do" in one screen and one button press. Large text, high contrast, WCAG AA.

The hand-written holdout set was written and committed before the rules were tuned. Results on it are reported as measured, including misses.

## Trust and responsible design

* **Nothing leaves the device.** The server listens on 127.0.0.1 only. No analytics, no external fonts or scripts, no network calls at check time. Messages and screenshots are processed in memory and not stored or logged.
* **Never claims "safe".** The best result is "no known scam pattern found", with a reminder that new tricks appear every week.
* **Explains every flag.** Each reason names the pattern, quotes the triggering words, and links to the public advisory it comes from. The rules are plain Python that anyone can read.
* **Links are shown defanged.** Any web link in the result is displayed as text that cannot be tapped (for example `hxxp://bit[.]ly/...`), so the tool never puts a dangerous link one tap away.
* **Classifier can only add caution.** The statistical model can raise "No known pattern" to "Be careful", never lower a rule-based warning. Its role and its training data are stated on screen.
* **The user can disagree.** Every result has an "I think this is wrong" path that explains how to check independently (call the person or bank on a number you already have) instead of asking the user to trust Kavach.
* **Not an emergency service.** Kavach points to 1930, cybercrime.gov.in and the bank. It does not report anything itself and does not replace them.
* **Synthetic demo data only.** All phone numbers, UPI IDs and links in examples and tests are made up.

## Limits

* Pattern rules catch known tricks. A new script written to avoid these phrases can pass as "no known scam pattern found".
* The classifier is trained on a public dataset that is mostly English. It knows little about Tamil or Hindi wording, so in those languages Kavach relies on the rules.
* Tamil and Hindi keyword coverage is smaller than English, and mixed-script messages (Tanglish, Hinglish) are only partly covered.
* OCR on low-quality screenshots can misread text, so the extracted text is always shown with the result, in a box the user can correct and check again. On a tilted, blurred test image a link came out as "nttp://sbi-kyc-. update.xyz", so link checks are weaker on screenshots than on pasted text. If very little text was read, the result page says so.
* The "Choose file" button text comes from the browser, so it follows the phone's language rather than the language picked in Kavach.
* Kavach cannot check whether a UPI ID, phone number or link belongs to a real bank. It only checks for impersonation patterns.
* The Tamil and Hindi wording should be reviewed by native speakers who work with older adults.

## Architecture

* Python 3.12, managed with uv.
* `kavach.rules`: one function per scam pattern, each with an id, a weight, trilingual explanation and a source.
* `kavach.engine`: runs the rules and the classifier and decides the verdict.
* `kavach.classifier`: TF-IDF character n-grams with logistic regression (scikit-learn), trained locally from the dataset in `data/`.
* `kavach.app`: FastAPI with Jinja2 templates. Server rendered HTML and one CSS file. Almost no JavaScript.
* `kavach.ocr`: Tesseract with English, Tamil and Hindi language data (tessdata_fast, hashes pinned). Images stay in memory; status bar lines are dropped and links broken across lines are rejoined before the rules run.
