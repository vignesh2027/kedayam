"""All user-facing text in English, Tamil and Hindi.

Sentences are kept short and use everyday words, because many readers are
older adults reading in their second or third language. The Tamil and Hindi
text should be reviewed by native speakers who work with older adults.
"""

from __future__ import annotations

import os

LANGS = ("en", "ta", "hi")
LANG_NAMES = {"en": "English", "ta": "தமிழ்", "hi": "हिन्दी"}

UI: dict[str, dict[str, str]] = {
    "en": {
        "tagline": "Check a message before you act on it",
        "privacy": "Your message or screenshot stays on this computer. Kedayam does not send it anywhere and does not save it.",
        "paste_label": "Paste the message here",
        "paste_hint": "Copy the SMS or WhatsApp message and paste it in this box.",
        "sender_label": "Who sent it? (optional)",
        "sender_hint": "For example a phone number, or a name like AX-SBIINB",
        "check": "Check this message",
        "shot_label": "Or check a screenshot",
        "shot_hint": "Choose a photo or screenshot of the message.",
        "shot_button": "Check this screenshot",
        "ocr_read": "Kedayam read this text from your picture",
        "ocr_read_hint": "Pictures can be misread. If a word is wrong, correct it here and check again.",
        "ocr_recheck": "Check the corrected text",
        "ocr_not_setup": "Screenshot reading is not set up on this computer. Please paste the message text instead.",
        "ocr_not_image": "Kedayam could not open this file as a picture. Please choose a screenshot or photo.",
        "ocr_too_big": "This picture is too large (over 8 MB). Please choose a smaller screenshot.",
        "ocr_no_text": "Kedayam could not find any text in this picture. Try a clearer screenshot, or paste the message text.",
        "ocr_failed": "Kedayam could not read this picture. Please try again, or paste the message text.",
        "ocr_little_text": "Kedayam could read only a little text from this picture, so this result may miss things. Try a clearer screenshot or paste the text.",
        "language": "Language",
        "level_danger": "Warning: this looks like a scam",
        "level_danger_sub": "Kedayam found a trick that scammers use. Do not do what the message asks.",
        "level_caution": "Be careful",
        "level_caution_sub": "Kedayam found some warning signs. Check with your bank or family before you do anything.",
        "level_none": "No known scam pattern found",
        "level_none_sub": "This does not mean the message is safe. New tricks appear every week.",
        "why": "Why Kedayam says this",
        "we_noticed": "In your message",
        "todo": "What to do now",
        "tips": "Good to know",
        "general_1": "If anyone asks for money, your UPI PIN, an OTP, or to install an app, stop and check with your family or your bank first.",
        "general_2": "Your bank will never ask for your PIN, OTP or password by SMS, call or WhatsApp.",
        "general_3": "If you are unsure, call the person or the bank on a number you already have, not a number in the message.",
        "report_1930": "If you lost money, call 1930 at once or report at cybercrime.gov.in. Calling quickly can help stop the money.",
        "report_chakshu": "You can report this message at sancharsaathi.gov.in under Chakshu.",
        "wrong_q": "I think this result is wrong",
        "wrong_a": "Kedayam can be wrong. Do not rely on it alone. Check yourself: call the person or the bank on a number you already have, such as the number printed on your card or passbook. If they confirm the message, you can go ahead. If the message asked for a PIN, an OTP or an app, it is still a scam.",
        "again": "Check another message",
        "your_message": "The message you checked (links are made safe to view)",
        "classifier_used": "Wording check (a hint only): a model trained on a public SMS dataset gave this message {pct} out of 100 for scam-like wording. It often scores normal bank messages high too, so it does not change the result.",
        "classifier_skipped": "The wording check only works for English text, so it was not used for this message. The pattern checks above still work in Tamil and Hindi.",
        "source": "Based on",
        "empty": "Please paste a message first.",
        "too_long": "This message is very long. Please paste only the suspicious message (up to {n} letters).",
        "helpline": "Cyber fraud helpline: 1930",
        "about": "How Kedayam works",
        "home": "Home",
        "limit_note": "Kedayam is a helper, not a guarantee. It does not replace your bank, the police or the 1930 helpline.",
        "family_title": "Family setup",
        "family_intro": "For a son, daughter or carer: set this up once on your parent's computer. Kedayam will then remind them to call you before acting on a suspicious message. It is saved only on this computer.",
        "family_lang": "Language for your parent",
        "family_name": "Your name (as your parent calls you)",
        "family_name_hint": "For example: Ravi, or Chinna",
        "family_phone": "Your phone number",
        "family_bank": "Bank name (optional)",
        "family_bank_phone": "Bank helpline from the back of the card (optional)",
        "family_save": "Save",
        "family_saved": "Saved. Kedayam will show these numbers on every warning.",
        "family_remove": "Remove family setup",
        "family_removed": "Family setup removed from this computer.",
        "family_invalid": "Please enter a name and a phone number with 6 to 15 digits.",
        "family_call": "Call {name} on {phone} before you do anything.",
        "family_bank_call": "Your bank ({bank}): {phone}, from the back of your card.",
        "family_unsure": "If you are unsure, call {name} on {phone}.",
        "family_card": "Print a reminder card",
        "card_title": "Before you pay or share anything",
        "card_1": "Never tell anyone your UPI PIN or OTP.",
        "card_2": "You never need a PIN to receive money.",
        "card_3": "Check the message in Kedayam.",
        "card_call": "Call {name}: {phone}",
        "card_5": "Lost money? Call 1930 at once.",
    },
    "ta": {
        "tagline": "செய்தியை நம்பும் முன் சரிபார்க்கவும்",
        "privacy": "உங்கள் செய்தியோ ஸ்கிரீன்ஷாட்டோ இந்தக் கணினியிலேயே இருக்கும். கேடயம் அதை எங்கும் அனுப்பாது, சேமிக்காது.",
        "paste_label": "செய்தியை இங்கே ஒட்டவும்",
        "paste_hint": "SMS அல்லது WhatsApp செய்தியை நகலெடுத்து இந்தப் பெட்டியில் ஒட்டவும்.",
        "sender_label": "யார் அனுப்பினார்கள்? (விருப்பம்)",
        "sender_hint": "உதாரணம்: ஒரு போன் நம்பர், அல்லது AX-SBIINB போன்ற பெயர்",
        "check": "இந்தச் செய்தியைச் சரிபார்",
        "shot_label": "அல்லது ஸ்கிரீன்ஷாட்டைச் சரிபார்க்கவும்",
        "shot_hint": "செய்தியின் புகைப்படம் அல்லது ஸ்கிரீன்ஷாட்டைத் தேர்ந்தெடுக்கவும்.",
        "shot_button": "இந்த ஸ்கிரீன்ஷாட்டைச் சரிபார்",
        "ocr_read": "உங்கள் படத்திலிருந்து கேடயம் படித்த உரை",
        "ocr_read_hint": "படங்கள் தவறாகப் படிக்கப்படலாம். ஏதாவது சொல் தவறாக இருந்தால், இங்கே திருத்தி மீண்டும் சரிபார்க்கவும்.",
        "ocr_recheck": "திருத்திய உரையைச் சரிபார்",
        "ocr_not_setup": "இந்தக் கணினியில் ஸ்கிரீன்ஷாட் படிக்கும் வசதி அமைக்கப்படவில்லை. செய்தியின் உரையை ஒட்டவும்.",
        "ocr_not_image": "இந்தக் கோப்பைப் படமாகத் திறக்க முடியவில்லை. ஸ்கிரீன்ஷாட் அல்லது புகைப்படத்தைத் தேர்ந்தெடுக்கவும்.",
        "ocr_too_big": "இந்தப் படம் மிகப் பெரியது (8 MB க்கு மேல்). சிறிய ஸ்கிரீன்ஷாட்டைத் தேர்ந்தெடுக்கவும்.",
        "ocr_no_text": "இந்தப் படத்தில் எந்த உரையும் கிடைக்கவில்லை. தெளிவான ஸ்கிரீன்ஷாட்டை முயற்சிக்கவும், அல்லது செய்தியின் உரையை ஒட்டவும்.",
        "ocr_failed": "இந்தப் படத்தைப் படிக்க முடியவில்லை. மீண்டும் முயற்சிக்கவும், அல்லது செய்தியின் உரையை ஒட்டவும்.",
        "ocr_little_text": "இந்தப் படத்திலிருந்து கொஞ்சம் உரை மட்டுமே படிக்க முடிந்தது, எனவே இந்த முடிவு சிலவற்றைத் தவறவிடலாம். தெளிவான ஸ்கிரீன்ஷாட்டை முயற்சிக்கவும் அல்லது உரையை ஒட்டவும்.",
        "language": "மொழி",
        "level_danger": "எச்சரிக்கை: இது மோசடி போலத் தெரிகிறது",
        "level_danger_sub": "மோசடிக்காரர்கள் பயன்படுத்தும் ஒரு தந்திரம் இதில் உள்ளது. செய்தி சொல்வதைச் செய்யாதீர்கள்.",
        "level_caution": "கவனமாக இருங்கள்",
        "level_caution_sub": "சில எச்சரிக்கை அறிகுறிகள் உள்ளன. எதையும் செய்யும் முன் வங்கியிடமோ குடும்பத்தினரிடமோ கேளுங்கள்.",
        "level_none": "தெரிந்த மோசடி முறை எதுவும் கிடைக்கவில்லை",
        "level_none_sub": "இதனால் செய்தி பாதுகாப்பானது என்று அர்த்தமில்லை. ஒவ்வொரு வாரமும் புதிய தந்திரங்கள் வருகின்றன.",
        "why": "கேடயம் ஏன் இப்படிச் சொல்கிறது",
        "we_noticed": "உங்கள் செய்தியில்",
        "todo": "இப்போது என்ன செய்ய வேண்டும்",
        "tips": "தெரிந்து கொள்ளுங்கள்",
        "general_1": "யாராவது பணம், UPI PIN, OTP கேட்டால் அல்லது ஒரு ஆப்பை நிறுவச் சொன்னால், நிறுத்துங்கள். முதலில் குடும்பத்தினரிடமோ வங்கியிடமோ கேளுங்கள்.",
        "general_2": "உங்கள் வங்கி SMS, போன் அல்லது WhatsApp மூலம் PIN, OTP, கடவுச்சொல் ஒருபோதும் கேட்காது.",
        "general_3": "சந்தேகம் இருந்தால், செய்தியில் உள்ள நம்பரை அல்ல, உங்களிடம் ஏற்கனவே உள்ள நம்பரில் அந்த நபரையோ வங்கியையோ அழையுங்கள்.",
        "report_1930": "பணம் இழந்திருந்தால், உடனே 1930 க்கு அழையுங்கள் அல்லது cybercrime.gov.in இல் புகார் செய்யுங்கள். விரைவாக அழைத்தால் பணத்தை நிறுத்த உதவும்.",
        "report_chakshu": "இந்தச் செய்தியை sancharsaathi.gov.in இல் Chakshu பகுதியில் புகார் செய்யலாம்.",
        "wrong_q": "இந்த முடிவு தவறு என்று நினைக்கிறேன்",
        "wrong_a": "கேடயம் தவறு செய்யலாம். அதை மட்டும் நம்ப வேண்டாம். நீங்களே சரிபார்க்கவும்: உங்கள் கார்டு அல்லது பாஸ்புக்கில் அச்சிட்ட நம்பர் போல, உங்களிடம் ஏற்கனவே உள்ள நம்பரில் அந்த நபரையோ வங்கியையோ அழையுங்கள். அவர்கள் உறுதிசெய்தால் தொடரலாம். செய்தி PIN, OTP அல்லது ஆப் கேட்டிருந்தால், அது இன்னும் மோசடிதான்.",
        "again": "இன்னொரு செய்தியைச் சரிபார்",
        "your_message": "நீங்கள் சரிபார்த்த செய்தி (லிங்குகள் பாதுகாப்பாகக் காட்டப்படுகின்றன)",
        "classifier_used": "சொல் சரிபார்ப்பு (குறிப்பு மட்டும்): பொது SMS தரவுத்தொகுப்பில் பயிற்சி பெற்ற மாதிரி, மோசடி போன்ற சொற்களுக்கு இந்தச் செய்திக்கு 100 க்கு {pct} மதிப்பெண் தந்தது. இது சாதாரண வங்கிச் செய்திகளுக்கும் அதிக மதிப்பெண் தருவதால், முடிவை மாற்றாது.",
        "classifier_skipped": "சொல் சரிபார்ப்பு ஆங்கிலத்தில் மட்டுமே வேலை செய்யும், எனவே இந்தச் செய்திக்குப் பயன்படுத்தவில்லை. மேலே உள்ள முறை சரிபார்ப்புகள் தமிழிலும் இந்தியிலும் வேலை செய்யும்.",
        "source": "ஆதாரம்",
        "empty": "முதலில் ஒரு செய்தியை ஒட்டவும்.",
        "too_long": "இந்தச் செய்தி மிக நீளமானது. சந்தேகமான செய்தியை மட்டும் ஒட்டவும் ({n} எழுத்துகள் வரை).",
        "helpline": "சைபர் மோசடி உதவி எண்: 1930",
        "about": "கேடயம் எப்படி வேலை செய்கிறது",
        "home": "முகப்பு",
        "limit_note": "கேடயம் ஒரு உதவி மட்டுமே, உத்தரவாதம் அல்ல. அது உங்கள் வங்கி, காவல்துறை அல்லது 1930 உதவி எண்ணுக்கு மாற்று அல்ல.",
        "family_title": "குடும்ப அமைப்பு",
        "family_intro": "மகன், மகள் அல்லது பராமரிப்பாளருக்கு: உங்கள் பெற்றோரின் கணினியில் இதை ஒருமுறை அமைக்கவும். சந்தேகமான செய்தி வந்தால், எதையும் செய்யும் முன் உங்களை அழைக்குமாறு கேடயம் நினைவூட்டும். இது இந்தக் கணினியில் மட்டுமே சேமிக்கப்படும்.",
        "family_lang": "பெற்றோருக்கான மொழி",
        "family_name": "உங்கள் பெயர் (பெற்றோர் அழைக்கும் விதம்)",
        "family_name_hint": "உதாரணம்: ரவி, அல்லது சின்னா",
        "family_phone": "உங்கள் போன் நம்பர்",
        "family_bank": "வங்கியின் பெயர் (விருப்பம்)",
        "family_bank_phone": "கார்டின் பின்புறம் உள்ள வங்கி உதவி எண் (விருப்பம்)",
        "family_save": "சேமி",
        "family_saved": "சேமிக்கப்பட்டது. ஒவ்வொரு எச்சரிக்கையிலும் கேடயம் இந்த நம்பர்களைக் காட்டும்.",
        "family_remove": "குடும்ப அமைப்பை நீக்கு",
        "family_removed": "குடும்ப அமைப்பு இந்தக் கணினியிலிருந்து நீக்கப்பட்டது.",
        "family_invalid": "ஒரு பெயரையும் 6 முதல் 15 இலக்க போன் நம்பரையும் உள்ளிடவும்.",
        "family_call": "எதையும் செய்யும் முன் {name} க்கு {phone} இல் போன் செய்யுங்கள்.",
        "family_bank_call": "உங்கள் வங்கி ({bank}): {phone}, உங்கள் கார்டின் பின்புறத்திலிருந்து.",
        "family_unsure": "சந்தேகம் இருந்தால், {name} க்கு {phone} இல் போன் செய்யுங்கள்.",
        "family_card": "நினைவூட்டல் அட்டையை அச்சிடு",
        "card_title": "பணம் கட்டும் முன் அல்லது எதையும் பகிரும் முன்",
        "card_1": "UPI PIN அல்லது OTP யை யாரிடமும் சொல்லாதீர்கள்.",
        "card_2": "பணம் பெற PIN ஒருபோதும் தேவையில்லை.",
        "card_3": "கேடயத்தில் செய்தியைச் சரிபாருங்கள்.",
        "card_call": "{name} க்கு போன் செய்யுங்கள்: {phone}",
        "card_5": "பணம் போனதா? உடனே 1930 ஐ அழையுங்கள்.",
    },
    "hi": {
        "tagline": "किसी संदेश पर कुछ करने से पहले उसे जाँच लें",
        "privacy": "आपका संदेश या स्क्रीनशॉट इसी कंप्यूटर पर रहता है। केडयम उसे कहीं नहीं भेजता और सेव नहीं करता।",
        "paste_label": "संदेश यहाँ पेस्ट करें",
        "paste_hint": "SMS या WhatsApp संदेश कॉपी करें और इस बॉक्स में पेस्ट करें।",
        "sender_label": "किसने भेजा? (ज़रूरी नहीं)",
        "sender_hint": "जैसे कोई फ़ोन नंबर, या AX-SBIINB जैसा नाम",
        "check": "यह संदेश जाँचें",
        "shot_label": "या स्क्रीनशॉट जाँचें",
        "shot_hint": "संदेश की फ़ोटो या स्क्रीनशॉट चुनें।",
        "shot_button": "यह स्क्रीनशॉट जाँचें",
        "ocr_read": "केडयम ने आपकी तस्वीर से यह लिखावट पढ़ी",
        "ocr_read_hint": "तस्वीर से पढ़ने में गलती हो सकती है। अगर कोई शब्द गलत है, तो यहाँ ठीक करें और फिर से जाँचें।",
        "ocr_recheck": "ठीक किया हुआ संदेश जाँचें",
        "ocr_not_setup": "इस कंप्यूटर पर स्क्रीनशॉट पढ़ने की सुविधा चालू नहीं है। कृपया संदेश का टेक्स्ट पेस्ट करें।",
        "ocr_not_image": "केडयम इस फ़ाइल को तस्वीर की तरह नहीं खोल सका। कृपया कोई स्क्रीनशॉट या फ़ोटो चुनें।",
        "ocr_too_big": "यह तस्वीर बहुत बड़ी है (8 MB से ज़्यादा)। कृपया छोटा स्क्रीनशॉट चुनें।",
        "ocr_no_text": "इस तस्वीर में कोई लिखावट नहीं मिली। साफ़ स्क्रीनशॉट आज़माएँ, या संदेश का टेक्स्ट पेस्ट करें।",
        "ocr_failed": "केडयम यह तस्वीर नहीं पढ़ सका। फिर से कोशिश करें, या संदेश का टेक्स्ट पेस्ट करें।",
        "ocr_little_text": "इस तस्वीर से थोड़ी ही लिखावट पढ़ी जा सकी, इसलिए यह नतीजा कुछ बातें छोड़ सकता है। साफ़ स्क्रीनशॉट आज़माएँ या टेक्स्ट पेस्ट करें।",
        "language": "भाषा",
        "level_danger": "चेतावनी: यह धोखाधड़ी लगती है",
        "level_danger_sub": "इसमें ठगों की एक जानी-पहचानी चाल मिली है। संदेश जो कहे, वह न करें।",
        "level_caution": "सावधान रहें",
        "level_caution_sub": "कुछ चेतावनी के संकेत मिले हैं। कुछ भी करने से पहले बैंक या परिवार से पूछ लें।",
        "level_none": "कोई जानी-पहचानी धोखाधड़ी नहीं मिली",
        "level_none_sub": "इसका मतलब यह नहीं कि संदेश सुरक्षित है। हर हफ़्ते नई चालें आती हैं।",
        "why": "केडयम ऐसा क्यों कह रहा है",
        "we_noticed": "आपके संदेश में",
        "todo": "अब क्या करें",
        "tips": "जानने लायक बात",
        "general_1": "अगर कोई पैसे, UPI PIN, OTP माँगे या कोई ऐप डालने को कहे, तो रुकिए। पहले परिवार या बैंक से पूछिए।",
        "general_2": "आपका बैंक SMS, कॉल या WhatsApp पर कभी PIN, OTP या पासवर्ड नहीं माँगता।",
        "general_3": "शक हो तो संदेश वाले नंबर पर नहीं, बल्कि अपने पास पहले से मौजूद नंबर पर उस व्यक्ति या बैंक को फ़ोन करें।",
        "report_1930": "अगर पैसे कट गए हैं, तो तुरंत 1930 पर कॉल करें या cybercrime.gov.in पर शिकायत करें। जल्दी कॉल करने से पैसा रोका जा सकता है।",
        "report_chakshu": "आप इस संदेश की शिकायत sancharsaathi.gov.in पर Chakshu में कर सकते हैं।",
        "wrong_q": "मुझे लगता है यह नतीजा गलत है",
        "wrong_a": "केडयम गलत हो सकता है। सिर्फ़ उस पर भरोसा न करें। खुद जाँचें: अपने कार्ड या पासबुक पर छपे नंबर जैसे, पहले से मौजूद नंबर पर उस व्यक्ति या बैंक को फ़ोन करें। अगर वे संदेश की पुष्टि करें, तो आगे बढ़ सकते हैं। अगर संदेश में PIN, OTP या ऐप माँगा गया है, तो वह फिर भी धोखाधड़ी है।",
        "again": "दूसरा संदेश जाँचें",
        "your_message": "आपने जो संदेश जाँचा (लिंक सुरक्षित रूप में दिखाए गए हैं)",
        "classifier_used": "शब्द जाँच (सिर्फ़ संकेत): सार्वजनिक SMS डेटासेट पर सिखाए गए मॉडल ने धोखाधड़ी जैसे शब्दों के लिए इस संदेश को 100 में से {pct} अंक दिए। यह आम बैंक संदेशों को भी अक्सर ज़्यादा अंक देता है, इसलिए नतीजा नहीं बदलता।",
        "classifier_skipped": "शब्द जाँच सिर्फ़ अंग्रेज़ी पर काम करती है, इसलिए इस संदेश पर नहीं चलाई गई। ऊपर की पैटर्न जाँच तमिल और हिन्दी में भी काम करती है।",
        "source": "आधार",
        "empty": "पहले कोई संदेश पेस्ट करें।",
        "too_long": "यह संदेश बहुत लंबा है। सिर्फ़ शक वाला संदेश पेस्ट करें ({n} अक्षरों तक)।",
        "helpline": "साइबर धोखाधड़ी हेल्पलाइन: 1930",
        "about": "केडयम कैसे काम करता है",
        "home": "मुख्य पेज",
        "limit_note": "केडयम एक मददगार है, गारंटी नहीं। यह आपके बैंक, पुलिस या 1930 हेल्पलाइन की जगह नहीं लेता।",
        "family_title": "परिवार सेटअप",
        "family_intro": "बेटे, बेटी या देखभाल करने वाले के लिए: इसे अपने माता-पिता के कंप्यूटर पर एक बार सेट करें। फिर शक वाले संदेश पर कुछ करने से पहले केडयम उन्हें आपको फ़ोन करने की याद दिलाएगा। यह सिर्फ़ इसी कंप्यूटर पर सेव होता है।",
        "family_lang": "माता-पिता के लिए भाषा",
        "family_name": "आपका नाम (जैसे माता-पिता आपको बुलाते हैं)",
        "family_name_hint": "जैसे: रवि, या मुन्ना",
        "family_phone": "आपका फ़ोन नंबर",
        "family_bank": "बैंक का नाम (ज़रूरी नहीं)",
        "family_bank_phone": "कार्ड के पीछे लिखा बैंक हेल्पलाइन नंबर (ज़रूरी नहीं)",
        "family_save": "सेव करें",
        "family_saved": "सेव हो गया। केडयम हर चेतावनी पर ये नंबर दिखाएगा।",
        "family_remove": "परिवार सेटअप हटाएँ",
        "family_removed": "परिवार सेटअप इस कंप्यूटर से हटा दिया गया।",
        "family_invalid": "कृपया एक नाम और 6 से 15 अंकों का फ़ोन नंबर डालें।",
        "family_call": "कुछ भी करने से पहले {name} को {phone} पर फ़ोन करें।",
        "family_bank_call": "आपका बैंक ({bank}): {phone}, आपके कार्ड के पीछे से।",
        "family_unsure": "शक हो तो {name} को {phone} पर फ़ोन करें।",
        "family_card": "याद दिलाने वाला कार्ड प्रिंट करें",
        "card_title": "पैसे भेजने या कुछ भी बताने से पहले",
        "card_1": "अपना UPI PIN या OTP किसी को न बताएँ।",
        "card_2": "पैसे पाने के लिए PIN की कभी ज़रूरत नहीं होती।",
        "card_3": "केडयम में संदेश जाँचें।",
        "card_call": "{name} को फ़ोन करें: {phone}",
        "card_5": "पैसे कट गए? तुरंत 1930 पर फ़ोन करें।",
    },
}

# Each rule: a short title and a plain explanation of why it matters.
RULE_TEXT: dict[str, dict[str, tuple[str, str]]] = {
    "pin_to_receive": {
        "en": ("Asks for your PIN to receive money", "The UPI PIN is only for sending money. You never need it to receive money. Entering it here will take money out of your account."),
        "ta": ("பணம் பெற PIN கேட்கிறது", "UPI PIN பணம் அனுப்ப மட்டுமே. பணம் பெற PIN ஒருபோதும் தேவையில்லை. இங்கே PIN போட்டால் உங்கள் கணக்கிலிருந்து பணம் போகும்."),
        "hi": ("पैसे पाने के लिए PIN माँग रहा है", "UPI PIN सिर्फ़ पैसे भेजने के लिए होता है। पैसे पाने के लिए PIN की कभी ज़रूरत नहीं होती। यहाँ PIN डालने से आपके खाते से पैसे कट जाएँगे।"),
    },
    "qr_to_receive": {
        "en": ("Asks you to scan a QR code to receive money", "Scanning a QR code is only for paying. You cannot receive money by scanning one."),
        "ta": ("பணம் பெற QR கோடை ஸ்கேன் செய்யச் சொல்கிறது", "QR கோடை ஸ்கேன் செய்வது பணம் கட்ட மட்டுமே. ஸ்கேன் செய்து பணம் பெற முடியாது."),
        "hi": ("पैसे पाने के लिए QR कोड स्कैन करने को कह रहा है", "QR कोड स्कैन करना सिर्फ़ भुगतान करने के लिए होता है। स्कैन करके पैसे नहीं मिलते।"),
    },
    "collect_request_lure": {
        "en": ("A payment request dressed up as a refund or prize", "A 'request' in your UPI app asks you to pay. If you approve it and enter your PIN, money leaves your account. Refunds and prizes never come this way."),
        "ta": ("ரீஃபண்ட் அல்லது பரிசு போல வேடமிட்ட பணக் கோரிக்கை", "UPI ஆப்பில் வரும் 'கோரிக்கை' என்றால் நீங்கள் பணம் கட்ட வேண்டும் என்று அர்த்தம். ஏற்று PIN போட்டால் பணம் போகும். ரீஃபண்ட், பரிசு இப்படி வராது."),
        "hi": ("रिफंड या इनाम के नाम पर पैसे की रिक्वेस्ट", "UPI ऐप में आई 'रिक्वेस्ट' का मतलब है कि आपसे पैसे माँगे जा रहे हैं। मंज़ूर करके PIN डालेंगे तो पैसे कट जाएँगे। रिफंड या इनाम ऐसे नहीं आते।"),
    },
    "otp_request": {
        "en": ("Asks you to share an OTP or code", "An OTP is like a key to your account. Anyone who asks for it, even if they say they are from the bank, is trying to take your money."),
        "ta": ("OTP அல்லது கோடைச் சொல்லச் சொல்கிறது", "OTP உங்கள் கணக்கின் சாவி போன்றது. வங்கியிலிருந்து என்று சொன்னாலும், அதைக் கேட்பவர் உங்கள் பணத்தை எடுக்க முயல்கிறார்."),
        "hi": ("OTP या कोड बताने को कह रहा है", "OTP आपके खाते की चाबी जैसा है। जो भी इसे माँगे, चाहे वह खुद को बैंक का बताए, वह आपका पैसा लेना चाहता है।"),
    },
    "secret_details_request": {
        "en": ("Asks for card, account or password details", "Banks and government offices never ask for your CVV, card number, PIN or password by message or link."),
        "ta": ("கார்டு, கணக்கு அல்லது கடவுச்சொல் விவரம் கேட்கிறது", "வங்கிகளும் அரசு அலுவலகங்களும் CVV, கார்டு எண், PIN, கடவுச்சொல்லை செய்தி அல்லது லிங்க் மூலம் ஒருபோதும் கேட்காது."),
        "hi": ("कार्ड, खाते या पासवर्ड की जानकारी माँग रहा है", "बैंक और सरकारी दफ़्तर कभी भी संदेश या लिंक से CVV, कार्ड नंबर, PIN या पासवर्ड नहीं माँगते।"),
    },
    "screen_share_app": {
        "en": ("Asks you to install a screen sharing app", "Apps like AnyDesk, TeamViewer or QuickSupport let a stranger see and control your phone, including your bank app."),
        "ta": ("திரையைப் பகிரும் ஆப்பை நிறுவச் சொல்கிறது", "AnyDesk, TeamViewer, QuickSupport போன்ற ஆப்கள் உங்கள் போனையும் வங்கி ஆப்பையும் அந்நியர் பார்க்கவும் இயக்கவும் விடும்."),
        "hi": ("स्क्रीन शेयर करने वाला ऐप डालने को कह रहा है", "AnyDesk, TeamViewer या QuickSupport जैसे ऐप से कोई अनजान व्यक्ति आपका फ़ोन और बैंक ऐप देख और चला सकता है।"),
    },
    "apk_link": {
        "en": ("Asks you to install an app from a link", "Files ending in .apk are apps from outside the Play Store. Fake bill or bank apps can read your messages and OTPs."),
        "ta": ("லிங்கிலிருந்து ஆப்பை நிறுவச் சொல்கிறது", ".apk என்று முடியும் கோப்புகள் Play Store க்கு வெளியே உள்ள ஆப்கள். போலி பில் அல்லது வங்கி ஆப்கள் உங்கள் செய்திகளையும் OTP யையும் படிக்கும்."),
        "hi": ("लिंक से ऐप डालने को कह रहा है", ".apk वाली फ़ाइलें Play Store से बाहर के ऐप होते हैं। नकली बिल या बैंक ऐप आपके संदेश और OTP पढ़ सकते हैं।"),
    },
    "digital_arrest": {
        "en": ("Threatens a 'digital arrest' or police video call", "Police, CBI, customs and courts never arrest anyone on a video call and never ask for money to close a case."),
        "ta": ("'டிஜிட்டல் கைது' அல்லது போலீஸ் வீடியோ கால் மிரட்டல்", "காவல்துறை, CBI, சுங்கத்துறை, நீதிமன்றம் வீடியோ காலில் யாரையும் கைது செய்யாது. வழக்கை முடிக்க பணம் கேட்காது."),
        "hi": ("'डिजिटल अरेस्ट' या पुलिस वीडियो कॉल की धमकी", "पुलिस, CBI, कस्टम और अदालत कभी वीडियो कॉल पर गिरफ़्तार नहीं करते और केस बंद करने के लिए पैसे नहीं माँगते।"),
    },
    "advance_fee": {
        "en": ("Asks for a fee before you get a prize, loan, job or parcel", "Real prizes, loans and jobs do not ask you to pay a 'processing' or 'clearance' fee first. Once paid, the money is gone."),
        "ta": ("பரிசு, கடன், வேலை அல்லது பார்சலுக்கு முன்பணம் கேட்கிறது", "உண்மையான பரிசு, கடன், வேலைக்கு முதலில் 'processing' அல்லது 'clearance' கட்டணம் கேட்க மாட்டார்கள். கட்டிய பணம் திரும்பாது."),
        "hi": ("इनाम, लोन, नौकरी या पार्सल से पहले फ़ीस माँग रहा है", "असली इनाम, लोन या नौकरी के लिए पहले 'प्रोसेसिंग' या 'क्लियरेंस' फ़ीस नहीं माँगी जाती। एक बार दिया पैसा वापस नहीं आता।"),
    },
    "wrong_transfer": {
        "en": ("Says money was sent to you by mistake", "Scammers send a fake 'money received' message and ask you to return it. Check your balance in your bank app, not in the message."),
        "ta": ("தவறுதலாக பணம் அனுப்பியதாகச் சொல்கிறது", "மோசடிக்காரர்கள் போலி 'பணம் வந்தது' செய்தி அனுப்பி திருப்பித் தரச் சொல்வார்கள். செய்தியை அல்ல, உங்கள் வங்கி ஆப்பில் இருப்பைப் பாருங்கள்."),
        "hi": ("कह रहा है कि गलती से पैसे भेज दिए", "ठग नकली 'पैसे आए' संदेश भेजकर पैसे लौटाने को कहते हैं। संदेश नहीं, अपने बैंक ऐप में बैलेंस देखें।"),
    },
    "lookalike_upi_id": {
        "en": ("A UPI ID that pretends to be a bank, company or office", "Anyone can create a UPI ID with words like 'sbi', 'refund' or 'electricity' in it. Banks and offices do not collect money through such IDs."),
        "ta": ("வங்கி, நிறுவனம் அல்லது அலுவலகம் போல நடிக்கும் UPI ID", "'sbi', 'refund', 'electricity' போன்ற சொற்களுடன் யார் வேண்டுமானாலும் UPI ID உருவாக்கலாம். வங்கிகளும் அலுவலகங்களும் இப்படிப் பணம் வசூலிக்காது."),
        "hi": ("बैंक, कंपनी या दफ़्तर होने का दिखावा करने वाली UPI ID", "कोई भी 'sbi', 'refund' या 'electricity' जैसे शब्दों वाली UPI ID बना सकता है। बैंक और दफ़्तर ऐसी ID से पैसे नहीं लेते।"),
    },
    "lookalike_link": {
        "en": ("A web link that pretends to be a bank or company", "The link uses a well known name but is not that company's real website. Fake sites copy the real page to steal your details."),
        "ta": ("வங்கி அல்லது நிறுவனம் போல நடிக்கும் லிங்க்", "இந்த லிங்கில் பிரபல பெயர் உள்ளது, ஆனால் அது அந்த நிறுவனத்தின் உண்மையான இணையதளம் அல்ல. போலி தளங்கள் உங்கள் விவரங்களைத் திருட உண்மையான பக்கத்தை நகலெடுக்கும்."),
        "hi": ("बैंक या कंपनी होने का दिखावा करने वाला लिंक", "लिंक में जाना-माना नाम है, पर यह उस कंपनी की असली वेबसाइट नहीं है। नकली साइटें आपकी जानकारी चुराने के लिए असली पेज की नकल करती हैं।"),
    },
    "suspicious_link": {
        "en": ("A short or unusual web link", "Short links and unusual web addresses hide where they really go. Banks do not send links like these."),
        "ta": ("சுருக்கப்பட்ட அல்லது வழக்கத்துக்கு மாறான லிங்க்", "சுருக்கிய லிங்குகளும் வினோதமான முகவரிகளும் உண்மையில் எங்கே போகின்றன என்பதை மறைக்கின்றன. வங்கிகள் இப்படி லிங்க் அனுப்பாது."),
        "hi": ("छोटा या अजीब लिंक", "छोटे लिंक और अजीब वेब पते छिपाते हैं कि वे असल में कहाँ ले जाते हैं। बैंक ऐसे लिंक नहीं भेजते।"),
    },
    "fake_security_alert": {
        "en": ("A fake security alert with a link", "Real banks do not ask you to click a link to stop an 'unusual' or 'unauthorised' transaction. The link leads to a fake site that steals your login."),
        "ta": ("லிங்குடன் கூடிய போலி பாதுகாப்பு எச்சரிக்கை", "'வழக்கத்துக்கு மாறான' அல்லது 'அனுமதியில்லாத' பரிவர்த்தனையை நிறுத்த உண்மையான வங்கிகள் லிங்கைக் கிளிக் செய்யச் சொல்லாது. அந்த லிங்க் உங்கள் உள்நுழைவு விவரங்களைத் திருடும் போலி தளத்துக்குக் கொண்டு செல்லும்."),
        "hi": ("लिंक वाली नकली सुरक्षा चेतावनी", "असली बैंक किसी 'अजीब' या 'बिना अनुमति' लेन-देन को रोकने के लिए लिंक दबाने को नहीं कहते। लिंक एक नकली साइट पर ले जाता है जो आपकी लॉगिन जानकारी चुराती है।"),
    },
    "parcel_problem_link": {
        "en": ("Says a parcel could not be delivered", "Fake courier messages ask you to update your address or pay a small fee through a link or a phone number. Check your order in the shop's own app instead."),
        "ta": ("பார்சல் டெலிவரி ஆகவில்லை என்கிறது", "போலி கூரியர் செய்திகள் லிங்க் அல்லது போன் நம்பர் மூலம் முகவரியைப் புதுப்பிக்கவோ சிறு கட்டணம் கட்டவோ சொல்லும். அதற்குப் பதிலாக கடையின் சொந்த ஆப்பில் உங்கள் ஆர்டரைப் பாருங்கள்."),
        "hi": ("कह रहा है कि पार्सल डिलीवर नहीं हो सका", "नकली कूरियर संदेश लिंक या फ़ोन नंबर से पता अपडेट करने या छोटी फ़ीस भरने को कहते हैं। इसकी जगह दुकान के अपने ऐप में अपना ऑर्डर देखें।"),
    },
    "reward_link": {
        "en": ("A refund, prize or cashback through a link", "Money you are owed reaches your account by itself. A link that asks you to 'claim' it usually leads to a fake page that asks for card details or your PIN."),
        "ta": ("லிங்க் மூலம் ரீஃபண்ட், பரிசு அல்லது கேஷ்பேக்", "உங்களுக்கு வர வேண்டிய பணம் தானாகவே கணக்கில் வரும். அதைப் 'பெற' சொல்லும் லிங்க் பெரும்பாலும் கார்டு விவரம் அல்லது PIN கேட்கும் போலிப் பக்கத்துக்குக் கொண்டு செல்லும்."),
        "hi": ("लिंक से रिफंड, इनाम या कैशबैक", "जो पैसा आपको मिलना है, वह अपने आप खाते में आता है। उसे 'क्लेम' करने वाला लिंक अक्सर नकली पेज पर ले जाता है जो कार्ड की जानकारी या PIN माँगता है।"),
    },
    "account_block_threat": {
        "en": ("Threatens to block your account, KYC or SIM", "Scammers say your KYC, PAN or account will be blocked so you act in a hurry. Banks ask you to visit the branch or use their official app."),
        "ta": ("கணக்கு, KYC அல்லது SIM முடக்கப்படும் என்று மிரட்டுகிறது", "நீங்கள் அவசரப்பட KYC, PAN அல்லது கணக்கு முடக்கப்படும் என்று மோசடிக்காரர்கள் சொல்வார்கள். வங்கிகள் கிளைக்கு வரச் சொல்லும் அல்லது அதிகாரப்பூர்வ ஆப்பைப் பயன்படுத்தச் சொல்லும்."),
        "hi": ("खाता, KYC या SIM बंद करने की धमकी", "ठग कहते हैं कि KYC, PAN या खाता बंद हो जाएगा ताकि आप जल्दबाज़ी करें। बैंक ब्रांच आने या अपना असली ऐप इस्तेमाल करने को कहते हैं।"),
    },
    "utility_disconnection": {
        "en": ("Threatens to cut your electricity or gas", "Electricity boards do not send SMS asking you to call an 'officer' on a mobile number to stop a disconnection tonight."),
        "ta": ("மின்சாரம் அல்லது கேஸ் துண்டிக்கப்படும் என்று மிரட்டுகிறது", "இன்று இரவு இணைப்பைத் துண்டிப்பதை நிறுத்த ஒரு 'அதிகாரியின்' மொபைல் நம்பரை அழைக்கச் சொல்லி மின்வாரியம் SMS அனுப்பாது."),
        "hi": ("बिजली या गैस काटने की धमकी", "बिजली विभाग आज रात कनेक्शन कटने से रोकने के लिए किसी 'अधिकारी' के मोबाइल नंबर पर कॉल करने का SMS नहीं भेजता।"),
    },
    "authority_threat": {
        "en": ("Uses police, CBI, customs or a court to scare you", "Scammers pretend to be officers and talk about arrest or a case. Real officers do not threaten you by SMS or phone and do not ask for money."),
        "ta": ("காவல், CBI, சுங்கம் அல்லது நீதிமன்றம் பெயரில் பயமுறுத்துகிறது", "மோசடிக்காரர்கள் அதிகாரிகள் போல நடித்து கைது, வழக்கு என்று பேசுவார்கள். உண்மையான அதிகாரிகள் SMS அல்லது போனில் மிரட்டிப் பணம் கேட்க மாட்டார்கள்."),
        "hi": ("पुलिस, CBI, कस्टम या अदालत के नाम से डरा रहा है", "ठग अधिकारी बनकर गिरफ़्तारी या केस की बात करते हैं। असली अधिकारी SMS या फ़ोन पर धमकाकर पैसे नहीं माँगते।"),
    },
    "prize_lottery": {
        "en": ("Says you won a prize or lottery", "You cannot win a lottery or lucky draw you never entered. This is the first step of a scam that later asks for fees or details."),
        "ta": ("நீங்கள் பரிசு அல்லது லாட்டரி வென்றதாகச் சொல்கிறது", "நீங்கள் கலந்துகொள்ளாத லாட்டரியில் வெல்ல முடியாது. பிறகு கட்டணம் அல்லது விவரம் கேட்கும் மோசடியின் முதல் படி இது."),
        "hi": ("कह रहा है कि आपने इनाम या लॉटरी जीती", "जिस लॉटरी में आपने हिस्सा नहीं लिया, उसे आप जीत नहीं सकते। यह धोखाधड़ी का पहला कदम है, बाद में फ़ीस या जानकारी माँगी जाती है।"),
    },
    "easy_money_job": {
        "en": ("Offers easy money or a work from home task", "Jobs that pay a lot for liking videos or simple tasks usually end with you being asked to 'invest' or pay a fee."),
        "ta": ("எளிதான பணம் அல்லது வீட்டிலிருந்து வேலை தருவதாகச் சொல்கிறது", "வீடியோக்களை லைக் செய்வது போன்ற சிறிய வேலைக்கு அதிக பணம் தரும் வேலைகள் கடைசியில் 'முதலீடு' அல்லது கட்டணம் கேட்கும்."),
        "hi": ("आसान कमाई या घर बैठे काम का लालच", "वीडियो लाइक करने जैसे छोटे काम के बदले ज़्यादा पैसे देने वाली नौकरियाँ आख़िर में 'निवेश' या फ़ीस माँगती हैं।"),
    },
    "family_money_request": {
        "en": ("Someone claiming to be family asks for money urgently", "Scammers pretend to be a son, daughter or grandchild on a 'new number' or in an 'accident'. Call them on the number you already have."),
        "ta": ("குடும்பத்தினர் என்று சொல்லி அவசரமாகப் பணம் கேட்கிறார்கள்", "மோசடிக்காரர்கள் 'புது நம்பர்' அல்லது 'விபத்து' என்று சொல்லி மகன், மகள், பேரன் போல நடிப்பார்கள். உங்களிடம் ஏற்கனவே உள்ள நம்பரில் அவர்களை அழையுங்கள்."),
        "hi": ("परिवार का कोई बनकर तुरंत पैसे माँग रहा है", "ठग 'नया नंबर' या 'एक्सीडेंट' बताकर बेटा, बेटी या पोता बनते हैं। उन्हें उसी नंबर पर फ़ोन करें जो पहले से आपके पास है।"),
    },
    "sender_is_mobile_number": {
        "en": ("Claims to be a bank or company but came from a mobile number", "Banks and companies send SMS from short sender names like AX-SBIINB, not from an ordinary 10 digit mobile number."),
        "ta": ("வங்கி அல்லது நிறுவனம் என்கிறது, ஆனால் மொபைல் நம்பரிலிருந்து வந்தது", "வங்கிகளும் நிறுவனங்களும் AX-SBIINB போன்ற குறும் பெயர்களிலிருந்து SMS அனுப்பும், சாதாரண 10 இலக்க மொபைல் நம்பரிலிருந்து அல்ல."),
        "hi": ("बैंक या कंपनी होने का दावा, पर मोबाइल नंबर से आया", "बैंक और कंपनियाँ AX-SBIINB जैसे छोटे नाम से SMS भेजती हैं, किसी आम 10 अंकों के मोबाइल नंबर से नहीं।"),
    },
    "urgency": {
        "en": ("Pushes you to act fast", "Words like 'today', 'tonight' or 'immediately' are meant to stop you from thinking or asking someone."),
        "ta": ("அவசரப்படுத்துகிறது", "'இன்று', 'இன்று இரவு', 'உடனே' போன்ற சொற்கள் நீங்கள் யோசிக்காமல், யாரிடமும் கேட்காமல் செய்வதற்காக."),
        "hi": ("जल्दी करने का दबाव", "'आज', 'आज रात' या 'तुरंत' जैसे शब्द इसलिए होते हैं कि आप सोचें नहीं और किसी से पूछें नहीं।"),
    },
    "secrecy": {
        "en": ("Tells you to keep it secret", "Scammers ask you not to tell family, because family would stop the scam."),
        "ta": ("ரகசியமாக வைக்கச் சொல்கிறது", "குடும்பத்தினர் மோசடியைத் தடுப்பார்கள் என்பதால், அவர்களிடம் சொல்ல வேண்டாம் என்று மோசடிக்காரர்கள் சொல்வார்கள்."),
        "hi": ("बात छुपाने को कह रहा है", "ठग परिवार को न बताने को कहते हैं, क्योंकि परिवार धोखाधड़ी रोक देगा।"),
    },
    "call_this_number": {
        "en": ("Asks you to call or WhatsApp a mobile number", "A number given inside a suspicious message can connect you to the scammer. Use the number on your card, bill or the official website instead."),
        "ta": ("ஒரு மொபைல் நம்பரை அழைக்க அல்லது WhatsApp செய்யச் சொல்கிறது", "சந்தேகமான செய்தியில் உள்ள நம்பர் உங்களை மோசடிக்காரரிடம் இணைக்கலாம். கார்டு, பில் அல்லது அதிகாரப்பூர்வ தளத்தில் உள்ள நம்பரைப் பயன்படுத்துங்கள்."),
        "hi": ("किसी मोबाइल नंबर पर कॉल या WhatsApp करने को कह रहा है", "शक वाले संदेश में दिया नंबर आपको ठग से जोड़ सकता है। इसकी जगह कार्ड, बिल या असली वेबसाइट पर दिया नंबर इस्तेमाल करें।"),
    },
    "otp_message": {
        "en": ("This looks like a code from a bank or app", "That is normal if you just asked for it. Never tell this code to anyone, even someone who says they are from the bank."),
        "ta": ("இது வங்கி அல்லது ஆப்பிலிருந்து வந்த கோட் போலத் தெரிகிறது", "நீங்களே கேட்டிருந்தால் இது சாதாரணம். வங்கியிலிருந்து என்று சொன்னாலும், இந்தக் கோடை யாரிடமும் சொல்லாதீர்கள்."),
        "hi": ("यह किसी बैंक या ऐप का कोड लगता है", "अगर आपने खुद माँगा था तो यह सामान्य है। यह कोड किसी को न बताएँ, चाहे वह खुद को बैंक का बताए।"),
    },
    "has_link": {
        "en": ("The message has a web link", "Do not tap links in messages you did not expect. To reach your bank, open its app or type its address yourself."),
        "ta": ("செய்தியில் ஒரு லிங்க் உள்ளது", "எதிர்பாராத செய்திகளில் உள்ள லிங்குகளைத் தொடாதீர்கள். வங்கியை அணுக அதன் ஆப்பைத் திறக்கவும் அல்லது முகவரியை நீங்களே டைப் செய்யவும்."),
        "hi": ("संदेश में एक लिंक है", "अचानक आए संदेशों के लिंक न दबाएँ। बैंक तक पहुँचने के लिए उसका ऐप खोलें या पता खुद टाइप करें।"),
    },
}

ACTION_TEXT: dict[str, dict[str, str]] = {
    "no_pin": {
        "en": "Do not enter your UPI PIN. The PIN is only for sending money.",
        "ta": "UPI PIN போடாதீர்கள். PIN பணம் அனுப்ப மட்டுமே.",
        "hi": "अपना UPI PIN न डालें। PIN सिर्फ़ पैसे भेजने के लिए है।",
    },
    "no_qr": {
        "en": "Do not scan the QR code.",
        "ta": "QR கோடை ஸ்கேன் செய்யாதீர்கள்.",
        "hi": "QR कोड स्कैन न करें।",
    },
    "no_pay": {
        "en": "Do not pay, and do not approve any request in your UPI app.",
        "ta": "பணம் கட்டாதீர்கள். UPI ஆப்பில் எந்தக் கோரிக்கையையும் ஏற்காதீர்கள்.",
        "hi": "पैसे न भेजें, और UPI ऐप में कोई रिक्वेस्ट मंज़ूर न करें।",
    },
    "no_otp": {
        "en": "Do not tell anyone the OTP or code, not even someone who says they are from the bank.",
        "ta": "OTP அல்லது கோடை யாரிடமும் சொல்லாதீர்கள், வங்கியிலிருந்து என்று சொன்னாலும் கூட.",
        "hi": "OTP या कोड किसी को न बताएँ, चाहे वह खुद को बैंक का बताए।",
    },
    "no_details": {
        "en": "Do not share your card number, CVV, PIN, password or Aadhaar details.",
        "ta": "கார்டு எண், CVV, PIN, கடவுச்சொல், ஆதார் விவரங்களைப் பகிராதீர்கள்.",
        "hi": "कार्ड नंबर, CVV, PIN, पासवर्ड या आधार की जानकारी न दें।",
    },
    "no_link": {
        "en": "Do not tap the link. To reach your bank, open its official app or type its address yourself.",
        "ta": "லிங்கைத் தொடாதீர்கள். வங்கியை அணுக அதன் அதிகாரப்பூர்வ ஆப்பைத் திறக்கவும் அல்லது முகவரியை நீங்களே டைப் செய்யவும்.",
        "hi": "लिंक न दबाएँ। बैंक तक पहुँचने के लिए उसका असली ऐप खोलें या पता खुद टाइप करें।",
    },
    "no_app": {
        "en": "Do not install the app. If you already did, turn off mobile data and Wi-Fi, uninstall it, and call your bank.",
        "ta": "ஆப்பை நிறுவாதீர்கள். ஏற்கனவே நிறுவியிருந்தால், மொபைல் டேட்டா, Wi-Fi ஐ அணைத்து, ஆப்பை நீக்கி, வங்கியை அழையுங்கள்.",
        "hi": "ऐप न डालें। अगर डाल चुके हैं, तो मोबाइल डेटा और Wi-Fi बंद करें, ऐप हटाएँ और बैंक को फ़ोन करें।",
    },
    "no_call_number": {
        "en": "Do not call the number in the message.",
        "ta": "செய்தியில் உள்ள நம்பரை அழைக்காதீர்கள்.",
        "hi": "संदेश में दिए नंबर पर फ़ोन न करें।",
    },
    "call_bank": {
        "en": "Call your bank on the number printed on your card or passbook.",
        "ta": "உங்கள் கார்டு அல்லது பாஸ்புக்கில் அச்சிட்ட நம்பரில் வங்கியை அழையுங்கள்.",
        "hi": "अपने कार्ड या पासबुक पर छपे नंबर पर बैंक को फ़ोन करें।",
    },
    "check_bill": {
        "en": "Check your bill amount on your printed bill or the official electricity board website or app.",
        "ta": "அச்சிட்ட பில்லில் அல்லது மின்வாரியத்தின் அதிகாரப்பூர்வ தளம் அல்லது ஆப்பில் உங்கள் பில் தொகையைப் பாருங்கள்.",
        "hi": "बिल की रकम अपने छपे बिल पर या बिजली विभाग की असली वेबसाइट या ऐप पर देखें।",
    },
    "check_balance": {
        "en": "Open your bank app or passbook and check whether any money really came in.",
        "ta": "வங்கி ஆப் அல்லது பாஸ்புக்கைத் திறந்து உண்மையில் பணம் வந்ததா என்று பாருங்கள்.",
        "hi": "अपना बैंक ऐप या पासबुक खोलकर देखें कि सच में पैसे आए हैं या नहीं।",
    },
    "check_payee": {
        "en": "Before paying anyone, check the name your UPI app shows for the UPI ID.",
        "ta": "யாருக்கும் பணம் கட்டும் முன், UPI ஆப் காட்டும் பெயரைச் சரிபாருங்கள்.",
        "hi": "किसी को भी पैसे भेजने से पहले UPI ऐप में दिख रहा नाम जाँच लें।",
    },
    "verify_family": {
        "en": "Call your family member on their old number that you already have.",
        "ta": "உங்களிடம் ஏற்கனவே உள்ள பழைய நம்பரில் குடும்பத்தினரை அழையுங்கள்.",
        "hi": "परिवार के उस सदस्य को उनके पुराने नंबर पर फ़ोन करें जो आपके पास है।",
    },
    "hang_up": {
        "en": "Cut the call. Police and courts never arrest anyone on a video call.",
        "ta": "காலைத் துண்டியுங்கள். காவல்துறையும் நீதிமன்றமும் வீடியோ காலில் யாரையும் கைது செய்யாது.",
        "hi": "कॉल काट दें। पुलिस और अदालत कभी वीडियो कॉल पर गिरफ़्तार नहीं करते।",
    },
    "tell_family": {
        "en": "Show this message to a family member before you do anything.",
        "ta": "எதையும் செய்யும் முன் இந்தச் செய்தியைக் குடும்பத்தினரிடம் காட்டுங்கள்.",
        "hi": "कुछ भी करने से पहले यह संदेश परिवार के किसी सदस्य को दिखाएँ।",
    },
    "slow_down": {
        "en": "Take your time. A real bank or office will still be there tomorrow.",
        "ta": "நிதானமாக இருங்கள். உண்மையான வங்கியோ அலுவலகமோ நாளையும் இருக்கும்.",
        "hi": "जल्दी न करें। असली बैंक या दफ़्तर कल भी वहीं होगा।",
    },
}

ABOUT: dict[str, dict] = {
    "en": {
        "does_h": "What it does",
        "does": "Kedayam checks a message or screenshot against a list of tricks that scammers use in India, taken from public advisories by RBI, NPCI, the Ministry of Home Affairs (I4C) and the Department of Telecommunications. It explains each warning sign in English, Tamil or Hindi and tells you what to do next.",
        "not_h": "What it does not do",
        "not": [
            "It never says a message is safe. The best result is \"No known scam pattern found\".",
            "It cannot check whether a phone number, UPI ID or link really belongs to a bank. It only spots impersonation patterns.",
            "New scam scripts that avoid these patterns will not be caught.",
            "It does not report anything for you. Call 1930 or use cybercrime.gov.in."
        ],
        "privacy_h": "Your privacy",
        "privacy": "Kedayam runs on this computer. It only accepts connections from this computer, does not send your message or screenshot anywhere, does not save them, and does not keep logs of what you check. Screenshots are read in memory by the Tesseract program on this computer. The page loads no outside fonts, scripts or trackers.",
        "model_h": "The wording check",
        "model": "Kedayam also has a small statistical model trained on a public SMS phishing dataset. In testing it often gave high scores to ordinary bank alerts, because the normal messages in its training data are mostly personal chat. So it does not change the result; it is only shown in the details for English messages.",
        "sources_h": "Sources"
    },
    "ta": {
        "does_h": "இது என்ன செய்கிறது",
        "does": "இந்தியாவில் மோசடிக்காரர்கள் பயன்படுத்தும் தந்திரங்களின் பட்டியலுடன் உங்கள் செய்தியையோ ஸ்கிரீன்ஷாட்டையோ கேடயம் ஒப்பிட்டுப் பார்க்கிறது. இந்தப் பட்டியல் RBI, NPCI, உள்துறை அமைச்சகம் (I4C), தொலைத்தொடர்புத் துறை ஆகியவற்றின் பொது எச்சரிக்கைகளிலிருந்து எடுக்கப்பட்டது. ஒவ்வொரு எச்சரிக்கை அறிகுறியையும் தமிழ், இந்தி அல்லது ஆங்கிலத்தில் விளக்கி, அடுத்து என்ன செய்ய வேண்டும் என்று சொல்கிறது.",
        "not_h": "இது என்ன செய்யாது",
        "not": [
            "ஒரு செய்தி பாதுகாப்பானது என்று இது ஒருபோதும் சொல்லாது. சிறந்த முடிவு \"தெரிந்த மோசடி முறை எதுவும் கிடைக்கவில்லை\" என்பதுதான்.",
            "ஒரு போன் நம்பர், UPI ID அல்லது லிங்க் உண்மையில் வங்கிக்குச் சொந்தமானதா என்று இதனால் சரிபார்க்க முடியாது. ஆள்மாறாட்ட முறைகளை மட்டுமே கண்டுபிடிக்கும்.",
            "இந்த முறைகளைத் தவிர்க்கும் புதிய மோசடிச் செய்திகள் பிடிபடாமல் போகலாம்.",
            "இது உங்களுக்காக எதையும் புகார் செய்யாது. 1930 க்கு அழையுங்கள் அல்லது cybercrime.gov.in ஐப் பயன்படுத்துங்கள்."
        ],
        "privacy_h": "உங்கள் தனியுரிமை",
        "privacy": "கேடயம் இந்தக் கணினியிலேயே இயங்குகிறது. இந்தக் கணினியிலிருந்து மட்டுமே இணைப்புகளை ஏற்கிறது. உங்கள் செய்தியையோ ஸ்கிரீன்ஷாட்டையோ எங்கும் அனுப்பாது, சேமிக்காது, நீங்கள் சரிபார்ப்பவற்றைப் பதிவு செய்யாது. ஸ்கிரீன்ஷாட்கள் இந்தக் கணினியில் உள்ள Tesseract நிரலால் நினைவகத்திலேயே படிக்கப்படுகின்றன. இந்தப் பக்கம் வெளி எழுத்துருக்கள், ஸ்கிரிப்டுகள், கண்காணிப்புக் கருவிகள் எதையும் ஏற்றாது.",
        "model_h": "சொல் சரிபார்ப்பு",
        "model": "பொது SMS மோசடித் தரவுத்தொகுப்பில் பயிற்சி பெற்ற ஒரு சிறிய புள்ளியியல் மாதிரியும் கேடயத்தில் உள்ளது. சோதனையில் அது சாதாரண வங்கிச் செய்திகளுக்கும் அதிக மதிப்பெண் தந்தது, ஏனெனில் அதன் பயிற்சித் தரவில் உள்ள சாதாரண செய்திகள் பெரும்பாலும் தனிப்பட்ட உரையாடல்கள். எனவே அது முடிவை மாற்றாது; ஆங்கிலச் செய்திகளுக்கு விவரங்களில் மட்டும் காட்டப்படுகிறது.",
        "sources_h": "ஆதாரங்கள்"
    },
    "hi": {
        "does_h": "यह क्या करता है",
        "does": "केडयम आपके संदेश या स्क्रीनशॉट को उन चालों की सूची से मिलाता है जो भारत में ठग इस्तेमाल करते हैं। यह सूची RBI, NPCI, गृह मंत्रालय (I4C) और दूरसंचार विभाग की सार्वजनिक चेतावनियों से ली गई है। यह हर चेतावनी के संकेत को हिन्दी, तमिल या अंग्रेज़ी में समझाता है और बताता है कि आगे क्या करें।",
        "not_h": "यह क्या नहीं करता",
        "not": [
            "यह कभी नहीं कहता कि कोई संदेश सुरक्षित है। सबसे अच्छा नतीजा \"कोई जानी-पहचानी धोखाधड़ी नहीं मिली\" है।",
            "यह नहीं जाँच सकता कि कोई फ़ोन नंबर, UPI ID या लिंक सच में किसी बैंक का है। यह सिर्फ़ नकल करने के तरीकों को पहचानता है।",
            "जो नए ठगी संदेश इन तरीकों से बचकर लिखे गए हों, वे पकड़ में नहीं आएँगे।",
            "यह आपके लिए कोई शिकायत दर्ज नहीं करता। 1930 पर कॉल करें या cybercrime.gov.in इस्तेमाल करें।"
        ],
        "privacy_h": "आपकी निजता",
        "privacy": "केडयम इसी कंप्यूटर पर चलता है। यह सिर्फ़ इसी कंप्यूटर से कनेक्शन लेता है, आपका संदेश या स्क्रीनशॉट कहीं नहीं भेजता, सेव नहीं करता, और आपने क्या जाँचा इसका कोई रिकॉर्ड नहीं रखता। स्क्रीनशॉट इसी कंप्यूटर पर Tesseract प्रोग्राम द्वारा मेमोरी में ही पढ़े जाते हैं। यह पेज कोई बाहरी फ़ॉन्ट, स्क्रिप्ट या ट्रैकर लोड नहीं करता।",
        "model_h": "शब्द जाँच",
        "model": "केडयम में एक छोटा सांख्यिकीय मॉडल भी है जिसे एक सार्वजनिक SMS धोखाधड़ी डेटासेट पर सिखाया गया है। जाँच में यह आम बैंक संदेशों को भी अक्सर ज़्यादा अंक देता था, क्योंकि इसके सीखने वाले डेटा में आम संदेश ज़्यादातर निजी बातचीत हैं। इसलिए यह नतीजा नहीं बदलता; अंग्रेज़ी संदेशों के लिए सिर्फ़ विवरण में दिखाया जाता है।",
        "sources_h": "स्रोत"
    }
}

SOURCE_LINKS = {
    "NPCI-SAFETY": ("NPCI UPI Safety Shield", "https://www.npci.org.in/what-we-do/upi/upi-safety-shield"),
    "RBI-BEAWARE": ("RBI BE(A)WARE booklet, 2022", "https://rbidocs.rbi.org.in/rdocs/content/pdfs/BEAWARE07032022.pdf"),
    "I4C-DIGITAL-ARREST": ("Ministry of Home Affairs (I4C), PIB, March 2025", "https://pib.gov.in/PressReleasePage.aspx?PRID=2110809"),
    "DOT-CHAKSHU": ("DoT Sanchar Saathi, Chakshu", "https://sancharsaathi.gov.in/sfc/"),
    "TRAI-HEADERS": ("TRAI commercial SMS rules (TCCCPR 2018)", "https://www.trai.gov.in/"),
}


def lang_or_default(lang: str | None) -> str:
    return lang if lang in LANGS else "en"


HOSTED = os.environ.get("KEDAYAM_HOSTED") == "1"

# Wording for the public demo, where Kedayam runs on a server rather than the parent's own computer.
HOSTED_UI = {
    "en": {
        "privacy": "This is the public demo. Your message or screenshot is checked in memory and then discarded. Kedayam does not save it or log it. Installed on your own computer, nothing leaves it.",
        "family_intro": "For a son, daughter or carer: set this up once on your parent's computer. Kedayam will then remind them to call you before acting on a suspicious message. On this public demo it is kept in memory for this browser only and is wiped when the demo restarts.",
        "family_removed": "Family setup removed from this browser.",
    },
    "ta": {
        "privacy": "இது பொது முன்னோட்டம். உங்கள் செய்தியோ ஸ்கிரீன்ஷாட்டோ நினைவகத்திலேயே சரிபார்க்கப்பட்டு உடனே நீக்கப்படும். கேடயம் அதைச் சேமிக்காது, பதிவு செய்யாது. உங்கள் சொந்தக் கணினியில் நிறுவினால், எதுவும் வெளியே செல்லாது.",
        "family_intro": "மகன், மகள் அல்லது பராமரிப்பாளருக்கு: உங்கள் பெற்றோரின் கணினியில் இதை ஒருமுறை அமைக்கவும். சந்தேகமான செய்தி வந்தால், எதையும் செய்யும் முன் உங்களை அழைக்குமாறு கேடயம் நினைவூட்டும். இந்தப் பொது முன்னோட்டத்தில் இது இந்த உலாவிக்கு மட்டும் நினைவகத்தில் வைக்கப்பட்டு, முன்னோட்டம் மீண்டும் தொடங்கும்போது அழிக்கப்படும்.",
        "family_removed": "குடும்ப அமைப்பு இந்த உலாவியிலிருந்து நீக்கப்பட்டது.",
    },
    "hi": {
        "privacy": "यह सार्वजनिक डेमो है। आपका संदेश या स्क्रीनशॉट मेमोरी में ही जाँचा जाता है और फिर हटा दिया जाता है। केडयम उसे सेव नहीं करता और उसका रिकॉर्ड नहीं रखता। अपने कंप्यूटर पर इंस्टॉल करने पर कुछ भी बाहर नहीं जाता।",
        "family_intro": "बेटे, बेटी या देखभाल करने वाले के लिए: इसे अपने माता-पिता के कंप्यूटर पर एक बार सेट करें। फिर शक वाले संदेश पर कुछ करने से पहले केडयम उन्हें आपको फ़ोन करने की याद दिलाएगा। इस सार्वजनिक डेमो में यह सिर्फ़ इसी ब्राउज़र के लिए मेमोरी में रहता है और डेमो दोबारा शुरू होने पर मिट जाता है।",
        "family_removed": "परिवार सेटअप इस ब्राउज़र से हटा दिया गया।",
    },
}
HOSTED_ABOUT_PRIVACY = {
    "en": "This public demo runs on a small Modal server. Your message or screenshot is checked in memory and discarded; it is not saved and there are no access logs. Screenshots are read in memory by Tesseract. Family setup is kept in memory for this browser only. Installed on your own computer, Kedayam only accepts connections from that computer and nothing leaves it. The page loads no outside fonts, scripts or trackers.",
    "ta": "இந்தப் பொது முன்னோட்டம் ஒரு சிறிய Modal சர்வரில் இயங்குகிறது. உங்கள் செய்தியோ ஸ்கிரீன்ஷாட்டோ நினைவகத்திலேயே சரிபார்க்கப்பட்டு நீக்கப்படும்; சேமிக்கப்படாது, அணுகல் பதிவுகளும் இல்லை. ஸ்கிரீன்ஷாட்டுகளை Tesseract நினைவகத்திலேயே படிக்கிறது. குடும்ப அமைப்பு இந்த உலாவிக்கு மட்டும் நினைவகத்தில் வைக்கப்படும். உங்கள் சொந்தக் கணினியில் நிறுவினால், கேடயம் அந்தக் கணினியிலிருந்து மட்டுமே இணைப்புகளை ஏற்கும், எதுவும் வெளியே செல்லாது. இந்தப் பக்கம் வெளி எழுத்துருக்கள், ஸ்கிரிப்டுகள் அல்லது கண்காணிப்புகளை ஏற்றுவதில்லை.",
    "hi": "यह सार्वजनिक डेमो एक छोटे Modal सर्वर पर चलता है। आपका संदेश या स्क्रीनशॉट मेमोरी में ही जाँचा जाता है और हटा दिया जाता है; न सेव होता है, न कोई एक्सेस लॉग रहता है। स्क्रीनशॉट Tesseract मेमोरी में ही पढ़ता है। परिवार सेटअप सिर्फ़ इसी ब्राउज़र के लिए मेमोरी में रहता है। अपने कंप्यूटर पर इंस्टॉल करने पर केडयम सिर्फ़ उसी कंप्यूटर से कनेक्शन लेता है और कुछ भी बाहर नहीं जाता। यह पेज कोई बाहरी फ़ॉन्ट, स्क्रिप्ट या ट्रैकर लोड नहीं करता।",
}


def t(lang: str, key: str, **kw: object) -> str:
    lang = lang_or_default(lang)
    s = HOSTED_UI[lang].get(key) if HOSTED else None
    s = s or UI[lang][key]
    return s.format(**kw) if kw else s
