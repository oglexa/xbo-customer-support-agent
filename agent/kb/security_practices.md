# ApexCrypto Security & Compliance: Best Practices and User Guidelines

ApexCrypto utilizes state-of-the-art security architecture, including multi-signature cold storage vaults and institutional-grade encryption, to protect user assets. However, individual account security depends heavily on the proactive measures taken by the user.

### Mandatory and Recommended Security Settings

1. **Multi-Factor Authentication (MFA):**
   * **Rule:** SMS-based 2FA is permitted for Tier 1 users but is strongly discouraged due to SIM-swapping risks. ApexCrypto mandates the use of app-based authenticators (e.g., Google Authenticator) for all **Tier 2** accounts and higher.
   * **Action:** MFA is strictly required to authorize withdrawals, modify API configurations, or change account credentials.

2. **Phishing Prevention (Anti-Phishing Code):**
   * **Rule:** Users should configure a personalized, alphanumeric "Anti-Phishing Code" within their security dashboard. 
   * **Action:** Once set, this exact code will appear in the header of every legitimate transactional and security email sent by ApexCrypto (such as alerts from security@apexcrypto.com). If an email claims to be from ApexCrypto but lacks this code, it must be treated as malicious.

3. **Withdrawal Address Whitelisting:**
   * **Rule:** Users can activate the "Address Whitelisting" feature in their security settings. 
   * **Action:** When enabled, the account can only withdraw assets to addresses that have been previously saved and confirmed via email/MFA. Adding a new address to the whitelist incurs a mandatory **24-hour cooling-off period**, during which withdrawals to that specific address are blocked.

### Recognizing Phishing and Social Engineering

* **Communication Standards:** ApexCrypto employees will **never** ask you for your password, MFA backup keys, or your seed phrases. 
* **Support Protocols:** All official support interactions are text-based and occur inside our secure helpdesk environment or via encrypted emails ending strictly in `@apexcrypto.com`. Anyone contacting you via Telegram, Discord, or phone claiming to be an ApexCrypto support agent or compliance officer is a scammer. 
* **Emergency Response:** If you suspect your account has been compromised, locate any recent login notification email and click the embedded "Freeze Account" link immediately to trigger an instant, automated self-lockout (see *Account Freeze Policy*).