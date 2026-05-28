# ApexCrypto Help Center: Fiat Currency Deposits & Withdrawals

To bridge the gap between traditional banking and digital assets, ApexCrypto supports a variety of fiat currency payment rails. All fiat operations are subject to regional banking laws, processing schedules, and explicit security parameters.

### Permitted Fiat Gateways and Processing Windows

ApexCrypto currently supports United States Dollars (USD) and Euros (EUR). The operational processing windows align directly with the guidelines referenced in our *Asset Withdrawal Fees Schedule*:

1. **SEPA (Eurozone):**
   * **Deposits:** Free of charge. Settles within 1–2 business days.
   * **Withdrawals:** Subject to a flat €1.50 fee. Settles within 1 business day.
2. **ACH (United States):**
   * **Deposits:** Free. Processing requires 3–5 business days for bank clearance.
   * **Withdrawals:** Free. Settles within 2–3 business days.
3. **Domestic & International Wires:**
   * **Deposits:** Free on ApexCrypto's end, though intermediary banks may apply wire fees. Settles within 24 hours if received before 13:00 EST.
   * **Withdrawals:** $25 flat fee for domestic; up to $250 for international SWIFT wires.

### Critical Compliance Rules for Fiat Transfers

* **Third-Party Payment Ban:** The legal name on the originating or destination bank account **must exactly match** the verified legal name on the ApexCrypto account (see *Account Verification Policy*). Third-party transfers—including deposits from friends, corporate accounts (for individual profiles), or unregistered entities—will be automatically rejected. Rejected transfers are returned to the source bank minus a 5% administrative handling fee.
* **Verification Gates:** Fiat operations are strictly prohibited for **Tier 1 (Basic)** accounts. A user must achieve **Tier 2** to unlock standard fiat banking limits, or **Tier 3** to execute large-scale wire transfers exceeding $10,000 USD daily (cross-referenced in *Withdrawal Limits Framework*).
* **Source of Funds Declaration:** For aggregate fiat deposits exceeding $50,000 USD within a rolling 30-day window, our compliance desk will issue a mandatory Source of Funds (SoF) questionnaire. Failure to provide supporting documents (such as tax returns or payslips) within 7 business days will trigger an automated **Full Freeze** of the account.