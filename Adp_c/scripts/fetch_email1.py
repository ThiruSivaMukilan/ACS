import imaplib
import email
import pandas as pd
import os
import ssl
from email.header import decode_header
from Adp_c.config import EMAIL_DATASET

def extract_email_features(username, password, num_emails=50, output_path=EMAIL_DATASET):
    rows = []
    try:
        print("🔐 Logging into email server...")
        mail = imaplib.IMAP4_SSL("imap.gmail.com")
        mail.login(username, password)
        mail.select("inbox")

        result, data = mail.search(None, "ALL")
        if result != "OK" or not data or not data[0]:
            print("❌ No emails found.")
            return

        email_ids = data[0].split()[-num_emails:]
        print(f"📥 Found {len(email_ids)} recent emails.")

        for eid in email_ids:
            result, msg_data = mail.fetch(eid, "(RFC822)")
            if result != "OK":
                print(f"⚠️ Failed to fetch email with ID {eid.decode()}")
                continue

            raw_email = msg_data[0][1]
            msg = email.message_from_bytes(raw_email)

            message_id = msg.get("Message-ID", f"<{eid.decode()}@imap.gmail.com>")

            subject = msg.get("subject", "")
            if subject:
                try:
                    decoded_subject, encoding = decode_header(subject)[0]
                    subject = decoded_subject.decode(encoding) if isinstance(decoded_subject, bytes) else decoded_subject
                except Exception:
                    pass
            subject_len = len(subject)

            priority = 1 if "important" in subject.lower() or "urgent" in subject.lower() else 0

            attachment_size = 0
            if msg.is_multipart():
                for part in msg.walk():
                    if part.get_content_maintype() == "multipart" or part.get("Content-Disposition") is None:
                        continue
                    payload = part.get_payload(decode=True)
                    if payload:
                        attachment_size += len(payload)

            time_since_access = 1  

            sender = msg.get("From", "unknown")

            rows.append([message_id, subject_len, attachment_size, time_since_access, priority, sender])

        df = pd.DataFrame(rows, columns=["message_id", "subject_length", "attachment_size", "time_since_access", "priority", "sender"])
        df.to_csv(output_path, index=False)
        print(f"✅ Email features saved to {output_path}")

    except ssl.SSLError as e:
        print(f"SSL error: {e}")
    except Exception as e:
        print(f"Error fetching emails: {e}")
