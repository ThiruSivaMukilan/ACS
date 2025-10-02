import sys
import os
import logging
import matplotlib.pyplot as plt

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from Adp_c.scripts.fetch_email1 import extract_email_features
from Adp_c.scripts.preprocess import preprocess_data
from Adp_c.model.train import train_model
from Adp_c.model.evaluate import evaluate_model, calculate_uncertainty
from Adp_c.model.reinforcement import reinforcement_loop
from Adp_c.scripts.migrate import perform_migration
from Adp_c.scripts.load_to_db import load_csv_to_db
from Adp_c.database import (
    insert_into_sqlite, insert_into_postgres,
    init_sqlite, init_postgres
)
from Adp_c.config import SHORT_TERM_DIR, LONG_TERM_DIR

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

UNCERTAINTY_PLOT_PATH = os.path.join("Adp_c", "static", "plots", "uncertainty_accuracy_plot.png")

def visualize_uncertainty(uncertainties, accuracy, save_path=UNCERTAINTY_PLOT_PATH):
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    plt.figure(figsize=(10, 6))
    plt.plot(range(len(uncertainties)), uncertainties, label='Uncertainty', color='red')
    plt.axhline(y=accuracy, color='green', linestyle='--', label=f'Accuracy: {accuracy:.2f}')
    plt.xlabel("Test Sample Index")
    plt.ylabel("Uncertainty / Accuracy")
    plt.title("Uncertainty Estimation and Model Accuracy")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(save_path)
    plt.close()
    logger.info(f"Uncertainty plot saved to {save_path}")

def save_email_text(folder, sender, subject, body, index):
    try:
        os.makedirs(folder, exist_ok=True)
        filename = os.path.join(folder, f"email_{index}.txt")
        with open(filename, "w", encoding="utf-8") as f:
            f.write(f"Sender: {sender}\n")
            f.write(f"Subject: {subject}\n")
            f.write(f"Body: {body}\n")
        logger.info(f"Saved email text to {filename}")
    except Exception as e:
        logger.error(f"Failed to save email {index} text: {e}")

def insert_email_to_db(insert_func, email_data, email_index, db_name="DB"):
    try:
        insert_func(email_data)
        logger.info(f"[{db_name}] Inserted email {email_index}")
    except Exception as e:
        logger.error(f"[{db_name}] Failed to insert email {email_index}: {e}")

def main():
    logger.info("Step 1: Extracting features from email...")
    extract_email_features("your email ", "your api key", num_emails=50)

    logger.info("Step 2: Initializing databases...")
    init_sqlite()
    init_postgres()

    logger.info("Step 3: Loading extracted features into SQLite...")
    load_csv_to_db()

    logger.info("Step 4: Preprocessing data...")
    X_train, X_test, y_train, y_test, email_meta_test = preprocess_data(return_meta=True)

    logger.info("Step 5: Training model...")
    model = train_model(X_train, y_train)

    logger.info("Step 6: Evaluating model...")
    predictions, accuracy = evaluate_model(model, X_test, y_test, return_predictions=True)
    uncertainties = calculate_uncertainty(model, X_test)
    logger.info(f"Accuracy: {accuracy:.2f}")

    visualize_uncertainty(uncertainties, accuracy)

    logger.info("Step 7: Storing results in DBs and saving emails to folders...")

    for i in range(len(predictions)):
    
        logger.info(f"email_meta_test[{i}] = {email_meta_test[i]} (length={len(email_meta_test[i])})")

        try:
            sender, subject_len, attachment_size, priority, subject, body = email_meta_test[i]
        except Exception as e:
            logger.error(f"Error unpacking email_meta_test[{i}]: {e}")
            continue 

        label = int(y_test[i])
        pred = int(predictions[i])
        uncertainty = float(uncertainties[i])
        some_score = round(1 - uncertainty, 3) 

        email_data = (
            sender,
            subject,
            body,
            subject_len,
            some_score,
            attachment_size,
            priority,
            pred,
            uncertainty,
            label
        )

        insert_email_to_db(insert_into_sqlite, email_data, i, "SQLite")

        if uncertainty < 0.2:
            insert_email_to_db(insert_into_postgres, email_data, i, "Postgres")

        if pred == 1 and uncertainty < 0.2:
            save_email_text(LONG_TERM_DIR, sender, subject, body, i)
        else:
            save_email_text(SHORT_TERM_DIR, sender, subject, body, i)

    logger.info("Step 8: Reinforcement learning loop...")
    reinforcement_loop(model, X_train, y_train)

    logger.info("Step 9: Performing migration...")
    perform_migration()

    logger.info("✅ All steps completed successfully.")

if __name__ == "__main__":
    main()
