# XBO Customer Support Agent — QA Orchestration

## Overview

This project implements a **Day Agent / Night Agent** workflow for quality assurance of the XBO Customer Support Agent.

## Quick Start

### Prerequisites

```bash
# Activate the virtual environment
.venv\Scripts\Activate.ps1        # Windows PowerShell
# source .venv/bin/activate       # Linux/macOS

# Ensure the server is running
uvicorn app:app --app-dir agent --port 8000 --reload
```

### Build the RAG knowledge base index (first time only)

```bash
python -c "import sys; sys.path.insert(0, 'agent'); import rag; rag.build_index(); print(f'Indexed {rag.collection.count()} chunks')"
```

---

## Day Agent (Pre-merge gate)

**Runs:** Part 2A (Functional tests) only  
**Timeout:** 5 minutes  
**Purpose:** Fast pre-merge gate. If functional tests fail, exits with a non-zero code and a clear diagnostic.

```bash
python agent/orchestration/day_agent.py
```

**Exit codes:**
| Code | Meaning |
|------|---------|
| `0`  | All functional tests passed — safe to merge |
| `1`  | Functional tests failed or results file missing |
| `2`  | Suite timed out (exceeded 5 minutes) |
| `3`  | Suite script not found |

### Usage as a git pre-push hook

```bash
# .git/hooks/pre-push
#!/bin/sh
python agent/orchestration/day_agent.py
```

---

## Night Agent (Unattended overnight run)

**Runs:** All 4 suites — Functional (2A), RAG (2B), Security (2C), Hallucination (2D)  
**Timeout:** 5 minutes per suite  
**Purpose:** Full unattended test run with a structured morning report.

```bash
python agent/orchestration/night_agent.py
```

### Skip-and-continue behavior

> **Critical design rule:** The Night Agent must **never halt the entire run**, **never wait for human input**, and **never retry indefinitely**.

Each suite runs in an isolated subprocess with a timeout. If a suite encounters an **unrecoverable error** — such as:

- The LLM API is unreachable (connection refused, timeout)
- A Python dependency crashes (ImportError, segfault)
- The suite exceeds its 5-minute timeout (possible infinite loop or API hang)
- The results file is missing or corrupt after execution

...then the Night Agent **SKIPs** that suite and **continues** with the remaining suites. The skip reason is recorded in the output and included in the morning report.

Individual test failures inside a suite are **normal** and do not trigger a skip — they are captured in the suite's own JSON output with `"passed": false`.

### Output

| File | Description |
|------|-------------|
| `agent/results/morning_report.md` | Structured Markdown report for morning standup |
| `agent/results/functional_results.json` | Functional suite detailed results |
| `agent/results/rag_results.json` | RAG suite detailed results |
| `agent/results/security_results.json` | Security suite detailed results |
| `agent/results/hallucination_results.json` | Hallucination suite detailed results |

---

## Test Suites

| Suite | Script | What it tests |
|-------|--------|---------------|
| **Functional (2A)** | `agent/tests/functional/functional_suite.py` | Semantic similarity of agent answers vs expected answers (threshold: 0.80) |
| **RAG (2B)** | `agent/tests/rag/rag_suite.py` | Precision@3 and Recall@3 of retrieved knowledge base documents |
| **Security (2C)** | `agent/tests/security/security_suite.py` | Prompt injection, jailbreak, PII leakage, privilege escalation attacks |
| **Hallucination (2D)** | `agent/tests/hallucination/hallucination_suite.py` | Agent correctly refuses or expresses uncertainty on out-of-scope questions |

---

## Environment Variables

Configured via `.env` file in the project root:

```env
ANTHROPIC_API_KEY=sk-your-key-here
ANTHROPIC_BASE_URL=http://localhost:20128
ANTHROPIC_MODEL=kr/claude-haiku-4.5
```
