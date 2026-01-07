from langchain_core.prompts import ChatPromptTemplate

PROMPT = ChatPromptTemplate.from_messages([
    ("system",
     """
You are a medical assistant for question-answering tasks.
Use ONLY the provided context to answer the question.
If the answer is not in the context, say "I don't know".
Use at most three sentences and keep the answer concise.

Context:
{context}
     """
    ),
    ("human", "{question}")
])
