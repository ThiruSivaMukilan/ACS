from Adp_c.scripts.fetch_emails import extract_email_features
from Adp_c.scripts.preprocess import preprocess_data
from Adp_c.model.train import train_model
from Adp_c.model.evaluate import evaluate_model
from Adp_c.model.reinforcement import reinforcement_loop
from Adp_c.scripts.migrate import perform_migration

def main():
    print("Step 1: Extracting features from email...")
    extract_email_features("sivamukilanthiru07@gmail.com","rvqz ugux aegl emgo")

    print("Step 2: Preprocessing data...")
    X_train, X_test, y_train, y_test = preprocess_data()

    print("Step 3: Training model...")
    model = train_model(X_train, y_train)

    print("Step 4: Evaluating model...")
    evaluate_model(model, X_test, y_test)

    print("Step 5: Reinforcement loop (optional feedback)...")
    reinforcement_loop(model, X_train, y_train)

    print("Step 6: Performing storage migration based on policy...")
    perform_migration()

    print("Process completed.")

if __name__ == "__main__":
    main()
