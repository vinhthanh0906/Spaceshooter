import torch 
import torch.nn as nn
import torch.optim as optim
import random
import numpy as np
from collections import deque


# Simple NN to learn angle to closest enemy

class AimingNN(nn.Module):
    def __init__(self):
        super().__init__()
        self.fc1 = nn.Linear(4, 64)
        self.fc2 = nn.Linear(64, 32)
        self.fc3 = nn.Linear(32, 1)
        self.relu = nn.ReLU()

    def forward(self, x):
        x = self.relu(self.fc1(x))
        x = self.relu(self.fc2(x))
        return self.fc3(x)



class BoundaryAvoidanceNN(nn.Module):
    def __init__(self):
        super().__init__()
        self.fc1 = nn.Linear(2, 16)
        self.relu = nn.ReLU()
        self.fc2 = nn.Linear(16, 1)  # Output: heading angle

    def forward(self, x):
        x = self.fc1(x)
        x = self.relu(x)
        return self.fc2(x)

model = AimingNN()
criterion = nn.MSELoss()
optimizer = optim.Adam(model.parameters(), lr=0.01)

boundary_model = BoundaryAvoidanceNN()
optimizer_boundary = torch.optim.Adam(boundary_model.parameters(), lr=0.01)


