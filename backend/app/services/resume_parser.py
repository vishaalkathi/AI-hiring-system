import json
import re
import requests

from pydantic import BaseModel, Field


# ============================================================
# OLLAMA CONFIG
# ============================================================

OLLAMA_URL = "http://localhost:11434/api/generate"

MODEL = "qwen3:8b"


# ============================================================
# PARSED RESUME MODEL
# ============================================================

class ParsedResume(BaseModel):

    candidate_role: str = ""

    candidate_skills: list[str] = Field(
        default_factory=list
    )

    candidate_experience: float = 0.0


# ============================================================
# SYSTEM PROMPT
# ============================================================

SYSTEM_PROMPT = """

You are a technical resume parsing system.

Extract structured information from the provided resume.

You must extract:

1. candidate_role
2. candidate_skills
3. candidate_experience

------------------------------------------------------------
CANDIDATE ROLE
------------------------------------------------------------

Return the candidate's primary professional or technical role.

Examples:

Software Engineer
Backend Developer
Data Scientist
Machine Learning Engineer
Frontend Developer
DevOps Engineer
Full Stack Developer

If the candidate is a student and does not have a clear
professional role, infer the most relevant technical role
from their education, projects, internships and technical
experience.

Keep the role concise.

------------------------------------------------------------
TECHNICAL SKILLS
------------------------------------------------------------

Extract ONLY concrete technical skills.

Valid examples:

Python
C++
Java
JavaScript
SQL
Spring Boot
FastAPI
React
Angular
Docker
Kubernetes
PostgreSQL
MySQL
AWS
Azure
Git
REST API
Machine Learning
Data Structures
Algorithms
System Design
Multithreading
Unity
Android
iOS

Do NOT extract:

- soft skills
- personality traits
- responsibilities
- job titles
- company names
- industries
- generic words
- business terms
- duplicate skills

Examples of INVALID skills:

development
experience
technology
performance
communication
management
scaling
teamwork
problem solving

Return at most 15 UNIQUE technical skills.

------------------------------------------------------------
EXPERIENCE
------------------------------------------------------------

Estimate the candidate's total relevant professional
experience in years.

Include relevant:

- full-time employment
- internships
- professional technical roles

Do not count education as professional experience.

If the candidate has no professional experience,
return 0.

Use decimals when appropriate.

Examples:

6 months -> 0.5
1 year -> 1.0
1 year 6 months -> 1.5
3 years -> 3.0

------------------------------------------------------------
OUTPUT
------------------------------------------------------------

Return ONLY valid JSON.

Exactly this structure:

{
    "candidate_role": "Software Engineer",
    "candidate_skills": [
        "python",
        "fastapi",
        "postgresql"
    ],
    "candidate_experience": 1.5
}

Do not include explanations.
Do not include markdown.
"""


# ============================================================
# SKILL CLEANING
# ============================================================

def clean_skills(skills):

    if not isinstance(skills, list):
        return []

    cleaned = []
    seen = set()

    for skill in skills:

        if not isinstance(skill, str):
            continue

        skill = skill.strip().lower()

        # Remove bullets / surrounding punctuation
        skill = re.sub(
            r"^[\s\-•*]+|[\s\-•*]+$",
            "",
            skill
        )

        # Normalize whitespace
        skill = re.sub(
            r"\s+",
            " ",
            skill
        )

        if not skill:
            continue

        # Ignore malformed long outputs
        if len(skill) > 60:
            continue

        if skill not in seen:

            seen.add(skill)
            cleaned.append(skill)

    return cleaned[:15]


# ============================================================
# JSON PARSER
# ============================================================

def parse_ollama_response(raw_response):

    raw_response = raw_response.strip()

    # --------------------------------------------------------
    # Direct JSON
    # --------------------------------------------------------

    try:

        data = json.loads(raw_response)

        if isinstance(data, dict):
            return data

    except json.JSONDecodeError:
        pass

    # --------------------------------------------------------
    # Remove markdown fences
    # --------------------------------------------------------

    cleaned = re.sub(
        r"```json\s*",
        "",
        raw_response,
        flags=re.IGNORECASE
    )

    cleaned = re.sub(
        r"```\s*",
        "",
        cleaned
    )

    cleaned = cleaned.strip()

    try:

        data = json.loads(cleaned)

        if isinstance(data, dict):
            return data

    except json.JSONDecodeError:
        pass

    # --------------------------------------------------------
    # Find JSON object
    # --------------------------------------------------------

    start = cleaned.find("{")
    end = cleaned.rfind("}")

    if start != -1 and end != -1:

        json_text = cleaned[
            start:end + 1
        ]

        try:

            data = json.loads(json_text)

            if isinstance(data, dict):
                return data

        except json.JSONDecodeError:
            pass

    raise ValueError(
        "Invalid JSON returned by Ollama:\n"
        + raw_response
    )


# ============================================================
# RESUME PARSER
# ============================================================

def parse_resume(resume_text: str) -> ParsedResume:

    if not resume_text or not resume_text.strip():
        return ParsedResume()

    prompt = f"""
{SYSTEM_PROMPT}

RESUME:

{resume_text}

Return ONLY the JSON object.
"""

    payload = {

        "model": MODEL,

        "prompt": prompt,

        "format": "json",

        "stream": False,

        "options": {
            "temperature": 0,
            "num_predict": 300
        }
    }

    response = requests.post(
        OLLAMA_URL,
        json=payload,
        timeout=120
    )

    response.raise_for_status()

    result = response.json()

    raw_response = result.get(
        "response",
        ""
    )

    if not raw_response:
        raise ValueError(
            "Ollama returned an empty response."
        )

    parsed = parse_ollama_response(
        raw_response
    )

    # --------------------------------------------------------
    # ROLE
    # --------------------------------------------------------

    role = str(
        parsed.get(
            "candidate_role",
            ""
        )
    ).strip()

    # --------------------------------------------------------
    # SKILLS
    # --------------------------------------------------------

    skills = clean_skills(
        parsed.get(
            "candidate_skills",
            []
        )
    )

    # --------------------------------------------------------
    # EXPERIENCE
    # --------------------------------------------------------

    try:

        experience = float(
            parsed.get(
                "candidate_experience",
                0
            ) or 0
        )

    except (TypeError, ValueError):

        experience = 0.0

    experience = max(
        0.0,
        experience
    )

    return ParsedResume(

        candidate_role=role,

        candidate_skills=skills,

        candidate_experience=experience
    )
