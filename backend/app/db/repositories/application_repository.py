import json
from psycopg.rows import dict_row

from backend.app.db.connection import get_connection

from backend.app.models.application import (
    ApplicationResponse,
    ApplicationUpdate
)

def create_application(
    candidate_user_id: str,
    job_id: str,
    match_score: float,
    resume_s3_key_snapshot: str,
    resume_text_snapshot: str,
    parsed_role_snapshot: str,
    parsed_skills_snapshot: list,
    parsed_experience_snapshot: float,
):

    query = """
        INSERT INTO applications
        (
            candidate_user_id,
            job_id,
            match_score,

            resume_s3_key_snapshot,
            resume_text_snapshot,
            parsed_role_snapshot,
            parsed_skills_snapshot,
            parsed_experience_snapshot
        )

        VALUES
        (
            %s,%s,%s,
            %s,%s,%s,%s,%s
        )

        RETURNING *;
    """

    with get_connection() as conn:

        with conn.cursor(
            row_factory=dict_row
        ) as cur:

            cur.execute(
                query,
                (
                    candidate_user_id,
                    job_id,
                    match_score,

                    resume_s3_key_snapshot,
                    resume_text_snapshot,
                    parsed_role_snapshot,
                    json.dumps(parsed_skills_snapshot),
                    parsed_experience_snapshot,
                ),
            )

            conn.commit()

            return cur.fetchone()


def application_exists(
        candidate_user_id: str,
        job_id: str
):
    query = """
        SELECT 1
        FROM applications
        WHERE candidate_user_id = %s
        AND job_id = %s;
    """

    with get_connection() as conn:
        with conn.cursor(row_factory=dict_row) as cur:

            cur.execute(
                query,
                (
                    candidate_user_id,
                    job_id,
                ),
            )

            return cur.fetchone() is not None
        
def get_candidate_applications(candidate_user_id: str):
    query = """
        SELECT *
        FROM applications
        WHERE candidate_user_id = %s
        ORDER BY created_at DESC;
    """

    with get_connection() as conn:
        with conn.cursor(row_factory=dict_row) as cur:

            cur.execute(
                query,
                (candidate_user_id,),
            )

            return cur.fetchall()


def get_job_applications(job_id: str):
    query = """
        SELECT *
        FROM applications
        WHERE job_id = %s
        ORDER BY created_at DESC;
    """

    with get_connection() as conn:
        with conn.cursor(row_factory=dict_row) as cur:

            cur.execute(
                query,
                (job_id,),
            )

            return cur.fetchall()


def get_application_by_id(application_id: str):
    query = """
        SELECT *
        FROM applications
        WHERE application_id = %s;
    """

    with get_connection() as conn:
        with conn.cursor(row_factory=dict_row) as cur:

            cur.execute(
                query,
                (application_id,),
            )

            return cur.fetchone()


def update_application_status(
    application_id: str,
    application: ApplicationUpdate,
):
    query = """
        UPDATE applications
        SET
            application_status = %s,
            updated_at = CURRENT_TIMESTAMP
        WHERE application_id = %s
        RETURNING *;
    """

    with get_connection() as conn:
        with conn.cursor(row_factory=dict_row) as cur:

            cur.execute(
                query,
                (
                    application.application_status,
                    application_id,
                ),
            )

            conn.commit()

            return cur.fetchone()


def delete_application(application_id: str):
    query = """
        DELETE FROM applications
        WHERE application_id = %s
        RETURNING *;
    """

    with get_connection() as conn:
        with conn.cursor(row_factory=dict_row) as cur:

            cur.execute(
                query,
                (application_id,),
            )

            conn.commit()

            return cur.fetchone()