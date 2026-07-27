import json

from psycopg.rows import dict_row

from backend.app.db.connection import get_connection

def upsert_leetcode_profile(
    user_id: str,
    leetcode_username: str,
    features: dict,
):
    query = """
    INSERT INTO leetcode_profiles
    (
        user_id,
        leetcode_username,

        language_diversity,
        language_list,
        primary_language,
        primary_language_share,

        skill_stats,

        contest_rating,
        contest_rank_percentile,
        contest_attended,

        total_solved,
        easy_solved,
        medium_solved,
        hard_solved,

        streak,
        active_days,

        last_synced_at
    )

    VALUES
    (
        %s,%s,
        %s,%s,%s,%s,
        %s,
        %s,%s,%s,
        %s,%s,%s,%s,
        %s,%s,
        CURRENT_TIMESTAMP
    )

    ON CONFLICT (user_id)

    DO UPDATE SET

        leetcode_username = EXCLUDED.leetcode_username,

        language_diversity = EXCLUDED.language_diversity,
        language_list = EXCLUDED.language_list,
        primary_language = EXCLUDED.primary_language,
        primary_language_share = EXCLUDED.primary_language_share,

        skill_stats = EXCLUDED.skill_stats,

        contest_rating = EXCLUDED.contest_rating,
        contest_rank_percentile = EXCLUDED.contest_rank_percentile,
        contest_attended = EXCLUDED.contest_attended,

        total_solved = EXCLUDED.total_solved,
        easy_solved = EXCLUDED.easy_solved,
        medium_solved = EXCLUDED.medium_solved,
        hard_solved = EXCLUDED.hard_solved,

        streak = EXCLUDED.streak,
        active_days = EXCLUDED.active_days,

        last_synced_at = CURRENT_TIMESTAMP,
        updated_at = CURRENT_TIMESTAMP

    RETURNING *;
    """

    with get_connection() as conn:
        with conn.cursor(row_factory = dict_row) as cur:

            cur.execute(
                query,
                (
                    user_id,
                    leetcode_username,

                    features["language_diversity"],
                    json.dumps(features["language_list"]),
                    features["primary_language"],
                    features["primary_language_share"],

                    json.dumps(features["skill_stats"]),

                    features["contest_rating"],
                    features["contest_rank_percentile"],
                    features["contest_attended"],

                    features["total_solved"],
                    features["easy"],
                    features["medium"],
                    features["hard"],

                    features["streak"],
                    features["active_days"],
                ),
            )

            conn.commit()

            return cur.fetchone()

def get_leetcode_profile(user_id: str):

    query = """
    SELECT *
    FROM leetcode_profiles
    WHERE user_id=%s;
    """

    with get_connection() as conn:
        with conn.cursor(row_factory=dict_row) as cur:

            cur.execute(query, (user_id,))

            return cur.fetchone()


def delete_leetcode_profile(user_id: str):

    query = """
    DELETE FROM leetcode_profiles
    WHERE user_id=%s
    RETURNING *;
    """

    with get_connection() as conn:
        with conn.cursor(row_factory=dict_row) as cur:

            cur.execute(query, (user_id,))

            conn.commit()

            return cur.fetchone()