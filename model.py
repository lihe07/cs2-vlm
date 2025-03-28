# Agent model arch
import torch
from torch import nn
from icecream import ic

from models.lstm import sLSTM
from models.resnet_cbam import resnet101_cbam


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

    - Scope probability: (B, 1) - Probability
    - Crouch probability: (B, 1) - Probability
    - Walk probability: (B, 1) - Probability
    """

    def __init__(self):
        super(Agent, self).__init__()

        self.cnn_backbone = resnet101_cbam(num_classes=1000)
        self.lstm_backbone = sLSTM(inp_dim=500, head_dim=100, head_num=5)

    @staticmethod
    def to_bucket(x: float, min: float, max: float, n: int) -> torch.Tensor:
        """
        Convert X to One-Hot bucket classification
        """
        y = torch.zeros(n)
        idx = int((x - min) / (max - min) * n)
        y[idx] = 1
        return y

    @staticmethod
    def from_bucket(
        x: torch.Tensor, min: float, max: float, temperature: float = 0.0
    ) -> torch.Tensor:
        """
        Convert bucket to X. Temperature is used to control the probability.
        Temperature = 0 -> Argmax
        Temperature = 1 -> Full random
        """
        if temperature == 0:
            return torch.argmax(x) / len(x) * (max - min) + min
        else:
            x = torch.softmax(x / temperature, dim=0)
            return torch.sum(x * torch.arange(len(x)) / len(x) * (max - min) + min)

    def forward(self, x):
        image = x["image"]
        image = self.cnn_backbone(image)
        latent = torch.cat(
            (
                image,
                x["ammo"],
                x["health"],
                x["granades"],
                x["incendiary"],
                x["smoke"],
                x["flash"],
            )
        )
        print(latent)

        return image


a = Agent()
BATCH = 1
a(
    {
        "image": torch.rand((BATCH, 3, 150, 280)),
        "ammo": torch.stack([Agent.to_bucket(114, 0, 500, 10) for _ in range(BATCH)]),
        "health": torch.stack([Agent.to_bucket(114, 0, 500, 10) for _ in range(BATCH)]),
        "granades": torch.stack([Agent.to_bucket(5, 0, 10, 10) for _ in range(BATCH)]),
        "incendiary": torch.stack(
            [Agent.to_bucket(5, 0, 10, 10) for _ in range(BATCH)]
        ),
        "smoke": torch.stack([Agent.to_bucket(5, 0, 10, 10) for _ in range(BATCH)]),
        "flash": torch.stack([Agent.to_bucket(5, 0, 10, 10) for _ in range(BATCH)]),
        #
        "policy_x": torch.stack(
            [Agent.to_bucket(123, 0, 200, 19) for _ in range(BATCH)]
        ),
        "policy_y": torch.stack(
            [Agent.to_bucket(123, 0, 200, 13) for _ in range(BATCH)]
        ),
    }
)
