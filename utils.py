import fitz  # PyMuPDF
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

# Load model once
model = SentenceTransformer('all-MiniLM-L6-v2')

# Predefined skills list
skills_list = [
    "Python", "SQL", "Machine Learning", "Deep Learning", "NLP",
    "TensorFlow", "PyTorch", "Pandas", "NumPy", "Data Science",
    "Generative AI", "LLMs", "LangChain", "Statistics"
]

# Extract text from PDF using PyMuPDF
def extract_text_from_pdf(pdf_file):
    text = ""
    with fitz.open(stream=pdf_file.read(), filetype="pdf") as doc:
        for page in doc:
            text += page.get_text()
    return text

# Calculate similarity between resume & JD
def get_similarity(resume_text, jd_text):
    embeddings = model.encode([resume_text, jd_text])
    similarity = cosine_similarity([embeddings[0]], [embeddings[1]])[0][0]
    return round(similarity * 100, 2)

# Extract matching skills
def extract_skills(text):
    found_skills = [skill for skill in skills_list if skill.lower() in text.lower()]
    return found_skills
