import re
from pathlib import Path

import pandas as pd


# ============================================================
# PATHS
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent

RAW_DIR = BASE_DIR / "data" / "raw"
PROCESSED_DIR = BASE_DIR / "data" / "processed"

PROCESSED_DIR.mkdir(
    parents=True,
    exist_ok=True
)


# ============================================================
# INPUT FILES
# ============================================================

APPLICANT_FILE = (
    RAW_DIR / "job_applicant_dataset.csv"
)

RECRUITER_FILE = (
    RAW_DIR / "recruiter_decision_dataset.csv"
)


# ============================================================
# OUTPUT FILES
# ============================================================

TECH_OUTPUT = (
    PROCESSED_DIR
    / "technical_matching_dataset.csv"
)

NON_TECH_OUTPUT = (
    PROCESSED_DIR
    / "non_technical_dataset.csv"
)

REVIEW_OUTPUT = (
    PROCESSED_DIR
    / "technical_review_dataset.csv"
)


# ============================================================
# TECHNICAL ROLE KEYWORDS
# ============================================================

TECH_KEYWORDS = {

    # --------------------------------------------------------
    # Software Engineering
    # --------------------------------------------------------

    "software engineer",
    "software developer",
    "software development",
    "software programmer",

    "developer",
    "programmer",

    "backend",
    "backend developer",
    "backend engineer",

    "frontend",
    "frontend developer",
    "frontend engineer",

    "front end",
    "front end developer",

    "full stack",
    "full stack developer",
    "full stack engineer",

    "web developer",
    "web development",

    "application developer",
    "application engineer",

    "mobile developer",
    "mobile application developer",

    "android developer",
    "ios developer",

    # --------------------------------------------------------
    # Data
    # --------------------------------------------------------

    "data scientist",
    "data science",

    "data analyst",
    "data analysis",

    "data engineer",
    "data engineering",

    "database administrator",
    "database engineer",
    "database developer",

    "business intelligence",
    "bi developer",

    # --------------------------------------------------------
    # AI / ML
    # --------------------------------------------------------

    "machine learning",
    "machine learning engineer",
    "ml engineer",

    "artificial intelligence",
    "ai engineer",

    "ai developer",
    "ai researcher",

    "deep learning",

    "nlp",
    "nlp engineer",
    "natural language processing",

    "computer vision",
    "computer vision engineer",

    "research engineer",
    "research scientist",

    # --------------------------------------------------------
    # Cloud / DevOps
    # --------------------------------------------------------

    "devops",
    "devops engineer",

    "cloud engineer",
    "cloud computing",

    "cloud architect",
    "cloud developer",

    "site reliability",
    "site reliability engineer",
    "sre",

    "platform engineer",
    "platform engineering",

    "infrastructure engineer",

    # --------------------------------------------------------
    # Systems / OS / Networking
    # --------------------------------------------------------

    "systems engineer",
    "system engineer",

    "systems analyst",

    "system administrator",
    "systems administrator",

    "network engineer",
    "network administrator",

    "networking",

    "infrastructure",

    "linux engineer",

    # --------------------------------------------------------
    # Cybersecurity
    # --------------------------------------------------------

    "cybersecurity",
    "cyber security",

    "cybersecurity engineer",
    "cyber security engineer",

    "security engineer",
    "security analyst",

    "information security",
    "information security engineer",

    # --------------------------------------------------------
    # Embedded / ECE
    # --------------------------------------------------------

    "embedded",
    "embedded engineer",
    "embedded software engineer",

    "embedded systems",

    "firmware",
    "firmware engineer",

    "hardware engineer",
    "hardware developer",

    "electronics engineer",
    "electronics",

    "electrical engineer",
    "electrical engineering",

    "vlsi",
    "vlsi engineer",

    "rtl",
    "rtl engineer",

    "fpga",
    "fpga engineer",

    "asic",
    "asic engineer",

    "verification engineer",

    "semiconductor",

    "microcontroller",
    "microprocessor",

    # --------------------------------------------------------
    # Robotics / IoT
    # --------------------------------------------------------

    "robotics",
    "robotics engineer",

    "robotics software engineer",

    "iot",
    "iot engineer",
    "internet of things",

    "automation engineer",

    # --------------------------------------------------------
    # Testing / QA
    # --------------------------------------------------------

    "qa engineer",
    "quality assurance engineer",

    "test engineer",
    "software tester",

    "software testing",

    "qa automation",
    "qa automation engineer",

    "automation testing",

    "sdet",

    # --------------------------------------------------------
    # Technical Support / Solutions
    # --------------------------------------------------------

    "technical support engineer",
    "technical support",

    "solutions engineer",
    "technical consultant",
}


# ============================================================
# STRONG TECHNICAL KEYWORDS
# ============================================================

STRONG_TECH_KEYWORDS = {

    "python",
    "java",
    "javascript",
    "typescript",
    "c++",
    "c#",
    "golang",
    "rust",

    "sql",
    "mysql",
    "postgresql",
    "mongodb",
    "oracle",

    "react",
    "angular",
    "vue",
    "node.js",
    "nodejs",

    "fastapi",
    "django",
    "flask",
    "spring boot",

    "docker",
    "kubernetes",
    "aws",
    "azure",
    "gcp",

    "tensorflow",
    "pytorch",
    "scikit-learn",

    "machine learning",
    "deep learning",

    "git",
    "github",

    "linux",

    "data structures",
    "algorithms",

    "operating systems",
    "computer networks",
    "dbms",

    "embedded systems",
    "firmware",

    "vlsi",
    "fpga",
    "rtl",

    "robotics",
    "ros",

    "cybersecurity",
    "cyber security",
}


# ============================================================
# NON-TECHNICAL KEYWORDS
# ============================================================

NON_TECH_KEYWORDS = {

    # Healthcare
    "dentist",
    "dental",
    "nurse",
    "nursing",
    "doctor",
    "physician",
    "medical doctor",
    "pharmacist",
    "pharmacy",
    "surgeon",
    "therapist",
    "veterinarian",
    "veterinary",

    # Legal
    "lawyer",
    "legal consultant",
    "legal advisor",
    "attorney",
    "paralegal",

    # Finance
    "accountant",
    "accounting",
    "financial analyst",
    "banker",
    "investment banker",

    # Sales / Marketing
    "sales representative",
    "sales executive",
    "sales manager",
    "marketing manager",
    "marketing specialist",
    "digital marketing",
    "brand manager",

    # Hospitality / Food
    "chef",
    "cook",
    "restaurant manager",
    "hotel manager",
    "hospitality",

    # Fitness
    "personal trainer",
    "fitness coach",
    "fitness trainer",

    # Events
    "event planner",
    "event manager",
    "event coordinator",

    # Real estate
    "real estate",
    "realty",
    "realtor",
    "property dealer",

    # Education
    "teacher",
    "school teacher",
    "professor",
    "lecturer",
    "tutor",
    "instructor",

    # Manual / Trades
    "gardener",
    "electrician",
    "plumber",
    "carpenter",
    "mechanic",

    # Creative
    "fashion designer",
    "interior designer",
    "graphic designer",
    "fashion",
    "beautician",

    # Other
    "social worker",
    "human resources",
    "hr manager",
    "recruiter",
}


# ============================================================
# LABEL NORMALIZATION
# ============================================================

LABEL_MAP = {

    # Positive
    "accepted": 1,
    "accept": 1,
    "selected": 1,
    "select": 1,
    "hired": 1,
    "hire": 1,
    "yes": 1,
    "true": 1,
    "1": 1,
    "pass": 1,
    "passed": 1,

    # Negative
    "rejected": 0,
    "reject": 0,
    "declined": 0,
    "decline": 0,
    "not selected": 0,
    "not_selected": 0,
    "no": 0,
    "false": 0,
    "0": 0,
    "fail": 0,
    "failed": 0,
}


# ============================================================
# TEXT CLEANING
# ============================================================

def clean_text(value):
    """
    Basic text cleaning.

    Keeps semantic content but removes:
    - NaN
    - null characters
    - excessive whitespace
    - repeated newlines
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


# ============================================================
# LABEL NORMALIZATION
# ============================================================

def normalize_label(value):
    """
    Convert hiring decisions into:

        1 = accepted
        0 = rejected

    Returns None if the value is unknown.
    """

    if pd.isna(value):
        return None

    value = str(value).strip().lower()

    return LABEL_MAP.get(
        value,
        None
    )


# ============================================================
# JOB TEXT
# ============================================================

def build_job_text(
    job_role,
    job_description
):
    """
    Combine role + description.

    Useful later because some datasets have
    very short job descriptions.
    """

    role = clean_text(job_role)
    description = clean_text(
        job_description
    )

    if role and description:
        return f"{role}. {description}"

    if role:
        return role

    return description


# ============================================================
# ROLE CLASSIFICATION
# ============================================================

def classify_job(
    job_role,
    job_description
):
    """
    Classify jobs into:

        TECH
        NON_TECH
        REVIEW

    REVIEW is intentionally conservative.
    """

    role = clean_text(
        job_role
    ).lower()

    description = clean_text(
        job_description
    ).lower()

    combined = (
        role + " " + description
    )

    # --------------------------------------------------------
    # Non-technical role evidence
    # --------------------------------------------------------

    for keyword in NON_TECH_KEYWORDS:

        if keyword in role:

            return (
                "NON_TECH",
                f"non-tech role: {keyword}"
            )

    # --------------------------------------------------------
    # Technical role evidence
    # --------------------------------------------------------

    for keyword in TECH_KEYWORDS:

        if keyword in role:

            return (
                "TECH",
                f"technical role: {keyword}"
            )

    # --------------------------------------------------------
    # Technical evidence from description
    # --------------------------------------------------------

    tech_matches = []

    for keyword in STRONG_TECH_KEYWORDS:

        if keyword in combined:

            tech_matches.append(
                keyword
            )

    if len(tech_matches) >= 2:

        return (
            "TECH",
            "multiple technical skills: "
            + ", ".join(
                sorted(tech_matches)[:5]
            )
        )

    if len(tech_matches) == 1:

        keyword = tech_matches[0]

        if keyword in {
            "python",
            "java",
            "javascript",
            "c++",
            "c#",
            "sql",
            "machine learning",
            "embedded systems",
            "vlsi",
            "fpga",
            "robotics",
            "cybersecurity",
        }:

            return (
                "TECH",
                f"technical skill: {keyword}"
            )

    # --------------------------------------------------------
    # Non-technical evidence from description
    # --------------------------------------------------------

    for keyword in NON_TECH_KEYWORDS:

        if keyword in description:

            return (
                "NON_TECH",
                f"non-tech description: {keyword}"
            )

    # --------------------------------------------------------
    # Ambiguous
    # --------------------------------------------------------

    return (
        "REVIEW",
        "ambiguous role"
    )


# ============================================================
# NORMALIZE DATASET STRUCTURE
# ============================================================

# ============================================================
# NORMALIZE DATASET STRUCTURE
# ============================================================

def normalize_dataset(
    df,
    dataset_name
):
    """
    Convert different source dataset schemas into
    one standardized schema.

    Standard output:

        candidate_resume
        job_role
        job_description
        label
        source_dataset
        decision_reason
    """

    df = df.copy()

    # --------------------------------------------------------
    # Normalize column names
    # --------------------------------------------------------

    df.columns = [
        str(column)
        .strip()
        .lower()
        .replace(" ", "_")
        for column in df.columns
    ]

    print()
    print(
        f"Normalized columns for {dataset_name}:"
    )

    print(
        df.columns.tolist()
    )

    # --------------------------------------------------------
    # COLUMN ALIASES
    #
    # Different datasets use different names for
    # the same piece of information.
    # --------------------------------------------------------

    COLUMN_ALIASES = {

        "candidate_resume": [
            "candidate_resume",
            "resume",
            "candidate_cv",
            "cv",
        ],

        "job_role": [
            "job_role",
            "role",
            "job_roles",
            "job_title",
            "position",
        ],

        "job_description": [
            "job_description",
            "job_desc",
            "description",
            "jobdetails",
            "job_details",
        ],

        "label": [
            "label",
            "decision",
            "status",
            "outcome",
            "hiring_decision",
            "best_match",
        ],

        "decision_reason": [
            "decision_reason",
            "reason_for_decision",
            "reason",
            "rejection_reason",
        ],
    }

    # --------------------------------------------------------
    # Find actual column for each standardized field
    # --------------------------------------------------------

    resolved_columns = {}

    for standard_name, aliases in COLUMN_ALIASES.items():

        found_column = None

        for alias in aliases:

            if alias in df.columns:

                found_column = alias
                break

        resolved_columns[
            standard_name
        ] = found_column

    # --------------------------------------------------------
    # Print mapping
    # --------------------------------------------------------

    print()
    print("Column mapping:")

    for standard_name, actual_column in resolved_columns.items():

        print(
            f"  {standard_name:20} <- "
            f"{actual_column}"
        )

    # --------------------------------------------------------
    # Required columns
    # --------------------------------------------------------

    required_fields = [
        "candidate_resume",
        "job_role",
        "job_description",
        "label",
    ]

    missing = [
        field
        for field in required_fields
        if resolved_columns[field] is None
    ]

    if missing:

        raise ValueError(
            f"{dataset_name} is missing required "
            f"fields: {missing}\n\n"
            f"Available columns: "
            f"{df.columns.tolist()}"
        )

    # --------------------------------------------------------
    # Create standardized dataframe
    # --------------------------------------------------------

    output = pd.DataFrame()

    # --------------------------------------------------------
    # Resume
    # --------------------------------------------------------

    output["candidate_resume"] = (
        df[
            resolved_columns[
                "candidate_resume"
            ]
        ]
        .apply(clean_text)
    )

    # --------------------------------------------------------
    # Job role
    # --------------------------------------------------------

    output["job_role"] = (
        df[
            resolved_columns[
                "job_role"
            ]
        ]
        .apply(clean_text)
    )

    # --------------------------------------------------------
    # Job description
    # --------------------------------------------------------

    output["job_description"] = (
        df[
            resolved_columns[
                "job_description"
            ]
        ]
        .apply(clean_text)
    )

    # --------------------------------------------------------
    # Label
    # --------------------------------------------------------

    output["label"] = (
        df[
            resolved_columns[
                "label"
            ]
        ]
        .apply(normalize_label)
    )

    # --------------------------------------------------------
    # Source dataset
    # --------------------------------------------------------

    output["source_dataset"] = (
        dataset_name
    )

    # --------------------------------------------------------
    # Decision reason
    # --------------------------------------------------------

    reason_column = (
        resolved_columns[
            "decision_reason"
        ]
    )

    if reason_column is not None:

        output["decision_reason"] = (
            df[reason_column]
            .apply(clean_text)
        )

    else:

        output["decision_reason"] = ""

    return output
# ============================================================
# PROCESS DATASET
# ============================================================

def process_dataset(
    df,
    dataset_name
):

    print()
    print("=" * 70)
    print(
        f"PROCESSING: {dataset_name}"
    )
    print("=" * 70)

    print(
        f"Original rows: {len(df)}"
    )

    # --------------------------------------------------------
    # Normalize structure
    # --------------------------------------------------------

    df = normalize_dataset(
        df,
        dataset_name
    )

    # --------------------------------------------------------
    # Normalize labels
    # --------------------------------------------------------

    before_labels = len(df)

    df = df.dropna(
        subset=["label"]
    )

    removed_labels = (
        before_labels - len(df)
    )

    print(
        f"Removed invalid labels: "
        f"{removed_labels}"
    )

    df["label"] = (
        df["label"]
        .astype(int)
    )

    # --------------------------------------------------------
    # Remove empty resumes
    # --------------------------------------------------------

    before_resume = len(df)

    df = df[
        df["candidate_resume"].str.len() > 0
    ]

    print(
        "Removed empty resumes: "
        f"{before_resume - len(df)}"
    )

    # --------------------------------------------------------
    # Remove empty job roles
    # --------------------------------------------------------

    before_role = len(df)

    df = df[
        df["job_role"].str.len() > 0
    ]

    print(
        "Removed empty job roles: "
        f"{before_role - len(df)}"
    )

    # --------------------------------------------------------
    # Classify jobs
    # --------------------------------------------------------

    classifications = (
        df.apply(
            lambda row: classify_job(
                row["job_role"],
                row["job_description"]
            ),
            axis=1
        )
    )

    df["job_type"] = [
        result[0]
        for result in classifications
    ]

    df["classification_reason"] = [
        result[1]
        for result in classifications
    ]

    # --------------------------------------------------------
    # Statistics
    # --------------------------------------------------------

    print()
    print("Job classification:")

    print(
        df["job_type"]
        .value_counts()
    )

    # --------------------------------------------------------
    # Remove exact duplicates
    # --------------------------------------------------------

    before_duplicates = len(df)

    df = df.drop_duplicates(
        subset=[
            "candidate_resume",
            "job_role",
            "job_description",
            "label",
        ]
    )

    print(
        "Removed exact duplicates: "
        f"{before_duplicates - len(df)}"
    )

    return df


# ============================================================
# DATA QUALITY REPORT
# ============================================================

def print_quality_report(
    df,
    dataset_name
):

    print()
    print("=" * 70)
    print(
        f"QUALITY REPORT: {dataset_name}"
    )
    print("=" * 70)

    print(
        f"Rows: {len(df)}"
    )

    print()
    print("Label distribution:")

    print(
        df["label"]
        .value_counts()
        .sort_index()
    )

    print()
    print("Label percentages:")

    print(
        df["label"]
        .value_counts(
            normalize=True
        )
        .sort_index()
        .mul(100)
        .round(2)
    )

    print()
    print("Job types:")

    print(
        df["job_type"]
        .value_counts()
    )

    # --------------------------------------------------------
    # Most common technical roles
    # --------------------------------------------------------

    print()
    print(
        "Most common technical roles:"
    )

    technical = df[
        df["job_type"] == "TECH"
    ]

    print(
        technical["job_role"]
        .value_counts()
        .head(20)
    )

    # --------------------------------------------------------
    # Label distribution by source
    # --------------------------------------------------------

    print()
    print(
        "Labels by source:"
    )

    print(
        pd.crosstab(
            df["source_dataset"],
            df["label"]
        )
    )


# ============================================================
# MAIN
# ============================================================

def main():

    print("=" * 70)
    print("TECHNICAL DATASET CLEANING")
    print("=" * 70)

    # --------------------------------------------------------
    # Load datasets
    # --------------------------------------------------------

    print()
    print("Loading datasets...")

    applicant_df = pd.read_csv(
        APPLICANT_FILE
    )

    recruiter_df = pd.read_csv(
        RECRUITER_FILE
    )

    print(
        f"Job Applicant: "
        f"{len(applicant_df)} rows"
    )

    print(
        f"Recruiter Decision: "
        f"{len(recruiter_df)} rows"
    )

    # --------------------------------------------------------
    # Process datasets independently
    # --------------------------------------------------------

    applicant_clean = process_dataset(
        applicant_df,
        "job_applicant"
    )

    recruiter_clean = process_dataset(
        recruiter_df,
        "recruiter_decision"
    )

    # --------------------------------------------------------
    # Combine
    # --------------------------------------------------------

    combined = pd.concat(
        [
            applicant_clean,
            recruiter_clean,
        ],
        ignore_index=True
    )

    print()
    print("=" * 70)
    print("COMBINED DATASET")
    print("=" * 70)

    print(
        f"Rows before final filtering: "
        f"{len(combined)}"
    )

    # --------------------------------------------------------
    # Split by classification
    # --------------------------------------------------------

    technical_df = combined[
        combined["job_type"] == "TECH"
    ].copy()

    non_technical_df = combined[
        combined["job_type"] == "NON_TECH"
    ].copy()

    review_df = combined[
        combined["job_type"] == "REVIEW"
    ].copy()

    # --------------------------------------------------------
    # Shuffle technical dataset
    # --------------------------------------------------------

    technical_df = (
        technical_df
        .sample(
            frac=1,
            random_state=42
        )
        .reset_index(drop=True)
    )

    non_technical_df = (
        non_technical_df
        .reset_index(drop=True)
    )

    review_df = (
        review_df
        .reset_index(drop=True)
    )

    # --------------------------------------------------------
    # Save technical dataset
    # --------------------------------------------------------

    technical_df.to_csv(
        TECH_OUTPUT,
        index=False
    )

    # --------------------------------------------------------
    # Save non-technical dataset
    # --------------------------------------------------------

    non_technical_df.to_csv(
        NON_TECH_OUTPUT,
        index=False
    )

    # --------------------------------------------------------
    # Save review dataset
    # --------------------------------------------------------

    review_df.to_csv(
        REVIEW_OUTPUT,
        index=False
    )

    # --------------------------------------------------------
    # Reports
    # --------------------------------------------------------

    print_quality_report(
        technical_df,
        "FINAL TECHNICAL DATASET"
    )

    print()
    print("=" * 70)
    print("FINAL RESULTS")
    print("=" * 70)

    print(
        f"Technical rows: "
        f"{len(technical_df)}"
    )

    print(
        f"Non-technical rows: "
        f"{len(non_technical_df)}"
    )

    print(
        f"Review rows: "
        f"{len(review_df)}"
    )

    print()
    print(
        f"Technical dataset saved to:\n"
        f"{TECH_OUTPUT}"
    )

    print()
    print(
        f"Non-technical dataset saved to:\n"
        f"{NON_TECH_OUTPUT}"
    )

    print()
    print(
        f"Review dataset saved to:\n"
        f"{REVIEW_OUTPUT}"
    )

    # --------------------------------------------------------
    # Show review roles
    # --------------------------------------------------------

    if len(review_df) > 0:

        print()
        print("=" * 70)
        print("REVIEW REQUIRED")
        print("=" * 70)

        print(
            review_df[
                [
                    "job_role",
                    "job_description",
                    "classification_reason",
                ]
            ]
            .head(30)
            .to_string(index=False)
        )

    # --------------------------------------------------------
    # Sample technical rows
    # --------------------------------------------------------

    print()
    print("=" * 70)
    print("SAMPLE TECHNICAL ROWS")
    print("=" * 70)

    print(
        technical_df[
            [
                "job_role",
                "label",
                "source_dataset",
            ]
        ]
        .head(20)
        .to_string(index=False)
    )

    print()
    print("=" * 70)
    print("CLEANING COMPLETE")
    print("=" * 70)


# ============================================================
# ENTRY POINT
# ============================================================

if __name__ == "__main__":
    main()