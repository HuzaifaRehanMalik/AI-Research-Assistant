from database import get_connection


def create_session(title="New Chat"):
    """Create a new chat session."""

    connection = get_connection()

    try:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO sessions (title)
                VALUES (%s)
                RETURNING id;
                """,
                (title,),
            )

            session_id = cursor.fetchone()[0]

        connection.commit()

        return session_id

    finally:
        connection.close()


def get_sessions():
    """Return all chat sessions, newest first."""

    connection = get_connection()

    try:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT
                    id,
                    title,
                    created_at,
                    updated_at
                FROM sessions
                ORDER BY updated_at DESC;
                """
            )

            rows = cursor.fetchall()

            return [
                {
                    "id": row[0],
                    "title": row[1],
                    "created_at": row[2],
                    "updated_at": row[3],
                }
                for row in rows
            ]

    finally:
        connection.close()


def save_message(
    session_id,
    role,
    content,
):
    """Save a message to a chat session."""

    connection = get_connection()

    try:
        with connection.cursor() as cursor:
            cursor.execute(
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

            cursor.execute(
                """
                UPDATE sessions
                SET updated_at = NOW()
                WHERE id = %s;
                """,
                (session_id,),
            )

        connection.commit()

    finally:
        connection.close()


def load_history(session_id):
    """Load all messages for a chat."""

    connection = get_connection()

    try:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT
                    role,
                    content
                FROM messages
                WHERE session_id = %s
                ORDER BY id ASC;
                """,
                (session_id,),
            )

            rows = cursor.fetchall()

            return [
                {
                    "role": row[0],
                    "content": row[1],
                }
                for row in rows
            ]

    finally:
        connection.close()


def update_session_title(
    session_id,
    title,
):
    """Update the title of a chat."""

    connection = get_connection()

    try:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                UPDATE sessions
                SET
                    title = %s,
                    updated_at = NOW()
                WHERE id = %s;
                """,
                (
                    title,
                    session_id,
                ),
            )

        connection.commit()

    finally:
        connection.close()


def delete_session(session_id):
    """Delete a chat and all of its messages."""

    connection = get_connection()

    try:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                DELETE FROM sessions
                WHERE id = %s;
                """,
                (session_id,),
            )

        connection.commit()

    finally:
        connection.close()


def rename_chat(
    session_id,
    title,
):
    """Rename an existing chat."""

    update_session_title(
        session_id,
        title,
    )


def delete_chat(session_id):
    """Delete an existing chat."""

    delete_session(session_id)
