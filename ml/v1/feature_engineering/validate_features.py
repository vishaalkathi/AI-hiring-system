from pathlib import Path

import numpy as np
import pandas as pd


# ============================================================
# PATHS
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent

PROCESSED_DIR = (
    BASE_DIR / "data" / "processed"
)

FEATURE_FILE = (
    PROCESSED_DIR
    / "technical_feature_matrix.csv"
)


# ============================================================
# EXPECTED FEATURES
# ============================================================

EXPECTED_FEATURES = [
    # --------------------------------------------------------
    # Semantic
    # --------------------------------------------------------

    "semantic_similarity",

    # --------------------------------------------------------
    # Lexical
    # --------------------------------------------------------

    "tfidf_similarity",
    "word_overlap",

    # --------------------------------------------------------
    # Explicit - Skills
    # --------------------------------------------------------

    "resume_skill_count",
    "job_skill_count",
    "matched_skill_count",
    "skill_match_ratio",
    "skill_coverage",

    # --------------------------------------------------------
    # Explicit - Education
    # --------------------------------------------------------

    "resume_education_level",
    "job_education_level",
    "education_match",

    # --------------------------------------------------------
    # Explicit - Experience
    # --------------------------------------------------------

    "resume_experience_years",
    "job_required_experience_years",
    "experience_match",

    # --------------------------------------------------------
    # Explicit - Technical knowledge
    # --------------------------------------------------------

    "resume_core_cs_count",
    "job_core_cs_count",

    # --------------------------------------------------------
    # Explicit - Degrees
    # --------------------------------------------------------

    "resume_degree_count",
    "job_degree_count",

    # --------------------------------------------------------
    # Explicit - Text statistics
    # --------------------------------------------------------

    "resume_length",
    "job_description_length",
    "resume_word_count",
    "job_word_count",
]


# ============================================================
# VALIDATION HELPERS
# ============================================================

def print_section(title):

    print()
    print("=" * 70)
    print(title)
    print("=" * 70)


# ============================================================
# MAIN VALIDATION
# ============================================================

def main():

    print("=" * 70)
    print("TECHNICAL FEATURE MATRIX VALIDATION")
    print("=" * 70)

    # --------------------------------------------------------
    # Load
    # --------------------------------------------------------

    print()
    print("Loading feature matrix...")

    df = pd.read_csv(
        FEATURE_FILE
    )

    print(
        f"Rows: {len(df)}"
    )

    print(
        f"Columns: {len(df.columns)}"
    )

    # ========================================================
    # 1. COLUMN VALIDATION
    # ========================================================

    print_section(
        "1. COLUMN VALIDATION"
    )

    actual_features = [
        column
        for column in df.columns
        if column != "label"
    ]

    missing_features = [
        feature
        for feature in EXPECTED_FEATURES
        if feature not in df.columns
    ]

    unexpected_features = [
        feature
        for feature in actual_features
        if feature not in EXPECTED_FEATURES
    ]

    print(
        f"Expected features: "
        f"{len(EXPECTED_FEATURES)}"
    )

    print(
        f"Actual features: "
        f"{len(actual_features)}"
    )

    if missing_features:

        print()
        print("MISSING FEATURES:")

        for feature in missing_features:
            print(
                f"  ❌ {feature}"
            )

    else:

        print(
            "✓ All expected features present"
        )

    if unexpected_features:

        print()
        print("UNEXPECTED FEATURES:")

        for feature in unexpected_features:
            print(
                f"  ⚠ {feature}"
            )

    else:

        print(
            "✓ No unexpected features"
        )

    # ========================================================
    # 2. LABEL VALIDATION
    # ========================================================

    print_section(
        "2. LABEL VALIDATION"
    )

    if "label" not in df.columns:

        print(
            "❌ LABEL COLUMN MISSING"
        )

    else:

        print(
            "Label values:"
        )

        print(
            df["label"]
            .value_counts()
            .sort_index()
        )

        invalid_labels = df[
            ~df["label"].isin([0, 1])
        ]

        print()

        if len(invalid_labels) == 0:

            print(
                "✓ Labels are valid binary values"
            )

        else:

            print(
                f"❌ Invalid labels: "
                f"{len(invalid_labels)}"
            )

    # ========================================================
    # 3. MISSING VALUES
    # ========================================================

    print_section(
        "3. MISSING VALUES"
    )

    missing = (
        df[
            EXPECTED_FEATURES
        ]
        .isna()
        .sum()
    )

    missing = missing[
        missing > 0
    ]

    if len(missing) == 0:

        print(
            "✓ No missing feature values"
        )

    else:

        print(
            "❌ Missing values found:"
        )

        print(
            missing
        )

    # ========================================================
    # 4. INFINITE VALUES
    # ========================================================

    print_section(
        "4. INFINITE VALUES"
    )

    numeric_features = df[
        EXPECTED_FEATURES
    ].select_dtypes(
        include=np.number
    ).columns

    infinite_counts = {}

    for column in numeric_features:

        count = np.isinf(
            df[column]
        ).sum()

        if count > 0:

            infinite_counts[
                column
            ] = count

    if not infinite_counts:

        print(
            "✓ No infinite values"
        )

    else:

        print(
            "❌ Infinite values found:"
        )

        for column, count in infinite_counts.items():

            print(
                f"  {column}: {count}"
            )

    # ========================================================
    # 5. DUPLICATES
    # ========================================================

    print_section(
        "5. DUPLICATE ANALYSIS"
    )

    duplicate_rows = (
        df.duplicated()
        .sum()
    )

    print(
        f"Exact duplicate rows: "
        f"{duplicate_rows}"
    )

    if duplicate_rows == 0:

        print(
            "✓ No exact duplicate feature rows"
        )

    else:

        print(
            "⚠ Duplicate rows detected"
        )

    # ========================================================
    # 6. FEATURE DATA TYPES
    # ========================================================

    print_section(
        "6. FEATURE DATA TYPES"
    )

    dtype_table = pd.DataFrame({
        "feature": EXPECTED_FEATURES,
        "dtype": [
            df[column].dtype
            if column in df.columns
            else "MISSING"
            for column in EXPECTED_FEATURES
        ]
    })

    print(
        dtype_table.to_string(
            index=False
        )
    )

    non_numeric = dtype_table[
        ~dtype_table["dtype"].astype(str).isin(
            [
                "int64",
                "float64",
                "int32",
                "float32",
            ]
        )
    ]

    print()

    if len(non_numeric) == 0:

        print(
            "✓ All model features are numeric"
        )

    else:

        print(
            "⚠ Non-numeric features detected:"
        )

        print(
            non_numeric.to_string(
                index=False
            )
        )

    # ========================================================
    # 7. FEATURE RANGE CHECK
    # ========================================================

    print_section(
        "7. FEATURE RANGE CHECK"
    )

    range_checks = {

        "semantic_similarity": (
            0,
            1
        ),

        "tfidf_similarity": (
            0,
            1
        ),

        "word_overlap": (
            0,
            1
        ),

        "skill_match_ratio": (
            0,
            1
        ),

        "skill_coverage": (
            0,
            1
        ),

        "education_match": (
            0,
            1
        ),

        "experience_match": (
            0,
            1
        ),
    }

    range_errors = []

    for feature, (
        minimum,
        maximum
    ) in range_checks.items():

        if feature not in df.columns:
            continue

        invalid = df[
            (df[feature] < minimum)
            |
            (df[feature] > maximum)
        ]

        if len(invalid) > 0:

            range_errors.append(
                (
                    feature,
                    len(invalid),
                    minimum,
                    maximum
                )
            )

    if not range_errors:

        print(
            "✓ All bounded features are within expected ranges"
        )

    else:

        print(
            "❌ Range violations:"
        )

        for (
            feature,
            count,
            minimum,
            maximum
        ) in range_errors:

            print(
                f"  {feature}: "
                f"{count} rows outside "
                f"[{minimum}, {maximum}]"
            )

    # ========================================================
    # 8. FEATURE STATISTICS
    # ========================================================

    print_section(
        "8. FEATURE STATISTICS"
    )

    statistics = (
        df[
            EXPECTED_FEATURES
        ]
        .describe()
        .T
    )

    statistics = statistics[
        [
            "min",
            "mean",
            "std",
            "50%",
            "max",
        ]
    ]

    print(
        statistics.round(4)
        .to_string()
    )

    # ========================================================
    # 9. CONSTANT FEATURES
    # ========================================================

    print_section(
        "9. CONSTANT FEATURES"
    )

    constant_features = []

    for feature in EXPECTED_FEATURES:

        unique_count = (
            df[feature]
            .nunique()
        )

        if unique_count <= 1:

            constant_features.append(
                feature
            )

    if not constant_features:

        print(
            "✓ No constant features"
        )

    else:

        print(
            "⚠ Constant features:"
        )

        for feature in constant_features:

            print(
                f"  {feature}"
            )

    # ========================================================
    # 10. LOW VARIANCE FEATURES
    # ========================================================

    print_section(
        "10. LOW VARIANCE FEATURES"
    )

    low_variance = []

    for feature in EXPECTED_FEATURES:

        variance = (
            df[feature]
            .var()
        )

        if variance < 1e-4:

            low_variance.append(
                (
                    feature,
                    variance
                )
            )

    if not low_variance:

        print(
            "✓ No extremely low-variance features"
        )

    else:

        print(
            "⚠ Very low variance:"
        )

        for feature, variance in low_variance:

            print(
                f"  {feature}: "
                f"{variance:.8f}"
            )

    # ========================================================
    # 11. CORRELATION WITH LABEL
    # ========================================================

    print_section(
        "11. FEATURE / LABEL CORRELATION"
    )

    correlations = (
        df[
            EXPECTED_FEATURES + ["label"]
        ]
        .corr()["label"]
        .drop("label")
        .sort_values(
            key=abs,
            ascending=False
        )
    )

    correlation_table = pd.DataFrame({
        "feature": correlations.index,
        "correlation": correlations.values
    })

    print(
        correlation_table
        .round(4)
        .to_string(index=False)
    )

    # ========================================================
    # 12. POTENTIAL LEAKAGE CHECK
    # ========================================================

    print_section(
        "12. POTENTIAL LABEL LEAKAGE"
    )

    suspicious_features = []

    for feature in EXPECTED_FEATURES:

        correlation = abs(
            df[
                [
                    feature,
                    "label"
                ]
            ]
            .corr()
            .iloc[0, 1]
        )

        if correlation > 0.95:

            suspicious_features.append(
                (
                    feature,
                    correlation
                )
            )

    if not suspicious_features:

        print(
            "✓ No feature shows suspiciously high "
            "correlation with label"
        )

    else:

        print(
            "⚠ Potential leakage:"
        )

        for feature, correlation in suspicious_features:

            print(
                f"  {feature}: "
                f"{correlation:.4f}"
            )

    # ========================================================
    # 13. FEATURE GROUP SUMMARY
    # ========================================================

    print_section(
        "13. FEATURE GROUP SUMMARY"
    )

    semantic_features = [
        "semantic_similarity"
    ]

    lexical_features = [
        "tfidf_similarity",
        "word_overlap",
    ]

    explicit_features = [
        feature
        for feature in EXPECTED_FEATURES
        if feature not in (
            semantic_features
            + lexical_features
        )
    ]

    print(
        f"Semantic features : "
        f"{len(semantic_features)}"
    )

    for feature in semantic_features:
        print(
            f"  • {feature}"
        )

    print()

    print(
        f"Lexical features  : "
        f"{len(lexical_features)}"
    )

    for feature in lexical_features:
        print(
            f"  • {feature}"
        )

    print()

    print(
        f"Explicit features : "
        f"{len(explicit_features)}"
    )

    for feature in explicit_features:
        print(
            f"  • {feature}"
        )

    # ========================================================
    # 14. FINAL STATUS
    # ========================================================

    print_section(
        "FINAL VALIDATION STATUS"
    )

    errors = []

    if missing_features:
        errors.append(
            "missing features"
        )

    if len(missing) > 0:
        errors.append(
            "missing values"
        )

    if infinite_counts:
        errors.append(
            "infinite values"
        )

    if "label" not in df.columns:
        errors.append(
            "missing label"
        )

    if len(non_numeric) > 0:
        errors.append(
            "non-numeric features"
        )

    if range_errors:
        errors.append(
            "range violations"
        )

    if errors:

        print(
            "❌ VALIDATION FAILED"
        )

        print()
        print(
            "Problems found:"
        )

        for error in errors:

            print(
                f"  • {error}"
            )

        print()
        print(
            "Fix these issues before training."
        )

    else:

        print(
            "✓ FEATURE MATRIX PASSED VALIDATION"
        )

        print()
        print(
            "The dataset is ready for the "
            "model experimentation stage."
        )

    print()
    print("=" * 70)
    print(
        "FEATURE VALIDATION COMPLETE"
    )
    print("=" * 70)


# ============================================================
# ENTRY POINT
# ============================================================

if __name__ == "__main__":
    main()