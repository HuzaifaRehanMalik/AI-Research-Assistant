import os
import psycopg
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError(
        "DATABASE_URL not found in .env"
    )


def get_connection():
    """
    Create a new PostgreSQL connection.
    """
    return psycopg.connect(
        DATABASE_URL,
        autocommit=False,
    )


def initialize_database():
    """
    Create all required tables.
    """

    with get_connection() as conn:

        with conn.cursor() as cur:

            cur.execute("""
                CREATE EXTENSION IF NOT EXISTS "pgcrypto";
            """)

            cur.execute("""
                CREATE TABLE IF NOT EXISTS sessions (

                    id UUID PRIMARY KEY
                        DEFAULT gen_random_uuid(),

                    title TEXT NOT NULL,

                    created_at TIMESTAMP
                        DEFAULT CURRENT_TIMESTAMP

                );
            """)

            cur.execute("""
                CREATE TABLE IF NOT EXISTS messages (

                    id UUID PRIMARY KEY
                        DEFAULT gen_random_uuid(),

                    session_id UUID
                        REFERENCES sessions(id)
                        ON DELETE CASCADE,

                    role TEXT NOT NULL,

                    content TEXT NOT NULL,

                    created_at TIMESTAMP
                        DEFAULT CURRENT_TIMESTAMP

                );
            """)

        conn.commit()

    print("✓ Database initialized.")