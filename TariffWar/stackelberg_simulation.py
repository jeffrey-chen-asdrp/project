from social_dilemmas import SocialDilemmaSimulation
import numpy as np

class StackelbergLeaderAgent:
    def __init__(self, name, sim):
        self.name = name
        self.sim = sim
        self.total_payoff = 0
        self.history = []

    def decide_tariff(self):
        best_tariff = 0
        best_payoff = float('-inf')

        for t in range(0, 40, 5):
            cn_response = self.sim.get_follower_response_preview(t)
            us_payoff, _ = self.simulate_payoffs(t, cn_response)
            if us_payoff > best_payoff:
                best_payoff = us_payoff
                best_tariff = t

        return best_tariff

    def simulate_payoffs(self, t_us, t_cn):
        export_loss_us = 0.6 * t_cn
        domestic_gain_us = 1.2 * t_us
        return domestic_gain_us - export_loss_us, None

    def record_payoff(self, payoff):
        self.total_payoff += payoff
        self.history.append(payoff)


class FollowerPiecewise:
    def __init__(self, name):
        self.name = name
        self.total_payoff = 0
        self.history = []

    def respond_to_tariff(self, leader_tariff):
        return self.respond_preview(leader_tariff)

    def respond_preview(self, leader_tariff):
        if leader_tariff <= 10:
            return 5
        elif leader_tariff <= 30:
            return leader_tariff * 0.6
        elif leader_tariff <= 60:
            return leader_tariff * 0.8
        else:
            return 50

    def record_payoff(self, payoff):
        self.total_payoff += payoff
        self.history.append(payoff)


class FollowerDataDriven:
    def __init__(self, name):
        self.name = name
        self.total_payoff = 0
        self.history = []
        self.response_table = {0: 0, 10: 5, 20: 12, 30: 22, 40: 32, 50: 38, 60: 42}

    def respond_to_tariff(self, leader_tariff):
        return self.respond_preview(leader_tariff)

    def respond_preview(self, leader_tariff):
        keys = sorted(self.response_table.keys())
        values = [self.response_table[k] for k in keys]
        return float(np.interp(leader_tariff, keys, values))

    def record_payoff(self, payoff):
        self.total_payoff += payoff
        self.history.append(payoff)


class FollowerStrategicBluff:
    def __init__(self, name):
        self.name = name
        self.total_payoff = 0
        self.history = []
        self.round = 0

    def respond_to_tariff(self, leader_tariff):
        self.round += 1
        return self._bluff_logic(leader_tariff, self.round)

    def respond_preview(self, leader_tariff):
        # Simulate early round behavior for preview
        return self._bluff_logic(leader_tariff, round=1)

    def _bluff_logic(self, leader_tariff, round):
        if round < 3 and leader_tariff > 25:
            return min(50, leader_tariff + 15)
        else:
            return leader_tariff * 0.7

    def record_payoff(self, payoff):
        self.total_payoff += payoff
        self.history.append(payoff)


class StackelbergTariffSimulation(SocialDilemmaSimulation):
    def initialize_agents(self):
        follower_type = self.config.get("parameters", {}).get("follower_type", "piecewise")

        if follower_type == "data_table":
            self.follower = FollowerDataDriven("China")
        elif follower_type == "bluffing":
            self.follower = FollowerStrategicBluff("China")
        else:
            self.follower = FollowerPiecewise("China")

        self.leader = StackelbergLeaderAgent("USA", self)
        self.agents = [self.leader, self.follower]

    def get_follower_response_preview(self, leader_tariff):
        if hasattr(self.follower, "respond_preview"):
            return self.follower.respond_preview(leader_tariff)
        else:
            return self.follower.respond_to_tariff(leader_tariff)

    def run_round(self):
        self.round += 1
        round_data = {"round": self.round}

        leader_tariff = self.leader.decide_tariff()
        round_data["leader_tariff"] = leader_tariff

        follower_tariff = self.follower.respond_to_tariff(leader_tariff)
        round_data["follower_tariff"] = follower_tariff

        us_payoff, cn_payoff = self.calculate_payoffs(leader_tariff, follower_tariff)
        self.leader.record_payoff(us_payoff)
        self.follower.record_payoff(cn_payoff)

        round_data["us_payoff"] = us_payoff
        round_data["china_payoff"] = cn_payoff

        self.results["rounds"].append(round_data)

        # Debug info
        print(f"Round {self.round}")
        print(f"  USA sets tariff:     {leader_tariff:.1f}%")
        print(f"  China responds with: {follower_tariff:.1f}%")
        print(f"  USA payoff:          {us_payoff:.2f}")
        print(f"  China payoff:        {cn_payoff:.2f}")
        print("-" * 40)

    def calculate_payoffs(self, us_tariff, cn_tariff):
        us_export_loss = 0.6 * cn_tariff
        cn_export_loss = 0.7 * us_tariff
        us_domestic_gain = 1.2 * us_tariff
        cn_substitution_gain = 1.2 * (100 - us_tariff)

        us_payoff = us_domestic_gain - us_export_loss
        cn_payoff = cn_substitution_gain - cn_export_loss

        return us_payoff, cn_payoff

    def calculate_final_stats(self):
        self.results["leader_total_payoff"] = self.leader.total_payoff
        self.results["follower_total_payoff"] = self.follower.total_payoff



