import PyPDF2
import re
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

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
