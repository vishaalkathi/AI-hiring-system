import re


# ============================================================
# SKILL ALIASES
# ============================================================

SKILL_ALIASES = {

    # -------------------------
    # Programming languages
    # -------------------------
    "c plus plus": "c++",
    "cpp": "c++",
    "c/c++": "c++",

    "javascript": "javascript",
    "js": "javascript",

    "typescript": "typescript",
    "ts": "typescript",

    "python3": "python",
    "python 3": "python",

    "c sharp": "c#",
    "c-sharp": "c#",

    "golang": "go",

    # -------------------------
    # Java ecosystem
    # -------------------------
    "j2ee": "java ee",
    "java ee": "java ee",
    "springboot": "spring boot",
    "spring-boot": "spring boot",

    # -------------------------
    # Frontend
    # -------------------------
    "reactjs": "react",
    "react.js": "react",
    "react js": "react",

    "angularjs": "angular",
    "angular.js": "angular",

    "vuejs": "vue",
    "vue.js": "vue",

    "nodejs": "node.js",
    "node js": "node.js",

    "nextjs": "next.js",
    "next js": "next.js",

    # -------------------------
    # Databases
    # -------------------------
    "postgres": "postgresql",
    "postgre": "postgresql",

    "mongo": "mongodb",

    "mysql database": "mysql",

    # -------------------------
    # Cloud
    # -------------------------
    "amazon web services": "aws",
    "amazon aws": "aws",

    "microsoft azure": "azure",

    "google cloud platform": "gcp",
    "google cloud": "gcp",

    # -------------------------
    # DevOps
    # -------------------------
    "k8s": "kubernetes",

    "ci/cd": "ci cd",
    "cicd": "ci cd",
    "continuous integration": "ci cd",
    "continuous integration and deployment": "ci cd",

    # -------------------------
    # Machine Learning
    # -------------------------
    "ml": "machine learning",
    "ai": "artificial intelligence",

    "deep-learning": "deep learning",

    "tensorflow": "tensorflow",
    "pytorch": "pytorch",

    # -------------------------
    # DSA
    # -------------------------
    "data structures and algorithms": "data structures",
    "data structure and algorithms": "data structures",
    "dsa": "data structures",

    # -------------------------
    # APIs
    # -------------------------
    "restful api": "rest api",
    "restful apis": "rest api",
    "rest apis": "rest api",

    # -------------------------
    # Operating systems
    # -------------------------
    "unix": "unix/linux",
    "linux/unix": "unix/linux",

    # -------------------------
    # Version control
    # -------------------------
    "github": "git",
}


# ============================================================
# NORMALIZE ONE SKILL
# ============================================================

def normalize_skill(skill: str) -> str:

    if not isinstance(skill, str):
        return ""

    skill = skill.lower().strip()

    # Remove bullets / weird punctuation
    skill = re.sub(r"^[\-\*\•\s]+", "", skill)
    skill = re.sub(r"\s+", " ", skill)

    # Normalize separators
    skill = skill.replace("_", " ")
    skill = skill.strip(" ,.;:()[]{}")

    # Alias replacement
    if skill in SKILL_ALIASES:
        skill = SKILL_ALIASES[skill]

    return skill


# ============================================================
# NORMALIZE SKILL LIST
# ============================================================

def normalize_skills(skills):

    if not skills:
        return []

    normalized = []

    for skill in skills:

        skill = normalize_skill(skill)

        if skill and skill not in normalized:
            normalized.append(skill)

    return normalized