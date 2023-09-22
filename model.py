import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F 
import os

class Qnet(nn.Module):
    def __init__(self, input_size, hidden_size, output_size):
        super().__init__()
        self.linear1 = nn.Linear(input_size, hidden_size)
        self.linear2 = nn.Linear(hidden_size, output_size)
    
    def forward(self, x):
        x = self.linear1(x)
        x = F.relu(x)
        x = self.linear2(x)
        return x
    
    def save(self, file_name='model.pth'):
        model_folder = './model'
        if not os.path.exists(model_folder):
            os.mkdir(model_folder)

        torch.save(self.state_dict(), os.path.join(model_folder, file_name))

class Qtrainer():
    def __init__(self, model, lr, gamma):
        self.lr = lr
        self.gamma = gamma
        self.model = model
        self.optimizer = optim.Adam(model.parameters(), lr = lr)
        self.loss = nn.MSELoss()

    def train_step(self, state, action, reward, next, game_over):
        state = torch.tensor(state, dtype=torch.float)
        action = torch.tensor(action, dtype=torch.float)
        reward = torch.tensor(reward, dtype=torch.float)
        next = torch.tensor(next, dtype=torch.float)

        # add a dimension if we have a single entity
        if len(state.shape) ==  1:
            state = torch.unsqueeze(state, dim=0)
            action = torch.unsqueeze(action, dim=0)
            reward = torch.unsqueeze(reward, dim=0)
            next = torch.unsqueeze(next, dim=0)
            game_over = (game_over, )

        # Bellman equation

        prediction = self.model(state)

        target = prediction.clone()

        # ciclo per calcolare valore su tutta la batch
        for idx in range(len(game_over)):
            Q_new = reward[idx]
            if not game_over[idx]:
                Q_new = reward[idx] + self.gamma * torch.max(self.model(next[idx]))

            target[idx][torch.argmax(action).item()] = Q_new

        self.optimizer.zero_grad()
        loss = self.loss(target, prediction)
        loss.backward()

        self.optimizer.step()