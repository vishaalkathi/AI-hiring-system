![Status](https://img.shields.io/badge/status-in%20development-orange)

# AI-Hire 🚀

## AI-Powered Candidate Evaluation and Intelligent Hiring Assistant

AI-Hire is an AI-driven recruitment platform that analyzes multiple technical signals from candidates, including coding profiles, GitHub activity, resumes, and job requirements, to help employers make data-driven hiring decisions.

The goal is to move beyond traditional resume-based screening and build a system that evaluates what candidates can actually build.

---

# 🌟 Overview

Traditional hiring often relies heavily on resumes, which may not accurately represent a developer's practical skills.

AI-Hire aims to create a complete candidate intelligence system by combining:

- GitHub engineering activity
- LeetCode problem-solving ability
- Resume intelligence
- Skill extraction
- Job requirement matching
- AI-based candidate ranking

---

# 🏗️ Architecture

                     Candidate
                         |
                         |
                Profile Information
                         |
                         ▼

                Candidate Sync Service

                         |
      -----------------------------------------
      |                    |                  |
      ▼                    ▼                  ▼  
    GitHub Analyzer   LeetCode Analyzer    Resume Analyzer
      |                    |                  |
      ▼                    ▼                  ▼  
    Feature Extraction Feature Extraction   NLP Extraction
      |                    |                  |
      -----------------------------------------
                         |
                         ▼
                  PostgreSQL Database

                         |
                         ▼

                Candidate Ranking Engine

                         |
                         ▼

             Job Matching & Recommendations

---

# ⚙️ Tech Stack

### Backend

- Python
- FastAPI
- PostgreSQL

### APIs

- GitHub REST API
- LeetCode GraphQL API

### AI/ML (Planned)

- NLP based resume parsing
- Embeddings
- Candidate-job similarity models
- Ranking algorithms

## Development Tools

- Git
- GitHub
- VS Code

---

# Roadmap

### Backend Foundation ✅

- FastAPI setup
- PostgreSQL integration
- Authentication system
- Candidate and employer profiles
- Jobs and applications database

### Developer Intelligence 🚧

Currently working on:

- Developer profile analysis
- Coding activity insights
- Technical feature extraction
- Candidate evaluation pipeline

Upcoming:

- Persistent feature storage
- Candidate synchronization service
- Improved developer metrics


### AI Hiring Intelligence

Planned:

- Resume parsing
- Skill extraction
- Job description understanding
- Candidate-job matching model
- AI ranking system


### Platform Development

Planned:

- Employer dashboard
- Candidate dashboard
- Hiring analytics
- Interview recommendations

---

# 🚀 Environment Setup

Create a `.env` file:

```
DATABASE_URL=

GITHUB_TOKEN=

SECRET_KEY=
```

Clone repository:
```
git clone https://github.com/<username>/AI-Hire.git
```

Install dependencies:
```
pip install -r requirements.txt
```

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

The goal is simple:

"Don't just analyze what a candidate claims they know.
Analyze what they can actually build."

---

# 👨‍💻Author

Built as an AI + Backend Engineering project exploring:

- Machine Learning
- Software Architecture
- Recruitment Intelligence
- Data-driven hiring systems
