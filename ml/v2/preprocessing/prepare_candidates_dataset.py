import pandas as pd
from pathlib import Path


# ============================================================
# CONFIG
# ============================================================

INPUT_PATH = Path(
    "ml/data/processed/technical_normalized_dataset.csv"
)

OUTPUT_PATH = Path(
    "ml/data/processed/candidates_v2.csv"
)


# ============================================================
# LOAD
# ============================================================

print("=" * 70)
print("CANDIDATE DATA PREPARATION — V2")
print("=" * 70)

df = pd.read_csv(INPUT_PATH)

print(f"\nOriginal rows: {len(df)}")


# ============================================================
# KEEP ONLY REAL CANDIDATE DATA
# ============================================================

df = df[
    df["source_dataset"] == "recruiter_decision"
].copy()

print(
    f"Job applicant rows: {len(df)}"
)


# ============================================================
# SELECT COLUMNS
# ============================================================

candidate_df = df[
    [
        "candidate_resume",
        "job_role",
        "normalized_resume",
        "normalized_job_role"
    ]
].copy()


# ============================================================
# CLEAN
# ============================================================

for column in candidate_df.columns:

    candidate_df[column] = (
        candidate_df[column]
        .fillna("")
        .astype(str)
        .str.strip()
    )


# ============================================================
# REMOVE EMPTY RESUMES
# ============================================================

empty_resume = (
    candidate_df["normalized_resume"].str.len() == 0
)

print(
    f"Empty resumes: {empty_resume.sum()}"
)

candidate_df = candidate_df[
    ~empty_resume
].copy()


# ============================================================
# REMOVE DUPLICATES
# ============================================================

duplicate_mask = candidate_df.duplicated(
    subset=["normalized_resume"],
    keep="first"
)

print(
    f"Duplicate resumes: {duplicate_mask.sum()}"
)

candidate_df = candidate_df[
    ~duplicate_mask
].copy()


# ============================================================
# RESUME LENGTH
# ============================================================

candidate_df["resume_word_count"] = (
    candidate_df["normalized_resume"]
    .str.split()
    .str.len()
)


# ============================================================
# REMOVE EXTREMELY SHORT RESUMES
# ============================================================

short_resume = (
    candidate_df["resume_word_count"] < 20
)

print(
    f"Very short resumes (<20 words): "
    f"{short_resume.sum()}"
)

candidate_df = candidate_df[
    ~short_resume
].copy()


# ============================================================
# RESET INDEX
# ============================================================

candidate_df.reset_index(
    drop=True,
    inplace=True
)


# ============================================================
# ADD CANDIDATE ID
# ============================================================

candidate_df.insert(
    0,
    "candidate_id",
    range(1, len(candidate_df) + 1)
)


# ============================================================
# SUMMARY
# ============================================================

print()
print("=" * 70)
print("FINAL CANDIDATE DATASET")
print("=" * 70)

print(
    f"Candidates: {len(candidate_df)}"
)

print(
    "\nRole distribution:"
)

print(
    candidate_df["job_role"]
    .value_counts()
    .head(20)
)


# ============================================================
# SAVE
# ============================================================

OUTPUT_PATH.parent.mkdir(
    parents=True,
    exist_ok=True
)

candidate_df.to_csv(
    OUTPUT_PATH,
    index=False
)

print()
print("=" * 70)
print("CANDIDATE PREPARATION COMPLETE")
print("=" * 70)

print(
    f"\nSaved to:\n{OUTPUT_PATH}"
)