import sqlite3

def create_sample_db(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

   
    cursor.execute("DROP TABLE IF EXISTS short_term_emails")

  
    cursor.execute("""
        CREATE TABLE short_term_emails (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sender TEXT,
            subject_length INTEGER,
            attachment_size INTEGER,
            time_since_access INTEGER,
            priority INTEGER,
            label INTEGER
        )
    """)

    # Insert sample rows
    sample_data = [
        ('alice@example.com', 45, 1024, 12, 3, 1),
        ('bob@example.com', 30, 0, 7, 1, 0),
        ('carol@example.com', 75, 2048, 20, 2, 1),
        ('dan@example.com', 60, 512, 5, 3, 0),
        ('eve@example.com', 50, 0, 15, 2, 1)
    ]

    cursor.executemany("""
        INSERT INTO short_term_emails (sender, subject_length, attachment_size, time_since_access, priority, label)
        VALUES (?, ?, ?, ?, ?, ?)
    """, sample_data)

    conn.commit()
    conn.close()
    print("Sample database created with sample data.")

