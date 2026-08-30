import json
import re
import requests


OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "qwen3:8b"


SYSTEM_PROMPT = """
You are a technical skill extraction system.

Extract ONLY concrete technical skills from the provided job information.

Valid examples:
Python, C++, Java, JavaScript, SQL, Spring Boot, FastAPI,
React, Angular, Docker, Kubernetes, PostgreSQL, MySQL,
AWS, Azure, Git, REST API, Machine Learning, Data Structures,
Algorithms, System Design, Multithreading, Unity, Android, iOS.

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

Return ONLY valid JSON:

{
  "skills": ["skill1", "skill2"]
}
"""


def clean_skills(skills):
    """
    Clean, normalize and deduplicate skills.
    """

    if not isinstance(skills, list):
        return []

    cleaned = []
    seen = set()

    for skill in skills:

        if not isinstance(skill, str):
            continue

        skill = skill.strip().lower()

        # Remove bullets/punctuation around the skill
        skill = re.sub(r"^[\s\-•*]+|[\s\-•*]+$", "", skill)

        # Normalize whitespace
        skill = re.sub(r"\s+", " ", skill)

        if not skill:
            continue

        # Ignore extremely long malformed outputs
        if len(skill) > 60:
            continue

        # Deduplicate
        if skill not in seen:
            seen.add(skill)
            cleaned.append(skill)

    return cleaned[:15]


def parse_ollama_response(raw_response):
    """
    Parse Ollama JSON output robustly.
    """

    raw_response = raw_response.strip()

    # Direct JSON
    try:
        data = json.loads(raw_response)

        if isinstance(data, dict):
            return data

    except json.JSONDecodeError:
        pass

    # Remove markdown fences
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

    # Find JSON object
    start = cleaned.find("{")
    end = cleaned.rfind("}")

    if start != -1 and end != -1:

        json_text = cleaned[start:end + 1]

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


def extract_skills(text):
    """
    Extract technical skills from text using Ollama.

    Designed for relatively short inputs such as:
        job_title + job_skills
    """

    if not text or not text.strip():
        return []

    prompt = f"""
{SYSTEM_PROMPT}

JOB INFORMATION:
{text}

Return ONLY the JSON object.
"""

    payload = {
        "model": MODEL,
        "prompt": prompt,
        "format": "json",
        "stream": False,

        "options": {
            "temperature": 0,
            "num_predict": 150
        }
    }

    response = requests.post(
        OLLAMA_URL,
        json=payload,
        timeout=60
    )

    response.raise_for_status()

    result = response.json()

    raw_response = result.get("response", "")

    if not raw_response:
        raise ValueError("Ollama returned an empty response.")

    parsed = parse_ollama_response(raw_response)

    return clean_skills(
        parsed.get("skills", [])
    )