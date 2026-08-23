from pathlib import Path

import pandas as pd


from .semantic_features import (
    SemanticFeatureEngineer
)

from .lexical_features import (
    LexicalFeatureEngineer
)

from .explicit_features import (
    calculate_skill_features,
    calculate_education_features,
    calculate_experience_features,
    calculate_signal_features
)


# ============================================================
# PATHS
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent

INPUT_FILE = (
    BASE_DIR
    / "data"
    / "processed"
    / "technical_normalized_dataset.csv"
)

OUTPUT_FILE = (
    BASE_DIR
    / "data"
    / "processed"
    / "technical_feature_matrix.csv"
)


# ============================================================
# EXPLICIT FEATURES
# ============================================================

def build_explicit_features(
    df
):

    rows = []

    print(
        "Generating explicit features..."
    )

    for _, row in df.iterrows():

        resume = row[
            "candidate_resume"
        ]

        job = row[
            "job_description"
        ]

        features = {}

        # ----------------------------------------------------
        # Skills
        # ----------------------------------------------------

        features.update(
            calculate_skill_features(
                resume,
                job
            )
        )

        # ----------------------------------------------------
        # Education
        # ----------------------------------------------------

        features.update(
            calculate_education_features(
                resume,
                job
            )
        )

        # ----------------------------------------------------
        # Experience
        # ----------------------------------------------------

        features.update(
            calculate_experience_features(
                resume,
                job
            )
        )

        # ----------------------------------------------------
        # Other signals
        # ----------------------------------------------------

        features.update(
            calculate_signal_features(
                resume,
                job
            )
        )

        rows.append(
            features
        )

    return pd.DataFrame(
        rows
    )


# ============================================================
# BUILD ALL FEATURES
# ============================================================

def build_feature_matrix(
    df
):

    resumes = (
        df["candidate_resume"]
        .fillna("")
        .tolist()
    )

    job_descriptions = (
        df["job_description"]
        .fillna("")
        .tolist()
    )

    # ========================================================
    # SEMANTIC
    # ========================================================

    semantic_engineer = (
        SemanticFeatureEngineer()
    )

    semantic_scores = (
        semantic_engineer.transform(
            resumes,
            job_descriptions
        )
    )

    semantic_df = pd.DataFrame({

        "semantic_similarity":
            semantic_scores
    })

    # ========================================================
    # LEXICAL
    # ========================================================

    lexical_engineer = (
        LexicalFeatureEngineer()
    )

    lexical_features = (
        lexical_engineer.transform(
            resumes,
            job_descriptions
        )
    )

    lexical_df = pd.DataFrame(
        lexical_features
    )

    # ========================================================
    # EXPLICIT
    # ========================================================

    explicit_df = (
        build_explicit_features(
            df
        )
    )

    # ========================================================
    # COMBINE
    # ========================================================

    feature_df = pd.concat(
        [
            semantic_df,
            lexical_df,
            explicit_df
        ],
        axis=1
    )

    # ========================================================
    # ADD LABEL
    # ========================================================

    feature_df["label"] = (
        df["label"]
        .values
    )

    return feature_df


# ============================================================
# MAIN
# ============================================================

def main():

    print("=" * 70)
    print(
        "FEATURE ENGINEERING"
    )
    print("=" * 70)

    # --------------------------------------------------------
    # Load dataset
    # --------------------------------------------------------

    print()
    print(
        "Loading normalized dataset..."
    )

    df = pd.read_csv(
        INPUT_FILE
    )

    print(
        f"Rows: {len(df)}"
    )

    # --------------------------------------------------------
    # Build features
    # --------------------------------------------------------

    feature_df = (
        build_feature_matrix(
            df
        )
    )

    # --------------------------------------------------------
    # Report
    # --------------------------------------------------------

    print()
    print("=" * 70)
    print(
        "FEATURE MATRIX"
    )
    print("=" * 70)

    print(
        f"Rows: {len(feature_df)}"
    )

    print(
        f"Features: "
        f"{len(feature_df.columns) - 1}"
    )

    print()
    print(
        "Feature columns:"
    )

    for column in feature_df.columns:

        print(
            f"  {column}"
        )

    # --------------------------------------------------------
    # Missing values
    # --------------------------------------------------------

    print()
    print(
        "Missing values:"
    )

    print(
        feature_df.isna()
        .sum()
        .loc[
            lambda x: x > 0
        ]
    )

    # --------------------------------------------------------
    # Save
    # --------------------------------------------------------

    feature_df.to_csv(
        OUTPUT_FILE,
        index=False
    )

    print()
    print(
        f"Feature matrix saved to:\n"
        f"{OUTPUT_FILE}"
    )

    print()
    print(
        "=" * 70
    )

    print(
        "FEATURE ENGINEERING COMPLETE"
    )

    print(
        "=" * 70
    )


# ============================================================
# ENTRY POINT
# ============================================================

if __name__ == "__main__":

    main()