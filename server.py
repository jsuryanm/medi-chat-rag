from fastapi import FastAPI
from pydantic import BaseModel

from src.helper import build_rag_chain


app = FastAPI(title="Medical Chat-RAG API")

rag_chain = build_rag_chain()

class Query(BaseModel):
    question: str


@app.post("/ask")
def ask(query: Query):
    answer = rag_chain.invoke(query.question)
    return {"answer":answer}