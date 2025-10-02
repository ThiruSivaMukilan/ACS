import sqlite3
import pandas as pd
from Adp_c.config import SHORT_TERM_DB

def load_data():
    return pd.read_csv('Adp_c/data/emails.csv')

def store_to_db(df, predictions):
    conn = sqlite3.connect(SHORT_TERM_DB)
    df['predicted'] = predictions
    df['access_count'] = 0
    df.to_sql("short_term", conn, if_exists='replace', index=False)
    conn.close()
