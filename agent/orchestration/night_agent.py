"""
Night Agent — full unattended test run.
Runs ALL test suites: functional (2A), RAG (2B), security (2C), hallucination (2D).

Critical behavior — skip and continue:
  - Individual test failures inside a suite are NORMAL and are captured in the
    suite's own JSON output.
  - If an entire suite hits an UNRECOVERABLE error (API unreachable, dependency
    crash, timeout, import error, etc.), the Night Agent SKIPS that suite and
    continues with the remaining suites.
  - It NEVER halts the entire run, NEVER waits for human input, and NEVER
    retries indefinitely.

Output:
  - Per-suite JSON results in agent/results/
  - A structured morning report (Markdown) saved to agent/results/morning_report.md

Usage:
    python agent/orchestration/night_agent.py
"""
import subprocess
import sys
import os
import json
import time
from datetime import datetime


SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, "..", ".."))
AGENT_DIR = os.path.join(PROJECT_ROOT, "agent")
RESULTS_DIR = os.path.join(AGENT_DIR, "results")
PYTHON = sys.executable

SUITE_TIMEOUT = 300  # 5 minutes per suite

SUITES = [
    {
        "name": "functional",
        "label": "Part 2A — Functional Tests",
        "script": os.path.join(AGENT_DIR, "tests", "functional", "functional_suite.py"),
        "results_file": "functional_results.json",
    },
    {
        "name": "rag",
        "label": "Part 2B — RAG Retrieval Tests",
        "script": os.path.join(AGENT_DIR, "tests", "rag", "rag_suite.py"),
        "results_file": "rag_results.json",
    },
    {
        "name": "security",
        "label": "Part 2C — Security / Injection Tests",
        "script": os.path.join(AGENT_DIR, "tests", "security", "security_suite.py"),
        "results_file": "security_results.json",
    },
    {
        "name": "hallucination",
        "label": "Part 2D — Hallucination Tests",
        "script": os.path.join(AGENT_DIR, "tests", "hallucination", "hallucination_suite.py"),
        "results_file": "hallucination_results.json",
    },
]


def run_suite(suite):
    """
    Run a single test suite as a subprocess with a timeout.

    Returns a dict with:
      - status: "completed" | "skipped"
      - reason: (only if skipped) human-readable explanation
      - results: (only if completed) parsed JSON from the suite's results file
      - elapsed: runtime in seconds
      - stdout / stderr: captured output
    """
    script = suite["script"]
    results_path = os.path.join(RESULTS_DIR, suite["results_file"])

    start = time.time()

    # --- Execute the suite subprocess ---
    try:
        proc = subprocess.run(
            [PYTHON, script],
            timeout=SUITE_TIMEOUT,
            capture_output=True,
            text=True,
            cwd=PROJECT_ROOT
        )
    except subprocess.TimeoutExpired:
        return {
            "status": "skipped",
            "reason": f"Suite timed out after {SUITE_TIMEOUT}s — possible API hang or infinite loop.",
            "elapsed": time.time() - start,
            "stdout": "",
            "stderr": "",
        }
    except FileNotFoundError:
        return {
            "status": "skipped",
            "reason": f"Suite script not found: {script}",
            "elapsed": time.time() - start,
            "stdout": "",
            "stderr": "",
        }
    except Exception as e:
        return {
            "status": "skipped",
            "reason": f"Unexpected error launching suite: {type(e).__name__}: {e}",
            "elapsed": time.time() - start,
            "stdout": "",
            "stderr": "",
        }

    elapsed = time.time() - start

    # --- Suite process crashed ---
    if proc.returncode != 0:
        return {
            "status": "skipped",
            "reason": f"Suite process exited with code {proc.returncode}. Likely a crash (import error, API unreachable, etc.).",
            "elapsed": elapsed,
            "stdout": proc.stdout,
            "stderr": proc.stderr,
        }

    # --- Read suite results ---
    if not os.path.exists(results_path):
        return {
            "status": "skipped",
            "reason": f"Suite ran but did not produce results file: {suite['results_file']}",
            "elapsed": elapsed,
            "stdout": proc.stdout,
            "stderr": proc.stderr,
        }

    try:
        with open(results_path) as f:
            results_data = json.load(f)
    except (json.JSONDecodeError, IOError) as e:
        return {
            "status": "skipped",
            "reason": f"Results file is corrupt or unreadable: {e}",
            "elapsed": elapsed,
            "stdout": proc.stdout,
            "stderr": proc.stderr,
        }

    return {
        "status": "completed",
        "results": results_data,
        "elapsed": elapsed,
        "stdout": proc.stdout,
        "stderr": proc.stderr,
    }


def generate_report(suite_outcomes, total_elapsed):
    """Generate a structured Markdown morning report."""

    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    lines = []
    lines.append("# 🌙 Night Agent — Morning Report")
    lines.append("")
    lines.append(f"**Generated:** {now}  ")
    lines.append(f"**Total runtime:** {total_elapsed:.1f}s  ")
    lines.append("")

    # --- Summary table ---
    lines.append("## Summary")
    lines.append("")
    lines.append("| Suite | Status | Pass Rate | Passed | Failed | Time |")
    lines.append("|-------|--------|-----------|--------|--------|------|")

    for entry in suite_outcomes:
        suite = entry["suite"]
        outcome = entry["outcome"]
        status = outcome["status"]
        elapsed = f"{outcome['elapsed']:.1f}s"

        if status == "completed":
            results = outcome["results"]
            all_results = results.get("results", [])
            total = len(all_results)
            passed = sum(1 for r in all_results if r.get("passed"))
            failed = total - passed
            pass_rate = results.get("pass_rate", passed / total if total > 0 else 0)
            status_emoji = "✅ Completed" if failed == 0 else "⚠️ Completed"
            lines.append(f"| {suite['label']} | {status_emoji} | {pass_rate:.1%} | {passed} | {failed} | {elapsed} |")
        else:
            lines.append(f"| {suite['label']} | ⏭️ Skipped | — | — | — | {elapsed} |")

    lines.append("")

    # --- Detailed results per suite ---
    for entry in suite_outcomes:
        suite = entry["suite"]
        outcome = entry["outcome"]
        status = outcome["status"]

        lines.append(f"## {suite['label']}")
        lines.append("")

        if status == "skipped":
            lines.append(f"**Status:** ⏭️ SKIPPED  ")
            lines.append(f"**Reason:** {outcome['reason']}  ")
            # Include stderr snippet if available
            stderr = outcome.get("stderr", "").strip()
            if stderr:
                lines.append("")
                lines.append("<details><summary>Error output</summary>")
                lines.append("")
                lines.append("```")
                lines.append(stderr[:2000])
                lines.append("```")
                lines.append("</details>")
            lines.append("")
            continue

        results = outcome["results"]
        all_results = results.get("results", [])
        total = len(all_results)
        passed = sum(1 for r in all_results if r.get("passed"))
        failed = total - passed

        lines.append(f"**Status:** {'✅ ALL PASSED' if failed == 0 else f'⚠️ {failed}/{total} FAILED'}  ")
        lines.append("")

        # List individual results
        for r in all_results:
            p = r.get("passed", False)
            icon = "✅" if p else "❌"

            # Different suites have different key names for the question/query
            label = r.get("question") or r.get("query") or r.get("attack_prompt") or "N/A"
            label = label[:100] + ("..." if len(label) > 100 else "")

            extra = ""
            if "similarity" in r:
                extra = f" (similarity: {r['similarity']:.4f})"
            elif "precision@k" in r:
                extra = f" (P@k: {r['precision@k']:.2f}, R@k: {r['recall@k']:.2f})"
            elif "category" in r:
                extra = f" [{r['category']}]"
            elif "expected_behavior" in r:
                extra = f" [expected: {r['expected_behavior']}]"

            lines.append(f"- {icon} {label}{extra}")

        lines.append("")

    # --- Footer ---
    lines.append("---")
    lines.append(f"*Report generated automatically by Night Agent at {now}*")

    return "\n".join(lines)


def main():
    print("=" * 60)
    print("  🌙 NIGHT AGENT — Full unattended test run")
    print("=" * 60)
    print(f"  Time: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"  Suites: {len(SUITES)}")
    print(f"  Timeout per suite: {SUITE_TIMEOUT}s")
    print("=" * 60)

    os.makedirs(RESULTS_DIR, exist_ok=True)

    total_start = time.time()
    suite_outcomes = []

    for suite in SUITES:
        print(f"\n{'─' * 60}")
        print(f"  Running: {suite['label']}...")
        print(f"{'─' * 60}")

        outcome = run_suite(suite)
        suite_outcomes.append({"suite": suite, "outcome": outcome})

        if outcome["status"] == "skipped":
            print(f"  ⏭️  SKIPPED: {outcome['reason']}")
            if outcome.get("stderr"):
                print(f"  stderr (last 500 chars):\n{outcome['stderr'][-500:]}")
        else:
            results = outcome["results"]
            all_results = results.get("results", [])
            total = len(all_results)
            passed_count = sum(1 for r in all_results if r.get("passed"))
            print(f"  ✅ Completed: {passed_count}/{total} passed ({outcome['elapsed']:.1f}s)")

        # Print suite stdout for visibility
        if outcome.get("stdout"):
            print(outcome["stdout"])

    total_elapsed = time.time() - total_start

    # --- Generate morning report ---
    report_md = generate_report(suite_outcomes, total_elapsed)
    report_path = os.path.join(RESULTS_DIR, "morning_report.md")
    with open(report_path, "w", encoding="utf-8") as f:
        f.write(report_md)

    # --- Final summary ---
    completed = sum(1 for e in suite_outcomes if e["outcome"]["status"] == "completed")
    skipped = sum(1 for e in suite_outcomes if e["outcome"]["status"] == "skipped")

    print(f"\n{'=' * 60}")
    print(f"  🌙 NIGHT AGENT COMPLETE")
    print(f"  Total time: {total_elapsed:.1f}s")
    print(f"  Completed: {completed}/{len(SUITES)} | Skipped: {skipped}/{len(SUITES)}")
    print(f"  Report saved: {report_path}")
    print(f"{'=' * 60}")


if __name__ == "__main__":
    main()
