from psycopg.rows import dict_row

from backend.app.db.connection import get_connection
import json

def create_job(
    employer_user_id: str,
    job_data: dict
):
    query = """
        INSERT INTO jobs
        (
            employer_user_id,
            title,
            description,
            location,
            employment_type,
            experience_required,
            required_skills,
            preferred_skills
        )
        VALUES
        (
            %s,%s,%s,%s,%s,%s,%s,%s
        )
        RETURNING *;
    """

    with get_connection() as conn:
        with conn.cursor(row_factory=dict_row) as cur:

            cur.execute(
                query,
                (
                    employer_user_id,
                    job_data["title"],
                    job_data["description"],
                    job_data.get("location"),
                    job_data.get("employment_type"),
                    job_data.get("experience_required"),
                    json.dumps(job_data.get("required_skills")),
                    json.dumps(job_data.get("preferred_skills")),
                ),
            )

            conn.commit()

            return cur.fetchone()

def get_job_by_id(job_id: str):

    query = """
        SELECT *
        FROM jobs
        WHERE job_id = %s;
    """

    with get_connection() as conn:
        with conn.cursor(row_factory=dict_row) as cur:

            cur.execute(
                query,
                (job_id,)
            )

            return cur.fetchone()

def get_jobs_by_employer(
    employer_user_id: str
):

    query = """
        SELECT *
        FROM jobs
        WHERE employer_user_id = %s
        ORDER BY created_at DESC;
    """

    with get_connection() as conn:
        with conn.cursor(row_factory=dict_row) as cur:

            cur.execute(
                query,
                (employer_user_id,)
            )

            return cur.fetchall()


def update_job(
    job_id: str,
    job_data: dict
):

    query = """
        UPDATE jobs
        SET
            title = COALESCE(%s,title),
            description = COALESCE(%s,description),
            location = COALESCE(%s,location),
            employment_type = COALESCE(%s,employment_type),
            experience_required = COALESCE(%s,experience_required),
            required_skills = COALESCE(%s,required_skills),
            preferred_skills = COALESCE(%s,preferred_skills),
            updated_at = CURRENT_TIMESTAMP

        WHERE job_id = %s

        RETURNING *;
    """

    with get_connection() as conn:
        with conn.cursor(row_factory=dict_row) as cur:

            cur.execute(
                query,
                (
                    job_data.get("title"),
                    job_data.get("description"),
                    job_data.get("location"),
                    job_data.get("employment_type"),
                    job_data.get("experience_required"),
                    json.dumps(job_data.get("required_skills")),
                    json.dumps(job_data.get("preferred_skills")),
                    job_id,
                ),
            )

            conn.commit()

            return cur.fetchone()

def delete_job(job_id: str):

    query = """
        DELETE FROM jobs
        WHERE job_id = %s
        RETURNING job_id;
    """

    with get_connection() as conn:
        with conn.cursor(row_factory=dict_row) as cur:

            cur.execute(
                query,
                (job_id,)
            )

            conn.commit()

            return cur.fetchone()
        
