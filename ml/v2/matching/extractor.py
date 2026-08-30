# ============================================================
# AI-HIRE V2
# LLM EXTRACTION
# ============================================================

import os
import json
import time

from openai import OpenAI
from dotenv import load_dotenv


load_dotenv()


client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)

MODEL = os.getenv("OPENAI_MODEL")


JOB_SYSTEM_PROMPT = """
You are a job description information extraction system.

Extract structured technical requirements from the provided job description.

IMPORTANT:

1. Do NOT decide whether a candidate is suitable.
2. Do NOT rank candidates.
3. Do NOT invent skills.
4. Distinguish required skills from preferred/nice-to-have skills.
5. Normalize obvious aliases.
6. Extract minimum and maximum experience when available.
7. Identify the primary role family.
8. Programming languages must be separated from general skills.

Return ONLY valid JSON.

Schema:

{
    "role": "string",
    "role_family": "software|data|ml_ai|devops_cloud|mobile|qa|database|security|robotics|game|ar_vr|business|management|design|other",
    "required_skills": [],
    "preferred_skills": [],
    "programming_languages": [],
    "frameworks": [],
    "databases": [],
    "cloud": [],
    "devops": [],
    "concepts": [],
    "min_experience_years": null,
    "max_experience_years": null
}
"""


CANDIDATE_SYSTEM_PROMPT = """
You are a resume information extraction system.

Extract structured technical information from the provided resume.

IMPORTANT:

1. Do NOT judge the candidate.
2. Do NOT rank the candidate.
3. Do NOT invent skills.
4. Normalize obvious aliases.
5. Extract programming languages separately.
6. Extract frameworks, databases, cloud and DevOps technologies.
7. Identify the candidate's likely role family.
8. Estimate professional experience only when the resume provides enough evidence.

Return ONLY valid JSON.

Schema:

{
    "role": "string",
    "role_family": "software|data|ml_ai|devops_cloud|mobile|qa|database|security|robotics|game|ar_vr|business|management|design|other",
    "skills": [],
    "programming_languages": [],
    "frameworks": [],
    "databases": [],
    "cloud": [],
    "devops": [],
    "concepts": [],
    "experience_years": null,
    "education": []
}
"""


def extract_json(system_prompt, text, retries=3):

    for attempt in range(retries):

        try:

            response = client.chat.completions.create(
                model=MODEL,
                temperature=0,
                response_format={
                    "type": "json_object"
                },
                messages=[
                    {
                        "role": "system",
                        "content": system_prompt
                    },
                    {
                        "role": "user",
                        "content": text
                    }
                ]
            )

            content = response.choices[0].message.content

            return json.loads(content)

        except Exception as e:

            print(
                f"Extraction failed "
                f"(attempt {attempt + 1}/{retries}): {e}"
            )

            time.sleep(2)

    return None


def extract_job(job_description):

    return extract_json(
        JOB_SYSTEM_PROMPT,
        job_description
    )


def extract_candidate(resume):

    return extract_json(
        CANDIDATE_SYSTEM_PROMPT,
        resume
    )