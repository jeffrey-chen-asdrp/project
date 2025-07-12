###############################################
#
# test_simulation.py
#
#
# Standalone pytest for prisoners_dilemma 
#
# @author: Nikhil Muthukumar
# @version: 1.0
# @since: 2025-07-11
###############################################

import pytest
from simulation import SimulationFactory
import matplotlib.pyplot as plt

@pytest.fixture
def sample_config():
    return {
        'game_type': 'prisoners_dilemma',
        'strategies': {
            'all_cooperate': 1,
            'all_defect': 1,
            'tit_for_tat': 1
        },
        'rounds': 5,
        'payoffs': {
            'T': 5,
            'R': 3,
            'P': 1,
            'S': 0
        }
    }

def test_verbose_simulation_with_chart(sample_config):
    sim = SimulationFactory.create_simulation(sample_config)

    print("\n=== AGENT INITIALIZATION ===")
    for agent in sim.agents:
        print(f"{agent['id']} ({agent['type']}) initialized.")

    for r in range(sample_config['rounds']):
        print(f"\n--- Round {r + 1} ---")
        round_result = sim.run_round()

        for interaction in round_result['interactions']:
            a1 = interaction['agent1']
            a2 = interaction['agent2']
            m1 = interaction['move1']
            m2 = interaction['move2']
            s1 = interaction['score1']
            s2 = interaction['score2']
            print(f"{a1} ({m1}) vs {a2} ({m2}) --> Scores: {s1}, {s2}")

        print("\nCurrent Total Scores:")
        for agent in sim.agents:
            aid = agent['id']
            score = agent['strategy'].score
            print(f"  {aid}: {score}")

    print("\n=== FINAL RESULTS ===")
    for agent in sim.agents:
        aid = agent['id']
        score = agent['strategy'].score
        print(f"{aid}: Final Score = {score}")

    # ✅ Plot cumulative scores
    print("\nGenerating plot...")
    scores = sim.results['scores']
    agents = list(scores.keys())
    rounds = list(range(1, len(next(iter(scores.values()))) + 1))

    plt.figure(figsize=(10, 6))
    for agent in agents:
        plt.plot(rounds, scores[agent], label=agent, marker='o')

    plt.xlabel("Round")
    plt.ylabel("Cumulative Score")
    plt.title("Agent Scores Over Rounds")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig("agent_scores_chart.png")  # Save the chart as a file
    plt.show()  # Also display if running interactively

    # ✅ Basic assertions
    assert len(sim.results['rounds']) == sample_config['rounds']
    for agent in sim.agents:
        assert agent['strategy'].score >= 0
