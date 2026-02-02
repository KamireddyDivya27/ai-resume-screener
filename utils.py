import PyPDF2
import re
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import A4

nltk.download('stopwords')
nltk.download('wordnet')

stop_words = set(stopwords.words('english'))
lemmatizer = WordNetLemmatizer()

def extract_text_from_pdf(file):
    text = ""
    pdf_reader = PyPDF2.PdfReader(file)
    for page in pdf_reader.pages:
        if page.extract_text():
            text += page.extract_text()
    return text

def clean_text(text):
    text = re.sub(r'\n', ' ', text.lower())
    words = re.findall(r'\b[a-z]+\b', text)
    words = [lemmatizer.lemmatize(word) for word in words if word not in stop_words]
    return " ".join(words)

def extract_experience(text):
    matches = re.findall(r'(\d+)\+?\s+year', text.lower())
    if matches:
        return max(map(int, matches))
    return 0

# 📄 PDF REPORT
def generate_pdf_report(name, score, skill_score, exp, role, matched, missing):
    file_path = f"{name}_report.pdf"

    styles = getSampleStyleSheet()
    story = []

    story.append(Paragraph(f"<b>Candidate Report: {name}</b>", styles['Title']))
    story.append(Spacer(1, 12))
    story.append(Paragraph(f"Match Score: {round(score*100,2)}%", styles['Normal']))
    story.append(Paragraph(f"Skill Match: {round(skill_score*100,2)}%", styles['Normal']))
    story.append(Paragraph(f"Experience: {exp} years", styles['Normal']))
    story.append(Paragraph(f"Role Type: {role}", styles['Normal']))
    story.append(Spacer(1, 12))
    story.append(Paragraph(f"Matched Skills: {', '.join(matched)}", styles['Normal']))
    story.append(Paragraph(f"Missing Skills: {', '.join(missing)}", styles['Normal']))

    doc = SimpleDocTemplate(file_path, pagesize=A4)
    doc.build(story)

    return file_path
