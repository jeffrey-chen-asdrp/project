# test_repeated_tariff_pd.py

import matplotlib.pyplot as plt
import random
import numpy as np
from RepeatedPD_simulation import RepeatedTariffPD, QLearningAgent


def test_repeated_tariff_pd_qlearning():
    # Set seed for reproducibility
    random.seed(42)
    np.random.seed(42)

    config = {
        "dilemma_type": "repeated_tariff_pd",
        "rounds": 1500,
        "parameters": {}
    }

    sim = RepeatedTariffPD(config)
    sim.initialize_agents()
    sim.results = {"rounds": []}
    sim.round = 0

    for _ in range(config["rounds"]):
        sim.run_round()

    sim.calculate_final_stats()
    plot_full_analysis(sim.us, sim, sim.china)


def is_q_learning_agent(agent):
    return isinstance(agent, QLearningAgent)


def get_agent_label(agent):
    if is_q_learning_agent(agent):
        return f"Q-Learning (ε={agent.epsilon}, γ={agent.gamma}, α={agent.alpha})"
    else:
        return agent.__class__.__name__


def plot_full_analysis(agent_us, sim, agent_china):
    rounds = range(1, len(sim.results["rounds"]) + 1)
    usa_actions = [r["usa_action"] for r in sim.results["rounds"]]
    usa_payoffs = [r["usa_payoff"] for r in sim.results["rounds"]]
    china_actions = [r["china_action"] for r in sim.results["rounds"]]
    china_payoffs = [r["china_payoff"] for r in sim.results["rounds"]]
    usa_cumulative = np.cumsum(usa_payoffs)
    china_cumulative = np.cumsum(china_payoffs)

    num_panels = 3 + is_q_learning_agent(agent_us) + is_q_learning_agent(agent_china)
    fig, axs = plt.subplots(num_panels, 1, figsize=(12, 4 * num_panels), sharex=True)

    panel = 0

    # Panel: USA Payoff, Action, and Policy Shifts
    usa_action_numeric = [0 if a == "C" else 1 for a in usa_actions]
    policy_shift = [i for i in range(1, len(usa_action_numeric)) if usa_action_numeric[i] != usa_action_numeric[i - 1]]
    agent_us_label = get_agent_label(agent_us)

    axs[panel].plot(rounds, usa_action_numeric, label="USA Action (0=C, 1=D)", drawstyle="steps-mid")
    axs[panel].plot(rounds, usa_payoffs, label="USA Payoff", marker='o')
    for idx in policy_shift:
        axs[panel].axvline(x=idx + 1, color='red', linestyle='--', alpha=0.5)
    axs[panel].set_title(f"USA Action, Payoff, and Policy Shifts ({agent_us_label})")
    axs[panel].legend()
    axs[panel].grid(True)
    panel += 1

    # Panel: USA Q-learning Diagnostics
    if is_q_learning_agent(agent_us):
        axs[panel].plot(rounds, agent_us.q_history["C"]["C"], label="Q(C | C)", marker='o')
        axs[panel].plot(rounds, agent_us.q_history["C"]["D"], label="Q(D | C)", marker='x')
        axs[panel].plot(rounds, agent_us.q_history["D"]["C"], label="Q(C | D)", marker='s')
        axs[panel].plot(rounds, agent_us.q_history["D"]["D"], label="Q(D | D)", marker='^')
        axs[panel].set_title(f"USA Q-Learning Q-value Evolution (ε={agent_us.epsilon}, γ={agent_us.gamma}, α={agent_us.alpha})")
        axs[panel].legend()
        axs[panel].grid(True)
        panel += 1

    # Panel: China Payoff and Action
    china_action_numeric = [0 if a == "C" else 1 for a in china_actions]
    agent_china_label = get_agent_label(agent_china)
    axs[panel].step(rounds, china_action_numeric, where='mid', label="China Action (0=C, 1=D)", color='purple')
    axs[panel].plot(rounds, china_payoffs, label="China Payoff", color='orange', marker='o')
    axs[panel].set_title(f"China Action and Payoff ({agent_china_label})")
    axs[panel].legend()
    axs[panel].grid(True)
    panel += 1

    # Panel: China Q-learning Diagnostics (if applicable)
    if is_q_learning_agent(agent_china):
        axs[panel].plot(rounds, agent_china.q_history["C"]["C"], label="Q(C | C)", marker='o')
        axs[panel].plot(rounds, agent_china.q_history["C"]["D"], label="Q(D | C)", marker='x')
        axs[panel].plot(rounds, agent_china.q_history["D"]["C"], label="Q(C | D)", marker='s')
        axs[panel].plot(rounds, agent_china.q_history["D"]["D"], label="Q(D | D)", marker='^')
        axs[panel].set_title(f"China Q-Learning Q-value Evolution (ε={agent_china.epsilon}, γ={agent_china.gamma}, α={agent_china.alpha})")
        axs[panel].legend()
        axs[panel].grid(True)
        panel += 1

    # Final Panel: Cumulative Payoffs
    axs[panel].plot(rounds, usa_cumulative, label="USA Cumulative Payoff", color='green')
    axs[panel].plot(rounds, china_cumulative, label="China Cumulative Payoff", color='blue')
    axs[panel].set_title("Cumulative Payoffs")
    axs[panel].legend()
    axs[panel].set_xlabel("Round")
    axs[panel].grid(True)
    plt.tight_layout(rect=[0, 0, 1, 0.96])
    plt.suptitle("Repeated Tariff PD: Adaptive and Static Agent Analysis")
    # plt.tight_layout()
    plt.savefig("repeated_tariff_pd_full_analysis.png")
    plt.show()


if __name__ == "__main__":
    test_repeated_tariff_pd_qlearning()
