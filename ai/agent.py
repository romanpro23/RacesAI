import numpy as np

from ai.brain import *
from ai.model import *
import torch


class Agent:

    state: list

    def __init__(self,
                 memory_size=10000,
                 action_size=4,
                 gamma=0.9,
                 learning_rate=0.001,
                 epsilon_min=0.01,
                 epsilon_decay=0.99
                 ):
        self.brain = Brain(model=LinearModel(9, [128, 64], action_size),
                           memory_size=memory_size,
                           action_size=action_size,
                           gamma=gamma,
                           learning_rate=learning_rate,
                           epsilon_min=epsilon_min,
                           epsilon_decay=epsilon_decay
                           )

    def action(self, inputs):
        return self.brain.action(torch.unsqueeze(torch.tensor(inputs), 0))

    def update(self, state, action, reward, next_state, done):
        self.brain.remember(state, action, reward, next_state, done)

    def train(self, batch_size=64, update_epsilon=False):
        self.brain.train(batch_size, update_epsilon)

    def save(self, path):
        self.brain.save(path)

    def load(self, path):
        self.brain.load(path)
