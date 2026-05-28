import json
import requests


TOP_K = 3


with open("tests/rag/rag_cases.json") as f:
    cases = json.load(f)


results = []


for case in cases:
    response = requests.post(
        "http://localhost:8000/chat",
        json={
            "user_id": "user_123",
            "message": case["query"]
        }
    )

    data = response.json()

    retrieved_docs = [
        d["source"]
        for d in data["retrieved_docs"]
    ]

    relevant_docs = case["relevant_docs"]

    relevant_retrieved = len(
        set(retrieved_docs) & set(relevant_docs)
    )

    precision = relevant_retrieved / TOP_K

    recall = relevant_retrieved / len(relevant_docs)

    results.append({
        "query": case["query"],
        "precision@k": precision,
        "recall@k": recall,
        "passed": precision >= 0.7 and recall >= 0.7
    })


output = {
    "suite": "rag",
    "results": results
}


with open("results/rag_results.json", "w") as f:
    json.dump(output, f, indent=2)
