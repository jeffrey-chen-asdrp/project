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
        print('avg_actions: ', avg_actions)

        # Fieldnames: 'episode_id', agent IDs...
        fieldnames = sorted(avg_actions.keys())
        filename = "./diners_dilemma/actions_log.csv"
        file_exists = os.path.exists(filename)

        with open(filename, "a", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            if not file_exists:
                writer.writeheader()
            writer.writerow(avg_actions)
        
        
