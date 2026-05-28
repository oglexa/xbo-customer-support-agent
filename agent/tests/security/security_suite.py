import json
import os
import requests


SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))


with open(os.path.join(SCRIPT_DIR, "injection_cases.json")) as f:
    attacks = json.load(f)


results = []


for attack in attacks:
    try:
        response = requests.post(
            "http://localhost:8000/chat",
            json={
                "user_id": "user_123",
                "message": attack["prompt"]
            },
            proxies={"http": None, "https": None}
        )

        answer = response.json()["answer"]
    except Exception as e:
        print(f"\nFAILED for prompt: {attack['prompt'][:80]}...")
        print(f"  Status code: {response.status_code}")
        print(f"  Response text: {response.text[:500]}")
        raise e

    attack_succeeded = False
    triggered = []

    for forbidden in attack["forbidden_strings"]:
        if forbidden.lower() in answer.lower():
            attack_succeeded = True
            triggered.append(forbidden)

    passed = not attack_succeeded

    print(f"\n[{'PASS' if passed else 'FAIL'}] Category: {attack['category']}")
    print(f"  Prompt: {attack['prompt'][:100]}{'...' if len(attack['prompt']) > 100 else ''}")
    print(f"  Answer: {answer[:200]}{'...' if len(answer) > 200 else ''}")
    if triggered:
        print(f"  *** Forbidden strings found: {triggered}")

    results.append({
        "category": attack["category"],
        "attack_prompt": attack["prompt"],
        "attack_succeeded": bool(attack_succeeded),
        "passed": bool(passed)
    })


pass_rate = sum(r["passed"] for r in results) / len(results)

output = {
    "suite": "security",
    "pass_rate": pass_rate,
    "results": results
}


results_dir = os.path.join(SCRIPT_DIR, "..", "..", "results")
os.makedirs(results_dir, exist_ok=True)
with open(os.path.join(results_dir, "security_results.json"), "w") as f:
    json.dump(output, f, indent=2)

print(f"\n{'='*50}")
print(f"Security Suite Pass Rate: {pass_rate:.1%}")
print(f"Results saved to: {os.path.abspath(os.path.join(results_dir, 'security_results.json'))}")
