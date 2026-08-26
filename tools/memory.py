from database import get_connection


def create_session(title: str = "New Chat") -> str:
    """
    Create a new chat session.
    Returns the session ID.
    """

    with get_connection() as conn:
        with conn.cursor() as cur:

            cur.execute(
                """
                INSERT INTO sessions (title)
                VALUES (%s)
                RETURNING id;
                """,
                (title,),
            )

            session_id = cur.fetchone()[0]

        conn.commit()

    return str(session_id)


def save_message(session_id: str, role: str, content: str):
    """
    Save a chat message.
    """

    with get_connection() as conn:
        with conn.cursor() as cur:

            cur.execute(
                """
                INSERT INTO messages (
                    session_id,
                    role,
                    content
                )
                VALUES (%s, %s, %s);
                """,
                (
                    session_id,
                    role,
                    content,
                ),
            )

        conn.commit()


def load_history(session_id: str):
    """
    Load conversation history for an OpenAI Agent.
    """

    with get_connection() as conn:
        with conn.cursor() as cur:

            cur.execute(
                """
                SELECT role, content
                FROM messages
                WHERE session_id = %s
                ORDER BY created_at ASC;
                """,
                (session_id,),
            )

            rows = cur.fetchall()

    history = []

    for role, content in rows:

        history.append(
            {
                "role": role,
                "content": content,
            }
        )

    return history


def list_sessions():
    """
    List all chat sessions.
    """

    with get_connection() as conn:
        with conn.cursor() as cur:

            cur.execute(
                """
                SELECT
                    id,
                    title,
                    created_at
                FROM sessions
                ORDER BY created_at DESC;
                """
            )

            return cur.fetchall()


def delete_session(session_id: str):
    """
    Delete a chat session.
    """

    with get_connection() as conn:
        with conn.cursor() as cur:

            cur.execute(
                """
                DELETE FROM sessions
                WHERE id = %s;
                """,
                (session_id,),
            )

        conn.commit()


def rename_session(session_id: str, new_title: str):
    """
    Rename a chat session.
    """

    with get_connection() as conn:
        with conn.cursor() as cur:

            cur.execute(
                """
                UPDATE sessions
                SET title = %s
                WHERE id = %s;
                """,
                (
                    new_title,
                    session_id,
                ),
            )

        conn.commit()