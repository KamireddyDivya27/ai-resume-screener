import streamlit as st
import pandas as pd
from utils import extract_text_from_pdf, clean_text, extract_experience, generate_pdf_report
from model import compute_similarity, get_top_keywords, skill_match_score, detect_role

st.set_page_config(page_title="AI Resume Screener", layout="wide")

st.title("🤖 AI Resume Screening System")

jd_text = st.text_area("📌 Paste Job Description")
uploaded_files = st.file_uploader("📂 Upload Resume PDFs", type=["pdf"], accept_multiple_files=True)

if st.button("🚀 Screen Candidates"):
    if not jd_text or not uploaded_files:
        st.warning("Please provide job description and resumes.")
    else:
        with st.spinner("Analyzing resumes..."):
            clean_jd = clean_text(jd_text)
            resumes, names, full_texts = [], [], []

            for file in uploaded_files:
                text = extract_text_from_pdf(file)
                resumes.append(clean_text(text))
                full_texts.append(text)
                names.append(file.name)

            scores = compute_similarity(clean_jd, resumes)

        results = []

        for name, score, resume_text, raw_text in zip(names, scores, resumes, full_texts):
            st.markdown(f"## {name}")
            st.write(f"📊 Match Score: {round(score*100,2)}%")

            skill_score, matched_skills = skill_match_score(clean_jd, resume_text)
            st.write(f"🧠 Skill Match: {round(skill_score*100,2)}%")
            st.write("✅ Matched Skills:", ", ".join(matched_skills))

            missing = get_top_keywords(clean_jd, resume_text)
            st.write("❌ Missing Skills:", ", ".join(missing))

            exp = extract_experience(raw_text)
            st.write(f"💼 Experience: {exp} years")

            role = detect_role(resume_text)
            st.write(f"🎯 Role Type: {role}")

            # 📄 PDF
            pdf_file = generate_pdf_report(name, score, skill_score, exp, role, matched_skills, missing)
            with open(pdf_file, "rb") as f:
                st.download_button(f"📄 Download Report for {name}", f, file_name=f"{name}_report.pdf")

            st.markdown("---")

            results.append((name, score, skill_score, exp, role))

        df = pd.DataFrame(results, columns=["Name", "Match Score", "Skill Score", "Experience", "Role"])
        st.bar_chart(df.set_index("Name")["Match Score"])
        st.download_button("⬇ Download All Results CSV", df.to_csv(index=False), "screening_results.csv")
