import pandas as pd
from pathlib import Path

from ml.v2.preprocessing.role_taxonomy import get_role_family

'''
Instead of taking all 91k rows im cutting it down
'''


# ============================================================
# CONFIG
# ============================================================

INPUT_PATH = Path(
    "ml/data/processed/naukri_matching_v2.csv"
)

OUTPUT_PATH = Path(
    "ml/data/processed/naukri_jobs_matching_v2.csv"
)

TARGET_ROWS = 10000

RANDOM_STATE = 42


# ============================================================
# LOAD
# ============================================================

print("=" * 70)
print("NAUKRI JOB SAMPLING — V2")
print("=" * 70)

print("\nLoading dataset...")

df = pd.read_csv(INPUT_PATH)

print(f"Original jobs: {len(df)}")


# ============================================================
# ROLE FAMILY
# ============================================================

print("\nAssigning role families...")

df["role_family"] = (
    df["job_title"]
    .apply(get_role_family)
)


# ============================================================
# ROLE DISTRIBUTION
# ============================================================

print()
print("=" * 70)
print("ROLE FAMILY DISTRIBUTION")
print("=" * 70)

print(
    df["role_family"]
    .value_counts()
)


# ============================================================
# REMOVE OTHER
# ============================================================

technical_df = df[
    df["role_family"] != "other"
].copy()

print(
    f"\nRecognized technical/relevant jobs: "
    f"{len(technical_df)}"
)

print(
    f"Unrecognized jobs: "
    f"{len(df) - len(technical_df)}"
)


# ============================================================
# STRATIFIED SAMPLING
# ============================================================

print()
print("=" * 70)
print("SAMPLING")
print("=" * 70)

# We want every role family represented.
#
# First allocate approximately equal space across families.
#
# Remaining capacity is distributed proportionally.

family_counts = (
    technical_df["role_family"]
    .value_counts()
)

families = list(family_counts.index)

base_per_family = TARGET_ROWS // len(families)

sample_parts = []

remaining_rows = TARGET_ROWS


for family in families:

    family_df = technical_df[
        technical_df["role_family"] == family
    ]

    n = min(
        base_per_family,
        len(family_df)
    )

    sampled = family_df.sample(
        n=n,
        random_state=RANDOM_STATE
    )

    sample_parts.append(sampled)

    remaining_rows -= n


# ============================================================
# FILL REMAINING CAPACITY
# ============================================================

if remaining_rows > 0:

    already_sampled = pd.concat(
        sample_parts,
        ignore_index=False
    )

    remaining_pool = technical_df.drop(
        already_sampled.index,
        errors="ignore"
    )

    if len(remaining_pool) > 0:

        extra = remaining_pool.sample(
            n=min(
                remaining_rows,
                len(remaining_pool)
            ),
            random_state=RANDOM_STATE
        )

        sample_parts.append(extra)


# ============================================================
# COMBINE
# ============================================================

sampled_df = pd.concat(
    sample_parts,
    ignore_index=True
)


# ============================================================
# SHUFFLE
# ============================================================

sampled_df = sampled_df.sample(
    frac=1,
    random_state=RANDOM_STATE
).reset_index(drop=True)


# ============================================================
# FINAL LIMIT
# ============================================================

sampled_df = sampled_df.head(
    TARGET_ROWS
)


# ============================================================
# SUMMARY
# ============================================================

print(
    f"\nSelected jobs: "
    f"{len(sampled_df)}"
)

print()
print("Selected role distribution:")

print(
    sampled_df["role_family"]
    .value_counts()
)


# ============================================================
# SAVE
# ============================================================

OUTPUT_PATH.parent.mkdir(
    parents=True,
    exist_ok=True
)

sampled_df.to_csv(
    OUTPUT_PATH,
    index=False
)


print()
print("=" * 70)
print("SAMPLING COMPLETE")
print("=" * 70)

print(
    f"\nSaved to:\n"
    f"{OUTPUT_PATH}"
)

print(
    f"\nOriginal jobs : {len(df)}"
)

print(
    f"Selected jobs : {len(sampled_df)}"
)

print(
    f"Reduction     : "
    f"{len(df) - len(sampled_df)}"
)