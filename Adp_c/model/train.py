# Adp_c/model/train.py

import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, TensorDataset
from Adp_c.model.neural_net import FeedforwardNN
from Adp_c.config import EPOCHS, BATCH_SIZE, LEARNING_RATE

def train_model(X_train, y_train):
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model = FeedforwardNN().to(device)

    # Convert input and labels to float tensors
    X_train_tensor = torch.FloatTensor(X_train)
    y_train_tensor = torch.FloatTensor(y_train).unsqueeze(1)

    # Ensure target values are 0 or 1 (important for BCELoss)
    y_train_tensor = torch.clamp(y_train_tensor, min=0.0, max=1.0)

    train_dataset = TensorDataset(X_train_tensor, y_train_tensor)
    train_loader = DataLoader(train_dataset, batch_size=BATCH_SIZE, shuffle=True)

    criterion = nn.BCELoss()
    optimizer = optim.Adam(model.parameters(), lr=LEARNING_RATE)

    for epoch in range(EPOCHS):
        model.train()
        epoch_loss = 0.0

        for inputs, labels in train_loader:
            inputs, labels = inputs.to(device), labels.to(device)

            outputs = model(inputs)
            loss = criterion(outputs, labels)

            optimizer.zero_grad()
            loss.backward()
            optimizer.step()

            epoch_loss += loss.item()

        print(f"📊 Epoch {epoch+1}/{EPOCHS} - Loss: {epoch_loss:.4f}")

    return model
