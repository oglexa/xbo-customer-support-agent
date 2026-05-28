from pathlib import Path
from sentence_transformers import SentenceTransformer
import chromadb


SCRIPT_DIR = Path(__file__).parent


model = SentenceTransformer("all-MiniLM-L6-v2")

client = chromadb.PersistentClient(path=str(SCRIPT_DIR / "chroma_db"))
collection = client.get_or_create_collection("xbo_docs")


def chunk_text(text, chunk_size=800, overlap=200):
    chunks = []

    start = 0

    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start += chunk_size - overlap

    return chunks


def build_index():
    kb_path = SCRIPT_DIR / "kb"

    global collection
    try:
        client.delete_collection("xbo_docs")
    except Exception:
        pass
    collection = client.get_or_create_collection("xbo_docs")

    counter = 0

    for file in kb_path.glob("*.md"):
        text = file.read_text(encoding="utf-8")

        chunks = chunk_text(text)

        for chunk in chunks:
            embedding = model.encode(chunk).tolist()

            collection.add(
                ids=[str(counter)],
                documents=[chunk],
                embeddings=[embedding],
                metadatas=[{"source": file.name}]
            )

            counter += 1

    return counter


def retrieve(query, top_k=3):
    """
    Retrieve top_k documents, deduplicated by source file.
    Internally fetches more chunks, then keeps only the best chunk per unique source.
    """
    embedding = model.encode(query).tolist()

    # Fetch extra chunks to ensure we get enough unique sources
    fetch_k = top_k * 4

    results = collection.query(
        query_embeddings=[embedding],
        n_results=min(fetch_k, collection.count())
    )

    if not results["documents"][0]:
        return results

    # Deduplicate by source: keep only the first (best) chunk per source file
    seen_sources = set()
    dedup_indices = []

    for i, meta in enumerate(results["metadatas"][0]):
        source = meta["source"]
        if source not in seen_sources:
            seen_sources.add(source)
            dedup_indices.append(i)
        if len(dedup_indices) >= top_k:
            break

    # Rebuild results with deduplicated entries
    dedup_results = {
        "documents": [[results["documents"][0][i] for i in dedup_indices]],
        "metadatas": [[results["metadatas"][0][i] for i in dedup_indices]],
        "distances": [[results["distances"][0][i] for i in dedup_indices]] if results.get("distances") else None,
    }

    return dedup_results
