import re


# ============================================================
# EDUCATION LEVELS
# ============================================================

EDUCATION_LEVELS = {

    "high_school": 1,

    "diploma": 2,

    "associate": 2,

    "bachelor": 3,

    "btech": 3,

    "be": 3,

    "bs": 3,

    "master": 4,

    "mtech": 4,

    "me": 4,

    "ms": 4,

    "mba": 4,

    "phd": 5,

    "doctorate": 5,
}


# ============================================================
# DETECT EDUCATION
# ============================================================

def detect_education_level(text):

    if not isinstance(text, str):
        return 0

    text = text.lower()

    detected_level = 0

    for education, level in EDUCATION_LEVELS.items():

        if re.search(
            r"\b"
            + re.escape(education)
            + r"\b",
            text
        ):

            detected_level = max(
                detected_level,
                level
            )

    return detected_level


# ============================================================
# EDUCATION FEATURES
# ============================================================

def calculate_education_features(
    resume,
    job_description
):

    resume_level = (
        detect_education_level(
            resume
        )
    )

    job_level = (
        detect_education_level(
            job_description
        )
    )

    if job_level == 0:

        education_match = 0.0

    else:

        education_match = (
            1.0
            if resume_level >= job_level
            else 0.0
        )

    return {

        "resume_education_level":
            resume_level,

        "job_education_level":
            job_level,

        "education_match":
            education_match
    }