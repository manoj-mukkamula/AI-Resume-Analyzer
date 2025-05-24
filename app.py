import nltk
# Download required NLTK data
nltk.download('punkt_tab')
nltk.download('punkt')
nltk.download('stopwords')

import os
import uuid
import PyPDF2
from flask import Flask, render_template, request
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.probability import FreqDist
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Import skills list from skills.py
from skills import skills_list


app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
DATA_FOLDER = 'data'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(DATA_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Convert skills list to lowercase set for fast lookup
skill_set = set(skill.lower() for skill in skills_list)

def extract_text_from_pdf(pdf_path):
    text = ""
    with open(pdf_path, 'rb') as f:
        reader = PyPDF2.PdfReader(f)
        for page in reader.pages:
            text += page.extract_text() or ""
    return text

def clean_text(text):
    tokens = word_tokenize(text.lower())
    words = [w for w in tokens if w.isalpha() and w not in stopwords.words('english')]
    return ' '.join(words)

def extract_keywords(text):
    tokens = word_tokenize(text.lower())
    words = [w for w in tokens if w.isalpha() and w in skill_set]
    freq_dist = FreqDist(words)
    keywords = [word for word, _ in freq_dist.most_common(15)]
    return set(keywords)

@app.route('/')
def index():
    return render_template('index.html')

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

    with open(os.path.join(DATA_FOLDER, 'resumetext.txt'), 'w') as f:
        f.write(resume_clean)
    with open(os.path.join(DATA_FOLDER, 'jobdesc.txt'), 'w') as f:
        f.write(jd_clean)

    vectorizer = TfidfVectorizer()
    vectors = vectorizer.fit_transform([resume_clean, jd_clean])
    score = cosine_similarity(vectors[0:1], vectors[1:2])[0][0]
    match_percentage = round(score * 100, 2)

    resume_keywords = extract_keywords(resume_clean)
    jd_keywords = extract_keywords(jd_clean)
    missing_keywords = list(jd_keywords - resume_keywords)

    tips = "Consider adding these missing skills to improve your match." if missing_keywords else "Great! No major missing skills detected."

    return render_template('result.html',
                           match=match_percentage,
                           missing=missing_keywords[:10],
                           tips=tips)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
