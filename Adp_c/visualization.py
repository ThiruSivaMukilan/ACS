import matplotlib.pyplot as plt
from config import ACCURACY_PLOT, UNCERTAINTY_PLOT

def plot_accuracy(accuracy_list):
    plt.figure()
    plt.plot(accuracy_list, marker='o')
    plt.title("Model Training Accuracy")
    plt.xlabel("Epoch")
    plt.ylabel("Accuracy")
    plt.grid(True)
    plt.savefig(ACCURACY_PLOT)
    plt.close()

def plot_uncertainties(uncertainties):
    plt.figure(figsize=(12, 5))
    plt.bar(range(len(uncertainties)), uncertainties)
    plt.title("Per-email Uncertainty Estimation")
    plt.xlabel("Email Index")
    plt.ylabel("Uncertainty")
    plt.savefig(UNCERTAINTY_PLOT)
    plt.close()
