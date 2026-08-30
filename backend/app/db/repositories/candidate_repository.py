from psycopg.rows import dict_row
import json

from backend.app.db.connection import get_connection
from backend.app.models.candidate import (
    CandidateProfileCreate,
    CandidateProfileUpdate
)


def create_candidate_profile(
    user_id: str,
    profile: CandidateProfileCreate
):
    query = """
        INSERT INTO candidate_profiles
        (
            user_id,
            phone,
            current_location,
            linkedin_url,
            portfolio_url
        )
        VALUES (%s,%s,%s,%s,%s)
        RETURNING *;
    """

    with get_connection() as conn:
        with conn.cursor(row_factory=dict_row) as cur:

            cur.execute(
                query,
                (
                    user_id,
                    profile.phone,
                    profile.current_location,
                    str(profile.linkedin_url) if profile.linkedin_url else None,
                    str(profile.portfolio_url) if profile.portfolio_url else None,
                ),
            )

            conn.commit()

            return cur.fetchone()
        
def get_candidate_profile(
    user_id: str
):
    query = """
        SELECT *
        FROM candidate_profiles
        WHERE user_id = %s;
    """

    with get_connection() as conn:
        with conn.cursor(row_factory=dict_row) as cur:

            cur.execute(query,(user_id,),)

            return cur.fetchone()
        
def update_candidate_profile(
    user_id: str,
    profile: CandidateProfileUpdate,
):
    query = """
        UPDATE candidate_profiles
        SET
            phone = %s,
            current_location = %s,
            linkedin_url = %s,
            portfolio_url = %s,
            updated_at = CURRENT_TIMESTAMP
        WHERE user_id = %s
        RETURNING *;
    """

    with get_connection() as conn:
        with conn.cursor(row_factory=dict_row) as cur:

            cur.execute(
                query,
                (
                    profile.phone,
                    profile.current_location,
                    str(profile.linkedin_url) if profile.linkedin_url else None,
                    str(profile.portfolio_url) if profile.portfolio_url else None,
                    user_id,
                ),
            )

            conn.commit()
            return cur.fetchone()


def delete_candidate_profile(user_id: str):
    query = """
        DELETE FROM candidate_profiles
        WHERE user_id = %s;
    """

    with get_connection() as conn:
        with conn.cursor(row_factory=dict_row) as cur:

            cur.execute(query, (user_id,))
            conn.commit()

            return cur.rowcount > 0

def update_resume_parsed_data(
    user_id: str,
    resume_text: str,
    parsed_role: str,
    parsed_skills: list,
    parsed_experience: float,
):

    query = """
        UPDATE candidate_profiles
        SET
            resume_text = %s,
            parsed_role = %s,
            parsed_skills = %s,
            parsed_experience = %s,
            resume_parsed_at = CURRENT_TIMESTAMP,
            updated_at = CURRENT_TIMESTAMP
        WHERE user_id = %s
        RETURNING *;
    """

    with get_connection() as conn:
        with conn.cursor(row_factory=dict_row) as cur:

            cur.execute(
                query,
                (
                    resume_text,
                    parsed_role,
                    json.dumps(parsed_skills),
                    parsed_experience,
                    user_id,
                ),
            )

            conn.commit()

            return cur.fetchone()
