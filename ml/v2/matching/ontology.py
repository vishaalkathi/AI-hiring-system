# ============================================================
# AI-HIRE V2
# SKILL ONTOLOGY
# ============================================================

LANGUAGE_FAMILIES = {
    "c": "systems_programming",
    "c++": "systems_programming",
    "cpp": "systems_programming",
    "rust": "systems_programming",
    "go": "systems_programming",

    "java": "jvm",
    "kotlin": "jvm",
    "scala": "jvm",

    "python": "scripting",
    "ruby": "scripting",
    "perl": "scripting",

    "javascript": "web",
    "typescript": "web",
    "php": "web",

    "swift": "mobile",
    "objective-c": "mobile",
    "dart": "mobile",
}


LANGUAGE_SIMILARITY = {
    ("c++", "c"): 0.85,
    ("c++", "rust"): 0.75,
    ("c++", "go"): 0.70,

    ("c", "rust"): 0.75,
    ("c", "go"): 0.70,

    ("rust", "go"): 0.75,

    ("java", "kotlin"): 0.90,
    ("java", "scala"): 0.80,
    ("kotlin", "scala"): 0.80,

    ("javascript", "typescript"): 0.90,
    ("javascript", "node.js"): 0.80,
    ("typescript", "node.js"): 0.80,

    ("swift", "objective-c"): 0.80,
}


SKILL_ALIASES = {
    "cpp": "c++",
    "c plus plus": "c++",
    "c/c++": "c++",

    "js": "javascript",
    "node": "node.js",
    "nodejs": "node.js",

    "ts": "typescript",

    "postgres": "postgresql",
    "postgres db": "postgresql",

    "mongo": "mongodb",

    "k8s": "kubernetes",

    "amazon web services": "aws",
    "microsoft azure": "azure",
    "google cloud platform": "gcp",

    "reactjs": "react",
    "react.js": "react",

    "angular.js": "angular",

    "rest api": "rest",
    "restful api": "rest",

    "machine learning": "machine learning",
    "ml": "machine learning",

    "artificial intelligence": "artificial intelligence",
    "ai": "artificial intelligence",

    "natural language processing": "nlp",
}


def normalize_skill(skill: str) -> str:
    """
    Normalize a single skill name.
    """

    skill = skill.lower().strip()

    skill = SKILL_ALIASES.get(skill, skill)

    return skill


def normalize_skills(skills):
    """
    Normalize and deduplicate a list of skills.
    """

    if not skills:
        return []

    normalized = set()

    for skill in skills:

        if not isinstance(skill, str):
            continue

        skill = normalize_skill(skill)

        if skill:
            normalized.add(skill)

    return sorted(normalized)


def language_similarity(candidate_skill: str, required_skill: str):
    """
    Returns:
        1.0  -> exact match
        0-1  -> related language
        0.0  -> unrelated
    """

    candidate_skill = normalize_skill(candidate_skill)
    required_skill = normalize_skill(required_skill)

    if candidate_skill == required_skill:
        return 1.0

    pair = (candidate_skill, required_skill)

    if pair in LANGUAGE_SIMILARITY:
        return LANGUAGE_SIMILARITY[pair]

    reverse_pair = (required_skill, candidate_skill)

    if reverse_pair in LANGUAGE_SIMILARITY:
        return LANGUAGE_SIMILARITY[reverse_pair]

    return 0.0