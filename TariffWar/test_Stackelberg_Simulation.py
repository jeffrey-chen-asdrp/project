import matplotlib.pyplot as plt
from stackelberg_simulation import StackelbergTariffSimulation

def run_simulation_for_follower(follower_type, rounds=20):
    config = {
        "dilemma_type": "stackelberg_tariff",
        "rounds": rounds,
        "parameters": {"follower_type": follower_type}
    }
    sim = StackelbergTariffSimulation(config)
    sim.initialize_agents()
    return sim.run_simulation()

def test_compare_followers():
    follower_types = ["piecewise", "data_table", "bluffing"]
    results_by_type = {ftype: run_simulation_for_follower(ftype) for ftype in follower_types}

    rounds = list(range(1, 21))
    fig, axes = plt.subplots(3, 1, figsize=(10, 14), sharex=True)

    # 1. Tariff Comparison
    for ftype, result in results_by_type.items():
        leader_tariffs = [r["leader_tariff"] for r in result["rounds"]]
        follower_tariffs = [r["follower_tariff"] for r in result["rounds"]]
        axes[0].plot(rounds, leader_tariffs, label=f"{ftype} (leader)")
        axes[0].plot(rounds, follower_tariffs, linestyle='--', label=f"{ftype} (follower)")
    axes[0].set_title("Tariff Levels per Round by Follower Type")
    axes[0].set_ylabel("Tariff (%)")
    axes[0].legend()
    axes[0].grid(True)

    # 2. Payoff Comparison
    for ftype, result in results_by_type.items():
        us_payoffs = [r["us_payoff"] for r in result["rounds"]]
        cn_payoffs = [r["china_payoff"] for r in result["rounds"]]
        axes[1].plot(rounds, us_payoffs, label=f"{ftype} (USA)")
        axes[1].plot(rounds, cn_payoffs, linestyle='--', label=f"{ftype} (China)")
    axes[1].set_title("Payoffs per Round by Follower Type")
    axes[1].set_ylabel("Payoff")
    axes[1].legend()
    axes[1].grid(True)

    # 3. Cumulative Payoffs
    for ftype, result in results_by_type.items():
        us_cum = [sum(r["us_payoff"] for r in result["rounds"][:i+1]) for i in range(20)]
        cn_cum = [sum(r["china_payoff"] for r in result["rounds"][:i+1]) for i in range(20)]
        axes[2].plot(rounds, us_cum, label=f"{ftype} (USA)")
        axes[2].plot(rounds, cn_cum, linestyle='--', label=f"{ftype} (China)")
    axes[2].set_title("Cumulative Payoff Over Time")
    axes[2].set_xlabel("Round")
    axes[2].set_ylabel("Cumulative Payoff")
    axes[2].legend()
    axes[2].grid(True)

    plt.tight_layout()
    plt.savefig("StacklebergTariff.png")
    plt.show()

# Run the test manually if not using pytest:
if __name__ == "__main__":
    test_compare_followers()
