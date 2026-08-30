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

from ml.matching.extractor import extract_candidate


INPUT = "ml/data/processed/candidates_matching_v2.csv"
OUTPUT = "ml/data/processed/candidates_extracted_v2.jsonl"


candidates = pd.read_csv(INPUT)

print(f"Candidates: {len(candidates)}")


existing_ids = set()

if os.path.exists(OUTPUT):

    with open(OUTPUT, "r", encoding="utf-8") as f:

        for line in f:

            try:
                data = json.loads(line)
                existing_ids.add(
                    str(data["candidate_id"])
                )

            except Exception:
                pass


print(
    f"Already extracted: "
    f"{len(existing_ids)}"
)


with open(
    OUTPUT,
    "a",
    encoding="utf-8"
) as f:

    for _, row in tqdm(
        candidates.iterrows(),
        total=len(candidates)
    ):

        candidate_id = str(
            row["candidate_id"]
        )

        if candidate_id in existing_ids:
            continue

        resume = str(
            row["candidate_resume"]
        )

        result = extract_candidate(resume)

        if result is None:
            continue

        result["candidate_id"] = candidate_id
        result["job_role"] = row["job_role"]

        f.write(
            json.dumps(
                result,
                ensure_ascii=False
            ) + "\n"
        )

        f.flush()


print(
    "Candidate extraction complete."
)