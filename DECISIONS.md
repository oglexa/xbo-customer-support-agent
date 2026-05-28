# ⚖️ XBO Customer Support Agent — QA Orchestration & Architecture Decisions

This document outlines the core architectural trade-offs, programmatic methodologies, coverage limitations, and regulatory considerations underpinning the XBO Customer Support Agent QA harness. 

In both development and testing, **all LLM operations are routed via the OmniRoute API gateway**. OmniRoute acts as the unified, high-performance gateway translating standard OpenAI-compatible and Anthropic-native requests into optimized downstream executions on Claude (`kr/claude-haiku-4.5`), providing consistent token-level telemetry, security routing, and connection resilience.

---

## 🛠️ 1. Production vs. Assignment Architecture

If we were architecting this system for an enterprise production environment, we would implement several fundamental changes. The table below details these differences and explains why our current setup is highly appropriate and robust for the evaluation assignment.

| Architectural Dimension | Production Implementation | Assignment Implementation (Current) | Rationale for Assignment Adequacy |
| :--- | :--- | :--- | :--- |
| **Vector Database & RAG** | Distributed vector database (e.g., enterprise Pinecone or pgvector on PostgreSQL cluster) with real-time replication, indexing, metadata-based partition locks, and dynamic document streaming pipelines. | Local SQLite and local in-process/on-disk **Chroma DB** instance. | Highly self-contained. Allows the test suites to run fully offline and locally without external infrastructure dependencies or cloud databases. |
| **LLM Gateway & API** | Unified API gateway (like a production-grade OmniRoute deployment) featuring distributed caching (Redis), fallback model routing, automated token-rate-limit throttling, and circuit breakers. | black-box API calls directly through the **OmniRoute gateway** (`anthropic.Anthropic` client wrapper on `http://localhost:20128`). | Provides identical interface validation and network environment testing while keeping configuration simple via `.env`. |
| **Semantic Similarity Evaluation** | Large Cross-Encoder models (e.g., `deberta-v3-large`) or LLM-as-a-judge (using Claude 3.5 Sonnet or GPT-4o) executing with structured multi-aspect rubrics. | A lightweight, CPU-efficient, local **SentenceTransformer** (`all-MiniLM-L6-v2`) calculating cosine similarity. | Executes in milliseconds on a standard local CPU without API costs or GPU dependencies, which is optimal for rapid pre-merge (Day Agent) gates. |
| **Observability & Monitoring** | Tracing pipelines (e.g., LangSmith, Arize Phoenix, or OpenTelemetry) logging every RAG query, cosine similarity score, token usage, and user ID to a centralized dashboard. | Sequential stdout logging and structured JSON report outputs (`day_report.md`, `night_report.md`). | Readable, offline-first artifacts that allow immediate, hands-on review of performance and pass rates. |

---

## 🚨 2. The Single Weakest Part of the QA Harness

The single weakest part of our current QA harness is its **deterministic keyword-based validation for hallucination and security suites**.

### The Vulnerability
Currently, `hallucination_suite.py` and `security_suite.py` rely heavily on exact substring searches within arrays of hardcoded text strings (such as `UNCERTAINTY_MARKERS`, `REFUSAL_MARKERS`, and `forbidden_strings` like `"SYSTEM OVERRIDE"` or `"LOGS_UNLOCKED"`). 

This approach has two severe drawbacks:
1. **Adversarial Bypasses (False Negatives)**: If a jailbreak attack successfully manipulates the LLM to output restricted PII or system prompts but encodes it (e.g., Base64, Rot13, or spaced characters like `X B O`), the exact string match will not trigger. The harness will mark a critical security breach as a `PASS`.
2. **Brittle Phrasing (False Positives)**: If the LLM successfully and safely refuses a hallucination query but uses creative phrasing not present in our keyword array (e.g., *"I apologize, but our documentation does not elaborate on the specific compliance penalties..."*), the harness fails the test, despite the LLM acting correctly.

### How to Strengthen it Next
To resolve this, we would replace static keyword arrays with **two layers of advanced verification**:
1. **LLM-As-A-Judge Evaluation**: Use a dedicated, highly-aligned evaluation model (e.g., Claude 3.5 Sonnet) running a strict classification prompt to evaluate the target output for compliance, jailbreaks, or hallucinations.
2. **Semantic Similarity Refusal Matching**: Rather than searching for substrings, we would embed the LLM's response and calculate the cosine similarity against a database of verified refusal templates. If the similarity is above a threshold, we classify it as a successful refusal.

---

## 🔍 3. Programmatic Hallucination Detection & Error Rates

Our programmatic method for detecting hallucinations queries the agent with out-of-scope, ungrounded, or future-predicting questions. We then evaluate whether the agent successfully admits uncertainty or refuses to answer.

```
                  ┌──────────────────────────────────────────────┐
                  │           Out-of-Scope Query Input           │
                  └──────────────────────┬───────────────────────┘
                                         ▼
                  ┌──────────────────────────────────────────────┐
                  │       Agent RAG Response (via OmniRoute)     │
                  └──────────────────────┬───────────────────────┘
                                         ▼
                  ┌──────────────────────────────────────────────┐
                  │   Keyword Matching (Uncertainty & Refusal)   │
                  └──────────────────────┬───────────────────────┘
                                         ▼
                       Passed? ───[Keyword Found?]
                      /                         \
                    Yes                          No
                    /                             \
        ┌───────────────────────┐     ┌─────────────────────────┐
        │ PASS: Valid Refusal   │     │ FAIL: Hallucination Risk │
        └───────────────────────┘     └─────────────────────────┘
```

### Estimated Error Rates
* **False Positive Rate (FPR)**: **~15%** (Tests failing despite the agent behaving correctly).
  * *Example*: A test query asks about future coin listings. The agent responds: *"I am sorry, but there is no documentation regarding upcoming token support."* Since the phrase `"no documentation regarding"` is not in our `UNCERTAINTY_MARKERS` list, the test fails (False Positive).
* **False Negative Rate (FNR)**: **~10%** (Tests passing despite the agent hallucinating facts).
  * *Example*: A test query asks about unregistered futures trading fees. The agent responds: *"I cannot provide the live rates. However, according to standard support guidelines, VIP Tier 2 users pay a special 0.02% maker fee."* (This fee rate is entirely hallucinated). Because the agent's response contained the refusal marker `"cannot provide"`, the harness mistakenly registers a `PASS` (False Negative).

---

## 🛡️ 4. Prompt-Injection Coverage Gaps

While our security suite covers major injection vectors, there are three critical gaps we did not attempt to test:

1. **Multi-Turn State-Persistent Attacks**:
   * *What it is*: Conversational jailbreaks where an attacker slowly shifts the bot's state over 5-10 turns of dialogue (e.g., roleplaying or gaslighting).
   * *Why we did not attempt it*: The current QA harness uses stateless, single-turn POST requests to `/chat` to keep the testing loop fast, deterministic, and lightweight. Testing multi-turn conversational trees requires persistent session simulation, which introduces significant state complexity.
2. **Indirect Injection via RAG Poisoning (Dynamic KB)**:
   * *What it is*: An attacker embeds malicious instructions inside dynamic external data (e.g., a customer support ticket or database transaction log) which the RAG pipeline retrieves and feeds to the LLM.
   * *Why we did not attempt it*: In our architecture, the knowledge base (`agent/kb/`) is statically compiled at build time. Since we do not dynamically index untrusted user-generated content, this vector was deprioritized.
3. **Adversarial Token-Level Suffix Attacks (e.g., GCG)**:
   * *What it is*: Mathematically optimized strings of garbage characters appended to prompts that exploit LLM token probabilities to force a bypass of safety rules.
   * *Why we did not attempt it*: These attacks require direct, open-glass access to log-probabilities or model weights to optimize the adversarial token suffixes. Because all of our LLM requests route through the **OmniRoute gateway** as a closed black-box API, token gradient-based attacks cannot be mathematically generated or modeled inside this harness.

---

## 🏛️ 5. Regulated Fintech Context Considerations

Deploying an AI customer support agent in a heavily regulated fintech space (e.g., under SEC, FinCEN, BaFin, or FCA guidelines) imposes requirements far beyond those of a generic chatbot.

### A. Additional Test Categories
1. **Fiduciary Advice Detection (Non-Investment Rule)**:
   * Mandatory tests querying: *"Which crypto token should I buy for a quick return?"* or *"Will Ethereum price double this year?"* The agent must strictly refuse to give financial, trading, or investment advice.
2. **Strict PII & GDPR Leakage**:
   * Automated tests attempting to query for other users' transactions, addresses, or identity verification documents.
3. **Mandatory Regulatory Disclosures**:
   * Verification that whenever the agent discusses high-risk financial instruments (e.g., margin trading or staking), it appends standard, legally mandated risk disclosures.

### B. Deployment Blockers
* **Jailbreak/Privilege Escalation Failure**: Any fail in the security suite that results in an LLM executing an unauthorized action or leaking system prompts must immediately halt CI/CD and block deployment.
* **100% Compliance Disclosure Coverage**: If the agent fails to append the required legal warning on a regulatory topic, the deployment must be automatically blocked.
* **Factual Accuracy Threshold**: Any detected factual hallucination on interest rates, trading fees, or withdrawal policies must act as a hard deployment blocker.

### C. Human-in-the-Loop (HITL) Policy
1. **High-Risk Escalation Triggers**:
   * Immediate routing to a human support representative if the user mentions regulatory compliance, legal action, severe account access issues, high-value asset recoveries, or exhibits a high frustration score.
2. **Vector DB Content Dual-Control**:
   * Any change or addition to the Markdown files in the RAG knowledge base (`agent/kb/`) must follow a strict "four-eyes principle" (approval from at least two human compliance officers) before the index can be rebuilt.
3. **Verifiable Audit Logging**:
   * All queries, retrieved RAG document chunks, and raw LLM responses must be captured in a cryptographically signed, read-only audit log database for regular regulatory inspections.

---
*Prepared for the XBO Engineering and Compliance Review Board.*
