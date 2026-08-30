import pandas as pd
from pathlib import Path


# ============================================================
# CONFIG
# ============================================================

INPUT_PATH = Path(
    "ml/data/processed/technical_normalized_dataset.csv"
)

OUTPUT_PATH = Path(
    "ml/data/processed/technical_normalized_dataset_v2.csv"
)

MIN_JOB_WORDS = 25


# ============================================================
# LOAD DATA
# ============================================================

print("=" * 70)
print("TECHNICAL DATASET CLEANING — V2")
print("=" * 70)

print("\nLoading dataset...")

df = pd.read_csv(INPUT_PATH)

print(f"Original rows: {len(df)}")
print(f"Original columns: {len(df.columns)}")


# ============================================================
# INITIAL CLEANING
# ============================================================

text_columns = [
    "candidate_resume",
    "job_role",
    "job_description",
    "normalized_resume",
    "normalized_job_description",
    "normalized_job_role"
]

for column in text_columns:

    df[column] = (
        df[column]
        .fillna("")
        .astype(str)
        .str.strip()
    )


# ============================================================
# QUALITY ANALYSIS
# ============================================================

print()
print("=" * 70)
print("QUALITY ANALYSIS")
print("=" * 70)


# ------------------------------------------------------------
# 1. EMPTY RESUMES
# ------------------------------------------------------------

empty_resume = (
    df["normalized_resume"].str.len() == 0
)

print(
    f"\nEmpty resumes: "
    f"{empty_resume.sum()} "
    f"({empty_resume.mean() * 100:.2f}%)"
)


# ------------------------------------------------------------
# 2. EMPTY JOB DESCRIPTIONS
# ------------------------------------------------------------

empty_job_description = (
    df["normalized_job_description"].str.len() == 0
)

print(
    f"Empty job descriptions: "
    f"{empty_job_description.sum()} "
    f"({empty_job_description.mean() * 100:.2f}%)"
)


# ------------------------------------------------------------
# 3. EMPTY JOB ROLES
# ------------------------------------------------------------

empty_job_role = (
    df["normalized_job_role"].str.len() == 0
)

print(
    f"Empty job roles: "
    f"{empty_job_role.sum()} "
    f"({empty_job_role.mean() * 100:.2f}%)"
)


# ------------------------------------------------------------
# 4. JOB DESCRIPTION LENGTH
# ------------------------------------------------------------

job_word_count = (
    df["normalized_job_description"]
    .str.split()
    .str.len()
)

short_job_15 = job_word_count < 15
short_job_25 = job_word_count < MIN_JOB_WORDS

print(
    f"\nJob descriptions < 15 words: "
    f"{short_job_15.sum()} "
    f"({short_job_15.mean() * 100:.2f}%)"
)

print(
    f"Job descriptions < {MIN_JOB_WORDS} words: "
    f"{short_job_25.sum()} "
    f"({short_job_25.mean() * 100:.2f}%)"
)


# ------------------------------------------------------------
# 5. DUPLICATE RECORDS
# ------------------------------------------------------------

duplicate_rows = df.duplicated(
    subset=[
        "normalized_resume",
        "normalized_job_description",
        "label"
    ],
    keep="first"
)

print(
    f"\nDuplicate resume-job-label rows: "
    f"{duplicate_rows.sum()} "
    f"({duplicate_rows.mean() * 100:.2f}%)"
)


# ============================================================
# CLEANING RULES
# ============================================================

# IMPORTANT:
#
# We deliberately DO NOT use:
#
#   job_skill_count
#   matched_skill_count
#   skill_match_ratio
#   education features
#   experience features
#
# because those are extracted features.
#
# Cleaning should be based on the original dataset quality,
# not on whether our feature extractor happened to work.


remove_mask = (
    empty_resume
    |
    empty_job_description
    |
    empty_job_role
    |
    short_job_25
    |
    duplicate_rows
)


# ============================================================
# REMOVAL ANALYSIS
# ============================================================

print()
print("=" * 70)
print("REMOVAL ANALYSIS")
print("=" * 70)


# ------------------------------------------------------------
# Individual removal reasons
# ------------------------------------------------------------

print(
    f"\nEmpty resume: "
    f"{empty_resume.sum()}"
)

print(
    f"Empty job description: "
    f"{empty_job_description.sum()}"
)

print(
    f"Empty job role: "
    f"{empty_job_role.sum()}"
)

print(
    f"Short job description (< {MIN_JOB_WORDS} words): "
    f"{short_job_25.sum()}"
)

print(
    f"Duplicate rows: "
    f"{duplicate_rows.sum()}"
)

print(
    f"\nTotal rows marked for removal: "
    f"{remove_mask.sum()}"
)

print(
    f"Rows remaining: "
    f"{(~remove_mask).sum()}"
)


# ============================================================
# INSPECT REMOVED ROWS
# ============================================================

unreliable_rows = df[remove_mask]

print()
print("=" * 70)
print("EXAMPLES OF REMOVED ROWS")
print("=" * 70)

for idx, row in unreliable_rows.head(20).iterrows():

    print("-" * 70)

    print(f"ROW: {idx}")

    print(
        f"SOURCE: "
        f"{row['source_dataset']}"
    )

    print(
        f"ROLE: "
        f"{row['job_role']}"
    )

    print(
        f"JOB WORDS: "
        f"{job_word_count.loc[idx]}"
    )

    print(
        f"JOB DESCRIPTION:\n"
        f"{row['job_description']}"
    )


# ============================================================
# CREATE V2 DATASET
# ============================================================

clean_df = df.loc[
    ~remove_mask
].copy()


# ============================================================
# RESET INDEX
# ============================================================

clean_df.reset_index(
    drop=True,
    inplace=True
)


# ============================================================
# LABEL DISTRIBUTION
# ============================================================

print()
print("=" * 70)
print("LABEL DISTRIBUTION")
print("=" * 70)


original_label_distribution = (
    df["label"]
    .value_counts(normalize=True)
    .sort_index()
    .mul(100)
    .round(2)
)

cleaned_label_distribution = (
    clean_df["label"]
    .value_counts(normalize=True)
    .sort_index()
    .mul(100)
    .round(2)
)


print("\nOriginal:")

print(
    original_label_distribution
)


print("\nCleaned:")

print(
    cleaned_label_distribution
)


# ============================================================
# SOURCE DISTRIBUTION
# ============================================================

print()
print("=" * 70)
print("SOURCE DISTRIBUTION")
print("=" * 70)


original_source_distribution = (
    df["source_dataset"]
    .value_counts()
)


cleaned_source_distribution = (
    clean_df["source_dataset"]
    .value_counts()
)


print("\nOriginal:")

print(
    original_source_distribution
)


print("\nCleaned:")

print(
    cleaned_source_distribution
)


# ============================================================
# SOURCE LABEL DISTRIBUTION
# ============================================================

print()
print("=" * 70)
print("LABEL DISTRIBUTION BY SOURCE")
print("=" * 70)


original_source_labels = (
    df.groupby("source_dataset")["label"]
    .value_counts(normalize=True)
    .unstack(fill_value=0)
    .round(3)
)


cleaned_source_labels = (
    clean_df.groupby("source_dataset")["label"]
    .value_counts(normalize=True)
    .unstack(fill_value=0)
    .round(3)
)


print("\nOriginal:")

print(
    original_source_labels
)


print("\nCleaned:")

print(
    cleaned_source_labels
)


# ============================================================
# JOB DESCRIPTION STATISTICS
# ============================================================

print()
print("=" * 70)
print("JOB DESCRIPTION STATISTICS")
print("=" * 70)


original_job_stats = (
    job_word_count
    .agg([
        "count",
        "mean",
        "median",
        "std",
        "min",
        "max"
    ])
    .round(2)
)


cleaned_job_word_count = (
    clean_df["normalized_job_description"]
    .str.split()
    .str.len()
)


cleaned_job_stats = (
    cleaned_job_word_count
    .agg([
        "count",
        "mean",
        "median",
        "std",
        "min",
        "max"
    ])
    .round(2)
)


print("\nOriginal:")

print(
    original_job_stats
)


print("\nCleaned:")

print(
    cleaned_job_stats
)


# ============================================================
# FINAL DATASET SUMMARY
# ============================================================

print()
print("=" * 70)
print("FINAL DATASET SUMMARY")
print("=" * 70)


print(
    f"\nOriginal rows : "
    f"{len(df)}"
)

print(
    f"Cleaned rows  : "
    f"{len(clean_df)}"
)

print(
    f"Removed rows  : "
    f"{len(df) - len(clean_df)}"
)

print(
    f"Retention     : "
    f"{len(clean_df) / len(df) * 100:.2f}%"
)

print(
    f"Columns       : "
    f"{len(clean_df.columns)}"
)


# ============================================================
# SAVE V2
# ============================================================

OUTPUT_PATH.parent.mkdir(
    parents=True,
    exist_ok=True
)

clean_df.to_csv(
    OUTPUT_PATH,
    index=False
)


# ============================================================
# COMPLETE
# ============================================================

print()
print("=" * 70)
print("CLEANING COMPLETE")
print("=" * 70)

print(
    f"\nSaved V2 dataset to:"
)

print(
    OUTPUT_PATH
)