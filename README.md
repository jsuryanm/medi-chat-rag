#  Medical RAG Chatbot

**Medi-Chat RAG** is an **educational medical question-answering chatbot** built using **Retrieval-Augmented Generation (RAG)**.
It allows users to ask medical-related questions and receive answers grounded in uploaded PDF documents.

⚠️ **Important Disclaimer**
This project is for **educational and research purposes only**.
It **does NOT provide medical advice**.
Always consult a **qualified doctor or healthcare professional** for diagnosis and treatment decisions.

---

##  Features

*  Ingests **medical PDF documents**
*  Semantic search using **ChromaDB**
*  RAG pipeline with **LangChain**
*  Local LLM inference using **Mistral-7B (4-bit quantized)**
*  Backend API with **FastAPI**
*  Chat-based frontend using **Streamlit**
*  GPU acceleration (CUDA supported)

---

## Project Structure

```
medi-chat-rag/
│
├── src/
│   ├── __init__.py
│   ├── helper.py        # RAG pipeline logic
│   └── prompt.py        # Prompt template with disclaimer
│   └── guard.py                 
│
├── research/
│   ├── chroma_db/       # Persistent Chroma vector store
│   └── trials.ipynb     # Experiments & notebooks
│
├── data/                # Medical PDF documents
│   ├── Medical_book.pdf      
│
├── app.py               # Streamlit frontend
├── server.py            # FastAPI backend
├── requirements.txt
├── setup.py
├── .env
└── README.md
```

---

## RAG Architecture

1. **PDF Loading** – Medical PDFs are loaded from the `data/` folder
2. **Chunking** – Documents are split into overlapping chunks
3. **Embeddings** – Generated using `sentence-transformers/all-MiniLM-L6-v2`
4. **Vector Store** – Stored in **ChromaDB**
5. **Retriever** – Fetches top-k relevant chunks
6. **LLM** – Mistral-7B-Instruct (4-bit quantized)
7. **Prompt** – Constrained, context-only medical QA
8. **Response** – Short, safe, educational answers

---

##  Installation

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/jsuryanm/medi-chat-rag.git
cd medi-chat-rag
```

### 2️⃣ Create Virtual Environment (Recommended)

```bash
conda create --name myenv python=3.11
conda activate myenv
```

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

>  **Note**
> CUDA-enabled PyTorch is configured for **CUDA 12.8**.
> Make sure your GPU and drivers support this.

---

## Preparing the Vector Database

1. Place your medical PDFs inside the `data/` folder
2. Run the backend once to build/load the Chroma vector store:

```bash
python server.py
```

The vector database will be persisted in:

```text
research/chroma_db/
```

---

## Running the Application

### Start FastAPI Backend

```bash
uvicorn server:app --reload
```

API runs at:

```
http://localhost:8000
```

### Start Streamlit Frontend

```bash
streamlit run app.py
```

App runs at:

```
http://localhost:8501
```

---

##  Example Usage

* Ask questions like:

  * *What are the symptoms of diabetes?*
  * *What is hypertension?*
* Answers are **strictly based on the uploaded PDFs**
* If questions are not relevant to medical context it will instruct user to ask medical questions:

  > *"Please ask questions about healtcare topics,medications,...."*

---

##  Safety & Disclaimer

* Uses **context-only answering**
* Limits answers to **3 concise sentences**
* Includes **explicit medical disclaimer**
* Encourages consultation with healthcare professionals

---

##  Tech Stack

* **Python**
* **FastAPI**
* **Streamlit**
* **LangChain**
* **ChromaDB**
* **HuggingFace Transformers**
* **Sentence Transformers**
* **PyTorch (CUDA)**

---

##  Future Improvements

* Authentication & user sessions
* Improvise by using an agentic rag
* Source citation highlighting
* Multi-document collections
* Deployment with Docker
