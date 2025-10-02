import sqlite3
import pandas as pd
from Adp_c.config import SHORT_TERM_DB, LONG_TERM_CSV

def perform_migration():
    conn = sqlite3.connect(SHORT_TERM_DB)
    cursor = conn.cursor()

    try:
        df = pd.read_sql_query("SELECT * FROM short_term", conn)
    except:
        print("No data to migrate.")
        return

    df["access_count"] = df.get("access_count", 0)
    to_migrate = df[df['access_count'] < 2]
    remain = df[df['access_count'] >= 2]

    if not to_migrate.empty:
        to_migrate.to_csv(LONG_TERM_CSV, mode='a', index=False, header=False)

    remain.to_sql("short_term", conn, if_exists="replace", index=False)
    conn.close()
    print(f"Migrated {len(to_migrate)} items to long-term storage.")
