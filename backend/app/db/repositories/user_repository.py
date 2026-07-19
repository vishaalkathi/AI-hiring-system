from psycopg.rows import dict_row

from backend.app.db.connection import get_connection

def create_user(email:str, password_hash: str, name: str, role: str) -> dict:
    """
    Create a new user and return the created row.
    """

    query = """
        INSERT INTO users (
            email,
            password_hash,
            name,
            role
        )
        VALUES (%s, %s, %s,%s)
        RETURNING *;
    """

    with get_connection() as conn:
        with conn.cursor(row_factory = dict_row) as cur:

            cur.execute(
                query,
                (email, password_hash, name, role)
            )

            conn.commit()

            return cur.fetchone()

def get_user_by_id(user_id: str) -> dict | None:

    query = """
        SELECT *
        FROM users
        WHERE user_id = %s;
    """

    with get_connection() as conn:
        with conn.cursor(row_factory = dict_row) as cur:
            cur.execute(query, (user_id,))

            return cur.fetchone()

def get_user_by_email(email: str) ->dict | None:

    query = """
        SELECT *
        FROM users
        WHERE email = %s;
    """

    with get_connection() as conn:
        with conn.cursor(row_factory=dict_row) as cur:

            cur.execute(query, (email,))

            return cur.fetchone()
        

def delete_user(user_id: str) -> None:

    query = """
        DELETE
        FROM users
        WHERE user_id = %s;
    """

    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(query, (user_id,))

            conn.commit()
