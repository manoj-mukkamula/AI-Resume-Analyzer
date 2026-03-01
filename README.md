# AI Resume Analyzer

A modern, AI-powered web application that analyzes your resume against a job description and provides actionable feedback, skill matching, and improvement suggestions.

---

## 🚀 Features

- **AI-Powered Resume Analysis:** Upload your resume (PDF or text) and compare it with any job description.
- **Skill Match & Content Similarity:** Get detailed scores for skill overlap and content relevance.
- **Missing Skills Detection:** Instantly see which skills you should add to your resume.
- **Actionable Recommendations:** Receive AI-generated tips to improve your resume and boost your chances.
- **Modern, Responsive UI:** Clean, professional design with mobile-friendly layouts.
- **Sample Resumes & Job Descriptions:** Explore sample data for quick testing.
- **Downloadable PDF Report:** Download a styled PDF report of your analysis (now powered by ReportLab for cross-platform compatibility).

---

## 🖥️ Live Demo

> **Deployed on Render:**  
> [[https://your-render-url.onrender.com](https://your-render-url.onrender.com](https://ai-resume-analyzer-sahw.onrender.com/)  ](https://ai-resume-analyzer-sahw.onrender.com/)

---

## 📦 Installation & Local Development

### 1. Clone the repository

```sh
git clone https://github.com/yourusername/ai-resume-analyzer.git
cd ai-resume-analyzer
```

### 2. Create a virtual environment and activate it

```sh
python -m venv venv
# On Windows:
venv\Scripts\activate
# On Mac/Linux:
source venv/bin/activate
```

### 3. Install dependencies

```sh
pip install -r requirements.txt
```

### 4. Download NLTK data (first run only)

```python
# In Python shell:
import nltk
nltk.download('punkt')
nltk.download('stopwords')
```

### 5. Run the app locally

```sh
flask run
```

or

```sh
python app.py
```

---

## 🗂️ Project Structure

```
.
├── app.py
├── requirements.txt
├── Procfile
├── static/
│   └── style.css
├── templates/
│   ├── home.html
│   ├── analyze.html
│   ├── result.html
│   ├── about.html
│   ├── sample.html
│   └── navbar.html
├── skills.py
├── suggestions.py
├── uploads/
├── .gitignore
└── README.md
```

---

## 🌐 Deployment (Render)

1. **Push your code to GitHub.**
2. **Connect your repo to [Render](https://render.com/).**
3. **Set the build and start commands:**
   - Build: `pip install -r requirements.txt`
   - Start: `gunicorn app:app`
4. **Ensure your `Procfile` is present:**
   ```
   web: gunicorn app:app
   ```
5. **Add an empty `uploads/` folder (for resume uploads).**
6. **Set environment variables/secrets in Render dashboard if needed.**

---

## 🤝 Contributing

Contributions are welcome!  
Feel free to open issues or submit pull requests for new features, bug fixes, or improvements.

---

## 📄 License

This project is for educational purposes.  
Contact the authors for licensing details.

---

## 👨‍💻 Authors

- Manoj
- Manisha
- Pobeer

AAR Mahaveer Engineering College, CSE 2025 Batch

---

## 📬 Contact

For questions or support, open an issue or contact the project maintainers.
