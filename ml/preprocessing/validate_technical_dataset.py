import re
from pathlib import Path

import pandas as pd


# ============================================================
# PATHS
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent

PROCESSED_DIR = (
    BASE_DIR
    / "data"
    / "processed"
)

INPUT_FILE = (
    PROCESSED_DIR
    / "technical_matching_dataset.csv"
)

REPORT_FILE = (
    PROCESSED_DIR
    / "technical_validation_report.txt"
)

QUALITY_OUTPUT = (
    PROCESSED_DIR
    / "technical_dataset_with_quality.csv"
)


# ============================================================
# CONFIGURATION
# ============================================================

# Descriptions shorter than this are considered short.
SHORT_DESCRIPTION_LENGTH = 50

# Descriptions shorter than this are considered extremely short.
VERY_SHORT_DESCRIPTION_LENGTH = 20

# Resumes shorter than this are considered suspicious.
SHORT_RESUME_LENGTH = 100

# Number of words used to flag repetitive/generic descriptions.
MIN_DESCRIPTION_WORDS = 5


# ============================================================
# TEXT UTILITIES
# ============================================================

def clean_text(value):
    """
    Convert a value into normalized text.
    """

    if pd.isna(value):
        return ""

    text = str(value)

    text = text.replace(
        "\x00",
        " "
    )

    text = re.sub(
        r"\s+",
        " ",
        text
    )

    return text.strip()


def word_count(text):
    """
    Count words in a piece of text.
    """

    if not text:
        return 0

    return len(
        text.split()
    )


# ============================================================
# DESCRIPTION QUALITY
# ============================================================

def classify_description_quality(
    role,
    description
):
    """
    Classify job-description quality.

    GOOD
        Reasonably informative description.

    SHORT
        Description exists but contains little information.

    VERY_SHORT
        Extremely short description.

    EMPTY
        No description.

    SUSPICIOUS
        Description exists but looks generic/useless.
    """

    role = clean_text(role)
    description = clean_text(description)

    if not description:

        return "EMPTY"

    character_count = len(
        description
    )

    words = word_count(
        description
    )

    # --------------------------------------------------------
    # Extremely short
    # --------------------------------------------------------

    if (
        character_count
        < VERY_SHORT_DESCRIPTION_LENGTH
    ):

        return "VERY_SHORT"

    # --------------------------------------------------------
    # Short
    # --------------------------------------------------------

    if (
        character_count
        < SHORT_DESCRIPTION_LENGTH
        or words < MIN_DESCRIPTION_WORDS
    ):

        return "SHORT"

    # --------------------------------------------------------
    # Generic / suspicious descriptions
    # --------------------------------------------------------

    generic_patterns = [

        r"\byou will work\b",
        r"\bwill work\b",
        r"\bwork in\b",
        r"\bresponsible for\b",
        r"\bjoin our company\b",
        r"\bjoin our team\b",
        r"\bwork with us\b",
        r"\bperform various tasks\b",
        r"\bother duties\b",
        r"\bas assigned\b",

    ]

    generic_matches = 0

    for pattern in generic_patterns:

        if re.search(
            pattern,
            description.lower()
        ):

            generic_matches += 1

    # If the description is both short-ish and generic,
    # flag it as suspicious.

    if (
        generic_matches >= 2
        and character_count < 150
    ):

        return "SUSPICIOUS"

    return "GOOD"


# ============================================================
# DUPLICATE ANALYSIS
# ============================================================

def analyze_duplicates(df):

    results = {}

    # --------------------------------------------------------
    # Duplicate resumes
    # --------------------------------------------------------

    duplicate_resume_mask = (
        df["candidate_resume"]
        .duplicated(
            keep=False
        )
    )

    results["duplicate_resume_rows"] = int(
        duplicate_resume_mask.sum()
    )

    results["duplicate_resume_groups"] = int(
        df.loc[
            duplicate_resume_mask,
            "candidate_resume"
        ]
        .nunique()
    )

    # --------------------------------------------------------
    # Duplicate job descriptions
    # --------------------------------------------------------

    duplicate_description_mask = (
        df["job_description"]
        .duplicated(
            keep=False
        )
    )

    results["duplicate_description_rows"] = int(
        duplicate_description_mask.sum()
    )

    results["duplicate_description_groups"] = int(
        df.loc[
            duplicate_description_mask,
            "job_description"
        ]
        .nunique()
    )

    # --------------------------------------------------------
    # Duplicate job roles
    # --------------------------------------------------------

    duplicate_role_mask = (
        df["job_role"]
        .duplicated(
            keep=False
        )
    )

    results["duplicate_role_rows"] = int(
        duplicate_role_mask.sum()
    )

    results["unique_job_roles"] = int(
        df["job_role"].nunique()
    )

    # --------------------------------------------------------
    # Exact candidate-job duplicates
    # --------------------------------------------------------

    pair_columns = [
        "candidate_resume",
        "job_role",
        "job_description",
    ]

    duplicate_pair_mask = (
        df.duplicated(
            subset=pair_columns,
            keep=False
        )
    )

    results["duplicate_candidate_job_rows"] = int(
        duplicate_pair_mask.sum()
    )

    results["duplicate_candidate_job_groups"] = int(
        df.loc[
            duplicate_pair_mask,
            pair_columns
        ]
        .drop_duplicates()
        .shape[0]
    )

    return results


# ============================================================
# LABEL ANALYSIS
# ============================================================

def analyze_labels(df):

    results = {}

    counts = (
        df["label"]
        .value_counts()
        .sort_index()
    )

    results["rejected"] = int(
        counts.get(0, 0)
    )

    results["accepted"] = int(
        counts.get(1, 0)
    )

    total = (
        results["rejected"]
        + results["accepted"]
    )

    if total > 0:

        results["accepted_percentage"] = round(
            results["accepted"]
            / total
            * 100,
            2
        )

        results["rejected_percentage"] = round(
            results["rejected"]
            / total
            * 100,
            2
        )

    else:

        results["accepted_percentage"] = 0
        results["rejected_percentage"] = 0

    return results


# ============================================================
# ROLE / LABEL ANALYSIS
# ============================================================

def analyze_roles(df):

    role_stats = (
        df.groupby("job_role")
        .agg(
            total=("label", "count"),
            accepted=("label", "sum"),
        )
        .reset_index()
    )

    role_stats["rejected"] = (
        role_stats["total"]
        - role_stats["accepted"]
    )

    role_stats["acceptance_rate"] = (
        role_stats["accepted"]
        / role_stats["total"]
        * 100
    ).round(2)

    role_stats = role_stats.sort_values(
        "total",
        ascending=False
    )

    return role_stats


# ============================================================
# SOURCE ANALYSIS
# ============================================================

def analyze_sources(df):

    return pd.crosstab(
        df["source_dataset"],
        df["label"]
    )


# ============================================================
# TEXT STATISTICS
# ============================================================

def analyze_text(df):

    df = df.copy()

    df["resume_length"] = (
        df["candidate_resume"]
        .apply(len)
    )

    df["resume_words"] = (
        df["candidate_resume"]
        .apply(word_count)
    )

    df["description_length"] = (
        df["job_description"]
        .apply(len)
    )

    df["description_words"] = (
        df["job_description"]
        .apply(word_count)
    )

    return df


# ============================================================
# DATA QUALITY FLAGS
# ============================================================

def add_quality_columns(df):

    df = df.copy()

    # --------------------------------------------------------
    # Basic lengths
    # --------------------------------------------------------

    df["resume_length"] = (
        df["candidate_resume"]
        .apply(len)
    )

    df["resume_words"] = (
        df["candidate_resume"]
        .apply(word_count)
    )

    df["job_description_length"] = (
        df["job_description"]
        .apply(len)
    )

    df["job_description_words"] = (
        df["job_description"]
        .apply(word_count)
    )

    # --------------------------------------------------------
    # Description quality
    # --------------------------------------------------------

    df["description_quality"] = df.apply(
        lambda row: classify_description_quality(
            row["job_role"],
            row["job_description"]
        ),
        axis=1
    )

    # --------------------------------------------------------
    # Resume quality
    # --------------------------------------------------------

    df["resume_quality"] = "GOOD"

    df.loc[
        df["candidate_resume"].str.len() == 0,
        "resume_quality"
    ] = "EMPTY"

    df.loc[
        (
            df["candidate_resume"].str.len() > 0
        )
        &
        (
            df["candidate_resume"].str.len()
            < SHORT_RESUME_LENGTH
        ),
        "resume_quality"
    ] = "SHORT"

    # --------------------------------------------------------
    # Overall quality
    # --------------------------------------------------------

    df["quality_flag"] = "OK"

    df.loc[
        df["description_quality"].isin(
            [
                "EMPTY",
                "VERY_SHORT",
            ]
        ),
        "quality_flag"
    ] = "CHECK"

    df.loc[
        df["resume_quality"].isin(
            [
                "EMPTY",
                "SHORT",
            ]
        ),
        "quality_flag"
    ] = "CHECK"

    return df


# ============================================================
# PRINT SECTION
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
    print("TECHNICAL DATASET VALIDATION")
    print("=" * 70)

    # --------------------------------------------------------
    # Load dataset
    # --------------------------------------------------------

    print()
    print("Loading dataset...")

    if not INPUT_FILE.exists():

        raise FileNotFoundError(
            f"Could not find dataset:\n"
            f"{INPUT_FILE}"
        )

    df = pd.read_csv(
        INPUT_FILE
    )

    print(
        f"Loaded rows: {len(df)}"
    )

    print(
        f"Columns: {list(df.columns)}"
    )

    # --------------------------------------------------------
    # Normalize text
    # --------------------------------------------------------

    text_columns = [
        "candidate_resume",
        "job_role",
        "job_description",
    ]

    for column in text_columns:

        df[column] = (
            df[column]
            .apply(clean_text)
        )

    # --------------------------------------------------------
    # Add quality columns
    # --------------------------------------------------------

    df = add_quality_columns(
        df
    )

    # --------------------------------------------------------
    # Basic statistics
    # --------------------------------------------------------

    print_section(
        "1. BASIC DATASET STATISTICS"
    )

    print(
        f"Total rows: {len(df)}"
    )

    print(
        f"Unique resumes: "
        f"{df['candidate_resume'].nunique()}"
    )

    print(
        f"Unique job descriptions: "
        f"{df['job_description'].nunique()}"
    )

    print(
        f"Unique job roles: "
        f"{df['job_role'].nunique()}"
    )

    # --------------------------------------------------------
    # Missing values
    # --------------------------------------------------------

    print_section(
        "2. MISSING / EMPTY VALUES"
    )

    for column in [
        "candidate_resume",
        "job_role",
        "job_description",
        "label",
    ]:

        empty_count = (
            df[column]
            .isna()
            .sum()
        )

        if df[column].dtype == "object":

            empty_count += (
                df[column]
                .eq("")
                .sum()
            )

        print(
            f"{column}: {empty_count}"
        )

    # --------------------------------------------------------
    # Resume quality
    # --------------------------------------------------------

    print_section(
        "3. RESUME QUALITY"
    )

    print(
        df["resume_quality"]
        .value_counts()
    )

    print()
    print(
        "Shortest resumes:"
    )

    print(
        df[
            [
                "job_role",
                "resume_length",
                "candidate_resume",
            ]
        ]
        .sort_values(
            "resume_length"
        )
        .head(10)
        .to_string(
            index=False
        )
    )

    # --------------------------------------------------------
    # Job description quality
    # --------------------------------------------------------

    print_section(
        "4. JOB DESCRIPTION QUALITY"
    )

    description_counts = (
        df["description_quality"]
        .value_counts()
    )

    print(
        description_counts
    )

    print()

    total = len(df)

    for category in [
        "GOOD",
        "SHORT",
        "VERY_SHORT",
        "EMPTY",
        "SUSPICIOUS",
    ]:

        count = int(
            description_counts.get(
                category,
                0
            )
        )

        percentage = (
            count / total * 100
            if total > 0
            else 0
        )

        print(
            f"{category:12s}: "
            f"{count:5d} "
            f"({percentage:6.2f}%)"
        )

    # --------------------------------------------------------
    # Show bad descriptions
    # --------------------------------------------------------

    print_section(
        "5. SAMPLE FLAGGED JOB DESCRIPTIONS"
    )

    flagged = df[
        df["description_quality"] != "GOOD"
    ]

    print(
        f"Flagged descriptions: "
        f"{len(flagged)}"
    )

    print()

    if len(flagged) > 0:

        print(
            flagged[
                [
                    "job_role",
                    "description_quality",
                    "job_description",
                ]
            ]
            .head(30)
            .to_string(
                index=False
            )
        )

    # --------------------------------------------------------
    # Duplicate analysis
    # --------------------------------------------------------

    print_section(
        "6. DUPLICATE ANALYSIS"
    )

    duplicate_stats = analyze_duplicates(
        df
    )

    for key, value in duplicate_stats.items():

        print(
            f"{key}: {value}"
        )

    # --------------------------------------------------------
    # Exact duplicate pairs
    # --------------------------------------------------------

    print()

    pair_columns = [
        "candidate_resume",
        "job_role",
        "job_description",
    ]

    duplicate_pairs = (
        df[
            df.duplicated(
                subset=pair_columns,
                keep=False
            )
        ]
        .sort_values(
            [
                "job_role",
                "candidate_resume",
            ]
        )
    )

    print(
        f"Duplicate candidate-job rows: "
        f"{len(duplicate_pairs)}"
    )

    if len(duplicate_pairs) > 0:

        print()

        print(
            duplicate_pairs[
                [
                    "job_role",
                    "label",
                    "source_dataset",
                ]
            ]
            .head(20)
            .to_string(
                index=False
            )
        )

    # --------------------------------------------------------
    # Label analysis
    # --------------------------------------------------------

    print_section(
        "7. LABEL DISTRIBUTION"
    )

    label_stats = analyze_labels(
        df
    )

    print(
        f"Rejected: "
        f"{label_stats['rejected']}"
    )

    print(
        f"Accepted: "
        f"{label_stats['accepted']}"
    )

    print(
        f"Rejected %: "
        f"{label_stats['rejected_percentage']}%"
    )

    print(
        f"Accepted %: "
        f"{label_stats['accepted_percentage']}%"
    )

    # --------------------------------------------------------
    # Source analysis
    # --------------------------------------------------------

    print_section(
        "8. LABEL DISTRIBUTION BY SOURCE"
    )

    print(
        analyze_sources(
            df
        )
    )

    # --------------------------------------------------------
    # Role analysis
    # --------------------------------------------------------

    print_section(
        "9. ROLE DISTRIBUTION"
    )

    role_stats = analyze_roles(
        df
    )

    print(
        role_stats.head(30)
        .to_string(
            index=False
        )
    )

    # --------------------------------------------------------
    # Suspicious role distributions
    # --------------------------------------------------------

    print_section(
        "10. ROLES WITH EXTREME LABEL DISTRIBUTIONS"
    )

    # Only consider roles with at least 20 examples.
    substantial_roles = role_stats[
        role_stats["total"] >= 20
    ].copy()

    extreme_roles = substantial_roles[
        (
            substantial_roles[
                "acceptance_rate"
            ] <= 10
        )
        |
        (
            substantial_roles[
                "acceptance_rate"
            ] >= 90
        )
    ]

    if len(extreme_roles) == 0:

        print(
            "No roles with >=20 samples "
            "have an extreme label distribution."
        )

    else:

        print(
            extreme_roles
            .head(30)
            .to_string(
                index=False
            )
        )

    # --------------------------------------------------------
    # Text length statistics
    # --------------------------------------------------------

    print_section(
        "11. TEXT LENGTH STATISTICS"
    )

    print(
        "Resume character statistics:"
    )

    print(
        df["resume_length"]
        .describe()
        .round(2)
    )

    print()

    print(
        "Resume word statistics:"
    )

    print(
        df["resume_words"]
        .describe()
        .round(2)
    )

    print()

    print(
        "Job description character statistics:"
    )

    print(
        df["job_description_length"]
        .describe()
        .round(2)
    )

    print()

    print(
        "Job description word statistics:"
    )

    print(
        df["job_description_words"]
        .describe()
        .round(2)
    )

    # --------------------------------------------------------
    # Potential leakage indicators
    # --------------------------------------------------------

    print_section(
        "12. POTENTIAL DATA LEAKAGE"
    )

    # Resumes appearing with multiple labels.
    resume_label_counts = (
        df.groupby(
            "candidate_resume"
        )["label"]
        .nunique()
    )

    conflicting_resumes = (
        resume_label_counts[
            resume_label_counts > 1
        ]
    )

    print(
        "Resumes appearing with both "
        f"labels: {len(conflicting_resumes)}"
    )

    # Job descriptions appearing with multiple labels.
    description_label_counts = (
        df.groupby(
            "job_description"
        )["label"]
        .nunique()
    )

    conflicting_descriptions = (
        description_label_counts[
            description_label_counts > 1
        ]
    )

    print(
        "Job descriptions appearing with "
        f"both labels: {len(conflicting_descriptions)}"
    )

    # Exact candidate-job pair appearing with both labels.
    pair_label_counts = (
        df.groupby(
            pair_columns
        )["label"]
        .nunique()
    )

    conflicting_pairs = (
        pair_label_counts[
            pair_label_counts > 1
        ]
    )

    print(
        "Candidate-job pairs appearing with "
        f"both labels: {len(conflicting_pairs)}"
    )

    # --------------------------------------------------------
    # Overall quality
    # --------------------------------------------------------

    print_section(
        "13. OVERALL QUALITY SUMMARY"
    )

    check_rows = (
        df["quality_flag"]
        .eq("CHECK")
        .sum()
    )

    print(
        f"Rows requiring text-quality review: "
        f"{check_rows}"
    )

    print(
        f"Rows considered OK: "
        f"{len(df) - check_rows}"
    )

    # --------------------------------------------------------
    # Save quality-enriched dataset
    # --------------------------------------------------------

    df.to_csv(
        QUALITY_OUTPUT,
        index=False
    )

    print()
    print(
        f"Quality-enriched dataset saved to:"
    )

    print(
        QUALITY_OUTPUT
    )

    # --------------------------------------------------------
    # Save report
    # --------------------------------------------------------

    # Re-run the script's output isn't captured automatically,
    # so we create a compact machine-readable report separately.

    report_lines = [

        "TECHNICAL DATASET VALIDATION REPORT",
        "=" * 70,
        "",
        f"Total rows: {len(df)}",
        f"Unique resumes: {df['candidate_resume'].nunique()}",
        f"Unique job descriptions: {df['job_description'].nunique()}",
        f"Unique job roles: {df['job_role'].nunique()}",
        "",

        "DESCRIPTION QUALITY",
        "-" * 70,
    ]

    for category, count in (
        df["description_quality"]
        .value_counts()
        .items()
    ):

        percentage = (
            count / len(df) * 100
        )

        report_lines.append(
            f"{category}: "
            f"{count} "
            f"({percentage:.2f}%)"
        )

    report_lines.extend(
        [
            "",
            "DUPLICATES",
            "-" * 70,
        ]
    )

    for key, value in duplicate_stats.items():

        report_lines.append(
            f"{key}: {value}"
        )

    report_lines.extend(
        [
            "",
            "LABELS",
            "-" * 70,
            f"Rejected: {label_stats['rejected']}",
            f"Accepted: {label_stats['accepted']}",
            f"Rejected %: {label_stats['rejected_percentage']}",
            f"Accepted %: {label_stats['accepted_percentage']}",
            "",
            "POTENTIAL LEAKAGE",
            "-" * 70,
            f"Conflicting resumes: {len(conflicting_resumes)}",
            f"Conflicting job descriptions: {len(conflicting_descriptions)}",
            f"Conflicting candidate-job pairs: {len(conflicting_pairs)}",
        ]
    )

    with open(
        REPORT_FILE,
        "w",
        encoding="utf-8"
    ) as file:

        file.write(
            "\n".join(
                report_lines
            )
        )

    print()
    print(
        f"Validation report saved to:"
    )

    print(
        REPORT_FILE
    )

    print()
    print("=" * 70)
    print("VALIDATION COMPLETE")
    print("=" * 70)


# ============================================================
# ENTRY POINT
# ============================================================

if __name__ == "__main__":

    main()