import streamlit as st
import pandas as pd
from utils import extract_text_from_pdf, clean_text, extract_experience
from model import compute_similarity, get_top_keywords, skill_match_score, detect_role

st.set_page_config(page_title="AI Resume Screener", layout="wide")

# ---------- CUSTOM STYLING ----------
st.markdown("""
<style>
.main {background-color: #f5f7fb;}
h1 {color: #1f4e79;}
.card {
    background-color: white;
    padding: 20px;
    border-radius: 12px;
    box-shadow: 0px 4px 12px rgba(0,0,0,0.1);
    margin-bottom: 20px;
}
.score {
    font-size: 20px;
    font-weight: bold;
    color: #2e7d32;
}
</style>
""", unsafe_allow_html=True)

st.title("🤖 AI Resume Screening System")
st.write("Smart candidate analysis using NLP + AI")

# ---------- INPUT SECTION ----------
col1, col2 = st.columns(2)

with col1:
    jd_text = st.text_area("📌 Paste Job Description", height=200)

with col2:
    uploaded_files = st.file_uploader("📂 Upload Resume PDFs", type=["pdf"], accept_multiple_files=True)

# ---------- PROCESS BUTTON ----------
if st.button("🚀 Screen Candidates"):
    if not jd_text or not uploaded_files:
        st.warning("Please provide job description and resumes.")
    else:
        with st.spinner("Analyzing resumes using AI..."):
            clean_jd = clean_text(jd_text)

            resumes, names, full_texts = [], [], []

            for file in uploaded_files:
                text = extract_text_from_pdf(file)
                resumes.append(clean_text(text))
                full_texts.append(text)
                names.append(file.name)

            scores = compute_similarity(clean_jd, resumes)

        st.success("Analysis Complete!")

        results = []

        # ---------- RESULTS CARDS ----------
        for name, score, resume_text, raw_text in zip(names, scores, resumes, full_texts):

            skill_score, matched_skills = skill_match_score(clean_jd, resume_text)
            missing = get_top_keywords(clean_jd, resume_text)
            exp = extract_experience(raw_text)
            role = detect_role(resume_text)

            st.markdown(f"""
            <div class="card">
                <h3>{name}</h3>
                <p class="score">Match Score: {round(score*100,2)}%</p>
                <p>🧠 Skill Match: {round(skill_score*100,2)}%</p>
                <p>💼 Experience: {exp} years</p>
                <p>🎯 Role Type: {role}</p>
                <p>✅ Matched Skills: {", ".join(matched_skills)}</p>
                <p>❌ Missing Skills: {", ".join(missing)}</p>
            </div>
            """, unsafe_allow_html=True)

            results.append((name, score, skill_score, exp, role))

        # ---------- DASHBOARD ----------
        df = pd.DataFrame(results, columns=["Name", "Match Score", "Skill Score", "Experience", "Role"])

        st.subheader("📊 Candidate Score Overview")
        st.bar_chart(df.set_index("Name")["Match Score"])

        st.download_button("⬇ Download Results CSV",
                           df.to_csv(index=False),
                           "screening_results.csv")
