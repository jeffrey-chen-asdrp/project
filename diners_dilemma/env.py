import numpy as np
from ray.rllib.env.multi_agent_env import MultiAgentEnv
from gymnasium.spaces import Discrete, Box

class DinersDilemmaRLEnv(MultiAgentEnv):
    def __init__(self, config=None):
        super().__init__()
        cfg = config or {}
        self._num_agents = cfg.get("num_agents", 10)
        self._max_steps = cfg.get("max_steps", 200)

        self.dish_rewards = [6, 8] # default [3, 8]
        self.dish_costs = [2, 6] # default [2, 6]
        self.step_count = 0

        self.agents = [f"agent_{i}" for i in range(self._num_agents)]
        self.observation_spaces = {
            a: Box(0., 1., (self._num_agents,), dtype=np.float32)
            for a in self.agents
        }
        self.action_spaces = {
            a: Discrete(2) for a in self.agents
        }

    def reset(self, *, seed=None, options=None):
        self.step_count = 0
        obs = {a: np.zeros(self._num_agents, dtype=np.float32) for a in self.agents}
        return obs, {}

    def step(self, action_dict):
        self.step_count += 1

        total_cost = sum(self.dish_costs[action] for action in action_dict.values())
        shared_cost = total_cost / self._num_agents

        obs = {a: np.zeros(self._num_agents, dtype=np.float32) for a in self.agents}
        rewards = {
            a: self.dish_rewards[action] - shared_cost
            for a, action in action_dict.items()
        }

        done = self.step_count >= self._max_steps

        terminateds = {a: done for a in self.agents}
        truncateds = {a: False for a in self.agents}

        # ✅ Required keys:
        terminateds["__all__"] = done
        truncateds["__all__"] = False
        
        infos = {agent: {"action_taken": action} for agent, action in action_dict.items()}


        return obs, rewards, terminateds, truncateds, infos
