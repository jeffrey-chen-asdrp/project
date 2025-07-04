from diners_dilemma import DinersDilemmaEnv

NUM_ROUNDS = 3
env = DinersDilemmaEnv(num_agents=4)

for ep in range(NUM_ROUNDS):
    print(f"\n=== Round {ep + 1} ===")
    env.reset()

    for agent in env.agent_iter():
        obs, reward, termination, truncation, info = env.last()
        action = None if (termination or truncation) else env.action_spaces[agent].sample()
        print(f"{agent:>8} observes {obs} -> acts {action}")
        env.step(action)

    env.render()
