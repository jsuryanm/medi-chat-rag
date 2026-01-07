import streamlit as st
import requests

API_URL = "http://localhost:8000/ask"

st.set_page_config(page_title="Medi-Chat RAG", layout="centered")

st.title("🩺 Medi-Chat RAG")
st.write("Ask questions from your medical PDFs")

question = st.text_input("Enter your question")

if st.button("Ask") and question:
    with st.spinner("Thinking..."):
        response = requests.post(
            API_URL,
            json={"question": question}
        )
        st.success(response.json()["answer"])
