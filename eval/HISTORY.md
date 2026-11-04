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
