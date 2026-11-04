# Kedayam design

Kedayam (கேடயம், pronounced KAY-duh-yum) is the Tamil word for a shield: the thing that stands between you and harm (கேடு). The project was first called Kavach and was renamed on 4 November 2026 because that name is already widely used; see "Name search" at the end.

## The user

A retired parent in India, usually over 60, who has a smartphone with UPI (Google Pay, PhonePe, Paytm or a bank app) and gets SMS and WhatsApp messages in English, Tamil or Hindi. They are careful, but they were not raised with digital payments, and they often read English slowly. When a message worries them, their usual option today is to call a son or daughter, who may be at work or in another city.

A second user is that son or daughter, who wants to set things up once so the parent can check a message alone.

## The situation and the harm

The moment Kedayam is built for: a message arrives that says the electricity will be cut tonight, or that a refund is waiting, or that the KYC has expired, or that a parcel was seized by customs. It asks the reader to tap a link, call a number, scan a QR code, approve a request, install an app or tell an OTP. The person has a few minutes of doubt.

The harm is direct money loss through UPI, card or net banking, and often loss of savings. The core trick in many UPI scams is simple: the victim is told they will receive money, but the action they are asked to take (entering the UPI PIN, scanning a QR code, approving a collect request) sends money instead. NPCI's own guidance is that the UPI PIN is only entered to send money and is never needed to receive it.

## What Kedayam does

1. The person pastes or forwards the message text, or uploads a screenshot.
2. Kedayam checks it on the same computer against a list of known scam patterns drawn from public advisories by RBI, NPCI, I4C (Ministry of Home Affairs) and the Department of Telecommunications.
3. It shows one of three results, in large text, in the language the person picked:
   * **Warning: this looks like a scam.** At least one strong pattern was found (for example "enter your PIN to receive money").
   * **Be careful.** Some warning signs were found, but not a definite scam pattern.
   * **No known scam pattern found.** Kedayam never says a message is safe. It says what it checked and gives general advice.
4. Under the result it lists each reason in plain words, quotes the part of the message that triggered it, and says what to do: do not enter the PIN, do not tap the link, call the bank on the number printed on the card or passbook, and if money was lost, call 1930 or report at cybercrime.gov.in at once.

## How success is measured

* **Recall on scam patterns that matter.** On a hand-written set of realistic Indian scam messages based on public advisories, what share does Kedayam flag as "Warning" or "Be careful"?
* **False alarms on ordinary messages.** On real legitimate messages (bank debit alerts, OTP messages, bill reminders, family chat), how often does Kedayam raise a warning? A tool that cries wolf trains people to ignore it.
* **Classifier precision and recall** on a held-out split of a public, openly licensed SMS phishing dataset, reported honestly with its limits (it is mostly English and not Indian UPI specific).
* **Usability.** Can a person who reads slowly get from "I have a message" to "I know what to do" in one screen and one button press. Large text, high contrast, WCAG AA.

The hand-written holdout set was written and committed before the rules were tuned. Results on it are reported as measured, including misses.

## Trust and responsible design

* **Nothing leaves the device.** The server listens on 127.0.0.1 only. No analytics, no external fonts or scripts, no network calls at check time. Messages and screenshots are processed in memory and not stored or logged.
* **Never claims "safe".** The best result is "no known scam pattern found", with a reminder that new tricks appear every week.
* **Explains every flag.** Each reason names the pattern, quotes the triggering words, and links to the public advisory it comes from. The rules are plain Python that anyone can read.
* **Links are shown defanged.** Any web link in the result is displayed as text that cannot be tapped (for example `hxxp://bit[.]ly/...`), so the tool never puts a dangerous link one tap away.
* **Classifier can only add caution.** The statistical model can raise "No known pattern" to "Be careful", never lower a rule-based warning. Its role and its training data are stated on screen.
* **The user can disagree.** Every result has an "I think this is wrong" path that explains how to check independently (call the person or bank on a number you already have) instead of asking the user to trust Kedayam.
* **Not an emergency service.** Kedayam points to 1930, cybercrime.gov.in and the bank. It does not report anything itself and does not replace them.
* **Synthetic demo data only.** All phone numbers, UPI IDs and links in examples and tests are made up.

## Limits

* Pattern rules catch known tricks. A new script written to avoid these phrases can pass as "no known scam pattern found".
* The classifier is trained on a public dataset that is mostly English. It knows little about Tamil or Hindi wording, so in those languages Kedayam relies on the rules.
* Tamil and Hindi keyword coverage is smaller than English, and mixed-script messages (Tanglish, Hinglish) are only partly covered.
* OCR on low-quality screenshots can misread text, so the extracted text is always shown with the result, in a box the user can correct and check again. On a tilted, blurred test image a link came out as "nttp://sbi-kyc-. update.xyz", so link checks are weaker on screenshots than on pasted text. If very little text was read, the result page says so.
* The "Choose file" button text comes from the browser, so it follows the phone's language rather than the language picked in Kedayam.
* Kedayam cannot check whether a UPI ID, phone number or link belongs to a real bank. It only checks for impersonation patterns.
* The Tamil and Hindi wording should be reviewed by native speakers who work with older adults.

## Architecture

* Python 3.12, managed with uv.
* `kedayam.rules`: one function per scam pattern, each with an id, a weight, trilingual explanation and a source.
* `kedayam.engine`: runs the rules and the classifier and decides the verdict.
* `kedayam.classifier`: TF-IDF character n-grams with logistic regression (scikit-learn), trained locally from the dataset in `data/`.
* `kedayam.app`: FastAPI with Jinja2 templates. Server rendered HTML and one CSS file. Almost no JavaScript.
* `kedayam.ocr`: Tesseract with English, Tamil and Hindi language data (tessdata_fast, hashes pinned). Images stay in memory; status bar lines are dropped and links broken across lines are rejoined before the rules run.

## Logo

`src/kedayam/static/logo.svg` (and a 512 px PNG, `logo-512.png`): a violet shield with a blue field holding a watchful eye whose lower edge is a check mark, for "look, then check, before you pay". It uses only the theme colours. It deliberately avoids rupee signs, arrows, the tricolour, the Ashoka emblem, a tiger or palm tree, and bank-style roundels, so it does not resemble any bank, NPCI, UPI, RBI or government mark. It was drawn by hand for this project as a plain SVG.

## Name search

Requirement: a short, pronounceable name with no notable existing product, app, company or trademark, ideally meaning shield, guard or "check before you pay". Searched on 4 November 2026.

| Candidate | Meaning | App Store (India, US) | Google Play (India) | GitHub repositories | Web | Domain | Decision |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Kavach | shield (Sanskrit, Hindi) | 18+ apps named Kavach (M-Kavach 2, Mobile Kavach, Kavach User, Kavach Qr...) | 18+ apps with "kavach" in the package id | 100+ (top: LucidAkshay/kavach, 260 stars) | Indian Railways' Kavach train protection system; several government and security apps | | Rejected |
| Dhaal | shield (Hindi ढाल) | "Dhaal", "DhaalPay" | "Dhaal Pay" | 24 | | | Rejected: a payment app already uses it |
| Trana | protection (Sanskrit त्राण) | "Trana", "Trana - Fitness & Nutrition", a Korean trading app | "Trana Med Erika" | 100+ (TranAD, 708 stars) | | | Rejected |
| Jaanch | check (Hindi जाँच) | none | none | 38, including three created between 21 October and 2 November 2026 | | | Rejected: likely other entrants in this period |
| Nillu | stop (Tamil நில்லு) | none | none | 36 | | | Not chosen: weaker meaning |
| Paarthu | carefully, after looking (Tamil பார்த்து) | none | none | 18, none a product (mostly "Paarthurnax") | nearest hit is a singer named Parthu | paarthu.com registered November 2025, no site | Runner up: the registered domain suggests someone may plan to use it |
| **Kedayam** | **shield (Tamil கேடயம்)** | **none** | **none** | **1, empty, no description (coderxdk-1812/kedayam)** | **no product or company found** | **kedayam.com unregistered (WHOIS: no match)** | **Chosen** |

Method: Apple's public iTunes Search API (`entity=software`, countries `in` and `us`), the Google Play web search page for India, `gh search repos`, a general web search, `whois`. Trademark registries (IP India, WIPO Global Brand Database) were not searched because they need an interactive browser session. That should be checked before any use beyond this hackathon prototype.

Note for Malayalam speakers: Malayalam "കേട്" means "spoilt" or "broken". Kedayam is the Tamil word for shield and reads naturally to Tamil speakers, the first audience. Hindi speakers see the transliteration केडयम.
