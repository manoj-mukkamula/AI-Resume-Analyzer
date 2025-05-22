import nltk
# Download required NLTK data
nltk.download('punkt_tab')
nltk.download('punkt')
nltk.download('stopwords')

from flask import Flask, render_template, request
import os
import PyPDF2
import uuid
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import spacy



app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
DATA_FOLDER = 'data'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(DATA_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

nlp = spacy.load('en_core_web_sm')

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
    doc = nlp(text.lower())
    return set([token.text for token in doc if token.is_alpha and not token.is_stop])

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    resume = request.files.get('resume')
    jd = request.form.get('jobdesc')

    if not resume or resume.filename == '':
        return "No resume uploaded", 400
    if not jd or jd.strip() == '':
        return "Job description is empty", 400

    # Save resume PDF with unique name
    unique_filename = f"{uuid.uuid4().hex}_{resume.filename}"
    resume_path = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
    resume.save(resume_path)

    # Extract and clean text
    resume_text = extract_text_from_pdf(resume_path)
    resume_clean = clean_text(resume_text)
    jd_clean = clean_text(jd)

    # Save cleaned texts
    with open(os.path.join(DATA_FOLDER, 'resumetext.txt'), 'w', encoding='utf-8') as f:
        f.write(resume_clean)
    with open(os.path.join(DATA_FOLDER, 'jobdesc.txt'), 'w', encoding='utf-8') as f:
        f.write(jd_clean)

    # TF-IDF similarity for match %
    vectorizer = TfidfVectorizer()
    vectors = vectorizer.fit_transform([resume_clean, jd_clean])
    score = cosine_similarity(vectors[0:1], vectors[1:2])[0][0]
    match_percentage = round(score * 100, 2)

    # Keyword based missing skills
    resume_keywords = extract_keywords(resume_clean)
    jd_keywords = extract_keywords(jd_clean)
    missing_skills = sorted(list(jd_keywords - resume_keywords))

    return render_template('result.html',
                           match=match_percentage,
                           missing=missing_skills[:10],  # show top 10 missing
                           tips="Consider adding these missing skills to improve your match.")

@app.route('/result')
def result():
    return render_template('result.html')

if __name__ == '__main__':
    app.run(debug=True)
