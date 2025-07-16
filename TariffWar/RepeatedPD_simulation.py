# repeated_tariff_pd.py

from social_dilemmas import SocialDilemmaSimulation
import numpy as np
import random

TARIFF_HIGH = "D"  # Defect: High tariff
TARIFF_LOW = "C"   # Cooperate: Low tariff

PD_PAYOFFS = {
    ("C", "C"): (3, 3),
    ("C", "D"): (0, 5),
    ("D", "C"): (5, 0),
    ("D", "D"): (1, 1),
}

class TitForTatAgent:
    def __init__(self, name):
        self.name = name
        self.last_opponent_action = TARIFF_HIGH # Start nice
        self.history = []
        self.total_payoff = 0

    def choose_action(self):
        return self.last_opponent_action

    def learn(self, my_action, opponent_action, payoff):
        self.last_opponent_action = opponent_action
        self.history.append((my_action, opponent_action, payoff))
        self.total_payoff += payoff


class AlwaysDefectAgent:
    def __init__(self, name):
        self.name = name
        self.history = []
        self.total_payoff = 0

    def choose_action(self):
        return TARIFF_HIGH

    def learn(self, my_action, opponent_action, payoff):
        self.history.append((my_action, opponent_action, payoff))
        self.total_payoff += payoff

class AlwaysCoopAgent:
    def __init__(self, name):
        self.name = name
        self.history = []
        self.total_payoff = 0

    def choose_action(self):
        return TARIFF_LOW

    def learn(self, my_action, opponent_action, payoff):
        self.history.append((my_action, opponent_action, payoff))
        self.total_payoff += payoff


class QLearningAgent:
    def __init__(self, name, epsilon=0.1, gamma=0.9, alpha=0.1):
        #episilon : Exploration rate, gamma : High means long term, alpha : learning rate
        self.name = name
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon
        self.q_table = {
            "C": {"C": 0.0, "D": 0.0},
            "D": {"C": 0.0, "D": 0.0},
        }
        self.q_history = {
            "C": {"C": [], "D": []},
            "D": {"C": [], "D": []},
        }
        self.last_action = None
        #self.last_state = TARIFF_LOW #Nice
        self.last_state =TARIFF_HIGH #Not nice
        self.history = []
        self.total_payoff = 0

    def choose_action(self):
        if random.random() < self.epsilon:
            action = random.choice([TARIFF_LOW, TARIFF_HIGH])
        else:
            state_actions = self.q_table[self.last_state]
            max_q = max(state_actions.values())
            best_actions = [a for a, q in state_actions.items() if q == max_q]
            action = random.choice(best_actions)
        self.last_action = action
        return action

    def learn(self, my_action, opponent_action, reward):
        prev_q = self.q_table[self.last_state][my_action]
        future_q = max(self.q_table[opponent_action].values())
        new_q = prev_q + self.alpha * (reward + self.gamma * future_q - prev_q)
        self.q_table[self.last_state][my_action] = new_q
        self.last_state = opponent_action
        self.history.append((my_action, opponent_action, reward))
        self.total_payoff += reward

        # Record Q-values for plotting
        for state in ["C", "D"]:
            for action in ["C", "D"]:
                self.q_history[state][action].append(self.q_table[state][action])


class RepeatedTariffPD(SocialDilemmaSimulation):
    def initialize_agents(self):
        self.us = QLearningAgent("USA")
        self.china = TitForTatAgent("China")
        self.agents = [self.us, self.china]

    def run_round(self):
        self.round += 1
        round_data = {"round": self.round}

        us_action = self.us.choose_action()
        cn_action = self.china.choose_action()

        us_payoff, cn_payoff = PD_PAYOFFS[(us_action, cn_action)]

        self.us.learn(us_action, cn_action, us_payoff)
        self.china.learn(cn_action, us_action, cn_payoff)

        round_data["usa_action"] = us_action
        round_data["china_action"] = cn_action
        round_data["usa_payoff"] = us_payoff
        round_data["china_payoff"] = cn_payoff

        self.results["rounds"].append(round_data)

        print(f"Round {self.round}: USA {us_action}, China {cn_action}")
        print(f"  Payoffs -> USA: {us_payoff}, China: {cn_payoff}")

    def calculate_final_stats(self):
        self.results["leader_total_payoff"] = self.us.total_payoff
        self.results["follower_total_payoff"] = self.china.total_payoff


