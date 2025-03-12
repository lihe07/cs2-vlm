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
    
from demoparser2 import DemoParser
import pandas as pd
import numpy as np

parser = DemoParser("g2-vs-spirit-m3-dust2.dem")

ticks_df = parser.parse_ticks([
    "name",
    "X",
    "Y",
    "Z",
    "health",
    "fov",
    "is_scoped",
    "X",
    "Y",
    "Z",
    "ducked",
    "velocity_X",
    "velocity_Y",
    "velocity_Z",
    "pitch",
    "yaw",
    "FORWARD",
    "LEFT",
    "RIGHT",
    "BACK",
    "FIRE",
    "RIGHTCLICK",
    "RELOAD",
    "INSPECT",
    "USE",
    "ZOOM",
    "WALK",
    "JUMP",
    "DUCK",
    "buttons",
    "active_weapon_name",
    "total_rounds_played"
])

ticks_df.to_csv("g2-vs-spirit-m3-dust2.csv", index=False)

# Read the data



data = pd.read_csv("g2-vs-spirit-m3-dust2.csv")

# leave only data of player name NiKo
data = data[data["name"] == "NiKo"]

# Save the data

data.to_csv("g2-vs-spirit-m3-dust2-niko.csv", index=False)