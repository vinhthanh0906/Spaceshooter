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
        self.fc1 = nn.Linear(4, 16)
        self.relu = nn.ReLU()
        self.fc2 = nn.Linear(16, 1)  # Output: angle in degrees

    def forward(self, x):
        x = self.fc1(x)
        x = self.relu(x)
        return self.fc2(x)

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


class SafeFireNN(nn.Module):
    def __init__(self):
        super().__init__()
        self.fc1 = nn.Linear(6, 16)
        self.relu = nn.ReLU()
        self.fc2 = nn.Linear(16, 1)
        self.sigmoid = nn.Sigmoid()  # output in range 0–1

    def forward(self, x):
        x = self.fc1(x)
        x = self.relu(x)
        x = self.fc2(x)
        return self.sigmoid(x)







#Reinforcement Prevent ally shooting (Coming soon...)
# DQN model
# class DQN(nn.Module):
#     def __init__(self, input_dim, output_dim):
#         super(DQN, self).__init__()
#         self.fc1 = nn.Linear(input_dim, 64)
#         self.relu = nn.ReLU()
#         self.fc2 = nn.Linear(64, output_dim)

#     def forward(self, x):
#         x = self.fc1(x)
#         x = self.relu(x)
#         return self.fc2(x)

# # Replay Buffer
# class ReplayBuffer:
#     def __init__(self, capacity):
#         self.capacity = capacity
#         self.buffer = []

#     def push(self, transition):
#         if len(self.buffer) >= self.capacity:
#             self.buffer.pop(0)
#         self.buffer.append(transition)

#     def sample(self, batch_size):
#         return random.sample(self.buffer, batch_size)

#     def __len__(self):
#         return len(self.buffer)

# # Epsilon-greedy action selection
# def select_action(state, policy_net, epsilon, num_actions):
#     if random.random() < epsilon:
#         return random.randint(0, num_actions - 1)
#     else:
#         with torch.no_grad():
#             q_values = policy_net(torch.FloatTensor(state).unsqueeze(0))
#             return q_values.argmax().item()