import json
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
import requests

from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

model = SentenceTransformer("all-MiniLM-L6-v2")

THRESHOLD = 0.80


with open(os.path.join(SCRIPT_DIR, "cases.json")) as f:
    test_cases = json.load(f)


results = []


for case in test_cases:
    response = requests.post(
        "http://localhost:8000/chat",
        json={
            "user_id": "user_123",
            "message": case["question"]
        },
        proxies={"http": None, "https": None}
    )

    try:
        actual_answer = response.json()["answer"]
    except Exception as e:
        print(f"FAILED TO DECODE JSON: Status code = {response.status_code}")
        print(f"Headers: {response.headers}")
        print(f"Text content: {response.text[:1000]}")
        raise e

    expected_embedding = model.encode(
        case["expected_answer"]
    ).reshape(1, -1)

    actual_embedding = model.encode(
        actual_answer
    ).reshape(1, -1)

    similarity = cosine_similarity(
        expected_embedding,
        actual_embedding
    )[0][0]

    passed = similarity >= THRESHOLD

    print(f"\nQuestion: {case['question']}")
    print(f"Expected: {case['expected_answer']}")
    print(f"Actual:   {actual_answer}")
    print(f"Similarity: {similarity:.4f} | Passed: {passed}")

    results.append({
        "question": case["question"],
        "similarity": float(similarity),
        "passed": bool(passed)
    })


pass_rate = sum(r["passed"] for r in results) / len(results)

output = {
    "suite": "functional",
    "pass_rate": pass_rate,
    "results": results
}


results_dir = os.path.join(SCRIPT_DIR, "..", "..", "results")
os.makedirs(results_dir, exist_ok=True)
with open(os.path.join(results_dir, "functional_results.json"), "w") as f:
    json.dump(output, f, indent=2)
