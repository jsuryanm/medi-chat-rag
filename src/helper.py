import torch
from typing import List
from langchain_core.documents import Document
from langchain_community.document_loaders import PyPDFLoader, DirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface.embeddings import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from transformers import (
    AutoTokenizer, AutoModelForCausalLM,
    pipeline, BitsAndBytesConfig
)
from langchain_huggingface import HuggingFacePipeline
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

from src.prompt import PROMPT

DATA_PATH = "../data"
CHROMA_PATH = "../research/chroma_db"
MODEL_ID = "mistralai/Mistral-7B-Instruct-v0.2"

def load_pdf_files():
    loader = DirectoryLoader(
        path=DATA_PATH,
        glob="**/*.pdf",
        loader_cls=PyPDFLoader
    )
    return loader.load()


def filter_minimal_docs(docs: List[Document]):
    minimal_docs = []
    for doc in docs:
        minimal_docs.append(
            Document(
                page_content=doc.page_content,
                metadata={"source": doc.metadata.get("source")}
            )
        )
    return minimal_docs

def split_docs(docs):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=20
    )
    return splitter.split_documents(docs)

def get_embeddings():
    return HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2",
        model_kwargs={
            "device": "cuda" if torch.cuda.is_available() else "cpu"
        }
    )

def load_vectorstore(embeddings):
    return Chroma(
        persist_directory=CHROMA_PATH,
        embedding_function=embeddings
    )

def load_llm():
    bnb = BitsAndBytesConfig(
        load_in_4bit=True,
        bnb_4bit_compute_dtype=torch.float16,
        bnb_4bit_quant_type="nf4"
    )

    tokenizer = AutoTokenizer.from_pretrained(MODEL_ID)
    model = AutoModelForCausalLM.from_pretrained(
        MODEL_ID,
        device_map="auto",
        quantization_config=bnb
    )

    pipe = pipeline(
        "text-generation",
        model=model,
        tokenizer=tokenizer,
        max_new_tokens=256,
        temperature=0.2,
        return_full_text=False
    )

    return HuggingFacePipeline(pipeline=pipe)

def build_rag_chain():

    embeddings = get_embeddings()
    vectorstore = load_vectorstore(embeddings)
    retriever = vectorstore.as_retriever(search_kwargs={"k": 3})
    llm = load_llm()

    def format_docs(docs):
        return "\n\n".join(d.page_content for d in docs)

    chain = (
        {
            "context": retriever | format_docs,
            "question": RunnablePassthrough()
        }
        | PROMPT
        | llm
        | StrOutputParser()
    )

    return chain
