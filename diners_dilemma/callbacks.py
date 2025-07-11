import csv
import os
from ray.rllib.callbacks.callbacks import RLlibCallback
import numpy as np

class ActionLoggingCallbacks(RLlibCallback):
    def on_episode_end(self, *, episode, **kwargs):
        actions = episode.get_actions()

         # Compute average (fraction of 1's) for each agent
        avg_actions = {
            agent: float(np.mean(agent_actions))
            for agent, agent_actions in actions.items()
        }
        
        total_return = float(episode.get_return())

        row = {
            **avg_actions,
            "return": total_return
        }

        print('row: ', row)

        agent_cols = sorted(k for k in row.keys() if k.startswith("agent_"))
        fieldnames = agent_cols + ["return"]
        filename = "./diners_dilemma//data/25_iter_20_agents_[8,8][2,6].csv"
        file_exists = os.path.exists(filename)

        with open(filename, "a", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            if not file_exists:
                writer.writeheader()
            writer.writerow(row)
        
        
