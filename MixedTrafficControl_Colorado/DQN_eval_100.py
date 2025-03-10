import time
import numpy as np
from ray.rllib.algorithms.algorithm import Algorithm
import argparse
import ray
from Env import Env
from collections import defaultdict

parser = argparse.ArgumentParser()
parser.add_argument(
    "--run", type=str, default="DQN", help="The RLlib-registered algorithm to use."
)
parser.add_argument("--num-cpus", type=int, default=1)
parser.add_argument(
    "--stop-timesteps",
    type=int,
    default=1000,
    help="Number of timesteps to test.",
)
parser.add_argument(
    "--model-dir", type=str, required=True, help="path to the RL model for evaluation"
)
parser.add_argument(
    "--save-dir", type=str, required=False, help="folder directory for saving evaluation results"
)
parser.add_argument(
    "--rv-rate", type=float, default=0.2, help="RV percentage. 0.0-1.0"
)
parser.add_argument(
    "--explore-during-inference",
    action="store_true",
    help="Whether the trained policy should use exploration during action "
    "inference.",
)

if __name__ == "__main__":
    args = parser.parse_args()

    ray.init(local_mode=True)

    rv_rate = args.rv_rate
    print("rv_rate: ", rv_rate)
    checkpoint_path = args.model_dir
    print("checkpoint_path: ", checkpoint_path)
    algo = Algorithm.from_checkpoint(checkpoint_path)

    env = Env({
        "junction_list": [
            'cluster12203246695_12203246696_430572036_442436239',
            'cluster_2052409422_2052409707_542824247_542824770_#2more',
            'cluster_2093101229_2093101656_2093101781_2093101915_#8more',
            'cluster_439980117_439980118_442435910_442435912'],
        "spawn_rl_prob": {},
        "probablity_RL": rv_rate,
        "cfg": 'sumo_networks/colorado/colorado.sumocfg',
        "render": False,
        "map_xml": 'sumo_networks/colorado/colorado.net.xml',
        "max_episode_steps": args.stop_timesteps,
        "conflict_mechanism": 'flexible',
        "traffic_light_program": {
            "disable_state": 'G',
            "disable_light_start": 0
        }
    })

    results = []
    all_junction_wait_times = defaultdict(list)
    all_junction_throughputs = defaultdict(list)

    start_time = time.time()
    for i in range(100):
        print(f"{rv_rate}: Starting evaluation {i + 1}/100...")
        env.total_arrived_count = 0
        evaluation_start = time.time()
        dones = truncated = {}
        dones['__all__'] = truncated['__all__'] = False

        obs, info = env.reset()

        while not dones['__all__'] and not truncated['__all__']:
            actions = {}
            for agent_id, agent_obs in obs.items():
                actions[agent_id] = algo.compute_single_action(
                    agent_obs, explore=args.explore_during_inference, policy_id="shared_policy")
            obs, reward, dones, truncated, info = env.step(actions)
            for key, done in dones.items():
                if done:
                    obs.pop(key)
            if dones['__all__']:
                obs, info = env.reset()

        avg_wait, total_arrived, per_junction_avg_wait, per_junction_throughput = env.monitor.evaluate(env)

        # Append junction-level results
        for junc_id, avg_wait_time in per_junction_avg_wait.items():
            all_junction_wait_times[junc_id].append(avg_wait_time)
        for junc_id, throughput in per_junction_throughput.items():
            all_junction_throughputs[junc_id].append(throughput)

        # Append overall results
        results.append((avg_wait, total_arrived))
        evaluation_time = time.time() - evaluation_start
        print(f"{rv_rate}: Evaluation {i + 1}/100 completed: avg_wait={avg_wait}, total_arrived={total_arrived}, time={evaluation_time:.2f}s")

    total_time = time.time() - start_time
    print(f"\n{rv_rate}: 100 evaluations completed in {total_time:.2f}s.")

    # Unified statistics function
    def compute_stats(data, name, is_per_junction=False):
        q1 = np.percentile(data, 25)
        median = np.median(data)
        q3 = np.percentile(data, 75)
        iqr = q3 - q1
        minimum = np.min(data)
        maximum = np.max(data)
        print(f"\n{name} Statistics:")
        print(f"  Minimum: {minimum}")
        print(f"  Q1: {q1}")
        print(f"  Median: {median}")
        print(f"  Q3: {q3}")
        print(f"  IQR: {iqr}")
        print(f"  Maximum: {maximum}")
        if is_per_junction:
            return {
                "Minimum": minimum,
                "Q1": q1,
                "Median": median,
                "Q3": q3,
                "IQR": iqr,
                "Maximum": maximum
            }

    # Compute per-junction statistics
    print("\n--- Per Junction Statistics ---")
    junction_stats = {}
    for junc_id in all_junction_wait_times.keys():
        print(f"Junction {junc_id} - Waiting Time:")
        junction_stats[junc_id] = compute_stats(all_junction_wait_times[junc_id], f"Junction {junc_id} - Waiting Time", is_per_junction=True)
        print(f"Junction {junc_id} - Throughput:")
        compute_stats(all_junction_throughputs[junc_id], f"Junction {junc_id} - Throughput")

    # Compute overall statistics
    avg_wait_results = [r[0] for r in results]
    total_arrived_results = [r[1] for r in results]

    print(f"\n{rv_rate}: Overall Average Wait Time:")
    compute_stats(avg_wait_results, "Average Wait Time")
    print(f"\n{rv_rate}: Overall Total Arrived:")
    compute_stats(total_arrived_results, "Total Arrived")

    algo.stop()
    ray.shutdown()
