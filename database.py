import os

import psycopg
from dotenv import load_dotenv

load_dotenv()


# =========================================================
# DATABASE CONFIGURATION
# =========================================================

DATABASE_URL = os.getenv("DATABASE_URL")


if not DATABASE_URL:
    raise ValueError("DATABASE_URL is missing from your .env file.")


# =========================================================
# DATABASE CONNECTION
# =========================================================


def get_connection():
    """
    Create and return a connection to NeonDB.
    """

    return psycopg.connect(
        DATABASE_URL,
        sslmode="require",
    )


# =========================================================
# INITIALIZE DATABASE
# =========================================================


def initialize_database():
    """
    Create the required tables.

    This function is migration safe:
    it will not delete existing NeonDB data.
    """

    connection = get_connection()

    try:
        with connection.cursor() as cursor:
            # =================================================
            # SESSIONS TABLE
            # =================================================

            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS sessions (
                    id SERIAL PRIMARY KEY,
                    title TEXT NOT NULL DEFAULT 'New Chat',
                    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
                );
                """
            )

            # =================================================
            # ADD updated_at TO EXISTING TABLE
            # =================================================

            cursor.execute(
                """
                ALTER TABLE sessions
                ADD COLUMN IF NOT EXISTS
                updated_at TIMESTAMPTZ DEFAULT NOW();
                """
            )

            # =================================================
            # FIX OLD ROWS
            # =================================================

            cursor.execute(
                """
                UPDATE sessions
                SET updated_at = created_at
                WHERE updated_at IS NULL;
                """
            )

            # =================================================
            # MESSAGES TABLE
            # =================================================

            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS messages (
                    id SERIAL PRIMARY KEY,

                    session_id INTEGER NOT NULL,

                    role TEXT NOT NULL,

                    content TEXT NOT NULL,

                    created_at TIMESTAMPTZ NOT NULL
                    DEFAULT NOW(),

                    FOREIGN KEY (session_id)
                    REFERENCES sessions(id)
                    ON DELETE CASCADE
                );
                """
            )

            # =================================================
            # MESSAGE INDEX
            # =================================================

            cursor.execute(
                """
                CREATE INDEX IF NOT EXISTS
                messages_session_id_idx
                ON messages(session_id);
                """
            )

            # =================================================
            # SESSION INDEX
            # =================================================

            cursor.execute(
                """
                CREATE INDEX IF NOT EXISTS
                sessions_updated_at_idx
                ON sessions(updated_at DESC);
                """
            )

        connection.commit()

    except Exception:
        connection.rollback()

        raise

    finally:
        connection.close()
