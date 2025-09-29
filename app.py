import streamlit as st
from utils import extract_text_from_pdf, get_similarity, extract_skills
from fpdf import FPDF  # for PDF generation
import base64

# ----------------- PAGE CONFIG -----------------
st.set_page_config(
    page_title="Resume Analyzer",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ----------------- TITLE & HEADER -----------------
st.markdown(
    """
    <h2 style="text-align:center; color:#2E86C1;">
        🚀 AI-Powered Resume Analyzer
    </h2>
    <p style="text-align:center; font-size:16px; color:gray;">
        Upload your resume and a job description to see how well you match!
    </p>
    """,
    unsafe_allow_html=True
)

# ----------------- FILE UPLOADS -----------------
col1, col2 = st.columns(2)

with col1:
    resume_file = st.file_uploader("📄 Upload Resume (PDF)", type=["pdf"])

with col2:
    jd_file = st.file_uploader("📝 Upload Job Description (PDF/TXT)", type=["pdf", "txt"])


# ----------------- MAIN LOGIC -----------------
if resume_file and jd_file:
    # Extract text
    resume_text = extract_text_from_pdf(resume_file)

    if jd_file.type == "text/plain":
        jd_text = jd_file.read().decode("utf-8")
    else:
        jd_text = extract_text_from_pdf(jd_file)

    # Calculate match score
    match_score = get_similarity(resume_text, jd_text)

    # Show Score
    st.subheader("📊 Match Result")
    st.progress(match_score / 100)
    st.success(f"🎯 Your Resume Match Score: {match_score}%")

    # Extract skills
    resume_skills = extract_skills(resume_text)
    jd_skills = extract_skills(jd_text)
    missing_skills = list(set(jd_skills) - set(resume_skills))

    # ----------------- SKILL DISPLAY -----------------
    def display_skills(title, skills, color):
        st.markdown(f"<h4 style='color:{color};'>{title}</h4>", unsafe_allow_html=True)
        if skills:
            st.markdown(
                " ".join(
                    [
                        f"<span style='background-color:{color}; color:white; padding:6px; margin:4px; border-radius:8px; font-size:14px;'>{s}</span>"
                        for s in skills
                    ]
                ),
                unsafe_allow_html=True,
            )
        else:
            st.info("No skills found")

    st.markdown("---")
    colA, colB, colC = st.columns(3)

    with colA:
        display_skills("✅ Skills in Resume", resume_skills, "#27AE60")

    with colB:
        display_skills("📌 Skills in Job Description", jd_skills, "#2980B9")

    with colC:
        display_skills("⚠ Missing Skills", missing_skills, "#E74C3C")

    # ----------------- PDF REPORT GENERATION -----------------
    def generate_pdf(match_score, resume_skills, jd_skills, missing_skills):
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", "B", 16)
        pdf.cell(200, 10, "Resume Analyzer Report", ln=True, align="C")

        pdf.set_font("Arial", size=12)
        pdf.ln(10)
        pdf.cell(200, 10, f"🎯 Match Score: {match_score}%", ln=True)

        pdf.ln(5)
        pdf.set_font("Arial", "B", 12)
        pdf.cell(200, 10, "✅ Skills in Resume:", ln=True)
        pdf.set_font("Arial", size=12)
        pdf.multi_cell(0, 8, ", ".join(resume_skills) if resume_skills else "None")

        pdf.ln(5)
        pdf.set_font("Arial", "B", 12)
        pdf.cell(200, 10, "📌 Skills in Job Description:", ln=True)
        pdf.set_font("Arial", size=12)
        pdf.multi_cell(0, 8, ", ".join(jd_skills) if jd_skills else "None")

        pdf.ln(5)
        pdf.set_font("Arial", "B", 12)
        pdf.cell(200, 10, "⚠ Missing Skills:", ln=True)
        pdf.set_font("Arial", size=12)
        pdf.multi_cell(0, 8, ", ".join(missing_skills) if missing_skills else "None")

        return pdf.output(dest="S").encode("latin-1")

    pdf_bytes = generate_pdf(match_score, resume_skills, jd_skills, missing_skills)

    st.download_button(
        label="⬇ Download Report as PDF",
        data=pdf_bytes,
        file_name="resume_analysis_report.pdf",
        mime="application/pdf",
    )

# ----------------- SIDEBAR INFO -----------------
st.sidebar.title("ℹ️ About This App")
st.sidebar.info(
    """
    This AI-powered tool helps job seekers match their resume 
    with job descriptions using **NLP & Sentence Transformers**.

    - 📄 Upload Resume (PDF)
    - 📝 Upload Job Description
    - 📊 Get a Match Score
    - 🎯 See Missing Skills
    - ⬇ Download Report as PDF

    👨‍💻 Built with **Streamlit**  
    🤖 Powered by **Sentence Transformers & FPDF**
    """
)
