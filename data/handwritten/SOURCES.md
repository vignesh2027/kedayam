# Sources for the hand-written message sets

Every message in `holdout.jsonl` and `dev.jsonl` was written by the Kavach author for this project. None is copied from a real person's phone. Phone numbers, UPI IDs, account numbers and links are made up. Numbers in the 70000xxxxx range are fictional placeholders, and IP addresses use the 198.51.100.0/24 documentation range.

Each scam message follows a pattern described in one of these public sources. The `source` field in each record uses the keys below.

| Key | Source | What it supports |
| --- | --- | --- |
| `RBI-BEAWARE` | Reserve Bank of India, "BE(A)WARE: A Booklet on Modus Operandi of Financial Frauds", 7 March 2022. Press release 2021-2022/1817: https://www.rbi.org.in/scripts/BS_PressReleaseDisplay.aspx?prid=53372 ; booklet: https://rbidocs.rbi.org.in/rdocs/content/pdfs/BEAWARE07032022.pdf | Phishing links, vishing calls asking for OTP or card details, screen sharing apps, QR code scans, lottery frauds, online job frauds, fake loan offers with fees, KYC update frauds, fake customer care numbers |
| `NPCI-SAFETY` | NPCI, UPI Safety Shield: https://www.npci.org.in/what-we-do/upi/upi-safety-shield ("Enter UPI PIN ONLY to deduct money from your account. UPI PIN is NOT required for receiving money.") | PIN to receive money, collect requests, verify the payee name before paying |
| `I4C-DIGITAL-ARREST` | Ministry of Home Affairs (I4C), "Steps taken to address the issue of digital arrest scams", PIB, 12 March 2025: https://pib.gov.in/PressReleasePage.aspx?PRID=2110809 . The same release refers to the MHA alert on blackmail and digital arrest by criminals impersonating police, NCB, CBI and RBI | Digital arrest, impersonation of police, CBI, customs and RBI; helpline 1930 and https://cybercrime.gov.in |
| `DOT-CHAKSHU` | Department of Telecommunications, Sanchar Saathi, Chakshu: https://sancharsaathi.gov.in/sfc/ | Reporting suspected fraud communication and suspicious links received by SMS, WhatsApp or calls |
| `TRAI-HEADERS` | TRAI Telecom Commercial Communications Customer Preference Regulations, 2018 (TCCCPR): businesses send commercial SMS through registered sender headers | A bank or utility message from an ordinary 10 digit mobile number is a warning sign |

The page at npci.org.in is rendered by script, so the quote above was taken from the search index copy of the page on 4 November 2026. CERT-In advisories were considered but could not be retrieved from cert-in.org.in on that date, so they are not cited.

Legitimate messages (label `legit`) are modelled on the format of ordinary bank alerts, OTP messages, bill reminders and family chat. Sender names and amounts are invented.
