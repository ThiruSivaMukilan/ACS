import sqlite3
import pandas as pd
from Adp_c.config import SHORT_TERM_DB, LONG_TERM_CSV
from Adp_c.gmail_api import gmail_authenticate, create_label, move_email_to_label

TIME_THRESHOLD = 1           
TEST_MIGRATION = True       

def perform_migration():
    conn = sqlite3.connect(SHORT_TERM_DB)
    cursor = conn.cursor()

    
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='items';")
    if not cursor.fetchone():
        print("⚠️ No 'items' table found in the short-term database.")
        conn.close()
        return


    df = pd.read_sql_query("SELECT * FROM items", conn)

    if df.empty:
        print("⚠️ The 'items' table is empty. Nothing to migrate.")
        conn.close()
        return

    if 'time_since_access' not in df.columns:
        print("❌ Error: 'time_since_access' column missing.")
        conn.close()
        return

    if 'message_id' not in df.columns:
        print("❌ Error: 'message_id' column missing.")
        conn.close()
        return

    print("📊 Current short-term items:")
    print(df[['subject_len', 'time_since_access']].to_string(index=False))

    if TEST_MIGRATION:
        print("🧪 TEST MODE: Migrating all items for Gmail label testing...")
        to_migrate = df.copy()
        remain = df.iloc[0:0] 
    else:
        to_migrate = df[df['time_since_access'] > TIME_THRESHOLD]
        remain = df[df['time_since_access'] <= TIME_THRESHOLD]

    if not to_migrate.empty:
        to_migrate.to_csv(LONG_TERM_CSV, mode='a', index=False, header=False)
        print(f"✅ Saved {len(to_migrate)} migrated item(s) to long-term storage CSV.")

        try:
            print("🔐 Authenticating with Gmail API...")
            service = gmail_authenticate()

            print("📂 Creating/fetching 'LongTerm' label...")
            label_id = create_label(service, "LongTerm")
            print(f"✅ Gmail Label ID: {label_id}")

            print("📩 Moving emails to Gmail label...")
            for msg_id in to_migrate['message_id']:
                try:
                    move_email_to_label(service, msg_id, label_id)
                    print(f"✅ Moved email {msg_id} to 'LongTerm' label.")
                except Exception as e:
                    print(f"❌ Could not move email {msg_id}: {e}")

            print(f"✅ Migration completed for {len(to_migrate)} item(s).")

        except Exception as gmail_error:
            print(f"❌ Gmail API failed: {gmail_error}")

    else:
        print("ℹ️ No items qualified for migration.")
    remain.to_sql("items", conn, if_exists="replace", index=False)
    print(f"📁 {len(remain)} item(s) remain in short-term storage.")

    conn.close()
