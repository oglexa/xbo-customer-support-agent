# ApexCrypto Help Center: Asset Withdrawal Fees Schedule

To maintain the operational integrity of the network bridges and cover public ledger mining costs, ApexCrypto charges standard fees on all outgoing asset transfers. Fees are dynamically or statically structured depending on the underlying blockchain asset and network congestion.

### Cryptocurrency Withdrawal Fees

Cryptocurrency withdrawal fees are dynamic and adjust periodically based on network traffic, block space demand, and gas prices. The fee is deducted directly from the gross withdrawal amount, meaning the destination address receives the requested amount minus the fee.

* **Bitcoin (BTC):** * Native SegWit (Bech32): 0.0004 BTC per transaction.
  * Legacy Network: 0.0008 BTC per transaction.
  * Minimum Withdrawal: 0.001 BTC.
* **Ethereum (ETH) & ERC-20 Tokens:**
  * Ethereum Mainnet: 0.005 ETH fixed baseline (subject to sharp spikes during network congestion up to 0.015 ETH).
  * Tether (USDT) / USD Coin (USDC) via ERC-20: 10 tokens per transaction.
  * Minimum Withdrawal: 0.01 ETH / 20 USDT.
* **Alternative Layer 1 Networks:**
  * Solana (SOL): 0.01 SOL per transaction. Minimum withdrawal: 0.1 SOL.
  * Ripple (XRP): 0.25 XRP per transaction (requires destination tag entry). Minimum withdrawal: 20 XRP.

### Fiat Currency Withdrawal Fees

Fiat processing involves external banking networks, processing intermediaries, and clearing houses. The fees depend heavily on the method chosen:

* **SEPA Transfer (Eurozone):** €1.50 flat fee per transfer. Usually settles within 1 business day.
* **ACH Transfer (United States):** Free of charge, but restricted to Tier 2 users and above. Settles within 2-3 business days.
* **Domestic Wire (United States):** $25.00 flat fee. Settles same-day if initiated before 13:00 EST.
* **International SWIFT Wire:** 0.1% of the total transfer value, with a minimum fee of $35.00 and a maximum fee cap of $250.00.

### Internal Transfers (Off-Chain)
Transfers between two distinct ApexCrypto accounts are executed off-chain and are entirely free of network fees. To leverage this, users must utilize the "Internal Pay" feature instead of routing the withdrawal through a public blockchain address.