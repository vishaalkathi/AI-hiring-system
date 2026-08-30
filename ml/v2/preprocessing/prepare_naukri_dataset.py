import pandas as pd
import re
from pathlib import Path


# ============================================================
# CONFIG
# ============================================================

INPUT_PATH = Path(
    "ml/data/processed/naukri_jobs_cleaned.csv"
)

OUTPUT_PATH = Path(
    "ml/data/processed/naukri_jobs_v2.csv"
)


# ============================================================
# HELPERS
# ============================================================

def clean_text(text):
    """
    Clean HTML and formatting artifacts while preserving
    useful job-description information.
    """

    if pd.isna(text):
        return ""

    text = str(text)

    # Convert HTML line breaks to spaces
    text = re.sub(r"<br\s*/?>", " ", text, flags=re.IGNORECASE)

    # Remove remaining HTML tags
    text = re.sub(r"<[^>]+>", " ", text)

    # Decode common HTML entities
    text = (
        text.replace("&nbsp;", " ")
            .replace("&amp;", "&")
            .replace("&lt;", "<")
            .replace("&gt;", ">")
            .replace("&quot;", '"')
    )

    # Normalize whitespace
    text = re.sub(r"\s+", " ", text)

    return text.strip()


def clean_skills(text):
    """
    Normalize job skills while preserving individual skills.
    """

    if pd.isna(text):
        return ""

    text = str(text)

    # Common separators → comma
    text = re.sub(r"[|;/]+", ",", text)

    # Normalize whitespace
    text = re.sub(r"\s+", " ", text)

    return text.strip()


# ============================================================
# LOAD
# ============================================================

print("=" * 70)
print("NAUKRI JOB DATA PREPARATION — V2")
print("=" * 70)

print("\nLoading dataset...")

df = pd.read_csv(INPUT_PATH)

print(f"Original rows   : {len(df)}")
print(f"Original columns : {len(df.columns)}")

print("\nColumns:")
print(df.columns.tolist())


# ============================================================
# REQUIRED COLUMNS
# ============================================================

required_columns = [
    "job_id",
    "job_title",
    "job_description",
    "job_skills",
    "experience"
]

missing_columns = [
    column
    for column in required_columns
    if column not in df.columns
]

if missing_columns:
    raise ValueError(
        f"Missing required columns: {missing_columns}"
    )


# ============================================================
# CLEAN TEXT
# ============================================================

text_columns = [
    "job_title",
    "job_description",
    "job_skills",
    "experience",
    "location",
    "company"
]

for column in text_columns:

    if column in df.columns:

        if column == "job_skills":
            df[column] = df[column].apply(clean_skills)

        else:
            df[column] = df[column].apply(clean_text)


# ============================================================
# REMOVE EMPTY JOBS
# ============================================================

empty_title = (
    df["job_title"].str.len() == 0
)

empty_description = (
    df["job_description"].str.len() == 0
)


print()
print("=" * 70)
print("EMPTY JOB ANALYSIS")
print("=" * 70)

print(
    f"Empty job titles       : "
    f"{empty_title.sum()}"
)

print(
    f"Empty job descriptions : "
    f"{empty_description.sum()}"
)


# ============================================================
# JOB DESCRIPTION LENGTH
# ============================================================

df["job_word_count"] = (
    df["job_description"]
    .str.split()
    .str.len()
)

print()
print("=" * 70)
print("JOB DESCRIPTION LENGTH")
print("=" * 70)

print(
    df["job_word_count"].describe()
)


# ============================================================
# REMOVE EXTREMELY LOW-INFORMATION JOBS
# ============================================================

# Unlike the previous dataset, we DO NOT want to throw away
# short descriptions automatically.
#
# Naukri sometimes stores useful requirements in job_skills
# and experience even when job_description is short.
#
# Therefore a job is considered unusable only if ALL of these
# are effectively empty/meaningless.

empty_skills = (
    df["job_skills"].str.len() == 0
)

empty_experience = (
    df["experience"].str.len() == 0
)

remove_mask = (
    empty_title
    |
    (
        empty_description
        & empty_skills
        & empty_experience
    )
)


print()
print("=" * 70)
print("REMOVAL ANALYSIS")
print("=" * 70)

print(
    f"Empty title                    : "
    f"{empty_title.sum()}"
)

print(
    f"Completely empty job           : "
    f"{(empty_description & empty_skills & empty_experience).sum()}"
)

print(
    f"Total rows marked for removal  : "
    f"{remove_mask.sum()}"
)

print(
    f"Rows remaining                 : "
    f"{(~remove_mask).sum()}"
)


# ============================================================
# DUPLICATES
# ============================================================

duplicate_mask = df.duplicated(
    subset=[
        "job_title",
        "job_description",
        "job_skills"
    ],
    keep="first"
)

print()
print("=" * 70)
print("DUPLICATES")
print("=" * 70)

print(
    f"Duplicate jobs: {duplicate_mask.sum()}"
)


# ============================================================
# FINAL CLEANING
# ============================================================

final_remove_mask = (
    remove_mask
    |
    duplicate_mask
)

clean_df = df.loc[
    ~final_remove_mask
].copy()


# ============================================================
# RESET INDEX
# ============================================================

clean_df.reset_index(
    drop=True,
    inplace=True
)


# ============================================================
# FINAL SUMMARY
# ============================================================

print()
print("=" * 70)
print("FINAL DATASET SUMMARY")
print("=" * 70)

print(
    f"Original rows : {len(df)}"
)

print(
    f"Cleaned rows  : {len(clean_df)}"
)

print(
    f"Removed rows  : {len(df) - len(clean_df)}"
)

print(
    f"Retention     : "
    f"{len(clean_df) / len(df) * 100:.2f}%"
)

print(
    f"Columns       : {len(clean_df.columns)}"
)


# ============================================================
# SAVE
# ============================================================

OUTPUT_PATH.parent.mkdir(
    parents=True,
    exist_ok=True
)

clean_df.to_csv(
    OUTPUT_PATH,
    index=False
)


print()
print("=" * 70)
print("PREPARATION COMPLETE")
print("=" * 70)

print(
    f"\nSaved to:\n{OUTPUT_PATH}"
)