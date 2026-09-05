![Status](https://img.shields.io/badge/status-in%20development-orange)

# AI-Hire 🚀

## AI-Powered Candidate Evaluation and Intelligent Hiring Assistant

AI-Hire is an AI-driven recruitment platform that analyzes multiple technical signals from candidates, including coding profiles, GitHub activity, resumes, and job requirements, to help employers make data-driven hiring decisions.

The goal is to move beyond traditional resume-based screening and build a system that evaluates what candidates can actually build.

---

# 🌟 Overview

AI Hiring Assistant is a full-stack hiring platform designed to improve candidate discovery and evaluation through machine learning.

The platform supports two types of users:

#### Candidates 
- Create and manage their profile
- Connect GitHub and LeetCode
- Browse available jobs
- Apply to jobs
- Track applications

#### Recruiters 
- Create and manage job postings
- View applicants
- Rank candidates using ML-generated match scores
- Inspect candidate matching signals

Instead of relying exclusively on keyword matching, the system combines structured candidate information with technical and activity-based signals from coding platforms to generate a candidate-job compatibility score.

# Problem

Traditional recruitment platforms often depend heavily on:

- Resume keywords
- Manual candidate filtering
- Basic skill matching
- Subjective initial screening

This can make it difficult to distinguish between candidates who list similar skills but have very different technical profiles.

AI Hiring Assistant approaches candidate matching as a machine learning ranking problem, combining information from multiple sources to estimate how relevant a candidate is for a particular job.

---

# 🏗️ Architecture

```
                              Candidate
                                  |
                                  ▼
                         Profile Information
                                  |
                  ┌───────────────┴───────────────┐
                  │                               │
                  ▼                               ▼
          Candidate Sync Service            Resume Upload
                  │                               │
        ┌─────────┼─────────┐                     ▼
        ▼         ▼         ▼               Resume Analyzer
     GitHub    LeetCode   Profile                 │
    Analyzer   Analyzer   Features                ▼
        │         │         │                Ollama / LLM
        │         │         │                     │
        │         │         │                     ▼
        ▼         ▼         ▼           Structured Resume Data
    Technical Feature Extraction                  │
        │         │         │                     ▼
        │         │         │               Extracted Skills
        └─────────┼─────────┴─────────────────────┘
                  ▼
          Candidate Features
                  │
                  ▼
            PostgreSQL
                  │
                  │
       Job Requirements / Description
                  │
                  ▼
          Feature Engineering
                  │
                  ▼
          ML Matching Model
                  │
                  ▼
             Match Score
                  │
                  ▼
          Candidate Ranking
                  │
                  ▼
          Recruiter Dashboard
```
## Core Flow
```
    Candidate Data + Job Data
            │
            ▼
    Feature Engineering
            │
            ▼
    Candidate-Job Feature Vector
            │
            ▼
      ML Matching Model
            │
            ▼
       Match Score
            │
            ▼
    Ranked Candidates
            │
            ▼
    Recruiter Dashboard
```    
---

## 🤖 Machine Learning

The core ML system treats hiring as a **candidate-job matching problem** rather than simple keyword filtering.

### Features

The matching pipeline uses signals including:

- Required skill coverage
- Skill similarity
- Role similarity
- Text similarity
- GitHub repository activity
- Programming language diversity
- GitHub stars
- LeetCode problems solved
- LeetCode activity
- Contest performance
- DSA-related signals

Candidate-job pairs are generated from publicly available datasets and transformed into feature vectors for model training and evaluation.

### Model Evaluation

The expanded feature set incorporating GitHub and LeetCode signals achieved approximately:


| Metric | Score |
|---|---:|
| MAE | 2.58 |
| RMSE | 3.37 |
| R² | 0.97 |
| Classification Accuracy | 96% |
| ROC-AUC | 0.99 |

These results represent offline model evaluation and should not be interpreted as real-world hiring accuracy.

### AI / Resume Intelligence

Resume processing uses an LLM-powered pipeline through Ollama to extract structured information from uploaded resumes, including candidate skills and relevant profile information.

The extracted information can then be incorporated into the broader candidate intelligence pipeline alongside GitHub and LeetCode signals.

---

# ⚙️ Tech Stack

### Backend

- Python
- FastAPI
- Pydantic
- PostgreSQL
- JWT Authentication

### Machine Learning

- Python
- Pandas
- NumPy
- Scikit-learn
- XGBoost
- Ollama
- LLM-based Resume Parsing
- Jupyter Notebook

### APIs & Storage

- GitHub REST API
- LeetCode GraphQL API
- AWS S3

### Frontend

- React
- JavaScript

## Development Tools

- Git
- GitHub
- VS Code

---

# Roadmap

### V1 — Core Platform
- [x] Authentication
- [x] Candidate profiles
- [x] Recruiter profiles
- [x] Job creation
- [x] Applications
- [x] GitHub integration
- [x] LeetCode integration
- [x] Feature extraction
- [x] ML candidate-job matching
- [x] Candidate ranking
- [ ] Production deployment

### V2 (Planned)
- [ ] Personalized job recommendations
- [ ] Resume parsing
- [ ] Skill-gap analysis
- [ ] Advanced recruiter analytics
- [ ] Improved ranking and recommendation signals

---

# 🚀 Environment Setup

Prerequisites
- Python 3.10+
- Node.js 18+
- PostgreSQL
- Git

Clone repository:
```
git clone https://github.com/<username>/AI-Hire.git
```

Install dependencies:
```
pip install -r requirements.txt
pip install -r requirements-ai.txt
```

**Environment Variables**
Create a `.env` file with the required application database, API and AWS S3 configuration:

```
GITHUB_TOKEN=

DATABASE_URL=
SECRET_KEY =

ALGORITHM =

ACCESS_TOKEN_EXPIRE_MINUTES =

AWS_ACCESS_KEY_ID =
AWS_SECRET_ACCESS_KEY =
AWS_REGION =
AWS_S3_BUCKET =
```

Use the exact variable names defined in the backend configuration. Never commit .env files or cloud credentials to the repository.

Run migrations:
```
psql -f migration_file.sql
```

Start server:
```
uvicorn backend.app.main:app --reload
```
---

# 🎯 Future Vision

AI-Hire aims to become an intelligent hiring assistant that can:

- Understand candidate capabilities
- Reduce manual screening effort
- Identify strong candidates beyond resumes
- Match developers with suitable opportunities
- Help recruiters make faster, data-driven decisions

The goal is simple:

"Don't just analyze what a candidate claims they know.
Analyze what they can actually build."

---

# 👨‍💻Author

Built as an AI + Backend Engineering project exploring:

- Machine Learning
- Software Architecture
- API-driven developer intelligence
- Recruitment Intelligence
- Data-driven hiring systems
