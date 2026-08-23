import re
from pathlib import Path

import pandas as pd


# ============================================================
# PATHS
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent

PROCESSED_DIR = BASE_DIR / "data" / "processed"

INPUT_FILE = (
    PROCESSED_DIR
    / "technical_matching_dataset.csv"
)

OUTPUT_FILE = (
    PROCESSED_DIR
    / "technical_normalized_dataset.csv"
)


# ============================================================
# TEXT NORMALIZATION
# ============================================================

def normalize_text(text):
    """
    Normalize resume / job-description text for NLP.

    Important:
    This does NOT aggressively remove words.

    We want to preserve technical information such as:

        C++
        C#
        .NET
        Node.js
        AWS
        SQL
        REST API
        machine learning

    because these will be useful for feature engineering.
    """

    if pd.isna(text):
        return ""

    text = str(text)

    # --------------------------------------------------------
    # Lowercase
    # --------------------------------------------------------

    text = text.lower()

    # --------------------------------------------------------
    # Replace common Unicode punctuation
    # --------------------------------------------------------

    replacements = {
        "–": "-",
        "—": "-",
        "−": "-",
        "“": '"',
        "”": '"',
        "‘": "'",
        "’": "'",
        "\u00a0": " ",
    }

    for old, new in replacements.items():
        text = text.replace(old, new)

    # --------------------------------------------------------
    # Normalize common technical variants
    #
    # Do this BEFORE punctuation removal.
    # --------------------------------------------------------

    technical_replacements = {

        # JavaScript
        "java script": "javascript",

        # Node
        "node js": "node.js",

        # React
        "react js": "react",

        # Next
        "next js": "next.js",

        # Machine Learning
        "machine-learning": "machine learning",

        # Deep Learning
        "deep-learning": "deep learning",

        # Computer Vision
        "computer-vision": "computer vision",

        # Natural Language Processing
        "natural-language-processing":
            "natural language processing",

        # Data Science
        "data-science": "data science",

        # Data Structures
        "data-structures": "data structures",

        # Operating Systems
        "operating-systems": "operating systems",

        # Computer Networks
        "computer-networks": "computer networks",

        # DBMS
        "database management systems":
            "dbms",

        # GitHub
        "git hub": "github",

        # APIs
        "restful api": "rest api",
        "restful apis": "rest apis",
    }

    for old, new in technical_replacements.items():
        text = text.replace(old, new)

    # --------------------------------------------------------
    # Normalize whitespace
    # --------------------------------------------------------

    text = re.sub(
        r"\s+",
        " ",
        text
    )

    # --------------------------------------------------------
    # Remove obvious formatting noise
    #
    # Keep letters, numbers and useful technical punctuation.
    # --------------------------------------------------------

    text = re.sub(
        r"[•●▪◦►◆◇]",
        " ",
        text
    )

    # --------------------------------------------------------
    # Normalize repeated punctuation
    # --------------------------------------------------------

    text = re.sub(
        r"\.{2,}",
        ".",
        text
    )

    text = re.sub(
        r"-{2,}",
        "-",
        text
    )

    # --------------------------------------------------------
    # Remove leading/trailing whitespace
    # --------------------------------------------------------

    text = text.strip()

    return text


# ============================================================
# NORMALIZE ROLE
# ============================================================

def normalize_role(role):
    """
    Normalize job-role names.

    This helps prevent:

        Software Engineer
        software engineer
        SOFTWARE ENGINEER

    from being treated as different roles.
    """

    if pd.isna(role):
        return ""

    role = str(role).strip().lower()

    role = re.sub(
        r"\s+",
        " ",
        role
    )

    # Common role variants

    role_mapping = {

        "swe":
            "software engineer",

        "software developer":
            "software engineer",

        "software development engineer":
            "software engineer",

        "ml engineer":
            "machine learning engineer",

        "machine learning developer":
            "machine learning engineer",

        "data science":
            "data scientist",

        "data engineering":
            "data engineer",

        "dev ops engineer":
            "devops engineer",

        "dev ops":
            "devops",

        "cyber security analyst":
            "cybersecurity analyst",

        "cyber security engineer":
            "cybersecurity engineer",

        "fullstack developer":
            "full stack developer",

        "fullstack engineer":
            "full stack engineer",
    }

    return role_mapping.get(
        role,
        role
    )


# ============================================================
# NORMALIZE DATASET
# ============================================================

def normalize_dataset(df):
    """
    Add normalized versions of the text fields.

    Original columns are preserved.

    New columns:

        normalized_resume
        normalized_job_description
        normalized_job_role
    """

    df = df.copy()

    # --------------------------------------------------------
    # Validate required columns
    # --------------------------------------------------------

    required_columns = [
        "candidate_resume",
        "job_role",
        "job_description",
        "label",
    ]

    missing = [
        column
        for column in required_columns
        if column not in df.columns
    ]

    if missing:
        raise ValueError(
            f"Missing required columns: {missing}\n"
            f"Available columns: {df.columns.tolist()}"
        )

    # --------------------------------------------------------
    # Resume normalization
    # --------------------------------------------------------

    print("Normalizing resumes...")

    df["normalized_resume"] = (
        df["candidate_resume"]
        .apply(normalize_text)
    )

    # --------------------------------------------------------
    # Job description normalization
    # --------------------------------------------------------

    print("Normalizing job descriptions...")

    df["normalized_job_description"] = (
        df["job_description"]
        .apply(normalize_text)
    )

    # --------------------------------------------------------
    # Role normalization
    # --------------------------------------------------------

    print("Normalizing job roles...")

    df["normalized_job_role"] = (
        df["job_role"]
        .apply(normalize_role)
    )

    return df


# ============================================================
# QUALITY CHECK
# ============================================================

def print_normalization_report(
    original_df,
    normalized_df
):

    print()
    print("=" * 70)
    print("NORMALIZATION REPORT")
    print("=" * 70)

    print(
        f"Rows: {len(normalized_df)}"
    )

    print()

    # --------------------------------------------------------
    # Empty normalized fields
    # --------------------------------------------------------

    print("Empty normalized resumes:",
          (
              normalized_df[
                  "normalized_resume"
              ]
              .str.len()
              .eq(0)
              .sum()
          ))

    print("Empty normalized job descriptions:",
          (
              normalized_df[
                  "normalized_job_description"
              ]
              .str.len()
              .eq(0)
              .sum()
          ))

    print("Empty normalized roles:",
          (
              normalized_df[
                  "normalized_job_role"
              ]
              .str.len()
              .eq(0)
              .sum()
          ))

    # --------------------------------------------------------
    # Changed text
    # --------------------------------------------------------

    resume_changed = (
        original_df["candidate_resume"]
        != normalized_df["normalized_resume"]
    ).sum()

    description_changed = (
        original_df["job_description"]
        != normalized_df["normalized_job_description"]
    ).sum()

    role_changed = (
        original_df["job_role"]
        != normalized_df["normalized_job_role"]
    ).sum()

    print()

    print(
        f"Resumes changed: "
        f"{resume_changed}"
    )

    print(
        f"Job descriptions changed: "
        f"{description_changed}"
    )

    print(
        f"Job roles changed: "
        f"{role_changed}"
    )

    # --------------------------------------------------------
    # Show examples
    # --------------------------------------------------------

    print()
    print("=" * 70)
    print("NORMALIZATION EXAMPLES")
    print("=" * 70)

    examples = normalized_df.head(5)

    for index, row in examples.iterrows():

        print()
        print(f"ROW {index}")

        print(
            "Original role:",
            row["job_role"]
        )

        print(
            "Normalized role:",
            row["normalized_job_role"]
        )

        print(
            "Original resume:",
            row["candidate_resume"][:250]
        )

        print(
            "Normalized resume:",
            row["normalized_resume"][:250]
        )


# ============================================================
# MAIN
# ============================================================

def main():

    print("=" * 70)
    print("TECHNICAL DATASET NORMALIZATION")
    print("=" * 70)

    # --------------------------------------------------------
    # Load cleaned dataset
    # --------------------------------------------------------

    print()
    print("Loading cleaned dataset...")

    df = pd.read_csv(
        INPUT_FILE
    )

    print(
        f"Loaded rows: {len(df)}"
    )

    print(
        f"Loaded columns: {df.columns.tolist()}"
    )

    # --------------------------------------------------------
    # Normalize
    # --------------------------------------------------------

    normalized_df = normalize_dataset(
        df
    )

    # --------------------------------------------------------
    # Report
    # --------------------------------------------------------

    print_normalization_report(
        df,
        normalized_df
    )

    # --------------------------------------------------------
    # Save
    # --------------------------------------------------------

    normalized_df.to_csv(
        OUTPUT_FILE,
        index=False
    )

    print()
    print("=" * 70)
    print("NORMALIZATION COMPLETE")
    print("=" * 70)

    print()
    print(
        "Normalized dataset saved to:"
    )

    print(
        OUTPUT_FILE
    )


# ============================================================
# ENTRY POINT
# ============================================================

if __name__ == "__main__":
    main()