EMAIL_DATASET = "Adp_c/data/emails.csv"
SHORT_TERM_DB = "Adp_c/database/short_term.db"
POSTGRES_PARAMS = {
    "dbname": "postgres",
    "user": "postgres",
    "password": "thiru",
    "host": "localhost",
    "port": 5432
}
SHORT_TERM_DIR = "Adp_c/short_term_storage"
LONG_TERM_DIR = "Adp_c/long_term_storage"
ACCURACY_PLOT = "Adp_c/static/plots/accuracy_plot.png"
LONG_TERM_CSV = "Adp_c/database/long_term.csv"

INPUT_SIZE = 4
HIDDEN_SIZES = [64, 32]
OUTPUT_SIZE = 1
DROPOUT_RATE = 0.3
EPOCHS = 10
BATCH_SIZE = 32
LEARNING_RATE = 0.001
