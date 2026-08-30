import pandas as pd
import numpy as np
from pathlib import Path

# ============================================================
# CONFIG
# ============================================================

BASE_DIR = Path(__file__).resolve().parents[2]

JOB_PATH = BASE_DIR / "data" / "processed" / "naukri_jobs_matching_v2_1000.csv"
CANDIDATE_PATH = BASE_DIR / "data" / "processed" / "candidates_matching_v2.csv"

OUTPUT_PATH = BASE_DIR / "data" / "processed" / "job_candidate_pairs_v2.csv"

PAIRS_PER_JOB = 50
RANDOM_SEED = 42

np.random.seed(RANDOM_SEED)


# ============================================================
# LOAD
# ============================================================

print("=" * 70)
print("GENERATING JOB-CANDIDATE PAIRS")
print("=" * 70)

jobs = pd.read_csv(JOB_PATH)
candidates = pd.read_csv(CANDIDATE_PATH)

print(f"\nJobs       : {len(jobs)}")
print(f"Candidates : {len(candidates)}")


# ============================================================
# FAMILY COMPATIBILITY
# ============================================================

# Families that are reasonably compatible with each other.
#
# This is NOT the final matching score.
# It only helps us create a realistic training dataset.

COMPATIBLE_FAMILIES = {
    "software": [
        "software",
        "mobile",
        "game",
        "data",
        "devops_cloud",
        "database",
        "qa",
        "ar_vr",
    ],

    "data": [
        "data",
        "ml_ai",
        "software",
        "business",
        "database",
        "devops_cloud",
    ],

    "ml_ai": [
        "ml_ai",
        "data",
        "software",
        "robotics",
        "devops_cloud",
    ],

    "devops_cloud": [
        "devops_cloud",
        "software",
        "database",
        "data",
        "security",
    ],

    "mobile": [
        "mobile",
        "software",
        "game",
        "ar_vr",
    ],

    "game": [
        "game",
        "software",
        "ar_vr",
        "mobile",
    ],

    "ar_vr": [
        "ar_vr",
        "game",
        "software",
        "design",
        "mobile",
    ],

    "database": [
        "database",
        "data",
        "software",
        "devops_cloud",
    ],

    "qa": [
        "qa",
        "software",
        "devops_cloud",
    ],

    "security": [
        "security",
        "software",
        "devops_cloud",
        "database",
    ],

    "robotics": [
        "robotics",
        "software",
        "ml_ai",
        "game",
    ],

    "business": [
        "business",
        "data",
        "management",
    ],

    "management": [
        "management",
        "business",
        "data",
        "software",
    ],

    "design": [
        "design",
        "ar_vr",
        "game",
        "mobile",
    ],
}


# ============================================================
# PREPARE CANDIDATE GROUPS
# ============================================================

candidate_groups = {
    family: group
    for family, group in candidates.groupby("candidate_role_family")
}


# ============================================================
# GENERATE PAIRS
# ============================================================

pairs = []

for _, job in jobs.iterrows():

    job_family = job["role_family"]

    # --------------------------------------------------------
    # Candidate families compatible with this job
    # --------------------------------------------------------

    compatible = COMPATIBLE_FAMILIES.get(
        job_family,
        [job_family]
    )

    available = []

    for family in compatible:

        if family in candidate_groups:

            group = candidate_groups[family]

            available.append(group)

    if not available:
        continue

    candidate_pool = pd.concat(
        available,
        ignore_index=True
    )

    # --------------------------------------------------------
    # Randomly select candidates
    # --------------------------------------------------------

    sample_size = min(
        PAIRS_PER_JOB,
        len(candidate_pool)
    )

    selected = candidate_pool.sample(
        n=sample_size,
        random_state=RANDOM_SEED + int(job.name)
    )

    # --------------------------------------------------------
    # Create pairs
    # --------------------------------------------------------

    for _, candidate in selected.iterrows():

        pairs.append({

            "job_id": job["job_id"],
            "job_title": job["job_title"],
            "job_description": job["job_description"],
            "job_skills": job["job_skills"],
            "job_role_family": job["role_family"],

            "candidate_id": candidate["candidate_id"],
            "candidate_role": candidate["job_role"],
            "candidate_resume": candidate["candidate_resume"],
            "candidate_role_family":
                candidate["candidate_role_family"],

        })


# ============================================================
# DATAFRAME
# ============================================================

pairs_df = pd.DataFrame(pairs)

print("\n" + "=" * 70)
print("PAIR GENERATION COMPLETE")
print("=" * 70)

print(f"\nTotal pairs: {len(pairs_df)}")


# ============================================================
# DISTRIBUTION
# ============================================================

print("\nJOB FAMILY × CANDIDATE FAMILY")
print("=" * 70)

distribution = (
    pairs_df
    .groupby(
        [
            "job_role_family",
            "candidate_role_family"
        ]
    )
    .size()
    .sort_values(ascending=False)
)

print(distribution)


# ============================================================
# SAVE
# ============================================================

pairs_df.to_csv(
    OUTPUT_PATH,
    index=False
)

print("\nSaved to:")
print(OUTPUT_PATH)
