import csv
import os
from datetime import datetime
from ray.rllib.callbacks.callbacks import RLlibCallback
import numpy as np

class ActionLoggingCallbacks(RLlibCallback):
    def __init__(self, a=None, b=None, k=None, l=None, n=None, experiment_name="none"):
        super().__init__()
        # Generate unique filename with timestamp when callback is initialized
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.filename = (
            f"./diners_dilemma/data/dd_{experiment_name}_a{a}_b{b}_k{k}_l{l}_n{n}_{timestamp}.csv"
        )
        
        # Ensure the directory exists
        os.makedirs(os.path.dirname(self.filename), exist_ok=True)
        
        # Flag to track if we've written the header
        self.header_written = False
            
    def on_episode_end(self, *, episode, **kwargs):
        """Log each episode immediately"""        
        try:
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
            
            # Write immediately
            agent_cols = sorted(k for k in row.keys() if k.startswith("agent_"))
            fieldnames = agent_cols + ["return"]
            
            with open(self.filename, "a", newline="") as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                if not self.header_written:
                    writer.writeheader()
                    self.header_written = True
                    print("Header written")
                writer.writerow(row)
                
        except Exception as e:
            print(f"Error in on_episode_end: {e}")
            import traceback
            traceback.print_exc()