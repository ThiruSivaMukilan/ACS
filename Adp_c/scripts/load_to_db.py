import sqlite3
import pandas as pd
from Adp_c.config import SHORT_TERM_DB

def load_csv_to_db():
    # Load the CSV file containing email features
    df = pd.read_csv('Adp_c/data/emails.csv')

    # Rename columns to match DB schema
    if 'subject_length' in df.columns:
        df.rename(columns={'subject_length': 'subject_len'}, inplace=True)
    if 'access count' in df.columns:
        df.rename(columns={'access count': 'access_count'}, inplace=True)
    if 'access_count' not in df.columns:
        df['access_count'] = 1
    if 'id' in df.columns:
        df.drop(columns=['id'], inplace=True)
    if 'message_id' not in df.columns:
        print("⚠️ Warning: 'message_id' column not found in CSV. Adding dummy IDs.")
        df['message_id'] = "<unknown>"
    if 'sender' not in df.columns:
        print("⚠️ Warning: 'sender' column not found in CSV. Adding dummy sender.")
        df['sender'] = "<unknown>"

    conn = sqlite3.connect(SHORT_TERM_DB)

    # Drop and recreate short_term_emails table
    conn.execute('DROP TABLE IF EXISTS short_term_emails')

    conn.execute('''
        CREATE TABLE IF NOT EXISTS short_term_emails (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sender TEXT,
            subject_len INTEGER,
            attachment_size REAL,
            time_since_access INTEGER,
            priority INTEGER,
            label INTEGER,
            access_count INTEGER,
            message_id TEXT
        )
    ''')

    required_columns = ['sender', 'subject_len', 'attachment_size', 'time_since_access',
                        'priority', 'label', 'access_count', 'message_id']

    df = df.reindex(columns=required_columns, fill_value=None)

    df.to_sql('short_term_emails', conn, if_exists='append', index=False)

    conn.commit()
    conn.close()

    print("✅ Loaded email features from CSV into SQLite DB.")
