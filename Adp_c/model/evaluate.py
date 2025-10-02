import torch
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import accuracy_score
from Adp_c.config import ACCURACY_PLOT
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

def evaluate_model(model, X_test, y_test, return_predictions=False):
    model.train()  # Keep dropout active for MC Dropout
    X_test_tensor = torch.FloatTensor(X_test).to(device)
    model.to(device)

    # Collect multiple stochastic forward passes
    outputs_list = []
    for _ in range(10):
        with torch.no_grad():
            output = model(X_test_tensor).cpu().numpy()
            outputs_list.append(output)

    # Average the predictions and apply threshold
    outputs_avg = np.mean(outputs_list, axis=0)
    y_pred = (outputs_avg > 0.5).astype(int).flatten()

    # Ensure y_test is also flattened and converted to numpy
    y_test_np = np.array(y_test).flatten()

    # Debug: log shapes
    logger.info(f"🔍 Predictions shape: {y_pred.shape}, Labels shape: {y_test_np.shape}")

    if len(y_pred) != len(y_test_np):
        raise ValueError(f"❌ Shape mismatch: y_pred ({len(y_pred)}) vs y_test ({len(y_test_np)})")

    # Accuracy score
    acc = accuracy_score(y_test_np, y_pred)
    logger.info(f"✅ Test Accuracy with Uncertainty: {acc:.4f}")

    # Plot histogram of averaged outputs
    plt.figure()
    plt.hist(outputs_avg.flatten(), bins=20, alpha=0.7, color="skyblue", edgecolor="black")
    plt.title("Uncertainty Distribution (Mean Output)")
    plt.xlabel("Predicted Probability")
    plt.ylabel("Frequency")
    plt.tight_layout()
    plt.savefig(ACCURACY_PLOT)
    plt.close()

    if return_predictions:
        return y_pred, acc
    else:
        return acc

def calculate_uncertainty(model, X_test, T=10):
    model.train()  # Enable dropout
    X_test_tensor = torch.FloatTensor(X_test).to(device)
    model.to(device)

    # MC Dropout predictions
    outputs = []
    for _ in range(T):
        with torch.no_grad():
            outputs.append(model(X_test_tensor).cpu().numpy())
    outputs = np.stack(outputs, axis=0)  # Shape: [T, N, 1]


    uncertainty = np.var(outputs, axis=0).flatten()
    return uncertainty
