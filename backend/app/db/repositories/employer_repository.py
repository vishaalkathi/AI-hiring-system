from psycopg.rows import dict_row

from backend.app.db.connection import get_connection
from backend.app.models.employer import (
    EmployerProfileCreate,
    EmployerProfileUpdate,
    EmployerProfileResponse
)

def create_employer_profile(
    user_id: str,
    profile: EmployerProfileCreate
):
    query = """
        INSERT INTO employer_profiles
        (
            user_id,
            company_name,
            company_description,
            website_url,
            company_location
        )
        VALUES (%s, %s, %s, %s, %s)
        RETURNING *;
    """

    with get_connection() as conn:
        with conn.cursor(row_factory=dict_row) as cur:

            cur.execute(
                query,
                (
                    user_id,
                    profile.company_name,
                    profile.company_description,
                    str(profile.website_url) if profile.website_url else None,
                    profile.company_location,
                ),
            )

            conn.commit()

            return cur.fetchone()
        

def get_employer_profile(user_id: str):

    query = """
        SELECT *
        FROM employer_profiles
        WHERE user_id = %s;
    """

    with get_connection() as conn:
        with conn.cursor(row_factory=dict_row) as cur:

            cur.execute(query, (user_id,))

            return cur.fetchone()


def update_employer_profile(
    user_id: str,
    profile: EmployerProfileUpdate,
):
    query = """
        UPDATE employer_profiles
        SET
            company_name = %s,
            company_description = %s,
            website_url = %s,
            company_location = %s,
            updated_at = CURRENT_TIMESTAMP
        WHERE user_id = %s
        RETURNING *;
    """

    with get_connection() as conn:
        with conn.cursor(row_factory=dict_row) as cur:

            cur.execute(
                query,
                (
                    profile.company_name,
                    profile.company_description,
                    str(profile.website_url) if profile.website_url else None,
                    profile.company_location,
                    user_id,
                ),
            )

            conn.commit()

            return cur.fetchone()


def delete_employer_profile(user_id: str):

    query = """
        DELETE FROM employer_profiles
        WHERE user_id = %s;
    """

    with get_connection() as conn:
        with conn.cursor() as cur:

            cur.execute(query, (user_id,))

            conn.commit()