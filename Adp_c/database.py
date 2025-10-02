import sqlite3
import psycopg2
from config import SHORT_TERM_DB, POSTGRES_PARAMS

EXPECTED_COLUMNS = [
    "sender", "subject", "body", "subject_length", "some_score",
    "attachment_size", "priority", "prediction", "uncertainty", "label"
]

def init_sqlite():
    create_sqlite_tables()

def create_sqlite_tables():
    conn = sqlite3.connect(SHORT_TERM_DB)
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS short_term_emails (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        sender TEXT,
        subject TEXT,
        body TEXT,
        subject_length INTEGER,
        some_score REAL,
        attachment_size INTEGER,
        priority INTEGER,
        prediction INTEGER,
        uncertainty REAL,
        label INTEGER
    )
    ''')
    conn.commit()
    conn.close()

def insert_into_sqlite(email_data):
    if len(email_data) != len(EXPECTED_COLUMNS):
        print(f"[SQLite] ❌ Invalid data length: expected {len(EXPECTED_COLUMNS)}, got {len(email_data)}")
        return

    try:
        conn = sqlite3.connect(SHORT_TERM_DB)
        cursor = conn.cursor()
        cursor.execute(f'''
            INSERT INTO short_term_emails (
                {", ".join(EXPECTED_COLUMNS)}
            ) VALUES ({", ".join(["?"] * len(EXPECTED_COLUMNS))})
        ''', email_data)
        conn.commit()
        print("[SQLite]  Inserted email successfully")
    except Exception as e:
        print(f"[SQLite]  Failed to insert email: {e}")
    finally:
        conn.close()

def init_postgres():
    create_postgres_tables()

def create_postgres_tables():
    conn = psycopg2.connect(**POSTGRES_PARAMS)
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS long_term_emails (
        id SERIAL PRIMARY KEY,
        sender TEXT,
        subject TEXT,
        body TEXT,
        subject_length INTEGER,
        some_score REAL,
        attachment_size INTEGER,
        priority INTEGER,
        prediction INTEGER,
        uncertainty REAL,
        label INTEGER
    )
    ''')
    conn.commit()
    cursor.close()
    conn.close()

def insert_into_postgres(email_data):
    if len(email_data) != len(EXPECTED_COLUMNS):
        print(f"[Postgres]  Invalid data length: expected {len(EXPECTED_COLUMNS)}, got {len(email_data)}")
        return

    try:
        conn = psycopg2.connect(**POSTGRES_PARAMS)
        cursor = conn.cursor()
        cursor.execute(f'''
            INSERT INTO long_term_emails (
                {", ".join(EXPECTED_COLUMNS)}
            ) VALUES ({", ".join(["%s"] * len(EXPECTED_COLUMNS))})
        ''', email_data)
        conn.commit()
        print("[Postgres]  Inserted email successfully")
    except Exception as e:
        print(f"[Postgres]  Failed to insert email: {e}")
    finally:
        cursor.close()
        conn.close()
