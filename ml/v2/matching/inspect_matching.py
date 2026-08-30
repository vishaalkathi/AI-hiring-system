import os
import json
import random

import pandas as pd
from tqdm import tqdm

from ml.matching.matcher import (
    match_candidate_to_job,
    role_compatibility
)


random.seed(42)


CANDIDATES_FILE = (
    "ml/data/processed/"
    "candidates_extracted_v2.jsonl"
)

JOBS_FILE = (
    "ml/data/processed/"
    "jobs_extracted_v2.jsonl"
)

OUTPUT = (
    "ml/data/processed/"
    "matching_pairs_v2.csv"
)


def load_jsonl(path):

    records = []

    with open(
        path,
        "r",
        encoding="utf-8"
    ) as f:

        for line in f:

            try:
                records.append(
                    json.loads(line)
                )

            except Exception:
                continue

    return records


print("Loading extracted data...")


candidates = load_jsonl(
    CANDIDATES_FILE
)

jobs = load_jsonl(
    JOBS_FILE
)


print(
    f"Candidates: {len(candidates)}"
)

print(
    f"Jobs: {len(jobs)}"
)


# ------------------------------------------------------------
# INDEX JOBS BY ROLE FAMILY
# ------------------------------------------------------------

jobs_by_family = {}

for job in jobs:

    family = job.get(
        "role_family",
        "other"
    )

    jobs_by_family.setdefault(
        family,
        []
    ).append(job)


# ------------------------------------------------------------
# GENERATE PAIRS
# ------------------------------------------------------------

rows = []


for candidate in tqdm(
    candidates,
    desc="Generating candidate-job pairs"
):

    candidate_family = candidate.get(
        "role_family",
        "other"
    )


    compatible_jobs = []

    hard_negative_jobs = []

    random_jobs = []


    # --------------------------------------------------------
    # FIND CANDIDATE JOBS
    # --------------------------------------------------------

    for family, family_jobs in jobs_by_family.items():

        compatibility = role_compatibility(
            candidate_family,
            family
        )

        if compatibility >= 0.5:

            compatible_jobs.extend(
                family_jobs
            )

        elif 0 < compatibility < 0.5:

            hard_negative_jobs.extend(
                family_jobs
            )

        else:

            random_jobs.extend(
                family_jobs
            )


    # --------------------------------------------------------
    # SAMPLE
    # --------------------------------------------------------

    n_positive = min(
        8,
        len(compatible_jobs)
    )

    n_hard = min(
        4,
        len(hard_negative_jobs)
    )

    n_random = min(
        3,
        len(random_jobs)
    )


    selected = []


    if n_positive:

        selected.extend(
            random.sample(
                compatible_jobs,
                n_positive
            )
        )


    if n_hard:

        selected.extend(
            random.sample(
                hard_negative_jobs,
                n_hard
            )
        )


    if n_random:

        selected.extend(
            random.sample(
                random_jobs,
                n_random
            )
        )


    # --------------------------------------------------------
    # SCORE
    # --------------------------------------------------------

    for job in selected:

        result = match_candidate_to_job(
            candidate,
            job
        )


        rows.append({

            "candidate_id":
                candidate["candidate_id"],

            "job_id":
                job["job_id"],

            "candidate_role":
                candidate.get(
                    "role",
                    candidate.get(
                        "job_role",
                        ""
                    )
                ),

            "job_title":
                job.get(
                    "job_title",
                    ""
                ),

            "candidate_role_family":
                candidate_family,

            "job_role_family":
                job.get(
                    "role_family",
                    "other"
                ),

            "match_score":
                result["score"],

            "label":
                result["label"],

            "role_score":
                result["role_score"],

            "required_skill_score":
                result[
                    "required_skill_score"
                ],

            "preferred_skill_score":
                result[
                    "preferred_skill_score"
                ],

            "experience_score":
                result[
                    "experience_score"
                ],

            "matched_skills":
                json.dumps(
                    result[
                        "matched_skills"
                    ]
                ),

            "missing_skills":
                json.dumps(
                    result[
                        "missing_skills"
                    ]
                ),

            "reason":
                result["reason"]
        })


# ------------------------------------------------------------
# SAVE
# ------------------------------------------------------------

df = pd.DataFrame(rows)


print()
print("=" * 70)
print("MATCHING DATASET")
print("=" * 70)

print(
    f"Generated pairs: {len(df)}"
)

print()
print("Label distribution:")

print(
    df["label"].value_counts()
    .sort_index()
)


df.to_csv(
    OUTPUT,
    index=False
)


print()
print(f"Saved to: {OUTPUT}")