import json
from psycopg.rows import dict_row

from backend.app.db.connection import get_connection
from backend.app.models.github import (
    GitHubProfileCreate,
    GitHubProfileResponse
)

def upsert_github_profile(
    user_id: str,
    github_username: str,
    features: dict,
):
    query = """
        INSERT INTO github_profiles
        (
            user_id,
            github_username,
            public_repos,
            followers,
            total_stars,
            languages,
            active_repos,
            last_synced_at
        )
        VALUES
        (
            %s,%s,%s,%s,%s,%s,%s,CURRENT_TIMESTAMP
        )

        ON CONFLICT (user_id)

        DO UPDATE SET

            github_username = EXCLUDED.github_username,
            public_repos = EXCLUDED.public_repos,
            followers = EXCLUDED.followers,
            total_stars = EXCLUDED.total_stars,
            languages = EXCLUDED.languages,
            active_repos = EXCLUDED.active_repos,
            last_synced_at = CURRENT_TIMESTAMP,
            updated_at = CURRENT_TIMESTAMP

        RETURNING *;
    """

    with get_connection() as conn:
        with conn.cursor(row_factory=dict_row) as cur:

            cur.execute(
                query,
                (
                    user_id,
                    github_username,
                    features["public_repos"],
                    features["followers"],
                    features["total_stars"],
                    json.dumps(features["languages"]),
                    features["active_repos"],
                ),
            )

            conn.commit()

            return cur.fetchone()


def get_github_profile(user_id: str):
    query = """
        SELECT *
        FROM github_profiles
        WHERE user_id = %s;
    """

    with get_connection() as conn:
        with conn.cursor(row_factory=dict_row) as cur:

            cur.execute(query, (user_id,))

            return cur.fetchone()


def delete_github_profile(user_id: str):
    query = """
        DELETE FROM github_profiles
        WHERE user_id = %s
        RETURNING *;
    """

    with get_connection() as conn:
        with conn.cursor(row_factory=dict_row) as cur:

            cur.execute(query, (user_id,))

            conn.commit()

            return cur.fetchone()


