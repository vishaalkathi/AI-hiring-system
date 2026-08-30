from pathlib import Path

import joblib
import pandas as pd


# ============================================================
# PATHS
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parents[3]

MODEL_PATH = (
    PROJECT_ROOT
    / "ml"
    / "v2"
    / "models"
    / "job_matcher.joblib"
)

VECTORIZER_PATH = (
    PROJECT_ROOT
    / "ml"
    / "v2"
    / "models"
    / "tfidf_vectorizer.joblib"
)


# ============================================================
# FEATURE ORDER
# ============================================================

FEATURES = [
    "job_skill_coverage",
    "skill_jaccard",
    "role_similarity",
    "text_similarity",
    "skill_overlap_count",
    "skill_overlap_ratio",
    "candidate_skill_coverage",
    "candidate_experience",
    "experience_gap",

    "github_public_repos",
    "github_followers",
    "github_total_stars",
    "github_language_diversity",
    "github_active_repos",

    "leetcode_total_solved",
    "leetcode_easy",
    "leetcode_medium",
    "leetcode_hard",
    "leetcode_contest_rating",
    "leetcode_contest_percentile",
    "leetcode_contests_attended",
    "leetcode_streak",
    "leetcode_active_days",

    "dp_strength",
    "graph_strength",
    "greedy_strength",
    "tree_strength",
    "binary_search_strength",
]


# ============================================================
# LOAD MODEL + VECTORIZER ONCE
# ============================================================

if not MODEL_PATH.exists():
    raise FileNotFoundError(
        f"XGBoost model not found at:\n{MODEL_PATH}"
    )

if not VECTORIZER_PATH.exists():
    raise FileNotFoundError(
        f"TF-IDF vectorizer not found at:\n{VECTORIZER_PATH}"
    )


model = joblib.load(MODEL_PATH)
vectorizer = joblib.load(VECTORIZER_PATH)


# ============================================================
# TEXT SIMILARITY
# ============================================================

def calculate_text_similarity(
    resume: str,
    job_description: str,
) -> float:

    resume = "" if resume is None else str(resume)
    job_description = (
        ""
        if job_description is None
        else str(job_description)
    )

    vectors = vectorizer.transform([
        resume,
        job_description,
    ])

    similarity = (
        vectors[0] @ vectors[1].T
    ).toarray()[0][0]

    return float(similarity)


# ============================================================
# PREDICTION
# ============================================================

def predict_match(features: dict) -> dict:

    row = {
        feature: features.get(feature, 0)
        for feature in FEATURES
    }

    X = pd.DataFrame(
        [row],
        columns=FEATURES,
    )

    prediction = float(
        model.predict(X)[0]
    )

    # Relevance score is 0–11
    prediction = max(
        0.0,
        min(11.0, prediction)
    )

    return {
        "relevance_score": round(
            prediction,
            2
        ),
        "fit_level": get_fit_level(
            prediction
        ),
    }


# ============================================================
# FIT LEVEL
# ============================================================

def get_fit_level(score: float) -> str:

    if score < 2:
        return "Very Poor"

    if score < 4:
        return "Poor"

    if score < 6:
        return "Fair"

    if score < 8:
        return "Good"

    if score < 10:
        return "Very Good"

    return "Excellent"