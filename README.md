## Stage 1

Recreate [this](https://github.com/TeaPearce/Counter-Strike_Behavioural_Cloning) with following changes:

- Additional input for the agent network that indicates the target position to move to.

- During SFT, use the future 30s position as the target position.

## Stage 2

Train the agent to follow text instructions.

- Manually (or via a VLM) label play recordings with text instructions policy.

- Additional layers in the agent network that process the text instructions.

- Train the agent through offline RL.

- Improve the alignment between the text instructions and the agent's actions.
