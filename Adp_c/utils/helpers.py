import sqlite3
from config import SHORT_TERM_DB

def load_data():
    import pandas as pd
    return pd.read_csv('data/emails.csv')

def store_to_db(df, predictions):
    conn = sqlite3.connect(SHORT_TERM_DB)
    df = df.copy()
    df['predicted'] = predictions
    df['access_count'] = 0
    df.to_sql("short_term", conn, if_exists='replace', index=False)
    conn.commit()
    conn.close()

