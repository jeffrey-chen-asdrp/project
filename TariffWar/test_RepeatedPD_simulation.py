# test_repeated_tariff_pd.py

import matplotlib.pyplot as plt
import random
import numpy as np
from RepeatedPD_simulation import RepeatedTariffPD


def test_repeated_tariff_pd_qlearning():
    # Set seed for reproducibility
    random.seed(42)
    np.random.seed(42)

    config = {
        "dilemma_type": "repeated_tariff_pd",
        "rounds": 100,
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


def plot_full_analysis(agent, sim, tit_agent):
    rounds = range(1, len(agent.q_history["C"]["C"]) + 1)
    usa_actions = [r["usa_action"] for r in sim.results["rounds"]]
    usa_payoffs = [r["usa_payoff"] for r in sim.results["rounds"]]
    china_actions = [r["china_action"] for r in sim.results["rounds"]]
    china_payoffs = [r["china_payoff"] for r in sim.results["rounds"]]
    usa_cumulative = np.cumsum(usa_payoffs)
    china_cumulative = np.cumsum(china_payoffs)

    fig, axs = plt.subplots(4, 1, figsize=(12, 14), sharex=True)

    # Panel 1: USA Payoff, Action, and Policy Shifts
    usa_action_numeric = [0 if a == "C" else 1 for a in usa_actions]
    policy_shift = [i for i in range(1, len(usa_action_numeric)) if usa_action_numeric[i] != usa_action_numeric[i - 1]]

    axs[0].plot(rounds, usa_action_numeric, label="USA Action (0=C, 1=D)", drawstyle="steps-mid")
    axs[0].plot(rounds, usa_payoffs, label="USA Payoff", marker='o')
    for idx in policy_shift:
        axs[0].axvline(x=idx + 1, color='red', linestyle='--', alpha=0.5)
    axs[0].set_title("Panel 1: USA Action, Payoff, and Policy Shifts")
    axs[0].legend()
    axs[0].grid(True)

    # Panel 2: USA Q-learning Diagnostics
    axs[1].plot(rounds, agent.q_history["C"]["C"], label="Q(C | C)", marker='o')
    axs[1].plot(rounds, agent.q_history["C"]["D"], label="Q(D | C)", marker='x')
    axs[1].plot(rounds, agent.q_history["D"]["C"], label="Q(C | D)", marker='s')
    axs[1].plot(rounds, agent.q_history["D"]["D"], label="Q(D | D)", marker='^')
    axs[1].set_title("Panel 2: Q-Learning Agent Q-value Evolution")
    axs[1].legend()
    axs[1].grid(True)

    # Panel 3: China Action and Payoff
    china_action_numeric = [0 if a == "C" else 1 for a in china_actions]
    axs[2].step(rounds, china_action_numeric, where='mid', label="China Action (0=C, 1=D)", color='purple')
    axs[2].plot(rounds, china_payoffs, label="China Payoff", color='orange', marker='o')
    axs[2].set_title("Panel 3: China  Action and Payoff")
    axs[2].legend()
    axs[2].grid(True)

    # Panel 4: Cumulative Payoffs
    axs[3].plot(rounds, usa_cumulative, label="USA Cumulative Payoff", color='green')
    axs[3].plot(rounds, china_cumulative, label="China Cumulative Payoff", color='blue')
    axs[3].set_title("Panel 4: Cumulative Payoffs")
    axs[3].legend()
    axs[3].set_xlabel("Round")
    axs[3].grid(True)

    plt.suptitle("Repeated Tariff PD: Agent Behaviors and Learning Diagnostics")
    plt.tight_layout()
    plt.savefig("repeated_tariff_pd_full_analysis.png")
    plt.show()


if __name__ == "__main__":
    test_repeated_tariff_pd_qlearning()

