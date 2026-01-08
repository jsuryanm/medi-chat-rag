from fastapi import FastAPI
from pydantic import BaseModel

from src.helper import build_rag_chain
from src.guard import is_medical_question


app = FastAPI(title="Medical Chat-RAG API")

rag_chain = build_rag_chain()

class Query(BaseModel):
    question: str


@app.post("/ask")
def ask(query: Query):
    if not is_medical_question(query.question):
        return {
            "answer": (
                "I can only answer medical-related questions.\n\n"
                "Please ask about symptoms, diseases, treatments, "
                "medications, or healthcare topics."
            )
        }

    answer = rag_chain.invoke(query.question)
    return {"answer": answer}
