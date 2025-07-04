import supersuit as ss
from stable_baselines3 import PPO
from pettingzoo.utils.conversions import aec_to_parallel
from diners_dilemma import DinersDilemmaEnv

env = DinersDilemmaEnv(num_agents=4)
env = aec_to_parallel(env)

# Wrap env for compatibility
env = ss.pettingzoo_env_to_vec_env_v1(env)
env = ss.concat_vec_envs_v1(env, num_vec_envs=1, num_cpus=1, base_class='stable_baselines3')

model = PPO("MlpPolicy", env, verbose=1)
model.learn(total_timesteps=10000)
