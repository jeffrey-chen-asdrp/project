from pettingzoo import AECEnv
from pettingzoo.utils.agent_selector import AgentSelector
import numpy as np
from gymnasium.spaces import Discrete, Box


class DinersDilemmaEnv(AECEnv):
    metadata = {
        "render_modes": ["human"], 
        "name": "diners_dilemma_v0",
        "is_parallelizable": True
    }

    def __init__(self, num_agents=4):
        super().__init__()

        self.render_mode = self.metadata["render_modes"][0]

        self._num_agents = num_agents
        self.agents = [f"agent_{i}" for i in range(num_agents)]
        self.possible_agents = self.agents[:]
        self.agent_selector = AgentSelector(self.agents)
        self.agent_selection = self.agent_selector.next()

        self.action_spaces = {agent: Discrete(2) for agent in self.agents}
        self.observation_spaces = {
            agent: Box(low=0, high=1, shape=(1,), dtype=np.float32)
            for agent in self.agents
        }

        self.dish_rewards = [3, 8]  # cheap, expensive
        self.dish_costs = [2, 6]    # cheap, expensive

        self.actions = {}
        self.terminated = False

        # PettingZoo expects these:
        self._rewards = {agent: 0 for agent in self.agents}
        self._cumulative_rewards = {agent: 0 for agent in self.agents}
        self.terminations = {agent: False for agent in self.agents}
        self.truncations = {agent: False for agent in self.agents}
        self.dones = {agent: False for agent in self.agents}
        self.infos = {agent: {} for agent in self.agents}

    def observe(self, agent):
        obs = np.zeros(self._num_agents, dtype=np.float32)
        for i, a in enumerate(self.agents):
            if a in self.actions:
                obs[i] = self.actions[a]
        return obs

    def reset(self, seed=None, options=None):
        self.agents = self.possible_agents[:]
        self.agent_selector.reinit(self.agents)
        self.agent_selection = self.agent_selector.next()
        self.actions = {}
        self.terminated = False

        self._rewards = {agent: 0 for agent in self.agents}
        self._cumulative_rewards = {agent: 0 for agent in self.agents}
        self.terminations = {agent: False for agent in self.agents}
        self.truncations = {agent: False for agent in self.agents}
        self.dones = {agent: False for agent in self.agents}
        self.infos = {agent: {} for agent in self.agents}

    def step(self, action):
        if self.terminated:
            return self._was_dead_step(action)

        self.actions[self.agent_selection] = action

        if self.agent_selector.is_last():
            self._resolve_round()
        else:
            self.agent_selection = self.agent_selector.next()

    def _resolve_round(self):
        total_cost = sum(self.dish_costs[a] for a in self.actions.values())
        shared_cost = total_cost / self._num_agents

        for agent, action in self.actions.items():
            reward = self.dish_rewards[action] - shared_cost
            self._rewards[agent] = reward
            self._cumulative_rewards[agent] += reward

        self.rewards = self._rewards.copy()

        for agent in self.agents:
            self.terminations[agent] = True
            self.dones[agent] = True

        self.terminated = True
        print("Resolved Round")

    def render(self):
        print("Actions:", self.actions)
        print("Rewards:", self._rewards)

    def close(self):
        pass
    
