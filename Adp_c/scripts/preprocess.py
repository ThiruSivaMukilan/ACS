import pandas as pd
import numpy as np
import sqlite3
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.impute import SimpleImputer
from Adp_c.config import SHORT_TERM_DB

def preprocess_data(return_meta=False):

    conn = sqlite3.connect(SHORT_TERM_DB)
    df = pd.read_sql_query("SELECT * FROM short_term_emails", conn)
    conn.close()

    if df.empty:
        raise ValueError("Database table 'short_term_emails' is empty! Add some data before running.")

    feature_cols = ['subject_length', 'attachment_size', 'time_since_access', 'priority']
    label_col = 'label'

    for col in feature_cols:
        if col not in df.columns:
            print(f"⚠️ Column '{col}' missing in DB. Adding default 0s.")
            df[col] = 0

    if label_col not in df.columns:
        print(f"⚠️ Label column '{label_col}' missing in DB. Adding default 0s.")
        df[label_col] = 0

    df[label_col] = pd.to_numeric(df[label_col], errors='coerce').fillna(0).astype(int)
    df[label_col] = df[label_col].clip(lower=0, upper=1)

    for col in ['sender', 'subject', 'body']:
        if col not in df.columns:
            print(f"⚠️ '{col}' column missing in DB. Adding default placeholders.")
            df[col] = 'unknown' if col != 'body' else 'no content'
    features = df[feature_cols].copy()
    labels = df[label_col].copy()

    imputer = SimpleImputer(strategy='mean')
    features_imputed = pd.DataFrame(imputer.fit_transform(features), columns=feature_cols)
    scaler = StandardScaler()
    features_scaled = pd.DataFrame(scaler.fit_transform(features_imputed), columns=feature_cols)

    X = features_scaled.astype(np.float32).values
    y = labels.astype(np.float32).values

 
    X_train, X_test, y_train, y_test, df_train, df_test = train_test_split(
        X, y, df, test_size=0.2, random_state=42
    )

    if return_meta:
        
        email_meta_test = list(zip(
            df_test['sender'],
            df_test['subject_length'],
            df_test['attachment_size'],
            df_test['priority'],
            df_test['subject'],
            df_test['body']
        ))
        return X_train, X_test, y_train, y_test, email_meta_test

    return X_train, X_test, y_train, y_test
