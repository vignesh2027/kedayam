# Synthetic set written from news reports

`blind_news_2026.jsonl` holds 20 synthetic messages (14 scam, 6 legitimate) written by the Kedayam author on 4 November 2026 from news reports of scam types that the rules were not designed around. They were written and committed after the rules were frozen at commit db2b4dd and before being run through Kedayam even once, and the rules are not changed in response to the result. Results are reported in `eval/RESULTS.md` as they come out, misses included.

This is not a truly independent test: the same person who wrote the rules wrote these messages. A set written by someone who has never seen the rules (for example a family member) would be stronger evidence.

All numbers, UPI IDs, vehicle numbers and links are made up. Legitimate messages imitate ordinary formats; sender names are invented.

## Sources (news reports the scam messages are based on)

* `NEWS-WEDDING-APK`: Wedding invitation APK scam on WhatsApp: The Quint WebQoof, https://www.thequint.com/news/webqoof/scammers-send-fake-wedding-invitations-on-whatsapp-with-apk-files-that-are-malware ; Maharashtra Cyber Police warning reported by Free Press Journal, https://www.freepressjournal.in/amp/mumbai/maharashtra-cyber-police-warn-citizens-of-wedding-invitation-scam-leading-to-malware-financial-losses-check-details
* `NEWS-ECHALLAN`: Fake RTO e-challan messages and APKs: BOOM, https://www.boomlive.in/amp/decode/scamcheck/fake-rto-e-challan-message-on-whatsapp-a-growing-apk-scam-29919 ; Telangana Police warning, https://hyderabadnewshunt.com/telangana-police-warn-fake-e-challan-scam
* `NEWS-REPLY-NO`: Hyderabad Police warning about replying 'NO' to a fake bank alert on WhatsApp, Free Press Journal, https://www.freepressjournal.in/tech/replying-no-on-whatsapp-could-empty-your-bank-account-hyderabad-police-warns
* `NEWS-GREETING-APK`: New Year greeting links and APK files, Government Railway Police Mumbai warning reported by Free Press Journal, https://www.freepressjournal.in/mumbai/new-year-2026-wishes-mumbaikars-think-before-you-open-apk-file-greetings-on-whatsapp-grp-warns-of-new-scam
* `NEWS-STOCK-GROUP`: WhatsApp stock tip groups leading to fake trading sites: Business Today, https://www.businesstoday.in/technology/news/story/stock-tip-that-turned-into-a-cyber-trap-how-a-bhuj-man-lost-rs16-lakh-and-how-to-protect-yourself-508366-2025-12-27 ; Deccan Herald, https://www.deccanherald.com/amp/story/india%2Fkarnataka%2Fmangaluru%2Fstock-market-scam-via-whatsapp-man-loses-rs-27-crore-in-mangaluru-3801288
* `NEWS-FASTAG`: FASTag KYC update scams with lookalike sites (blog level source only): https://ecozaar.in/blog/fastag-fraud-scams-alerts-tips-helplines/
* `NEWS-EVENT-REFUND`: Refund phishing aimed at India AI Impact Summit attendees, All India Radio News, https://www.newsonair.gov.in/govt-warns-attendees-of-india-ai-impact-summit-2026-against-phishing-scam
* `NEWS-WA-HIJACK`: WhatsApp account hacking cases, Kerala Police advisory reported by UNI, https://www.uniindia.com/whatsapp-hacking-scams-on-the-rise-kerala-police-issues-alert/south/news/3575672.html
* `NEWS-VOICE-CLONE`: Voice clone and family emergency scams, Moneylife, https://moneylife.in/article/fraud-alert-india-is-losing-over-22000-crore-a-year-in-cyber-scams-and-the-worst-is-yet-to-come/80612.html
* `RBI-BEAWARE`: see data/handwritten/SOURCES.md (insurance or loan amount released after paying a fee).
