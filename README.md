# 🤖 AI-Powered Resume Intelligence and Job Matching System
An AI-powered resume analysis and job matching system that analyzes resumes, evaluates ATS compatibility, matches candidates with job descriptions, identifies skill gaps, provides resume improvement recommendations, and recommends suitable job roles based on the candidate's profile.

## 📌 Overview
Finding the right job and understanding whether a resume matches a job description can be difficult for candidates.
This project uses **Natural Language Processing (NLP)**, **Sentence Transformers**, **semantic similarity**, and **skill-based analysis** to provide an intelligent resume evaluation and job recommendation system.

The application allows users to:

* Upload a resume in PDF or DOCX format
* Automatically extract resume information
* Detect technical skills
* Analyze job descriptions
* Calculate semantic similarity between resumes and jobs
* Calculate ATS Compatibility Score
* Identify matched and missing skills
* Perform skill-gap analysis
* Evaluate resume improvement areas
* Compare a resume against multiple jobs
* Automatically recommend suitable job roles
* Generate a downloadable PDF analysis report

The application is developed using **Python and Streamlit**.
# ✨ Key Features
## 📄 1. Resume Analysis
Upload a resume in:

* PDF
* DOCX

The system extracts:

* Candidate name
* Email
* Phone number
* Professional summary
* Education
* Experience
* Projects
* Certifications
* Achievements
* Publications
* Technical skills
## 🎯 2. Single Job Analysis
Users can paste a specific job description and compare it against their resume.

The system analyzes:

* Semantic relevance
* Required skills
* Matched skills
* Missing skills
* Additional skills
* Skill categories
* Overall compatibility
### Matching Formula
The job compatibility score combines:

65% Semantic Similarity
+
35% Explicit Skill Match

Semantic similarity is calculated using a **Sentence Transformer model**, while explicit skill matching is performed using the project's skill database.
# 🤖 3. ATS Compatibility Analysis

The system provides a transparent **ATS Compatibility Score out of 100**.

The score considers:

| Component                   |   Weight |
| --------------------------- | -------: |
| Keyword / Skill Match       |      30% |
| Semantic Job Relevance      |      25% |
| Resume Section Completeness |      15% |
| Experience Relevance        |      10% |
| Education Relevance         |       5% |
| Project Relevance           |       5% |
| ATS Parseability            |      10% |
| **Total**                   | **100%** |

### ATS Analysis Includes
* ATS Compatibility Score
* Keyword match analysis
* Section completeness
* Experience relevance
* Education relevance
* Project relevance
* Parseability analysis
* ATS issues
* Improvement recommendations

> **Note:** ATS scoring varies between Applicant Tracking Systems. This project provides a transparent compatibility estimate rather than claiming to reproduce a specific company's proprietary ATS algorithm.
# 🔍 4. Skill Gap Analysis
The system compares the candidate's skills with the skills required by the target job.
### Example
Matched Skills
---------------
Python
Machine Learning
NLP
Pandas
Missing Skills
--------------
SQL
Docker
AWS

The system also identifies:
* Critical skill gaps
* Missing skill categories
* Additional skills already present in the resume
# 📈 5. Resume Improvement Intelligence
The system evaluates how the resume can be improved for the selected job.
It provides:
### Resume Improvement Score
A score based on factors such as:
* Job skill coverage
* Summary quality
* Projects
* Education
* Experience
* Certifications and additional sections

### Strengths

Identifies areas where the resume already performs well.

### Weaknesses

Identifies missing or weak areas.

### Recommendations

Provides actionable suggestions for improving the resume.

The system does **not** recommend adding skills that the candidate does not actually possess.


# 📊 6. Multi-Job Recommendation

Users can compare a single resume against **multiple job descriptions**.

                 Resume
                    │
        ┌───────────┼───────────┐
        ▼           ▼           ▼
      Job 1       Job 2       Job 3
        │           │           │
        └───────────┼───────────┘
                    ▼
             AI Job Matching
                    │
                    ▼
              Job Ranking
                    │
          ┌─────────┼─────────┐
          ▼         ▼         ▼
       Best Job   Job 2     Job 3

Each job receives a compatibility score and is ranked accordingly.

The system displays:

* Job ranking
* Compatibility score
* Semantic relevance
* Skill match
* Matched skills
* Missing skills
* Additional skills

# 💼 7. Automatic Recommended Jobs

The system can also recommend suitable job **roles without requiring the user to paste job descriptions**.

The resume is compared against a built-in job-role database containing multiple career categories.

### Example Career Categories

* AI & Machine Learning
* Data & Analytics
* Software Development
* Web & Full Stack
* Cloud & DevOps
* Cybersecurity & IT
* Product & Project
* Design & Creative
* Marketing & Content
* Sales & Customer Success
* Finance & Accounting
* HR & Recruitment
* Operations & Management
* Healthcare & Life Sciences
* Education & Research

### Example Recommended Roles

Machine Learning Engineer
AI Engineer
Data Scientist
Data Analyst
Python Developer
Software Engineer
NLP Engineer
Data Engineer
Cloud Engineer
Cybersecurity Analyst
Business Analyst

The system ranks roles according to the candidate's resume and provides:

* Compatibility score
* Semantic relevance
* Skill match
* Matched skills
* Missing skills
* Recommended career areas
* Career direction

The job-role database can be expanded by adding new roles to:

data/jobs.csv

# 🧠 AI / NLP Approach

The project uses a combination of **rule-based NLP and transformer-based semantic matching**.

### Resume Processing

Resume
   ↓
PDF/DOCX Text Extraction
   ↓
Text Cleaning
   ↓
Section Detection
   ↓
Skill Extraction
   ↓
Resume Profile

### Job Matching

Resume Text
     ↓
Sentence Transformer
     ↓
Resume Embedding
     │
     │ Cosine Similarity
     ▼
Job Description Embedding
     ↓
Semantic Similarity
     +
Skill Matching
     ↓
Compatibility Score

# 🛠️ Technology Stack

## Programming Language

* Python

## Machine Learning / NLP

* Sentence Transformers
* Transformer-based embeddings
* Semantic similarity
* Cosine similarity
* NLP-based skill extraction

## Data Processing

* Pandas
* NumPy
* Regular Expressions

## Machine Learning

* Scikit-learn
* PyTorch

## Document Processing

* PyMuPDF
* python-docx

## Visualization

* Plotly

## Web Application

* Streamlit

## Report Generation

* ReportLab

## Testing

* Pytest

# 📁 Project Structure

AI-Resume-Intelligence-System/
│
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
├── pytest.ini
│
├── data/
│   ├── skills.csv
│   └── jobs.csv
│
├── src/
│   ├── __init__.py
│   ├── parser.py
│   ├── text_cleaner.py
│   ├── skill_extractor.py
│   ├── resume_analyzer.py
│   ├── job_analyzer.py
│   ├── embeddings.py
│   ├── matcher.py
│   ├── recommender.py
│   ├── multi_job_matcher.py
│   ├── resume_improver.py
│   ├── ats_scorer.py
│   ├── dashboard_utils.py
│   ├── report_generator.py
│   ├── job_recommender.py
│   └── utils.py
│
├── tests/
│   ├── test_parser.py
│   ├── test_skill_extractor.py
│   ├── test_resume_analyzer.py
│   ├── test_matcher.py
│   ├── test_resume_improver.py
│   ├── test_report_generator.py
│   └── test_ats_scorer.py
│
├── uploads/
└── models/

# 🔄 Application Workflow

                Upload Resume
                     │
                     ▼
             Resume Extraction
                     │
                     ▼
              Resume Analysis
                     │
          ┌──────────┼──────────┐
          ▼          ▼          ▼
       Skills     Sections    Profile
          │          │          │
          └──────────┼──────────┘
                     ▼
              Choose Analysis
                     │
       ┌─────────────┼──────────────┐
       ▼             ▼              ▼
 Single Job       Multi-Job      Recommended
 Analysis         Matching          Jobs
       │             │              │
       ▼             ▼              ▼
   ATS Score      Job Ranking    Role Ranking
       │             │              │
       └─────────────┼──────────────┘
                     ▼
              Skill Gap Analysis
                     │
                     ▼
           Resume Improvement
                     │
                     ▼
              PDF Report

# 📊 Project Outputs

The application provides:

* Resume profile
* Detected skills
* Job-required skills
* Semantic similarity
* Skill match percentage
* Compatibility score
* ATS Compatibility Score
* Matched skills
* Missing skills
* Critical skill gaps
* Resume strengths
* Resume weaknesses
* Improvement recommendations
* Job rankings
* Recommended job roles
* Career areas
* Downloadable PDF report

# 🔐 Privacy

Resume files may contain personal information.

For local usage:

* Do not upload private resumes to GitHub.
* Do not commit personal resume files.
* Do not commit sensitive information.
* Keep generated/uploaded resume files outside version control.

The `.gitignore` file excludes generated and local files from Git tracking.

# 🚀 Future Improvements

Possible future enhancements include:

* Live job vacancy integration
* Job-board API integration
* More comprehensive skill databases
* Industry-specific skill taxonomies
* Experience-level detection
* Salary-based job recommendations
* Location-based job recommendations
* Resume keyword optimization
* Advanced resume formatting analysis
* Multilingual resume support
* LLM-powered resume rewriting
* Cloud deployment
* User authentication and profile management

# 🎯 Use Cases

This system can be useful for:

* Students searching for suitable career roles
* Fresh graduates
* Job seekers
* Career guidance systems
* Resume screening tools
* Recruitment support systems
* Skill-gap analysis
* Career recommendation platforms

# ⚠️ Disclaimer

The ATS Compatibility Score and job compatibility scores are intended as **decision-support indicators**.

They are not official scores from any specific Applicant Tracking System, employer, or recruitment platform.

Recommendations should be used as guidance and candidates should only claim skills and experience they genuinely possess.


### 👨‍💻 Author : VANETHA A C K

Connect With Me

• LinkedIn: www.linkedin.com/in/vanetha24

• GitHub: https://github.com/vanetha24

• Email: vvanetha633@gmail.com

## ⭐ If you find this project useful

Feel free to explore the repository, suggest improvements, or use the project as a learning reference.

**Built with Python, NLP, Machine Learning, and Streamlit.**
