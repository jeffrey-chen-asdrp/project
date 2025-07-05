import random

class QLearningAgent:
    def __init__(self, name, alpha=0.8, gamma=0.9, epsilon=0.3):
        self.name = name
        self.q_table = {"cooperate": 0, "defect": 0}
        self.alpha = alpha      # Learning rate
        self.gamma = gamma      # Discount factor
        self.epsilon = epsilon  # Exploration rate
        self.last_action = None

    def decide(self):
        # Epsilon-greedy: Explore or exploit
        if random.random() < self.epsilon:
            action = random.choice(["cooperate", "defect"])

        else:
            action = min(self.q_table, key=self.q_table.get)
        self.last_action = action

        self.epsilon -= 0.001

        return action

    def learn(self, reward):
        # Basic Q-update
        old_value = self.q_table[self.last_action]
        self.q_table[self.last_action] = old_value + self.alpha * (reward - old_value)

    def __str__(self):
        return f"{self.name} Q-values: {self.q_table}"
    
agent1 = QLearningAgent("Agent1")
agent2 = QLearningAgent("Agent2")


def play_q_game(agent1, agent2):
    move1 = agent1.decide()
    move2 = agent2.decide()

    print(f"\n{agent1.name}: {move1.upper()} | {agent2.name}: {move2.upper()}")

    if move1 == "cooperate" and move2 == "cooperate":
        reward1, reward2 = 5, 5
    elif move1 == "cooperate" and move2 == "defect":
        reward1, reward2 = 2, 20
    elif move1 == "defect" and move2 == "cooperate":
        reward1, reward2 = 20, 2
    else:
        reward1, reward2 = 3, 3

    agent1.learn(reward1)
    agent2.learn(reward2)

    return reward1, reward2

for i in range(100):
    play_q_game(agent1, agent2)
    print(f"Agent1 Cooperate EV: {agent1.q_table['cooperate']}")
    print(f"Agent1 Defect EV: {agent1.q_table['defect']}")