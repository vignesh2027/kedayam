# Two minute demo script

Follows the Resources page advice: show the situation, the risk, the working solution and the outcome, then say what was built during the event, what was reused, and one limitation. Everything shown is fictional: the people, phone numbers, UPI IDs and links are made up.

## Before recording

```sh
export KEDAYAM_DATA_DIR=/tmp/kedayam-demo   # keeps demo family data out of the real folder
uv run kedayam
```

Open http://127.0.0.1:8740 in a browser at about 125% zoom. Have these ready to paste or upload:

* Tamil electricity message: the second example in the README.
* Screenshot: `tests/fixtures/screenshots/upi_collect_request.png`.
* Normal message: `482913 is your OTP for login. Do not share this OTP with anyone.`

Set up family mode once before recording (Family setup in the footer): language Tamil, name Ravi, phone +91 70000 11111, bank Indian Bank, helpline 1800 000 2222.

## Script

| Time | On screen | Narration |
| --- | --- | --- |
| 0:00 to 0:15 | Phone mockup with the Tamil electricity SMS | "This is Lakshmi, 67, in Chennai. At 8 pm she gets this: her electricity will be cut tonight unless she calls the 'officer' on this number. Her son Ravi is at work." |
| 0:15 to 0:30 | Kedayam home page in Tamil, privacy line visible | "If she calls, the next step is usually a screen sharing app or a 'small payment', and her savings go. Kedayam gives her a place to check first. It runs on her own computer, and the message never leaves it." |
| 0:30 to 0:55 | Paste the Tamil message, press the button, show the red Warning, scroll slowly | "She pastes the message. Kedayam says, in Tamil, that this looks like a scam. The first step is the one Ravi set up: call Ravi before doing anything. Then: do not call the number in the message, check the bill on the official app, and call 1930 if money was lost. Each reason quotes the words that triggered it and names the public advisory it comes from." |
| 0:55 to 1:15 | Switch to English, upload the UPI request screenshot | "Many scams arrive as a payment request. Here is a screenshot: a 'cashback' that asks for the PIN. Kedayam reads the picture in English, Tamil or Hindi, shows the text it read so mistakes can be fixed, and explains the key rule: your UPI PIN is only for sending money, never for receiving it." |
| 1:15 to 1:30 | Paste the normal OTP message | "A normal message gets 'No known scam pattern found', never 'safe', with a reminder never to share the code. There is also an 'I think this is wrong' section that tells her how to check for herself." |
| 1:30 to 1:40 | Family setup page, then the printed reminder card | "Ravi set this up once. It stays on this computer, and Kedayam refuses changes from other websites. The reminder card goes next to the phone." |
| 1:40 to 2:00 | README results table | "Everything in this repository was written during SafeSpace Hacks. It reuses Tesseract for reading screenshots, FastAPI and scikit-learn, and a CC BY phishing dataset. On that dataset's held out messages Kedayam raised no false alarms on 726 real messages and flagged about half of the smishing. The limit: it only knows the tricks it has rules for. A new script, like the WhatsApp stock tip groups in our news based test, can pass as 'no known pattern', which is exactly why it never says safe." |

About 300 words of narration, which fits two minutes at a calm pace.

## Shots to capture if recording is not possible

The `docs/screenshots/` folder already has every scene: 02 and 04 (Tamil home and warning), 08 (screenshot check), 07 (no pattern found), 12 to 14 (family mode and card).

## As recorded (8 Nov 2026)

The video follows this script on the hosted demo (https://applemacbook6sep2004--kedayam.us-east.modal.run) with family mode set up off camera first. It opens on a phone card with the fictional SMS, labelled as fictional. The README results step became an evaluation card with the same figures. It runs 2:38.8. Full notes: /Users/vignesh/dev-challenges/nov/video/kedayam-demo-notes.md.
