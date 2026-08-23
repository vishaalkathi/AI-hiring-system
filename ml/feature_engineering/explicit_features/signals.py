import re


# ============================================================
# DEGREE SIGNALS
# ============================================================

DEGREE_KEYWORDS = {

    "bachelor",
    "btech",
    "be",
    "bs",

    "master",
    "mtech",
    "me",
    "ms",

    "phd",
    "doctorate"
}


# ============================================================
# CORE CS SIGNALS
# ============================================================

CORE_CS_KEYWORDS = {

    "data structures",
    "algorithms",
    "operating systems",
    "computer networks",
    "database",
    "dbms",
    "object oriented",
    "oop",
    "computer architecture"
}


# ============================================================
# TEXT SIGNAL
# ============================================================

def keyword_count(
    text,
    keywords
):

    if not isinstance(text, str):
        return 0

    text = text.lower()

    count = 0

    for keyword in keywords:

        if re.search(
            r"(?<!\w)"
            + re.escape(keyword)
            + r"(?!\w)",
            text
        ):

            count += 1

    return count


# ============================================================
# SIGNAL FEATURES
# ============================================================

def calculate_signal_features(
    resume,
    job_description
):

    return {

        "resume_core_cs_count":
            keyword_count(
                resume,
                CORE_CS_KEYWORDS
            ),

        "job_core_cs_count":
            keyword_count(
                job_description,
                CORE_CS_KEYWORDS
            ),

        "resume_degree_count":
            keyword_count(
                resume,
                DEGREE_KEYWORDS
            ),

        "job_degree_count":
            keyword_count(
                job_description,
                DEGREE_KEYWORDS
            ),

        "resume_length":
            len(resume)
            if isinstance(resume, str)
            else 0,

        "job_description_length":
            len(job_description)
            if isinstance(job_description, str)
            else 0,

        "resume_word_count":
            len(resume.split())
            if isinstance(resume, str)
            else 0,

        "job_word_count":
            len(job_description.split())
            if isinstance(job_description, str)
            else 0
    }