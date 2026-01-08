MEDICAL_KEYWORDS = [
    "symptom", "disease", "treatment", "medicine", "drug",
    "diagnosis", "pain", "fever", "infection", "cancer",
    "diabetes", "blood", "heart", "doctor", "health",
    "therapy", "dose", "side effect", "surgery"
]

def is_medical_question(question: str) -> bool:
    q = question.lower()
    return any(keyword in q for keyword in MEDICAL_KEYWORDS)
