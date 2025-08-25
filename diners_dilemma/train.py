import ray
from ray.tune.registry import register_env
from ray.rllib.algorithms.ppo import PPOConfig
from env import DinersDilemmaRLEnv
from callbacks import ActionLoggingCallbacks
import warnings

warnings.filterwarnings("ignore", category=DeprecationWarning)

def train_diners_dilemma(a, b, k, l, num_agents=10, iterations=25, experiment_name="none"):
    """
    Train a PPO agent on the Diner's Dilemma environment.
    
    Args:
        a (float): Joy of eating the expensive meal
        b (float): Joy of eating the cheap meal
        k (float): Cost of the expensive meal
        l (float): Cost of the cheap meal
        num_agents (int): Number of agents in the environment
        iterations (int): Number of training iterations
        experiment_name (str): Name for this experiment (used in env registration)
    
    Returns:
        dict: Training results including returns and final metrics
    """
    
    print(f"Starting training: {experiment_name}")
    print(f"Parameters: a={a}, b={b}, k={k}, l={l}, agents={num_agents}")
    
    # Verify Diner's Dilemma conditions
    condition1 = k - l > a - b
    condition2 = a - k/num_agents > b - l/num_agents
    
    if not (condition1 and condition2):
        raise ValueError(f"Invalid Diner's Dilemma parameters. "
                        f"Condition 1 (k-l > a-b): {condition1}, "
                        f"Condition 2 (a-k/n > b-l/n): {condition2}")
    
    try:
        env = DinersDilemmaRLEnv({"num_agents": num_agents, 
                                  "b": b, "a": a, 
                                  "l": l, "k": k})

        # Use unique env name for each experiment to avoid conflicts
        env_name = f"diners_env_{experiment_name}"
        register_env(env_name, lambda cfg: DinersDilemmaRLEnv(cfg))

        config = (
            PPOConfig()
            .environment(env=env_name, env_config={
                "num_agents": num_agents, 
                "max_steps": 200,
                "b": b, "a": a,
                "l": l, "k": k 
            })
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
                num_envs_per_env_runner=1,
            )
            .training(
                lr=1e-5,
                train_batch_size_per_learner=2000,
                num_epochs=5,
            )
            .callbacks(callbacks_class=lambda: ActionLoggingCallbacks(a=a, b=b, k=k, l=l, n=num_agents, experiment_name=experiment_name))
            .resources(
                num_gpus=1
            )
            .debugging(
                logger_creator=None
            )
        )

        ppo = config.build_algo()

        # Track training results
        returns = []
        
        for i in range(iterations):
            result = ppo.train()
            episode_return = result['env_runners']['episode_return_mean']
            returns.append(episode_return)
            print(f"====== Iter {i}: return_mean={episode_return:.4f} ======")

        # Clean up
        ppo.stop()
        
        # Return results summary
        results = {
            'experiment_name': experiment_name,
            'parameters': {'a': a, 'b': b, 'k': k, 'l': l, 'num_agents': num_agents},
            'returns': returns,
            'avg_return': sum(returns) / len(returns),
            'final_return': returns[-1],
            'best_return': max(returns),
            'worst_return': min(returns),
            'iterations': iterations
        }
        
        return results
        
    except Exception as e:
        print(f"Error in training {experiment_name}: {e}")
        raise

if __name__ == "__main__":
    # Default single run for testing
    ray.init(ignore_reinit_error=True, num_gpus=1)
    
    try:
        # Default parameters
        a = 8  # expensive meal reward
        b = 6  # cheap meal reward  
        k = 6  # expensive meal cost
        l = 2  # cheap meal cost
        
        results = train_diners_dilemma(a, b, k, l, num_agents=10, iterations=50, experiment_name="single_test")
        
        print(f"\nTraining completed!")
        print(f"Average return: {results['avg_return']:.4f}")
        print(f"Final return: {results['final_return']:.4f}")
        print(f"Best return: {results['best_return']:.4f}")
        
    finally:
        try:
            ray.shutdown()
        except:
            pass