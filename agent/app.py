from fastapi import FastAPI
from pydantic import BaseModel

from rag import retrieve
from prompts import SYSTEM_PROMPT
from llm import ask_claude

app = FastAPI()


class ChatRequest(BaseModel):
    user_id: str
    message: str


@app.post("/chat")
def chat(request: ChatRequest):
    retrieval = retrieve(request.message)

    docs = retrieval["documents"][0]
    metadata = retrieval["metadatas"][0]

    context = "\n".join(docs)

    answer = ask_claude(
        SYSTEM_PROMPT,
        request.message,
        context
    )

    return {
        "answer": answer,
        "retrieved_docs": metadata,
        "context": docs
    }
