# Evaluation history

Each entry records what was run, what it showed, and what changed because of it. Numbers are copied from `eval/RESULTS.md` at the time.

## Run 1, 4 November 2026: first look at the frozen holdout set

Setup: 25 rules; the classifier (TF-IDF character n-grams with logistic regression, threshold 0.5 chosen on validation) was allowed to raise "No known pattern" to "Be careful".

Hand-written holdout set, 45 scam and 35 legitimate messages:

| System | Precision | Recall | False alarm rate |
| --- | --- | --- | --- |
| Rules only | 1.000 | 1.000 | 0.000 |
| Classifier only | 0.673 | 0.822 | 0.514 |
| Rules + classifier | 0.738 | 1.000 | 0.457 |

The classifier marked 16 of 35 ordinary messages as "Be careful", including an SBI debit alert (score 0.989), an Axis Bank credit alert (0.988), an HDFC OTP message, an Amazon delivery notice and an LIC premium reminder. In the public dataset the "ham" class is mostly personal chat, so any business SMS looks unusual to the model. Its 0.97 precision on the dataset's own test split did not carry over to Indian bank and service messages.

Change: the classifier no longer changes the result. It is still computed for English text and shown as a hint in the details, with its limits stated. A tool that warns about a real bank alert teaches people to ignore its warnings.

The perfect rules score is expected: the same author wrote the holdout set and then the rules, aiming at the same advisory patterns. It shows coverage, not real-world accuracy.

## Run 2, 4 November 2026: digit-for-letter spellings and prize wording

Looked only at smishing messages in the dataset's train split (not validation or test) to find patterns the rules missed. Found: digit-for-letter spellings ("W0N", "FL1PKART", "T0DAY'S"), "guaranteed cash prize", "awarded with a ... Bonus Prize", "HOLD YOUR PAYTM AMOUNT", and phone numbers introduced with "PH" or "Dial".

Changes: keyword rules now match on a copy of the text with digit-for-letter swaps undone inside words (numbers and amounts are untouched); prize, account hold and call-a-number patterns were extended; unit tests were added for each.

Results after the change:

* Holdout: rules precision 1.000, recall 1.000, false alarm rate 0.000 (unchanged).
* Public dataset test split, rules only: precision 1.000, recall 0.180, 0 false alarms on 726 legitimate messages. By original label, smishing 27 of 92 flagged, marketing spam 0 of 58.

The dataset test split was not used to choose any rule.

## Run 3, 4 November 2026: screenshot reading

Added Tesseract OCR with the tessdata_fast English, Tamil and Hindi models, all three loaded together. The best models were also tried and gave the same text on these images, so the smaller fast models are used.

Ten synthetic screenshots: seven clean renders (SMS, dark chat, a generic UPI payment request screen, Tamil, Hindi, a legitimate debit alert, and a 35% size JPEG), plus three made to look like a phone photo of a screen. All ten gave the same result as typing the text; word recall was 0.882 to 1.000.

Problems found and fixed while building it: Tesseract puts zero-width joiners inside Tamil words (now removed before matching), links broken across lines came out split (now rejoined), and phone status bar lines ("10:42 4G 72%", or "_ 48 72%" in the photo case) were read as message text (now dropped). Still open: on the blurred photo-like image a link was garbled to "nttp://sbi-kyc-. update.xyz", so link rules can miss on poor pictures.

## Run 4, 4 November 2026: raising smishing recall from the training split only

Goal set by the team: catch more smishing without raising false alarms, because a false warning on a real bank alert is worse for this user than a miss (and a miss still never says "safe").

Method: looked only at spam and smishing messages in the dataset's train and validation splits that the rules missed, and at the legitimate messages in those splits that the rules flagged. The test split was not looked at until the single run below.

Added general patterns rather than copies of specific messages:

* `fake_security_alert` (critical): "unusual activity", "if this was not you" and similar, together with a link to a site that is not an official bank or company domain.
* `parcel_problem_link` (strong): a parcel that "could not be delivered" or needs an "address update", with a link or a mobile number.
* `reward_link` (strong): a refund, prize, gift, bonus or cashback together with a non-official link.
* `account_block_threat` now also catches "your account or card will be / has been blocked, suspended or de-activated", but not when the message says it was "as per your request".
* Prize wording: "you've won ... prize", "claim ... cash", "awaiting collection", "you are a winner", "millions transferred to you".
* Lookalike links now also cover Apple, iCloud, PayPal, Microsoft, WhatsApp, Instagram, Facebook, Google and YouTube.

Development false alarms found and fixed on the way: "you won't" matched the prize pattern; "part time job" in ordinary chat matched the job scam pattern (it now needs an earning, salary, contact or amount nearby); "should I send you my account number" was treated as a request for secret details ("account number" removed from that list). Two development false alarms remain on purpose or as known noise: "Send me your id and password" (Kedayam warns, which is reasonable) and a riddle that mentions police and murder ("Be careful").

Development data (train and validation, used for tuning): smishing 132 of 451 (0.293) before, 236 of 451 (0.523) after; false alarms on legitimate messages 9 of 4,108 before, 2 of 4,108 after.

Test split, run once after tuning:

| | Before (run 2) | After (run 4) |
| --- | --- | --- |
| Smishing flagged | 27 of 92 (0.293) | 49 of 92 (0.533) |
| Marketing spam flagged | 0 of 58 | 1 of 58 |
| False alarms on legitimate messages | 0 of 726 | 0 of 726 |
| Precision | 1.000 | 1.000 |

Most of the new catches are "Be careful" rather than "Warning" (Warning-only recall on the test split stays at 0.020), which matches the intent: these patterns are warning signs, not proof. The hand-written holdout is unchanged at 45 of 45 scams flagged and 0 of 35 false alarms, and all 10 screenshots still give the same result as typed text.
