# stackelberg_tariff_sim.py

import random
import numpy as np

class StackelbergTariffGame:
    def __init__(self, config):
        self.rounds = config.get("rounds", 50)
        self.leader = config.get("leader")
        self.follower = config.get("follower")
        self.results = {"rounds": []}

    def calculate_payoff(self, leader_action, follower_action):
        payoff_matrix = {
            ("C", "C"): (3, 3),
            ("C", "D"): (0, 5),
            ("D", "C"): (5, 0),
            ("D", "D"): (1, 1)
        }
        return payoff_matrix[(leader_action, follower_action)]

    def run_round(self):
        state_leader = self.follower.last_action if hasattr(self.follower, "last_action") else random.choice(["C", "D"])
        leader_action = self.leader.decide_tariff(state_leader)

        state_follower = leader_action
        follower_action = self.follower.respond_to_tariff(state_follower)

        leader_payoff, follower_payoff = self.calculate_payoff(leader_action, follower_action)

        if hasattr(self.leader, "update"):
            self.leader.update(state_leader, leader_action, follower_action, leader_payoff)
        if hasattr(self.follower, "update"):
            self.follower.update(state_follower, follower_action, leader_action, follower_payoff)

        self.results["rounds"].append({
            "leader_action": leader_action,
            "follower_action": follower_action,
            "leader_payoff": leader_payoff,
            "follower_payoff": follower_payoff
        })

    def run(self):
        for _ in range(self.rounds):
            self.run_round()
        return self.results

# Leader Strategies

class GreedyLeader:
    def decide_tariff(self, state=None):
        return "D"

class BluffingLeader:
    def __init__(self, bluff_prob=0.2):
        self.bluff_prob = bluff_prob

    def decide_tariff(self, state=None):
        return "D" if random.random() < self.bluff_prob else "C"

class QLearningLeader:
    def __init__(self, epsilon=0.1, gamma=0.9, alpha=0.5):
        self.q = {}  # (state, action): value
        self.epsilon = epsilon
        self.gamma = gamma
        self.alpha = alpha

    def decide_tariff(self, state):
        if random.random() < self.epsilon:
            action = random.choice(["C", "D"])
        else:
            q_values = {a: self.q.get((state, a), 0) for a in ["C", "D"]}
            action = max(q_values, key=q_values.get)
        self.last_state = state
        self.last_action = action
        return action

    def update(self, state, action, opponent_action, reward):
        next_state = opponent_action
        max_q_next = max([self.q.get((next_state, a), 0) for a in ["C", "D"]])
        old_q = self.q.get((state, action), 0)
        self.q[(state, action)] = old_q + self.alpha * (reward + self.gamma * max_q_next - old_q)

# Follower Strategies

class BestResponseFollower:
    def respond_to_tariff(self, state):
        return "D" if state == "C" else "C"

class BluffingFollower:
    def __init__(self, bluff_prob=0.2):
        self.bluff_prob = bluff_prob

    def respond_to_tariff(self, state):
        if random.random() < self.bluff_prob:
            return random.choice(["C", "D"])
        return "D" if state == "C" else "C"

class PiecewiseRuleBasedFollower:
    def __init__(self):
        self.history = []

    def respond_to_tariff(self, state):
        self.history.append(state)
        if len(self.history) >= 3 and self.history[-3:] == ["D", "D", "D"]:
            return "D"
        return "C"

class QLearningFollower:
    def __init__(self, epsilon=0.1, gamma=0.9, alpha=0.5):
        self.q = {}
        self.epsilon = epsilon
        self.gamma = gamma
        self.alpha = alpha

    def respond_to_tariff(self, state):
        if random.random() < self.epsilon:
            action = random.choice(["C", "D"])
        else:
            q_values = {a: self.q.get((state, a), 0) for a in ["C", "D"]}
            action = max(q_values, key=q_values.get)
        self.last_state = state
        self.last_action = action
        return action

    def update(self, state, action, opponent_action, reward):
        next_state = opponent_action
        max_q_next = max([self.q.get((next_state, a), 0) for a in ["C", "D"]])
        old_q = self.q.get((state, action), 0)
        self.q[(state, action)] = old_q + self.alpha * (reward + self.gamma * max_q_next - old_q)

