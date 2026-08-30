import sys
import os
import json

import pandas as pd
from tqdm import tqdm

sys.path.append(
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), "../..")
    )
)

from ml.v2.matching.extractor import extract_job


INPUT = "ml/data/processed/naukri_jobs_matching_v2.csv"
OUTPUT = "ml/data/processed/jobs_extracted_v2.jsonl"


jobs = pd.read_csv(INPUT)

print(f"Jobs: {len(jobs)}")


existing_ids = set()

if os.path.exists(OUTPUT):

    with open(OUTPUT, "r", encoding="utf-8") as f:

        for line in f:

            try:
                data = json.loads(line)
                existing_ids.add(str(data["job_id"]))

            except Exception:
                pass


print(f"Already extracted: {len(existing_ids)}")


with open(OUTPUT, "a", encoding="utf-8") as f:

    for _, row in tqdm(
        jobs.iterrows(),
        total=len(jobs)
    ):

        job_id = str(row["job_id"])

        if job_id in existing_ids:
            continue

        description = str(
            row["job_description"]
        )
        skills = str(
            row["job_skills"]
        )

        text = f"""
        JOB TITLE:
        {row["job_title"]}

        JOB DESCRIPTION:
        {description}

        EXTRACTED JOB SKILLS FROM SOURCE DATA:
        {skills}
        """

        result = extract_job(text)

        if result is None:
            continue

        result["job_id"] = job_id
        result["job_title"] = row["job_title"]

        f.write(
            json.dumps(
                result,
                ensure_ascii=False
            ) + "\n"
        )

        f.flush()


print("Job extraction complete.")