# ApexCrypto Developer Portal: API Rate Limits and Usage Policy

To maintain the high availability, stability, and responsiveness of the ApexCrypto trading engine, strict rate limits are enforced across all public and private API endpoints. These limits prevent server abuse, mitigate DDoS vectors, and ensure a fair environment for both algorithmic and manual traders.

### Authentication Requirements
* **Public Endpoints (Market Data):** Can be accessed without authentication.
* **Private Endpoints (Trading & Account Management):** Require valid API Keys. Generating API keys requires the user account to have completed at least **Tier 2 (Advanced Verification)**, as defined in our *Account Verification Policy*.

### Standard Rate Limit Structures
Rate limits are calculated on a rolling-window basis per IP address for public endpoints, and per API Key / Account ID for private endpoints.

* **REST API Public Endpoints:** Maximum of 60 requests per rolling 1-minute window per IP.
* **REST API Private Endpoints (Orders and Trading):** Maximum of 120 requests per rolling 1-minute window per Account.
* **REST API Private Endpoints (Account/Wallet Data):** Maximum of 30 requests per rolling 1-minute window per Account.
* **WebSocket Connections:** A single IP address may open a maximum of 5 concurrent WebSocket connections. Each connection can subscribe to a maximum of 25 channels simultaneously.

### Rate Limit Violations and Penalties
If a user script or system exceeds the allocated limits, the ApexCrypto gateway will reject subsequent requests and return an **HTTP 429 Too Many Requests** error.

1. **First Warning:** If an IP triggers an HTTP 429 error more than 5 times within an hour, the IP is automatically banned from all public endpoints for 10 minutes.
2. **System Lockdown:** Persistent, high-velocity violations or deliberate attempts to bypass rate limits using proxy rotation will result in an automated platform response. The system will flag the account under the "Velocity Anomalies" protocol (see *Suspicious Activity Monitoring*), resulting in an immediate **Session Termination** and a temporary **Interim Withdrawal Lockdown** for 24 hours while engineering teams assess the script's intent.

### Requesting Limit Increases
Institutional traders or designated market makers operating under Tier 3 (Pro Verification) statuses can request customized, higher-throughput API bandwidth. Applications containing technical architecture descriptions should be sent to api-support@apexcrypto.com.