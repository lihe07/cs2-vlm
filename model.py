# Agent model arch
import torch
from torch import nn


class Agent(nn.Module):
    """
    CNN (CBAM) + LSTM (xLSTM)

    Inputs:
    - Image: (B, 3, 150, 280) B x C x H x W

    Metadata:
    - Ammo num: (B, n) - Ammo count
    - Health: (B, n) - Health

    - Granades: (B, n) - Granades count
    - Incendiary: (B, n) - Incendiary count
    - Smoke: (B, n) - Smoke count
    - Flash: (B, n) - Flash count

    - Policy x: (B, 19) - Classifications
    - Policy y: (B, 13) - Classifications

    Outputs:
    - Keys: (B, 4) - W, A, S, D
    - Mouse movement x: (B, 19) - Classifications
    - Mouse movement y: (B, 13) - Classifications
    - Weapon switch: (B, 7) - Classification
    - Fire probability: (B, 1) - Probability
    - Reload probability: (B, 1) - Probability
    - Jump probability: (B, 1) - Probability
    - Plant bomb probability: (B, 1) - Probability


    - Crouch probability: (B, 1) - Probability
    - Walk probability: (B, 1) - Probability
    """

    def __init__(self):
        pass

    def forward(self, x):
        pass
