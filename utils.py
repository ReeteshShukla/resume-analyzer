import pdfplumber
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

# Load the embedding model once
model = SentenceTransformer('all-MiniLM-L6-v2')

skills_list = [
    "Python", "SQL", "Machine Learning", "Deep Learning", "NLP",
    "TensorFlow", "PyTorch", "Pandas", "NumPy", "Data Science",
    "Generative AI", "LLMs", "LangChain", "Statistics"
]

def extract_text_from_pdf(pdf_file):
    text = ""
    with pdfplumber.open(pdf_file) as pdf:
        for page in pdf.pages:
            text += page.extract_text() + "\n"
    return text

def get_similarity(resume_text, jd_text):
    embeddings = model.encode([resume_text, jd_text])
    similarity = cosine_similarity([embeddings[0]], [embeddings[1]])[0][0]
    return round(similarity * 100, 2)

def extract_skills(text):
    found_skills = [skill for skill in skills_list if skill.lower() in text.lower()]
    return found_skills
