from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer

# Load BERT model once
bert_model = SentenceTransformer('all-MiniLM-L6-v2')

# 🔥 BERT similarity
def compute_similarity(job_desc, resumes):
    documents = [job_desc] + resumes

    embeddings = bert_model.encode(documents)

    job_embedding = embeddings[0].reshape(1, -1)
    resume_embeddings = embeddings[1:]

    scores = cosine_similarity(job_embedding, resume_embeddings)
    return scores[0]


def get_top_keywords(job_desc, resume):
    jd_words = set(job_desc.split())
    resume_words = set(resume.split())
    missing = jd_words - resume_words
    return list(missing)[:10]


def skill_match_score(job_desc, resume):
    jd_words = set(job_desc.split())
    resume_words = set(resume.split())
    matched = jd_words.intersection(resume_words)
    score = len(matched) / len(jd_words)
    return score, list(matched)[:10]


def detect_role(resume):
    roles = {
        "Data Scientist": ["machine learning", "pandas", "numpy", "model"],
        "Web Developer": ["html", "css", "javascript", "react"],
        "ML Engineer": ["tensorflow", "pytorch", "deployment"]
    }

    resume_lower = resume.lower()
    for role, keywords in roles.items():
        if any(word in resume_lower for word in keywords):
            return role
    return "Other"
