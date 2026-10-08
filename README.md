# 🎯 MatchPortal: Job & Internship Portal with Recommendation Engine

An intelligent, full-stack Job and Internship Web Application powered by a **Hybrid AI Recommendation Engine** (Skill Vector Overlap + TF-IDF Semantic Cosine Similarity + Preference Alignment).

Built with **Python (Flask)**, **SQLite**, and a modern **Tailwind CSS** responsive user interface.

---

## 🌟 Key Features

### 1. 🧠 Explainable Recommendation Engine (`recommendation.py`)
- **Weighted Multi-Factor Scoring**:
  - **Core Skill Match (55%)**: Normalized Jaccard overlap between candidate skills and required/preferred job skills.
  - **Resume Semantic Similarity (30%)**: TF-IDF Vectorization & Cosine Similarity on candidate bio/resume against job descriptions.
  - **Role & Experience Alignment (15%)**: Work preference (Internship vs. Full-time, Remote, Experience tier).
- **Skill Normalization & Synonyms**: Maps aliases (e.g. `react.js` $\rightarrow$ `react`, `py` $\rightarrow$ `python`, `k8s` $\rightarrow$ `kubernetes`, `ml` $\rightarrow$ `machine learning`).
- **Explainable Match Breakdown**:
  - Overall Match Score percentage (e.g. `94% - Exceptional Match`).
  - **Matched Skills**: Highlighted with green checkmark badges.
  - **Skill Gap Analysis**: Shows missing required skills with actionable learning recommendations.
- **Pure-Python Fallback**: Works seamlessly out of the box even before `scikit-learn` is installed.

### 2. 👥 Real-Time Persona Switcher
- Located right in the top navigation bar!
- Switch between 4 pre-seeded candidate personas with 1 click to watch the recommendation engine dynamically re-score and re-rank all opportunities:
  - **Aarav Patel** – Machine Learning & Data Science Student
  - **Sophia Rodriguez** – Frontend & React Developer
  - **Marcus Vance** – Full-Stack Python & DevOps Engineer
  - **Priya Sharma** – Product & UI/UX Designer

### 3. 📄 AI Resume Parser & Skill Extractor
- Paste any resume text, coursework summary, or project descriptions in the Profile tab.
- Click **"Extract & Add Skills"** to automatically parse technical skills and add them as interactive tags.

### 4. 💼 Recruiter Portal & Talent Scouting (`/recruiter`)
- **Job Posting**: Post new jobs and internships with required and nice-to-have skills.
- **Applicant Pipeline**: View incoming applications with match scores, skills breakdown, and status controls (`Applied`, `Under Review`, `Shortlisted`, `Interviewing`, `Accepted`, `Rejected`).
- **Talent Scouting**: AI automatically scores and ranks *all* platform candidates for any job listing.

### 5. 📊 Candidate Application Tracker (`/applications`)
- Real-time status pipeline of applied roles with compensation, match score at time of application, and status badges.

---

## 🚀 Quick Start

### Windows Launcher
Double-click `run.bat` in the project folder to start the app and open it in your browser.

### Manual Command Line
```bash
cd c:\Users\HP\OneDrive\Documents\job_internship_portal
pip install -r requirements.txt
python app.py
```
Open `http://127.0.0.1:5000` in your browser.
