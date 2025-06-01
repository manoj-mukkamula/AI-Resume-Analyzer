import nltk
# Download required NLTK data
nltk.download('punkt_tab')
nltk.download('punkt')
nltk.download('stopwords')

from suggestions import skill_tips
from skills import software_skills, alias_map
import os
import uuid
import re
import PyPDF2
from flask import Flask, render_template, request, jsonify, send_file, render_template_string
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import io
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors

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
    resume_file = request.files.get('resume')
    resume_text_input = request.form.get('resume_text', '').strip()
    jd = request.form['jobdesc']

    if resume_file and resume_file.filename:
        filename = f"{uuid.uuid4().hex}_{resume_file.filename}"
        resume_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        resume_file.save(resume_path)
        resume_text = extract_text_from_pdf(resume_path)
    elif resume_text_input:
        resume_text = resume_text_input
    else:
        return "Please upload a resume PDF or paste resume text.", 400

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
        tips = ["Job description doesn't contain known technical skills. Please refine it."]
    elif not missing_skills:
        tips = ["Great! No major missing skills detected."]
    else:
        tips = []
        for skill in missing_skills[:10]:
            tip = skill_tips.get(skill.lower(), f"Consider improving your {skill} skills.")
            tips.append(f"{skill.title()}: {tip}")

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

@app.route('/extract_resume_text', methods=['POST'])
def extract_resume_text():
    resume_file = request.files.get('resume')
    if not resume_file or not resume_file.filename:
        return jsonify({'error': 'No file uploaded'}), 400
    filename = f"{uuid.uuid4().hex}_{resume_file.filename}"
    resume_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    resume_file.save(resume_path)
    resume_text = extract_text_from_pdf(resume_path)
    return jsonify({'text': resume_text})

@app.route('/download_report', methods=['POST'])
def download_report():
    combined_match = request.form.get('combined_match')
    skill_match = request.form.get('skill_match')
    tfidf_match = request.form.get('tfidf_match')
    missing = request.form.get('missing', '')
    tips = request.form.get('tips', '')

    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter
    y = height - 60

    c.setFont("Helvetica-Bold", 20)
    c.setFillColor(colors.HexColor("#6c47ff"))
    c.drawString(72, y, "AI Resume Analyzer Report")

    c.setFont("Helvetica-Bold", 13)
    y -= 40
    c.setFillColor(colors.HexColor("#6c47ff"))
    c.drawString(72, y, f"Overall Resume Match: {combined_match}%")
    y -= 25
    c.setFillColor(colors.HexColor("#2563eb"))
    c.drawString(72, y, f"Skill Match Score: {skill_match}%")
    y -= 25
    c.setFillColor(colors.HexColor("#43d39e"))
    c.drawString(72, y, f"Content Similarity: {tfidf_match}%")

    y -= 35
    c.setFont("Helvetica-Bold", 12)
    c.setFillColor(colors.HexColor("#ff9800"))
    c.drawString(72, y, "Skills to Enhance:")
    y -= 20
    c.setFont("Helvetica", 11)
    for skill in missing.split(','):
        skill = skill.strip()
        if skill:
            c.drawString(90, y, f"- {skill}")
            y -= 15

    y -= 15
    c.setFont("Helvetica-Bold", 12)
    c.setFillColor(colors.HexColor("#3ddad7"))  # Title color for Recommendations
    c.drawString(72, y, "Recommendations:")
    y -= 20
    c.setFont("Helvetica", 11)
    for tip in tips.split('|'):
        tip = tip.strip()
        if tip:
            c.setFillColor(colors.HexColor("#43d39e"))  # <-- Set color for each recommendation
            c.drawString(90, y, f"- {tip}")
            y -= 15

    c.save()
    buffer.seek(0)
    return send_file(
        buffer,
        mimetype='application/pdf',
        as_attachment=True,
        download_name='resume_analysis_report.pdf'
    )

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
