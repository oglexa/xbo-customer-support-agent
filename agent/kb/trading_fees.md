# XBO Help Center: Trading Fees and VIP Tier Structure

XBO utilizes a transparent Maker-Taker fee model across all spot and derivatives trading pairs. Fees are dynamically adjusted based on the user's cumulative 30-day trading volume (calculated in USD equivalent) and the amount of native Apex Utility Tokens (APX) held in their exchange wallets.

### The Maker-Taker Model Explained

* **Maker Fees:** Applied when you add liquidity to the order book by placing a limit order that does not match instantly against an existing order.
* **Taker Fees:** Applied when you remove liquidity from the order book by placing an order (such as a market order) that executes immediately against an existing order.

### VIP Tier Structure and Fee Schedule

Trading volumes are evaluated daily at 00:00 UTC, and any tier upgrades or downgrades are applied automatically within 2 hours.

| VIP Tier | 30-Day Volume (USD) | Min APX Balance | Maker Fee | Taker Fee |
| :--- | :--- | :--- | :--- | :--- |
| **Standard** | < $50,000 | 0 APX | 0.100% | 0.100% |
| **VIP 1** | ≥ $50,000 | 1,000 APX | 0.080% | 0.090% |
| **VIP 2** | ≥ $250,000 | 5,000 APX | 0.060% | 0.080% |
| **VIP 3** | ≥ $1,000,000 | 25,000 APX | 0.040% | 0.060% |
| **VIP 4 (Pro)**| ≥ $5,000,000 | 100,000 APX | 0.020% | 0.040% |
| **VIP 5 (Inst)**| ≥ $25,000,000 | 500,000 APX | 0.000% | 0.020% |

### APX Token Fee Deduction Discount

Users can unlock an additional **25% flat discount** on all spot and margin trading fees by enabling the "Pay Fees with APX" toggle in their account profile. When active, the trading engine automatically calculates the fee equivalent in APX and deducts it from the user's APX balance instead of taking the base asset of the trading pair. 

* *Example:* A Standard tier user executing a Taker order would normally pay a 0.100% fee. With APX deduction active, the effective fee drops to 0.075%.

### Crucial Account Status and API Overlaps

1. **Account Freezes:** If an account enters a full or partial lockdown due to security or compliance reasons (as defined in the *Account Freeze Policy*), all pending limit orders on the book are automatically canceled. Upon account restoration, the user retains their historical 30-day trading volume baseline for VIP calculation purposes.
2. **API Trading:** Orders routed via the REST or WebSocket private API pipelines (referenced in *API Rate Limits and Usage Policy*) are subject to the exact same VIP fee schedules as manual web interface trades. There are no specialized execution discounts for automated scripts unless the account undergoes Enhanced Due Diligence (EDD) to obtain customized market-maker terms under Tier 3 (Pro Verification).