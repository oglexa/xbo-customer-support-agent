# 🤖 CLAUDE.md — Developer & AI Onboarding Context

This file serves as the definitive onboarding guide and operational runbook for any AI agent or human engineer inheriting the **XBO Customer Support Agent** repository. Use it to understand the system architecture, conventions, operational runbook, and key project gotchas.

---

## 🏗️ 1. Architecture & Tech Stack

The XBO Customer Support QA platform consists of two main pillars: the **FastAPI Agent Service** and the **Dual-Agent Test Orchestration Harness**.

* **FastAPI Service (`agent/app.py`)**: Exposes the `/chat` endpoint. Uses mock session databases (`agent/auth.py`), tool executors (`agent/tools.py`), and RAG utilities.
* **OmniRoute Gateway Routing (`agent/llm.py`)**: All LLM client calls go through the **OmniRoute gateway** (using `anthropic.Anthropic` over Bearer authorization on `http://localhost:20128` with model `kr/claude-haiku-4.5`).
* **Vector Store (`agent/rag.py`)**: Powered by a local SQLite-backed **Chroma DB** instance. Chroma loads and indexes Markdown documentation articles from `agent/kb/`.
* **Day Agent Orchestrator (`agent/orchestration/day_agent.py`)**: Runs functional tests (Part 2A) as a fast pre-merge gate. Blocks commits on failures.
* **Night Agent Orchestrator (`agent/orchestration/night_agent.py`)**: Full unattended overnight run across all 4 suites. Operates on a **Skip-and-Continue** policy.

---

## ⚡ 2. Operational Runbook (Key Commands)

Always run the following commands within the project's virtual environment:

### Virtual Environment Activation
```powershell
# Windows
.venv\Scripts\Activate.ps1

# Linux / macOS
source .venv/bin/activate
```

### Starting the FastAPI Server
```bash
.venv\Scripts\uvicorn app:app --app-dir agent --port 8000 --reload
```

### Rebuilding the RAG Database Index (Required after editing `agent/kb/` articles)
```bash
.venv\Scripts\python -c "import sys; sys.path.insert(0, 'agent'); import rag; rag.build_index(); print(f'Indexed {rag.collection.count()} chunks')"
```

### Running the Orchestrators
```bash
# Day Agent Pre-merge Gate (writes day_report.md)
.venv\Scripts\python agent/orchestration/day_agent.py

# Night Agent Unattended Full Run (writes night_report.md)
.venv\Scripts\python agent/orchestration/night_agent.py
```

### Running Individual Test Suites Directly
```bash
# Part 2A: Functional Suite (Semantic Similarity)
.venv\Scripts\python agent/tests/functional/functional_suite.py

# Part 2B: RAG Suite (Precision@3 / Recall@3)
.venv\Scripts\python agent/tests/rag/rag_suite.py

# Part 2C: Security Suite (Prompt Injections & Jailbreaks)
.venv\Scripts\python agent/tests/security/security_suite.py

# Part 2D: Hallucination Suite (Out-of-Scope / Refusal checking)
.venv\Scripts\python agent/tests/hallucination/hallucination_suite.py
```

---

## 📐 3. Coding Conventions & Best Practices

When writing or modifying files in this codebase, adhere to the following rules:

### A. 🏷️ Branding & Identity Compliance (Strict Rule)
* The platform has been **100% consolidated under the XBO brand**.

### B. 🖥️ Windows Console Unicode Safety
* Any python scripts designed for console execution that print emojis or non-ASCII characters (`🌞`, `🌙`, `✅`, `❌`, `✗`) **MUST reconfigure standard streams** in their initialization block. This prevents crash loops due to `UnicodeEncodeError` on Windows consoles with CP1252 encoding:
  ```python
  import sys
  if hasattr(sys.stdout, 'reconfigure'):
      sys.stdout.reconfigure(encoding='utf-8')
  if hasattr(sys.stderr, 'reconfigure'):
      sys.stderr.reconfigure(encoding='utf-8')
  ```

### C. 📂 Test Results and Reports
* Do **not** modify report paths.
  * Day Agent report **must** save to `agent/results/day_report.md`.
  * Night Agent report **must** save to `agent/results/night_report.md`.
  * Individual JSON results go to `agent/results/*_results.json`.

### D. 📜 Python / RAG Standards
* Standard import path insert when executing standalone scripts (e.g., `sys.path.insert(0, 'agent')`).
* All RAG context chunking and indexing are handled in `agent/rag.py`. Keep chunk size and overlap parameters harmonized.

---

## ⚠️ 4. Key Gotchas & Friction Points

* **Virtual Environment Execution**: If you run orchestration or test scripts with system python (`python script.py`), they will throw `ModuleNotFoundError: No module named 'sentence_transformers'`. **Always** use the environment interpreter: `.venv\Scripts\python`.
* **Port 8000 Binding**: If Uvicorn fails to start with `[Errno 10048]`, check for running instances. On Windows, locate the process owning the port using:
  `Get-NetTCPConnection -LocalPort 8000` and terminate it.
* **SentenceTransformer Model Load**: The first run of the functional suite will download the `all-MiniLM-L6-v2` model weights (approx. 90MB) to the local cache. Ensure active network access.
* **Brittle Keyword Assertions**: The security and hallucination test suites rely on exact keyword matches. If the model uses alternative language to reject an injection or admit uncertainty, the test might fail despite correct behavior (False Positive Rate is ~15%). Keep this in mind when designing cases in `injection_cases.json` and `hallucination_cases.json`.

---
*Good luck engineering. Keep the XBO support pipeline secure, precise, and highly performant.*
