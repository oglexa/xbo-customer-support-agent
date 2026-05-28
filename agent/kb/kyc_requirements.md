# ApexCrypto Compliance & Security: Technical KYC Requirements

This document establishes the precise technical standards, acceptable documentation formats, and global compliance criteria required to successfully pass Know Your Customer (KYC) verification on the ApexCrypto platform. 

### Acceptable Proof of Identity (PoI) Documents

To satisfy Tier 2 (Advanced) requirements, users must upload a valid, unexpired government-issued identification document. Acceptable document types vary by region:

* **International Passports:** Accepted globally. Must show the full bio-data page, including the machine-readable zone (MRZ).
* **National Identity Cards:** Accepted for citizens of the European Economic Area (EEA), Switzerland, the United Kingdom, Singapore, and Australia. Digital or paper slips are not accepted.
* **Driver’s Licenses:** Accepted for identity verification *only* for residents of the United States, Canada, and the United Kingdom. 

> **Strict Regulatory Prohibition:** ApexCrypto does not accept student IDs, corporate badges, military IDs, medical cards, or temporary residence visas as primary Proof of Identity.

### Technical Image and Upload Standards

The automated compliance verification engine utilizes advanced optical character recognition (OCR) and biometric face-matching algorithms. Submissions that fail to meet the following parameters will be rejected automatically:
* **File Format & Size:** Images must be in JPEG, PNG, or PDF format. Minimum file size is 500 KB; maximum threshold is 10 MB per file.
* **Visibility:** All four corners of the document card or book must be fully visible within the frame. No parts of the text, expiration dates, or photos may be obscured by fingers, tape, or plastic holders.
* **Glare and Lighting:** Submissions with significant flash glare or shadows over vital data patches will be instantly systematically discarded. Do not use scan-to-PDF mobile filters that alter natural coloring.

### Biometric Selfie and Liveness Checks
During the Tier 2 pipeline, users must execute a real-time biometric liveness scan via a webcam or mobile camera. 
* The user must rotate their head in a circular motion as prompted by the interface.
* Still photos, uploads of pre-recorded videos, or screenshots of existing digital photographs will be flagged by our anti-spoofing sub-systems as a *Suspicious Activity Flag*, potentially triggering an interim lockdown (see *Suspicious Activity Monitoring*).

### Politically Exposed Persons (PEP) and Sanctions Policy

ApexCrypto operates in strict compliance with international sanctions regimes and FATF guidelines. 
* **Sanctioned Jurisdictions:** Residents or citizens of countries currently undergoing comprehensive international embargoes (including but not limited to North Korea, Iran, Syria, and Cuba) are completely barred from passing KYC verification.
* **PEP Declaration:** During registration, users are legally obligated to declare if they hold, or have held within the past 12 months, a prominent public function (e.g., senior government official, politician, judicial officer). PEP accounts cannot be verified via standard automated processing; they are routed directly to Tier 3 manual compliance desk review and are subject to Enhanced Due Diligence (EDD), regardless of transaction volumes.