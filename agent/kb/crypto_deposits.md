# ApexCrypto Help Center: Cryptocurrency Deposits Guide

Depositing digital assets into your ApexCrypto account is automated and generally straightforward. However, due to the irreversible nature of blockchain networks, users must strictly adhere to the protocols outlined below to avoid permanent loss of funds.

### Standard Deposit Process and Confirmations
To credit a crypto deposit, the transaction must achieve a minimum number of block confirmations on the blockchain network. These requirements fluctuate based on network security baselines:

* **Bitcoin (BTC):** Requires 2 network confirmations (approx. 20 minutes).
* **Ethereum (ETH) & ERC-20 Tokens:** Requires 12 network confirmations (approx. 3 minutes).
* **Solana (SOL):** Requires 30 network confirmations (approx. 15 seconds).
* **Ripple (XRP):** Requires 1 confirmation (instantaneous).

### Crucial Deposit Rules

1. **Address Matching:** You must only send assets to the specific address generated for that exact token. For instance, sending Bitcoin Cash (BCH) to a Bitcoin (BTC) deposit address will result in the total and permanent loss of those tokens.
2. **Tag/Memo Requirements:** Certain networks, such as Ripple (XRP) and Cosmos (ATOM), utilize a shared wallet architecture. When depositing these assets, you **must** include both the unique deposit address and the correct **Destination Tag** or **Memo**. Omitting or entering an incorrect Tag/Memo will result in funds being routed to the main pool without account attribution, requiring a manual recovery process that takes up to 30 business days and incurs a 10% recovery fee.
3. **Smart Contract Deposits:** ApexCrypto does not support incoming ETH or ERC-20 deposits executed via smart contracts (internal transactions). Deposits must be sent as standard external transfers (EOA). Smart contract deposits will not be detected automatically and require manual compliance intervention.

### Minimum Deposit Thresholds
There is no maximum limit on cryptocurrency deposits for any verification tier (including Tier 1). However, minimal operational thresholds apply:
* **Bitcoin (BTC):** 0.0001 BTC
* **Ethereum (ETH):** 0.005 ETH
* **Tether (USDT):** 5 USDT
Deposits below these thresholds will not be processed or credited to the user's balance, nor can they be accumulated over multiple transactions.