

import torch
import torch.nn as nn
import torch.nn.functional as F
from Adp_c.config import INPUT_SIZE, HIDDEN_SIZES, OUTPUT_SIZE, DROPOUT_RATE

class FeedforwardNN(nn.Module):
    def __init__(self):
        super(FeedforwardNN, self).__init__()
        self.fc1 = nn.Linear(INPUT_SIZE, HIDDEN_SIZES[0])
        self.fc2 = nn.Linear(HIDDEN_SIZES[0], HIDDEN_SIZES[1])
        self.dropout = nn.Dropout(DROPOUT_RATE)
        self.output = nn.Linear(HIDDEN_SIZES[1], OUTPUT_SIZE)

    def forward(self, x):
        x = F.relu(self.fc1(x))
        x = self.dropout(x)
        x = F.relu(self.fc2(x))
        x = self.dropout(x)
        return torch.sigmoid(self.output(x))  