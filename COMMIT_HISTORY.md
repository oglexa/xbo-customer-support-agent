# 📋 XBO QA Orchestration — Git Commit History

This document contains a structured representation of the official Git commit history for the **XBO Customer Support Agent QA Orchestration** project. It serves as an easily readable, static reference showing the incremental development workflow and timeline.

---

## 📈 Development Timeline & Commits

| Commit Hash | Date & Time (UTC+3) | Author | Commit Message / Deliverables |
| :---: | :--- | :--- | :--- |
| `de5d4d0` | 2026-05-28 18:01:40 | Oleksiy | finalized tests and reporting, updated README.md, created DECISIONS.md, created CLAUDE.md |
| `09e4bee` | 2026-05-28 17:08:44 | Oleksiy | implemented orchestration between day agent and night agent |
| `b3f4aee` | 2026-05-28 16:45:17 | Oleksiy | created security tests tests and hallucination tests |
| `21126db` | 2026-05-28 16:13:13 | Oleksiy | created functional tests and rag tests |
| `7a408f9` | 2026-05-28 14:03:37 | Oleksiy | build the target agent |
| `de14d81` | 2026-05-28 13:56:21 | Oleksiy | created knowledge base |
| `798f247` | 2026-05-28 13:42:17 | Oleksiy | Initial commit |

---

## 🔍 Detailed Commit Descriptions & Changeset Log

### 1. `798f247` — Initial commit
* **Date**: 2026-05-28 13:42:17
* **Summary**: Standard base task skeleton setup.

### 2. `de14d81` — created knowledge base
* **Date**: 2026-05-28 13:56:21
* **Summary**: Added markdown documentation articles (`agent/kb/*.md`) outlining company KYC rules, account freeze, API limit policies, and regulatory guidelines.

### 3. `7a408f9` — build the target agent
* **Date**: 2026-05-28 14:03:37
* **Summary**: Implemented the customer support agent backend with FastAPI (`agent/app.py`), the RAG index indexing engine (`agent/rag.py`), prompt assets (`agent/prompts.py`), and system tool configurations.

### 4. `21126db` — created functional tests and rag tests
* **Date**: 2026-05-28 16:13:13
* **Summary**: Created Part 2A Functional Suite (measuring semantic answer similarities vs. ground truths via `SentenceTransformers` embeddings) and Part 2B RAG Suite (measuring retriever precision and recall metrics).

### 5. `b3f4aee` — created security tests tests and hallucination tests
* **Date**: 2026-05-28 16:45:17
* **Summary**: Added Part 2C Security Suite (testing jailbreaks, prompt injection, PII protection, and privilege escalation) and Part 2D Hallucination Suite (detecting out-of-scope queries and ensuring appropriate refusals).

### 6. `09e4bee` — implemented orchestration between day agent and night agent
* **Date**: 2026-05-28 17:08:44
* **Summary**: Programmed orchestration runners `day_agent.py` (pre-merge fast gate with timeout and exit codes) and `night_agent.py` (unattended full overnight test execution utilizing a resilient skip-and-continue policy).

### 7. `de5d4d0` — finalized tests and reporting, updated README.md, created DECISIONS.md, created CLAUDE.md
* **Date**: 2026-05-28 18:01:40
* **Summary**: Unified all deliverables. Handled brand consolidation under the XBO name. Integrated markdown report outputs (`day_report.md` and `night_report.md`). Added Unicode safety configurations to CLI stdout streams to prevent console errors on Windows. Authored comprehensive onboarding documentations (`README.md`, `DECISIONS.md`, and `CLAUDE.md`).

---
*Generated automatically from the official git metadata for reference.*
