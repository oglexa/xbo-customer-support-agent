# XBO Security & Compliance: Suspicious Activity Monitoring

XBO utilizes advanced, real-time automated behavioral monitoring systems combined with dedicated fraud investigation units to detect, prevent, and mitigate unauthorized account access, financial crime, and market manipulation.

### Indicators of Suspicious Activity

An account may be flagged for manual compliance review if any of the following triggers are met:
* **IP and Geographic Anomalies:** Rapid consecutive logins from geographically incompatible regions (e.g., a login from London followed by a login from Tokyo within a two-hour window).
* **Velocity Anomalies:** A sudden change in transaction frequency or volume, such as a dormant Tier 1 or Tier 2 account suddenly depositing and attempting to withdraw maximum limits within a 12-hour period.
* **Structuring:** Multiple consecutive withdrawals or deposits kept just below reporting or verification thresholds (e.g., executing several $9,900 transfers to avoid a $10,000 threshold notice).
* **High-Risk Counterparties:** Direct interaction with known high-risk blockchain entities, mixing services (e.g., Tornado Cash), or addresses associated with darknet marketplaces or reported hacks.

### Automated Mitigation Actions

When the automated monitoring system flags an account, the platform may execute immediate precautionary protocols without prior warning to the user:
1. **Interim Withdrawal Lockdown:** Outbound transfers are blocked for 24 hours while an investigator cross-checks transaction hashes and device logs.
2. **Session Termination:** All active web and mobile API sessions are killed, requiring the user to re-authenticate using full Multi-Factor Authentication (MFA).
3. **API Deactivation:** All linked API keys are deactivated or permanently deleted to halt automated trading scripts.

### Resolution Protocol
If your account is flagged for suspicious activity, you will receive an encrypted email notification from security@XBO.com. To lift restrictions, users are typically required to submit a "Video Verification Statement" holding their registered government ID and reciting a specific phrase provided by the compliance officer.