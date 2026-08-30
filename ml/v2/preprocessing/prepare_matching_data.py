import pandas as pd
from pathlib import Path


# ============================================================
# CONFIG
# ============================================================

NAUKRI_PATH = Path(
    "ml/data/processed/naukri_jobs_v2.csv"
)

CANDIDATE_PATH = Path(
    "ml/data/processed/candidates_v2.csv"
)

NAUKRI_OUTPUT = Path(
    "ml/data/processed/naukri_matching_v2.csv"
)

CANDIDATE_OUTPUT = Path(
    "ml/data/processed/candidates_matching_v2.csv"
)


# ============================================================
# LOAD
# ============================================================

print("=" * 70)
print("PREPARING MATCHING DATA")
print("=" * 70)

print("\nLoading datasets...")

jobs = pd.read_csv(NAUKRI_PATH)
candidates = pd.read_csv(CANDIDATE_PATH)

print(f"Naukri jobs : {len(jobs)}")
print(f"Candidates  : {len(candidates)}")


# ============================================================
# NORMALIZE ROLE
# ============================================================

def normalize_role(value):

    if pd.isna(value):
        return ""

    return (
        str(value)
        .lower()
        .strip()
    )


jobs["normalized_role"] = (
    jobs["job_title"]
    .apply(normalize_role)
)

candidates["normalized_role"] = (
    candidates["job_role"]
    .apply(normalize_role)
)


# ============================================================
# NORMALIZE TEXT
# ============================================================

for column in [
    "job_title",
    "job_description",
    "job_skills"
]:

    jobs[column] = (
        jobs[column]
        .fillna("")
        .astype(str)
        .str.strip()
    )


for column in [
    "candidate_resume",
    "normalized_resume"
]:

    candidates[column] = (
        candidates[column]
        .fillna("")
        .astype(str)
        .str.strip()
    )


# ============================================================
# REMOVE EMPTY JOBS
# ============================================================

before = len(jobs)

jobs = jobs[
    (jobs["normalized_role"] != "")
    &
    (jobs["job_description"].str.len() > 0)
].copy()

print(
    f"\nRemoved empty jobs: "
    f"{before - len(jobs)}"
)


# ============================================================
# REMOVE EMPTY CANDIDATES
# ============================================================

before = len(candidates)

candidates = candidates[
    candidates["normalized_resume"].str.len() > 0
].copy()

print(
    f"Removed empty candidates: "
    f"{before - len(candidates)}"
)


# ============================================================
# SAVE
# ============================================================

NAUKRI_OUTPUT.parent.mkdir(
    parents=True,
    exist_ok=True
)

jobs.to_csv(
    NAUKRI_OUTPUT,
    index=False
)

candidates.to_csv(
    CANDIDATE_OUTPUT,
    index=False
)


# ============================================================
# SUMMARY
# ============================================================

print()
print("=" * 70)
print("PREPARATION COMPLETE")
print("=" * 70)

print(
    f"\nJobs saved       : {len(jobs)}"
)

print(
    f"Candidates saved : {len(candidates)}"
)

print(
    f"\nJobs → {NAUKRI_OUTPUT}"
)

print(
    f"Candidates → {CANDIDATE_OUTPUT}"
)