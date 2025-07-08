import ray
from ray import tune
from ray.tune.registry import register_env
from ray.rllib.algorithms.ppo import PPOConfig
from env import DinersDilemmaRLEnv
from pprint import pprint
from callbacks import ActionLoggingCallbacks

num_agents = 20

env = DinersDilemmaRLEnv({"num_agents":num_agents})
obs_space = env.observation_spaces["agent_0"]
act_space = env.action_spaces["agent_0"]

ray.init(ignore_reinit_error=True)

env_name = "diners_rllib_env"
register_env(env_name, lambda cfg: DinersDilemmaRLEnv(cfg))

config = (
    PPOConfig()
    .environment(env=env_name, env_config={"num_agents":num_agents, "max_steps":200})
    .framework("torch")
    .multi_agent(
        policies={
            "shared_policy": (
                None,
                env.observation_spaces["agent_0"],
                env.action_spaces["agent_0"],
                {}
            )
        },
        policy_mapping_fn=lambda agent_id, episode, **kwargs: "shared_policy"
    )
    .env_runners(
        num_env_runners=1, 
        num_envs_per_env_runner=1
    )
    .training(
        lr=1e-5,
        train_batch_size_per_learner=2000,
        num_epochs=5,
    )
    .callbacks(callbacks_class=ActionLoggingCallbacks)
    .resources(
        num_gpus=1,
        num_gpus_per_worker=1
    )
)

ppo = config.build_algo()

for i in range(25):
    result = ppo.train()
    print(f"Iter {i}: return_mean={result['env_runners']['episode_return_mean']:.4f}")
