import re


# ============================================================
# SKILL VOCABULARY
# ============================================================

SKILLS = {

    # Programming
    "python",
    "java",
    "c",
    "c++",
    "c#",
    "javascript",
    "typescript",
    "go",
    "golang",
    "rust",

    # Backend
    "fastapi",
    "django",
    "flask",
    "spring",
    "spring boot",
    "node.js",
    "nodejs",

    # Frontend
    "react",
    "angular",
    "vue",

    # Databases
    "sql",
    "mysql",
    "postgresql",
    "mongodb",
    "oracle",
    "redis",

    # Cloud
    "aws",
    "azure",
    "gcp",
    "docker",
    "kubernetes",

    # AI / ML
    "machine learning",
    "deep learning",
    "tensorflow",
    "pytorch",
    "scikit-learn",
    "nlp",
    "computer vision",

    # Core CS
    "data structures",
    "algorithms",
    "operating systems",
    "computer networks",
    "dbms",
    "oop",

    # Tools
    "git",
    "github",
    "linux",

    # Other
    "robotics",
    "ros",
    "embedded systems",
    "firmware",
    "vlsi",
    "fpga",
    "cybersecurity",
}


# ============================================================
# NORMALIZE
# ============================================================

def normalize_skill(skill):

    return skill.lower().strip()


# ============================================================
# EXTRACT SKILLS
# ============================================================

def extract_skills(text):

    if not isinstance(text, str):
        return set()

    text = text.lower()

    found = set()

    for skill in SKILLS:

        pattern = (
            r"(?<!\w)"
            + re.escape(skill)
            + r"(?!\w)"
        )

        if re.search(
            pattern,
            text
        ):

            found.add(
                skill
            )

    return found


# ============================================================
# SKILL MATCH
# ============================================================

def calculate_skill_features(
    resume,
    job_description
):

    resume_skills = extract_skills(
        resume
    )

    job_skills = extract_skills(
        job_description
    )

    if not job_skills:

        return {
            "resume_skill_count":
                len(resume_skills),

            "job_skill_count":
                0,

            "matched_skill_count":
                0,

            "skill_match_ratio":
                0.0,

            "skill_coverage":
                0.0,
        }

    matched = (
        resume_skills &
        job_skills
    )

    return {

        "resume_skill_count":
            len(resume_skills),

        "job_skill_count":
            len(job_skills),

        "matched_skill_count":
            len(matched),

        "skill_match_ratio":
            len(matched)
            /
            len(job_skills),

        "skill_coverage":
            len(matched)
            /
            max(len(resume_skills), 1)
    }