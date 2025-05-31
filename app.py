import nltk
# Download required NLTK data
nltk.download('punkt_tab')
nltk.download('punkt')
nltk.download('stopwords')

import os
import uuid
import re
import PyPDF2
from flask import Flask, render_template, request
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from skills import software_skills

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Clean and normalize text
def clean_text(text):
    text = text.lower()
    text = re.sub(r'[^a-z0-9.\s/]', ' ', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

# Extract skill phrases from text
def extract_skills_from_text(text, skill_list):
    found_skills = set()
    for skill in skill_list:
        if re.search(r'\b' + re.escape(skill) + r'\b', text):
            found_skills.add(skill)
    return found_skills

# Extract text from PDF
def extract_text_from_pdf(pdf_path):
    text = ""
    with open(pdf_path, 'rb') as f:
        reader = PyPDF2.PdfReader(f)
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text
    return text

# Routes
@app.route("/")
def home():
    return render_template("home.html")

@app.route("/analyze")
def analyze():
    return render_template("analyze.html")

@app.route('/upload', methods=['POST'])
def upload():
    resume = request.files['resume']
    jd = request.form['jobdesc']

    filename = f"{uuid.uuid4().hex}_{resume.filename}"
    resume_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    resume.save(resume_path)

    resume_text = extract_text_from_pdf(resume_path)
    resume_clean = clean_text(resume_text)
    jd_clean = clean_text(jd)

    resume_skills = extract_skills_from_text(resume_clean, software_skills)
    jd_skills = extract_skills_from_text(jd_clean, software_skills)
    missing_skills = list(jd_skills - resume_skills)

    skill_match_percent = round(len(resume_skills & jd_skills) / max(len(jd_skills), 1) * 100, 2)

    vectorizer = TfidfVectorizer()
    vectors = vectorizer.fit_transform([resume_clean, jd_clean])
    tfidf_score = cosine_similarity(vectors[0:1], vectors[1:2])[0][0]
    tfidf_match = round(tfidf_score * 100, 2)

    combined_match = round(skill_match_percent * 0.85 + tfidf_match * 0.15, 2)

    if not jd_skills:
        tips = "Job description doesn't contain known technical skills. Please refine it."
    elif not missing_skills:
        tips = "Great! No major missing skills detected."
    else:
        tips = f"Consider learning or adding these skills: {', '.join(missing_skills[:5])}"

    return render_template('result.html',
                           combined_match=combined_match,
                           skill_match=skill_match_percent,
                           tfidf_match=tfidf_match,
                           missing=missing_skills[:10],
                           tips=tips)

@app.route("/sample")
def sample():
    return render_template("sample.html")

@app.route("/about")
def about():
    return render_template("about.html")

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
