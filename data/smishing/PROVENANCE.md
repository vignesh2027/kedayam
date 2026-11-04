# SMS Phishing Dataset (Mishra and Soni, 2022)

* **Title:** SMS PHISHING DATASET FOR MACHINE LEARNING AND PATTERN RECOGNITION
* **Authors:** Sandhya Mishra; Devpriya Soni (supervision), Jaypee Institute of Information Technology
* **Published:** Mendeley Data, version 1, 20 June 2022
* **DOI:** https://doi.org/10.17632/f45bkkt8pr.1
* **Licence:** Creative Commons Attribution 4.0 International (CC BY 4.0), https://creativecommons.org/licenses/by/4.0/
* **File:** `Dataset_5971.csv`, taken unchanged from `Dataset_5971.zip` in the dataset (zip SHA-256 `9bbf3188fdad81495d8e82825648b9b63b53fc86841a3d26c02629990b233cc3`; csv SHA-256 `649844f1c62a6b27e145eaf17a65f7010c56c390e11a794ea8329993a05ba71e`), downloaded 4 November 2026.

## What it contains

5,971 text messages with a `LABEL` column: 4,844 `ham`, 489 `spam` (written as `spam` or `Spam`), 638 `smishing` (written as `Smishing` or `smishing`). The authors describe the messages as collected by converting images found on the internet to text. Many of the ham messages appear to come from the earlier UCI SMS Spam Collection (Almeida and Gomez Hidalgo, 2011), and the smishing messages include Indian bank and KYC scams. The file contains about 185 Unicode replacement characters from the original conversion; we leave them as they are.

## How Kedayam uses it

* Labels are normalised to lower case. `spam` and `smishing` are merged into one class, "suspicious", and `ham` is the other class.
* Exact duplicate messages (after lower casing and collapsing whitespace) are removed before splitting, so the same text cannot appear in both training and test data.
* The data is split 70 / 15 / 15 into train, validation and test with a fixed seed, stratified by class. The decision threshold is chosen on validation only. Test numbers are reported once.
* No messages from this dataset are shown in the app.

## Limits of this data

It is mostly English and mostly older (pre-2022) messages. It has very little Tamil or Hindi text and few UPI collect request or digital arrest scams. Ham messages are personal chat more than bank alerts. That is why Kedayam treats the classifier only as a secondary signal.
