import numpy as np
import pandas as pd


# ============================================================
# ROLE FAMILY RELATIONSHIPS
# ============================================================

RELATED_FAMILIES = {
    "software": {
        "data",
        "devops_cloud",
        "mobile",
        "qa",
        "database",
        "ml_ai",
    },

    "data": {
        "software",
        "ml_ai",
        "business",
        "database",
        "devops_cloud",
    },

    "ml_ai": {
        "data",
        "software",
        "robotics",
    },

    "devops_cloud": {
        "software",
        "data",
        "security",
        "database",
    },

    "mobile": {
        "software",
        "game",
        "ar_vr",
    },

    "game": {
        "software",
        "mobile",
        "ar_vr",
    },

    "ar_vr": {
        "game",
        "mobile",
        "design",
        "software",
    },

    "database": {
        "data",
        "software",
        "devops_cloud",
    },

    "security": {
        "devops_cloud",
        "software",
        "network",
    },

    "qa": {
        "software",
        "devops_cloud",
    },

    "business": {
        "data",
        "management",
        "software",
    },

    "management": {
        "business",
        "software",
        "data",
    },

    "design": {
        "ar_vr",
        "game",
    },

    "robotics": {
        "ml_ai",
        "software",
    },
}


# ============================================================
# MAIN FUNCTION
# ============================================================

def generate_pairs(
    jobs,
    candidates,
    candidates_per_job=50,
    random_state=42,
):
    """
    Generate job-candidate pairs.

    Each job receives approximately `candidates_per_job`
    candidates distributed across:

        - same role family
        - related role family
        - different role family

    Returns:
        pandas.DataFrame
    """

    rng = np.random.default_rng(random_state)

    jobs = jobs.reset_index(drop=True)
    candidates = candidates.reset_index(drop=True)

    # --------------------------------------------------------
    # VALIDATION
    # --------------------------------------------------------

    required_job_columns = {
        "job_id",
        "job_title",
        "job_description",
        "job_skills",
        "role_family",
    }

    required_candidate_columns = {
        "candidate_id",
        "candidate_resume",
        "job_role",
        "role_family",
    }

    missing_jobs = required_job_columns - set(jobs.columns)
    missing_candidates = required_candidate_columns - set(candidates.columns)

    if missing_jobs:
        raise ValueError(
            f"Missing job columns: {missing_jobs}"
        )

    if missing_candidates:
        raise ValueError(
            f"Missing candidate columns: {missing_candidates}"
        )

    # --------------------------------------------------------
    # GROUP CANDIDATES BY ROLE FAMILY
    # --------------------------------------------------------

    candidate_groups = {
        family: group
        for family, group in candidates.groupby("role_family")
    }

    available_families = list(candidate_groups.keys())

    # --------------------------------------------------------
    # TARGET DISTRIBUTION
    # --------------------------------------------------------

    # Approximately:
    # 50% same family
    # 20% related family
    # 30% different family

    same_count = round(candidates_per_job * 0.50)
    related_count = round(candidates_per_job * 0.20)

    different_count = (
        candidates_per_job
        - same_count
        - related_count
    )

    # --------------------------------------------------------
    # HELPER
    # --------------------------------------------------------

    def sample_candidates(family, count):
        """
        Sample candidates from a family.

        Sampling is done with replacement so that even small
        role families can supply the requested number.
        """

        if family not in candidate_groups:
            return []

        group = candidate_groups[family]

        if len(group) == 0:
            return []

        indices = rng.integers(
            0,
            len(group),
            size=count,
        )

        return [
            group.iloc[idx]
            for idx in indices
        ]

    # --------------------------------------------------------
    # CREATE PAIR
    # --------------------------------------------------------

    def create_pair(job, candidate, pair_type):

        return {
            "job_id": job["job_id"],
            "job_title": job["job_title"],
            "job_description": job["job_description"],
            "job_skills": job["job_skills"],
            "job_role_family": job["role_family"],

            "candidate_id": candidate["candidate_id"],
            "candidate_role": candidate["job_role"],
            "candidate_resume": candidate["candidate_resume"],
            "candidate_role_family": candidate["role_family"],

            "pair_type": pair_type,
        }

    # --------------------------------------------------------
    # GENERATE
    # --------------------------------------------------------

    pairs = []

    for _, job in jobs.iterrows():

        job_family = job["role_family"]

        # ====================================================
        # SAME FAMILY
        # ====================================================

        same_candidates = sample_candidates(
            job_family,
            same_count,
        )

        for candidate in same_candidates:

            pairs.append(
                create_pair(
                    job,
                    candidate,
                    "same_family",
                )
            )

        # ====================================================
        # RELATED FAMILY
        # ====================================================

        related_families = [
            family
            for family in RELATED_FAMILIES.get(
                job_family,
                set(),
            )
            if family in candidate_groups
        ]

        if related_families:

            for _ in range(related_count):

                family = rng.choice(
                    related_families
                )

                candidate = sample_candidates(
                    family,
                    1,
                )

                if candidate:

                    pairs.append(
                        create_pair(
                            job,
                            candidate[0],
                            "related_family",
                        )
                    )

        # ====================================================
        # DIFFERENT FAMILY
        # ====================================================

        different_families = [
            family
            for family in available_families
            if (
                family != job_family
                and family not in RELATED_FAMILIES.get(
                    job_family,
                    set(),
                )
            )
        ]

        if different_families:

            for _ in range(different_count):

                family = rng.choice(
                    different_families
                )

                candidate = sample_candidates(
                    family,
                    1,
                )

                if candidate:

                    pairs.append(
                        create_pair(
                            job,
                            candidate[0],
                            "different_family",
                        )
                    )

    # --------------------------------------------------------
    # DATAFRAME
    # --------------------------------------------------------

    pairs_df = pd.DataFrame(pairs)

    # --------------------------------------------------------
    # SHUFFLE
    # --------------------------------------------------------

    if len(pairs_df) > 0:

        pairs_df = (
            pairs_df
            .sample(
                frac=1,
                random_state=random_state,
            )
            .reset_index(drop=True)
        )

    print("=" * 70)
    print("PAIR GENERATION COMPLETE")
    print("=" * 70)

    print(f"\nJobs: {len(jobs):,}")
    print(f"Candidates: {len(candidates):,}")
    print(f"Pairs: {len(pairs_df):,}")

    print("\nPair type distribution:")
    print(
        pairs_df["pair_type"]
        .value_counts()
    )

    print("\nJob family distribution:")
    print(
        pairs_df["job_role_family"]
        .value_counts()
    )

    return pairs_df
