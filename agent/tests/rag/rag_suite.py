import json
import os
import requests


SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

TOP_K = 3


with open(os.path.join(SCRIPT_DIR, "rag_cases.json")) as f:
    cases = json.load(f)


results = []


for case in cases:
    try:
        response = requests.post(
            "http://localhost:8000/chat",
            json={
                "user_id": "user_123",
                "message": case["query"]
            },
            proxies={"http": None, "https": None}
        )

        data = response.json()
    except Exception as e:
        print(f"\nFAILED for query: {case['query']}")
        print(f"  Status code: {response.status_code}")
        print(f"  Response text: {response.text[:500]}")
        raise e

    retrieved_docs = [
        d["source"]
        for d in data["retrieved_docs"]
    ]

    relevant_docs = case["relevant_docs"]

    unique_retrieved = set(retrieved_docs)

    relevant_retrieved = len(
        unique_retrieved & set(relevant_docs)
    )

    precision = relevant_retrieved / len(unique_retrieved) if unique_retrieved else 0

    recall = relevant_retrieved / len(relevant_docs)

    passed = precision >= 0.7 and recall >= 0.7

    print(f"\nQuery: {case['query']}")
    print(f"  Expected docs: {relevant_docs}")
    print(f"  Retrieved docs: {retrieved_docs}")
    print(f"  Precision@{TOP_K}: {precision:.2f} | Recall@{TOP_K}: {recall:.2f} | Passed: {passed}")

    results.append({
        "query": case["query"],
        "precision@k": precision,
        "recall@k": recall,
        "passed": bool(passed)
    })


pass_rate = sum(r["passed"] for r in results) / len(results)

output = {
    "suite": "rag",
    "pass_rate": pass_rate,
    "results": results
}


results_dir = os.path.join(SCRIPT_DIR, "..", "..", "results")
os.makedirs(results_dir, exist_ok=True)
with open(os.path.join(results_dir, "rag_results.json"), "w") as f:
    json.dump(output, f, indent=2)

print(f"\n{'='*50}")
print(f"RAG Suite Pass Rate: {pass_rate:.1%}")
print(f"Results saved to: {os.path.abspath(os.path.join(results_dir, 'rag_results.json'))}")
