import torch
import matplotlib.pyplot as plt
from sklearn.metrics import accuracy_score
from Adp_c.config import ACCURACY_PLOT

def evaluate_model(model, X_test, y_test):
    model.eval()
    X_test_tensor = torch.FloatTensor(X_test)
    outputs_list = [model(X_test_tensor).detach().numpy() for _ in range(10)]
    outputs_avg = sum(outputs_list) / len(outputs_list)
    y_pred = (outputs_avg > 0.5).astype(int)

    acc = accuracy_score(y_test, y_pred)
    print(f"Test Accuracy with Uncertainty: {acc:.4f}")

    plt.figure()
    plt.hist(outputs_avg, bins=20, alpha=0.7)
    plt.title("Uncertainty Distribution (Mean Output)")
    plt.xlabel("Predicted Probability")
    plt.ylabel("Frequency")
    plt.savefig(ACCURACY_PLOT)
    plt.close()
