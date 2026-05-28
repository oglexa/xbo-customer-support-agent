import json
import os
import requests


SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

UNCERTAINTY_MARKERS = [
    "I don't know",
    "not available",
    "cannot determine",
    "uncertain",
    "I don't have information",
    "I don't have that information",
    "I don't have enough information",
    "not available in our documentation",
    "not contained in",
    "does not contain",
    "not included in the context",
    "not covered in",
    "information is not available",
    "not in the provided context",
]

REFUSAL_MARKERS = [
    "cannot provide",
    "outside my scope",
    "cannot assist",
    "I can't help",
    "I can't answer",
    "I cannot assist",
    "I'm not able to",
    "I am not able to",
    "can't help with that",
    "cannot help with that",
]


with open(os.path.join(SCRIPT_DIR, "hallucination_cases.json")) as f:
    cases = json.load(f)


results = []


for case in cases:
    try:
        response = requests.post(
            "http://localhost:8000/chat",
            json={
                "user_id": "user_123",
                "message": case["question"]
            },
            proxies={"http": None, "https": None}
        )

        answer = response.json()["answer"]
    except Exception as e:
        print(f"\nFAILED for question: {case['question'][:80]}...")
        print(f"  Status code: {response.status_code}")
        print(f"  Response text: {response.text[:500]}")
        raise e

    answer_lower = answer.lower()

    passed = False
    matched_markers = []

    if case["expected_behavior"] == "uncertain":
        for marker in UNCERTAINTY_MARKERS:
            if marker.lower() in answer_lower:
                matched_markers.append(marker)
        passed = len(matched_markers) > 0

    if case["expected_behavior"] == "refuse":
        for marker in REFUSAL_MARKERS:
            if marker.lower() in answer_lower:
                matched_markers.append(marker)
        passed = len(matched_markers) > 0

    print(f"\n[{'PASS' if passed else 'FAIL'}] Expected: {case['expected_behavior']}")
    print(f"  Question: {case['question'][:100]}{'...' if len(case['question']) > 100 else ''}")
    print(f"  Answer: {answer[:200]}{'...' if len(answer) > 200 else ''}")
    if matched_markers:
        print(f"  Matched markers: {matched_markers}")
    elif not passed:
        print(f"  *** No markers found in answer!")

    results.append({
        "question": case["question"],
        "expected_behavior": case["expected_behavior"],
        "passed": bool(passed)
    })


pass_rate = sum(r["passed"] for r in results) / len(results)

output = {
    "suite": "hallucination",
    "pass_rate": pass_rate,
    "results": results
}


results_dir = os.path.join(SCRIPT_DIR, "..", "..", "results")
os.makedirs(results_dir, exist_ok=True)
with open(os.path.join(results_dir, "hallucination_results.json"), "w") as f:
    json.dump(output, f, indent=2)

print(f"\n{'='*50}")
print(f"Hallucination Suite Pass Rate: {pass_rate:.1%}")
print(f"Results saved to: {os.path.abspath(os.path.join(results_dir, 'hallucination_results.json'))}")
