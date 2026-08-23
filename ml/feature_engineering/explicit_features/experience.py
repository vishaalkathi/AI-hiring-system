import re


# ============================================================
# EXPERIENCE EXTRACTION
# ============================================================

def extract_years_experience(
    text
):

    if not isinstance(text, str):
        return 0.0

    text = text.lower()

    patterns = [

        r"(\d+(?:\.\d+)?)\+?\s*years?\s+(?:of\s+)?experience",

        r"(\d+(?:\.\d+)?)\+?\s*years?\s+in\s+the\s+field",

        r"experience\s+of\s+(\d+(?:\.\d+)?)\+?\s*years?"
    ]

    values = []

    for pattern in patterns:

        matches = re.findall(
            pattern,
            text
        )

        for match in matches:

            try:

                values.append(
                    float(match)
                )

            except ValueError:
                pass

    if not values:
        return 0.0

    return max(values)


# ============================================================
# EXPERIENCE FEATURES
# ============================================================

def calculate_experience_features(
    resume,
    job_description
):

    resume_years = (
        extract_years_experience(
            resume
        )
    )

    job_years = (
        extract_years_experience(
            job_description
        )
    )

    if job_years == 0:

        experience_match = 1.0

    else:

        experience_match = min(
            resume_years / job_years,
            1.0
        )

    return {

        "resume_experience_years":
            resume_years,

        "job_required_experience_years":
            job_years,

        "experience_match":
            experience_match
    }