"""
Day Agent — fast pre-merge gate.
Runs ONLY the functional test suite (Part 2A).
Must complete in under 5 minutes.
Exits with code 0 on success, non-zero on failure.

Usage:
    python agent/orchestration/day_agent.py
"""
import subprocess
import sys
import os
import json
import time


SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, "..", ".."))
AGENT_DIR = os.path.join(PROJECT_ROOT, "agent")
RESULTS_DIR = os.path.join(AGENT_DIR, "results")
PYTHON = sys.executable

FUNCTIONAL_SUITE = os.path.join(AGENT_DIR, "tests", "functional", "functional_suite.py")
FUNCTIONAL_RESULTS = os.path.join(RESULTS_DIR, "functional_results.json")

TIMEOUT_SECONDS = 300  # 5 minutes


def main():
    print("=" * 60)
    print("🌞 DAY AGENT — Pre-merge functional gate")
    print("=" * 60)
    print(f"  Time: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"  Suite: {FUNCTIONAL_SUITE}")
    print(f"  Timeout: {TIMEOUT_SECONDS}s")
    print("=" * 60)

    start = time.time()

    # --- Run functional suite ---
    try:
        result = subprocess.run(
            [PYTHON, FUNCTIONAL_SUITE],
            timeout=TIMEOUT_SECONDS,
            capture_output=True,
            text=True,
            cwd=PROJECT_ROOT
        )
    except subprocess.TimeoutExpired:
        print("\n[FATAL] Functional suite TIMED OUT (exceeded 5 minutes).")
        print("Diagnostic: The LLM API may be slow or unresponsive.")
        sys.exit(2)
    except FileNotFoundError:
        print(f"\n[FATAL] Suite script not found: {FUNCTIONAL_SUITE}")
        sys.exit(3)

    elapsed = time.time() - start

    # Print suite stdout/stderr for diagnostics
    if result.stdout:
        print(result.stdout)
    if result.stderr:
        print(result.stderr, file=sys.stderr)

    # --- Check if suite process itself crashed ---
    if result.returncode != 0:
        print(f"\n[FATAL] Functional suite process exited with code {result.returncode}.")
        print("Diagnostic: The suite script crashed. Check output above for tracebacks.")
        sys.exit(1)

    # --- Read and evaluate results ---
    if not os.path.exists(FUNCTIONAL_RESULTS):
        print(f"\n[FATAL] Results file not found: {FUNCTIONAL_RESULTS}")
        print("Diagnostic: Suite ran but did not produce output. Check the suite script.")
        sys.exit(1)

    with open(FUNCTIONAL_RESULTS) as f:
        data = json.load(f)

    pass_rate = data.get("pass_rate", 0)
    total = len(data.get("results", []))
    passed = sum(1 for r in data.get("results", []) if r.get("passed"))
    failed = total - passed

    print(f"\n{'=' * 60}")
    print(f"  RESULTS: {passed}/{total} passed | Pass rate: {pass_rate:.1%}")
    print(f"  Elapsed: {elapsed:.1f}s")
    print(f"{'=' * 60}")

    if pass_rate < 1.0:
        print(f"\n[FAIL] {failed} functional test(s) failed.")
        print("Diagnostic: The agent's answers did not meet the similarity threshold.")
        print("Review the failed cases in the console output above.")

        # Print failed cases for quick diagnosis
        for r in data.get("results", []):
            if not r.get("passed"):
                sim = r.get("similarity", "N/A")
                print(f"  ✗ {r['question'][:80]}  (similarity: {sim})")

        sys.exit(1)

    print("\n[OK] All functional tests passed. Safe to merge.")
    sys.exit(0)


if __name__ == "__main__":
    main()
