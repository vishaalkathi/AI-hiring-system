import ast
import re
import numpy as np
import pandas as pd

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


# ============================================================
# HELPERS
# ============================================================

def parse_skills(value):
    """
    Convert skills stored as:
        ['python', 'java']
    or
        "['python', 'java']"
    or
        "python,java"
    into a normalized Python set.
    """

    if pd.isna(value):
        return set()

    if isinstance(value, list):
        skills = value

    else:
        value = str(value).strip()

        try:
            parsed = ast.literal_eval(value)

            if isinstance(parsed, list):
                skills = parsed
            else:
                skills = [value]

        except (ValueError, SyntaxError):
            skills = value.split(",")

    return {
        str(skill).strip().lower()
        for skill in skills
        if str(skill).strip()
    }


def normalize_text(text):
    if pd.isna(text):
        return ""

    text = str(text).lower()

    text = re.sub(r"[^a-z0-9+#.\-/ ]+", " ", text)

    text = re.sub(r"\s+", " ", text).strip()

    return text


# ============================================================
# ROLE SIMILARITY
# ============================================================

def role_similarity(candidate_role, job_title):
    """
    Simple lexical similarity between candidate role and job title.
    """

    candidate_role = normalize_text(candidate_role)
    job_title = normalize_text(job_title)

    if not candidate_role or not job_title:
        return 0.0

    candidate_tokens = set(candidate_role.split())
    job_tokens = set(job_title.split())

    intersection = candidate_tokens & job_tokens
    union = candidate_tokens | job_tokens

    if not union:
        return 0.0

    return len(intersection) / len(union)


# ============================================================
# SKILL FEATURES
# ============================================================

def calculate_skill_features(candidate_skills, job_skills):

    candidate_skills = parse_skills(candidate_skills)
    job_skills = parse_skills(job_skills)

    if not candidate_skills or not job_skills:
        return {
            "skill_overlap_count": 0,
            "skill_overlap_ratio": 0.0,
            "candidate_skill_coverage": 0.0,
            "job_skill_coverage": 0.0,
            "skill_jaccard": 0.0,
        }

    overlap = candidate_skills & job_skills
    union = candidate_skills | job_skills

    overlap_count = len(overlap)

    # Fraction of job requirements candidate satisfies
    job_coverage = overlap_count / len(job_skills)

    # Fraction of candidate skills that are relevant
    candidate_coverage = overlap_count / len(candidate_skills)

    # Jaccard similarity
    jaccard = overlap_count / len(union)

    return {
        "skill_overlap_count": overlap_count,
        "skill_overlap_ratio": job_coverage,
        "candidate_skill_coverage": candidate_coverage,
        "job_skill_coverage": job_coverage,
        "skill_jaccard": jaccard,
    }


# ============================================================
# EXPERIENCE
# ============================================================

def extract_years_from_experience(text):
    """
    Extract approximate maximum years of experience
    mentioned in a resume.
    """

    if pd.isna(text):
        return 0.0

    text = str(text).lower()

    patterns = [
        r"(\d+(?:\.\d+)?)\s*\+?\s*years?\s+of\s+experience",
        r"(\d+(?:\.\d+)?)\s*\+?\s*years?\s+experience",
    ]

    values = []

    for pattern in patterns:

        matches = re.findall(pattern, text)

        for match in matches:
            try:
                values.append(float(match))
            except ValueError:
                pass

    if not values:
        return 0.0

    return max(values)


def extract_min_experience(text):
    """
    Extract minimum experience from job experience field.

    Examples:
        2-5 Yrs -> 2
        3-8 Yrs -> 3
        5+ Yrs  -> 5
    """

    if pd.isna(text):
        return 0.0

    text = str(text).lower()

    match = re.search(r"(\d+(?:\.\d+)?)", text)

    if match:
        return float(match.group(1))

    return 0.0


# ============================================================
# LABEL GENERATION
# ============================================================
def generate_relevance_score(row):
    """
    Weak-supervision relevance score for candidate-job matching.

    Returns a score from 0 to 11.
    Higher score = stronger evidence of candidate-job compatibility.
    """

    job_family = str(row["job_role_family"]).lower().strip()
    candidate_family = str(row["candidate_role_family"]).lower().strip()

    skill_coverage = float(row["job_skill_coverage"])
    jaccard = float(row["skill_jaccard"])
    role_sim = float(row["role_similarity"])
    text_sim = float(row["text_similarity"])

    same_family = job_family == candidate_family

    score = 0

    # Skill coverage: 0-3
    if skill_coverage >= 0.50:
        score += 3
    elif skill_coverage >= 0.25:
        score += 2
    elif skill_coverage >= 0.10:
        score += 1

    # Skill Jaccard: 0-2
    if jaccard >= 0.25:
        score += 2
    elif jaccard >= 0.10:
        score += 1

    # Role similarity: 0-3
    if role_sim >= 0.50:
        score += 3
    elif role_sim >= 0.25:
        score += 2
    elif role_sim >= 0.15:
        score += 1

    # Text similarity: 0-2
    if text_sim >= 0.20:
        score += 2
    elif text_sim >= 0.10:
        score += 1

    # Role family: 0-1
    if same_family:
        score += 1

    return score

def generate_label(row):
    """
    Weak-supervision label for candidate-job matching.

    Role family is used ONLY for label generation.
    It is NOT used as a model feature.

    The label is based on multiple independent signals:
        - skill coverage
        - skill Jaccard
        - role similarity
        - text similarity
        - role-family compatibility
    """

    job_family = str(row["job_role_family"]).lower().strip()
    candidate_family = str(row["candidate_role_family"]).lower().strip()

    skill_coverage = float(row["job_skill_coverage"])
    jaccard = float(row["skill_jaccard"])
    role_sim = float(row["role_similarity"])
    text_sim = float(row["text_similarity"])

    same_family = job_family == candidate_family

    # --------------------------------------------------------
    # Evidence score
    # --------------------------------------------------------

    score = 0.0

    # Skill evidence
    if skill_coverage >= 0.50:
        score += 3
    elif skill_coverage >= 0.25:
        score += 2
    elif skill_coverage >= 0.10:
        score += 1

    # Jaccard evidence
    if jaccard >= 0.25:
        score += 2
    elif jaccard >= 0.10:
        score += 1

    # Role/title evidence
    if role_sim >= 0.50:
        score += 3
    elif role_sim >= 0.25:
        score += 2
    elif role_sim >= 0.15:
        score += 1

    # Text evidence
    if text_sim >= 0.20:
        score += 2
    elif text_sim >= 0.10:
        score += 1

    # --------------------------------------------------------
    # Role family bonus
    # --------------------------------------------------------

    if same_family:
        score += 1

    # --------------------------------------------------------
    # Positive label
    # --------------------------------------------------------

    return int(score >= 4)

# ============================================================
# MAIN FEATURE GENERATION
# ============================================================

def generate_features(pairs):

    pairs = pairs.copy()

    print("Generating features...")
    print(f"Pairs: {len(pairs)}")

    # --------------------------------------------------------
    # Skill features
    # --------------------------------------------------------

    skill_features = pairs.apply(
        lambda row: calculate_skill_features(
            row["candidate_skills"],
            row["job_skills"],
        ),
        axis=1,
        result_type="expand",
    )

    pairs = pd.concat(
        [pairs, skill_features],
        axis=1,
    )

    # --------------------------------------------------------
    # Role similarity
    # --------------------------------------------------------

    pairs["role_similarity"] = pairs.apply(
        lambda row: role_similarity(
            row["candidate_role"],
            row["job_title"],
        ),
        axis=1,
    )

    # --------------------------------------------------------
    # Experience
    # --------------------------------------------------------

    pairs["candidate_experience"] = pairs[
        "resume"
    ].apply(extract_years_from_experience)

    pairs["required_experience"] = 0.0

    pairs["experience_gap"] = (
        pairs["candidate_experience"]
        - pairs["required_experience"]
    )
    # --------------------------------------------------------
    # TF-IDF resume ↔ job description
    # --------------------------------------------------------

    print("Computing TF-IDF text similarity...")

    resume_text = pairs["resume"].fillna("").apply(normalize_text)
    job_text = pairs["job_description"].fillna("").apply(normalize_text)

    vectorizer = TfidfVectorizer(
        max_features=10000,
        ngram_range=(1, 2),
        min_df=2,
    )

    combined_text = pd.concat(
        [resume_text, job_text],
        ignore_index=True,
    )

    tfidf = vectorizer.fit_transform(combined_text)
    
    # --------------------------------------------------------
    # SAVE FITTED TF-IDF VECTORIZER
    # --------------------------------------------------------

    import joblib
    from pathlib import Path

    # feature_generation.py is inside ml/v2/
    V2_DIR = Path(__file__).resolve().parent

    VECTORIZER_PATH = (
        V2_DIR
        / "models"
        / "tfidf_vectorizer.joblib"
    )

    VECTORIZER_PATH.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    joblib.dump(
        vectorizer,
        VECTORIZER_PATH
    )

    print(
        f"TF-IDF vectorizer saved to:\n{VECTORIZER_PATH}"
    )

    n = len(pairs)

    resume_vectors = tfidf[:n]
    job_vectors = tfidf[n:]

    similarities = cosine_similarity(
        resume_vectors,
        job_vectors,
    ).diagonal()

    pairs["text_similarity"] = similarities

    # --------------------------------------------------------
    # Labels
    # --------------------------------------------------------

    print("Generating labels...")

    pairs["label"] = pairs.apply(
        generate_label,
        axis=1,
    )
    # --------------------------------------------------------
    # Labels / relevance target
    # --------------------------------------------------------

    print("Generating relevance scores...")

    pairs["relevance_score"] = pairs.apply(
        generate_relevance_score,
        axis=1,
    )

    return pairs