import os
from config import SHORT_TERM_DIR, LONG_TERM_DIR

def save_email_text(folder, email_data, index):
    os.makedirs(folder, exist_ok=True)
    filename = os.path.join(folder, f"email_{index}.txt")
    with open(filename, "w", encoding="utf-8") as f:
        f.write(f"Sender: {email_data['sender']}\n")
        f.write(f"Subject: {email_data['subject']}\n")
        f.write(f"Body: {email_data['body']}\n")

def save_emails_to_folder(emails, predictions, uncertainties):
    for idx, email in enumerate(emails):
        folder = LONG_TERM_DIR if predictions[idx] == 1 else SHORT_TERM_DIR
        save_email_text(folder, email, idx)
