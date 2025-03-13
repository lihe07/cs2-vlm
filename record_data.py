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
    "is_scoped",
    "X",
    "Y",
    "Z",
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
    "total_rounds_played",
    "inventory"
])

ticks_df.to_csv("g2-vs-spirit-m3-dust2.csv", index=False)

data = pd.read_csv("g2-vs-spirit-m3-dust2.csv")

data = data[data["name"] == "NiKo"]


# Add columns for weapon change
data["Button 1"] = "FALSE"
data["Button 2"] = "FALSE"
data["Button 3"] = "FALSE"
data["Button 4"] = "FALSE"
data["Button 5"] = "FALSE"

# Iterate through each row and check for weapon change
previous_weapon = None
previous_previous_weapon = None
for index, row in data.iterrows():
    current_weapon = row["active_weapon_name"]
    if previous_previous_weapon != previous_weapon:
        if previous_weapon in ["Glock-18", "P250", "USP-S", "Desert Eagle"]:
            data.at[index, "Button 1"] = "TRUE"
        elif previous_weapon in ["AK-47", "M4A4", "M4A1-S", "Galil AR", "MP9", "MAC-10"]:
            data.at[index, "Button 2"] = "TRUE"
        elif previous_weapon in ["Butterfly Knife"]:
            data.at[index, "Button 3"] = "TRUE"
        elif previous_weapon in ["Smoke Grenade", "High Explosive Grenade", "Flashbang", "Molotov", "Incendiary Grenade"]:
            data.at[index, "Button 4"] = "TRUE"
        elif previous_weapon in ["C4 Explosive"]:
            data.at[index, "Button 5"] = "TRUE"
    previous_previous_weapon = previous_weapon
    previous_weapon = current_weapon
    # If button  "IN_WALK": 1 << 17, is pressed, then the player is walking, if button "IN_DUCK": 1 << 2, is pressed, then the player is crouching
    if row["buttons"] & (1 << 2):
        data.at[index, "DUCK"] = "TRUE"
    else:
        data.at[index, "DUCK"] = "FALSE"
    if row["buttons"] & (1 << 16):
        data.at[index, "WALK"] = "TRUE"
    else:
        data.at[index, "WALK"] = "FALSE"


# From the inventory column, extract the number of grenades, incendiary, smoke, and flash ['Butterfly Knife', 'Glock-18', 'Smoke Grenade', 'Flashbang', 'AK-47', 'High Explosive Grenade']
data["Granades"] = data["inventory"].apply(lambda x: x.count("High Explosive Grenade"))
data["Incendiary"] = data["inventory"].apply(lambda x: x.count("Incendiary Grenade"))
data["Incendiary"] = data["inventory"].apply(lambda x: x.count("Molotov"))
data["Smoke"] = data["inventory"].apply(lambda x: x.count("Smoke Grenade"))
data["Flash"] = data["inventory"].apply(lambda x: x.count("Flashbang"))

#


# Delete the inventory column
data = data.drop(columns=["inventory"])
data = data.drop(columns=["steamid"])
data = data.drop(columns=["name"])
data = data.drop(columns=["active_weapon_name"])
data = data.drop(columns=["buttons"])




# Save the data
data.to_csv("g2-vs-spirit-m3-dust2-niko.csv", index=False)
