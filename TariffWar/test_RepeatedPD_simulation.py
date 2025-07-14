# test_repeated_tariff_pd.py

import matplotlib.pyplot as plt
from RepeatedPD_simulation import RepeatedTariffPD

def test_repeated_tariff_pd():
    config = {
        "dilemma_type": "repeated_tariff_pd",
        "rounds": 20,
        "parameters": {}
    }

    sim = RepeatedTariffPD(config)
    sim.initialize_agents()
    sim.results = {"rounds": []}
    sim.round = 0

    for _ in range(config["rounds"]):
        sim.run_round()

    sim.calculate_final_stats()

    # Extract data
    rounds = [r["round"] for r in sim.results["rounds"]]
    usa_actions = [r["usa_action"] for r in sim.results["rounds"]]
    china_actions = [r["china_action"] for r in sim.results["rounds"]]
    usa_payoffs = [r["usa_payoff"] for r in sim.results["rounds"]]
    china_payoffs = [r["china_payoff"] for r in sim.results["rounds"]]
    usa_cum = [sum(usa_payoffs[:i+1]) for i in range(len(usa_payoffs))]
    china_cum = [sum(china_payoffs[:i+1]) for i in range(len(china_payoffs))]

    # Plot
    fig, axes = plt.subplots(3, 1, figsize=(10, 12), sharex=True)

    axes[0].plot(rounds, usa_payoffs, label="USA Payoff", marker='o')
    axes[0].plot(rounds, china_payoffs, label="China Payoff", marker='x')
    axes[0].set_title("Payoffs per Round")
    axes[0].set_ylabel("Payoff")
    axes[0].legend()
    axes[0].grid(True)

    def action_to_num(actions):
        return [0 if a == "C" else 1 for a in actions]

    axes[1].step(rounds, action_to_num(usa_actions), where='mid', label="USA (0=C, 1=D)")
    axes[1].step(rounds, action_to_num(china_actions), where='mid', label="China (0=C, 1=D)")
    axes[1].set_title("Actions per Round")
    axes[1].set_ylabel("Action")
    axes[1].legend()
    axes[1].grid(True)

    axes[2].plot(rounds, usa_cum, label="USA Cumulative")
    axes[2].plot(rounds, china_cum, label="China Cumulative")
    axes[2].set_title("Cumulative Payoff")
    axes[2].set_xlabel("Round")
    axes[2].set_ylabel("Total Payoff")
    axes[2].legend()
    axes[2].grid(True)

    plt.tight_layout()
    plt.savefig("repeated_tariff_pd_plot.png")
    plt.show()
