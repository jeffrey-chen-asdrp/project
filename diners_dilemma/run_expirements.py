import ray
from train import train_diners_dilemma
import json
import time
from datetime import datetime
import warnings

warnings.filterwarnings("ignore", category=DeprecationWarning)

# Test parameter sets for Diner's Dilemma
# Requirements: k - l > a - b, a - k/n > b - l/n
TEST_SETS = [
    # Set 1: Baseline (moderate dilemma)
    {"name": "Baseline", "a": 6, "b": 4, "k": 7, "l": 2},
    
    # Set 2: Strong dilemma (larger cost difference)
    {"name": "Strong_Dilemma", "a": 7, "b": 4, "k": 12, "l": 2},
    
    # Set 3: Weak dilemma (smaller cost difference)
    {"name": "Weak_Dilemma", "a": 5, "b": 4, "k": 6, "l": 2},
    
    # Set 4: High rewards (scaled up rewards)
    {"name": "High_Rewards", "a": 12, "b": 4, "k": 15, "l": 2},
    
    # Set 5: Low rewards (scaled down)
    {"name": "Low_Rewards", "a": 3, "b": 4, "k": 8, "l": 2},
    
    # Set 6: Low Cheap Cost
    {"name": "Low_Cheap_Cost", "a": 8, "b": 6, "k": 9, "l": 1},
    
    # Set 7: High cheap meal reward
    {"name": "High_Cheap_Reward", "a": 9, "b": 7, "k": 10, "l": 3},
    
    # Set 8: Extreme dilemma
    {"name": "Extreme_Dilemma", "a": 10, "b": 3, "k": 25, "l": 1},
]

def verify_dilemma_conditions(a, b, k, l, n):
    """Verify that parameters create a valid Diner's Dilemma"""
    condition1 = k - l > a - b
    condition2 = a - k/n > b - l/n
    
    print(f"  Condition 1 (k-l > a-b): {k-l} > {a-b} = {condition1}")
    print(f"  Condition 2 (a-k/n > b-l/n): {a-k/n:.2f} > {b-l/n:.2f} = {condition2}")
    print(f"  Individual utility - Expensive: {a-k/n:.2f}, Cheap: {b-l/n:.2f}")
    print(f"  Social optimum gap: {(a*n-k) - (b*n-l)} = {a*n-k} - {b*n-l} = {(a-b)*n - (k-l)}")
    
    return condition1 and condition2

def run_experiment_set(test_sets, num_agents=10, iterations=25, save_results=True):
    """
    Run a set of experiments with different parameter configurations.
    
    Args:
        test_sets (list): List of parameter dictionaries
        num_agents (int): Number of agents per experiment
        iterations (int): Number of training iterations per experiment
        save_results (bool): Whether to save results to JSON file
    
    Returns:
        list: List of experiment results
    """
    print("DINER'S DILEMMA PARAMETER TESTING")
    print(f"Testing {len(test_sets)} parameter configurations")
    print(f"Each experiment: {iterations} iterations, {num_agents} agents")
    print("=" * 60)
    
    all_results = []
    start_time = time.time()
    
    # Initialize Ray once for all experiments
    ray.init(ignore_reinit_error=True, num_gpus=1)
    
    try:
        for i, test_set in enumerate(test_sets):
            exp_start_time = time.time()
            
            print(f"\n[{i+1}/{len(test_sets)}] EXPERIMENT: {test_set['name']}")
            print(f"Parameters: a={test_set['a']}, b={test_set['b']}, k={test_set['k']}, l={test_set['l']}")
            print("-" * 50)
            
            # Verify conditions
            if not verify_dilemma_conditions(test_set['a'], test_set['b'], test_set['k'], test_set['l'], num_agents):
                print("❌ INVALID PARAMETERS - Skipping this set")
                continue
            
            print("✅ Valid Diner's Dilemma parameters")
            
            try:
                # Run the training
                results = train_diners_dilemma(
                    a=test_set['a'],
                    b=test_set['b'], 
                    k=test_set['k'],
                    l=test_set['l'],
                    num_agents=num_agents,
                    iterations=iterations,
                    experiment_name=test_set['name']
                )
                
                exp_time = time.time() - exp_start_time
                results['experiment_duration'] = exp_time
                
                # Summary
                print(f"\n{test_set['name']} SUMMARY:")
                print(f"  Duration: {exp_time:.1f}s")
                print(f"  Average return: {results['avg_return']:.4f}")
                print(f"  Final return: {results['final_return']:.4f}")
                print(f"  Best return: {results['best_return']:.4f}")
                print(f"  Improvement: {results['final_return'] - results['returns'][0]:.4f}")
                
                all_results.append(results)
                
            except Exception as e:
                print(f"❌ Error in experiment {test_set['name']}: {e}")
                # Add error result
                error_result = {
                    'experiment_name': test_set['name'],
                    'parameters': test_set,
                    'error': str(e),
                    'success': False
                }
                all_results.append(error_result)
                
    except KeyboardInterrupt:
        print("\nExperiments interrupted by user")
        
    finally:
        try:
            ray.shutdown()
        except:
            pass
    
    total_time = time.time() - start_time
    
    # Final summary
    print(f"\n{'='*60}")
    print(f"EXPERIMENT SUITE COMPLETED!")
    print(f"Total time: {total_time:.1f}s ({total_time/60:.1f} minutes)")
    print(f"Successful experiments: {len([r for r in all_results if 'error' not in r])}/{len(test_sets)}")

    return all_results

def main():
    """Main function to run all experiments"""
    # Configuration
    NUM_AGENTS = 10
    ITERATIONS = 25  # Reduced per scenario to manage total time
    
    # Run experiments
    results = run_experiment_set(
        test_sets=TEST_SETS,
        num_agents=NUM_AGENTS,
        iterations=ITERATIONS,
        save_results=True
    )

if __name__ == "__main__":
    main()