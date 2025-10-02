import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.impute import SimpleImputer
from Adp_c.config import EMAIL_DATASET

def preprocess_data():
    df = pd.read_csv(EMAIL_DATASET)

    imputer = SimpleImputer(strategy='mean')
    df.iloc[:, :-1] = imputer.fit_transform(df.iloc[:, :-1])

    scaler = StandardScaler()
    df.iloc[:, :-1] = scaler.fit_transform(df.iloc[:, :-1])

    X = df.iloc[:, :-1].values
    y = df.iloc[:, -1].values
    return train_test_split(X, y, test_size=0.2, random_state=42)
