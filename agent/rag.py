from pathlib import Path
from sentence_transformers import SentenceTransformer
import chromadb


SCRIPT_DIR = Path(__file__).parent


model = SentenceTransformer("all-MiniLM-L6-v2")

client = chromadb.PersistentClient(path=str(SCRIPT_DIR / "chroma_db"))
collection = client.get_or_create_collection("xbo_docs")


def chunk_text(text, chunk_size=400, overlap=50):
    chunks = []

    start = 0

    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start += chunk_size - overlap

    return chunks


def build_index():
    kb_path = SCRIPT_DIR / "kb"

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


def retrieve(query, top_k=3):
    embedding = model.encode(query).tolist()

    results = collection.query(
        query_embeddings=[embedding],
        n_results=top_k
    )

    return results
