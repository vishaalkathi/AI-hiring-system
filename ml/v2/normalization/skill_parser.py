import re

from .skill_normalizer import normalize_skills


def parse_job_skills(skill_text):

    if not isinstance(skill_text, str):
        return []

    if not skill_text.strip():
        return []

    # Naukri skills are generally comma separated
    skills = skill_text.split(",")

    return normalize_skills(skills)


def extract_candidate_skills(resume):

    """
    Lightweight candidate skill extraction.

    We are NOT using the LLM here yet.

    The purpose is to establish a clean baseline
    before adding more sophisticated extraction.
    """

    if not isinstance(resume, str):
        return []

    text = resume.lower()

    # Broad technical vocabulary.
    # This is intentionally conservative.
    known_skills = [
        "python",
        "java",
        "c++",
        "c",
        "c#",
        "javascript",
        "typescript",
        "go",
        "rust",
        "kotlin",
        "swift",

        "react",
        "angular",
        "vue",
        "node.js",
        "django",
        "flask",
        "fastapi",
        "spring",
        "spring boot",

        "html",
        "css",

        "sql",
        "mysql",
        "postgresql",
        "mongodb",
        "redis",

        "aws",
        "azure",
        "gcp",
        "docker",
        "kubernetes",

        "git",
        "github",
        "jenkins",

        "machine learning",
        "deep learning",
        "artificial intelligence",
        "tensorflow",
        "pytorch",
        "scikit-learn",

        "data structures",
        "algorithms",
        "system design",

        "linux",
        "unix",

        "rest api",
        "graphql",

        "android",
        "ios",

        "unity",
        "unity3d",
        "unreal engine",

        "solidity",
        "blockchain",

        "tableau",
        "power bi",

        "spark",
        "hadoop",
        "kafka",
    ]

    found = []

    for skill in known_skills:

        # Escape special regex characters
        pattern = r"(?<!\w)" + re.escape(skill) + r"(?!\w)"

        if re.search(pattern, text):

            normalized = normalize_skills([skill])[0]

            if normalized not in found:
                found.append(normalized)

    return found