import streamlit as st
import requests

API_URL = "http://localhost:8000/ask"

st.set_page_config(
    page_title="Medi-Chat RAG",
    page_icon="🩺",
    layout="centered"
)

st.title("🩺 Medical RAG Chatbot")

st.warning(
    "⚠️ **Disclaimer**: This application is for educational purposes only. "
    "It does NOT provide medical advice. "
    "Please consult a qualified doctor or healthcare professional."
)

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

user_input = st.chat_input("Ask a medical question")

if user_input:
    # Store & display user message
    st.session_state.messages.append(
        {"role": "user", "content": user_input}
    )
    with st.chat_message("user"):
        st.markdown(user_input)

    # Call FastAPI backend
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = requests.post(
                API_URL,
                json={"question": user_input}
            )
            answer = response.json()["answer"]
            st.markdown(answer)

    # Store assistant message
    st.session_state.messages.append(
        {"role": "assistant", "content": answer}
    )
