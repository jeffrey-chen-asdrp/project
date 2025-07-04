import supersuit as ss
from pettingzoo.utils.conversions import aec_to_parallel
from stable_baselines3 import PPO
from stable_baselines3.common.vec_env import VecMonitor
from stable_baselines3.common.monitor import Monitor
from stable_baselines3.common.logger import configure
from stable_baselines3.common.callbacks import EvalCallback
from diners_dilemma import DinersDilemmaEnv

# Set up environment
train_raw = DinersDilemmaEnv(num_agents=4)
train_par = aec_to_parallel(train_raw)
train_par = ss.pad_observations_v0(train_par)
vec_env = ss.pettingzoo_env_to_vec_env_v1(train_par)
vec_env = ss.concat_vec_envs_v1(vec_env, num_vec_envs=1, base_class="stable_baselines3")
vec_env = VecMonitor(vec_env)

# Configure logger with csv output
log_folder = "ppo_diners/"
new_logger = configure(log_folder, ["stdout", "csv", "tensorboard"])

# Initialize PPO with vectorize env
model = PPO("MlpPolicy", vec_env, verbose=1)
model.set_logger(new_logger)

# Prepare EvalCallback to run evaluation every 1000 timesteps
eval_cb = EvalCallback(
    vec_env,
    best_model_save_path='./best_model/',
    log_path=log_folder,
    eval_freq=1000,
    n_eval_episodes=10,
    deterministic=True,
    render=False,
    verbose=1
)

# Train and save the model
model.learn(total_timesteps=20000, callback=eval_cb)
model.save("ppo_diners_model")

print("Training complete!")
