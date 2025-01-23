import time, json, datetime
import numpy as np
from ray.rllib.algorithms.algorithm import Algorithm
import argparse
import ray
from Env_original import Env
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
    "--save-dir", type=str, required=True, help="folder directory for saving evaluation results"
)
parser.add_argument(
    "--rv-rate", type=float, default=0.6, help="RV percentage. 0.0-1.0"
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
            "junction_list":['229','499','332','334'],
            "spawn_rl_prob":{},
            "probablity_RL":rv_rate,
            "cfg":'real_data/osm.sumocfg',
            "render":False,
            "map_xml":'real_data/CSeditClean_1.net_threelegs.xml',
            "max_episode_steps":args.stop_timesteps,
            "conflict_mechanism": 'flexible',
            "traffic_light_program":{
                "disable_state":'G',
                "disable_light_start":0
            }
        })

    results = []
    all_junction_wait_times = defaultdict(list)
    # Data storage structure
    evaluation_data = {}
    vehicle_path_data_collection = {}

    start_time = time.time()
    times = 2
    for i in range(times):
        print(f"{rv_rate}: Starting evaluation {i + 1}/{times}...")
        evaluation_start = time.time()
        dones = truncated = {}
        dones['__all__'] = truncated['__all__'] = False

        obs, info = env.reset()

        while not dones['__all__'] and not truncated['__all__']:
            actions = {}
            for agent_id, agent_obs in obs.items():
                actions[agent_id] = algo.compute_single_action(agent_obs, explore=args.explore_during_inference, policy_id="shared_policy")
            obs, reward, dones, truncated, info = env.step(actions)
            for key, done in dones.items():
                if done:
                    obs.pop(key)
            if dones['__all__']:
                obs, info = env.reset()

        # Collect statistics for each junction
        run_key = f"run_{i + 1}"
        evaluation_data[run_key] = {"junctions": {}}
        for junc_id in env.junction_list:
            junction_stats = env.get_junction_stats(junc_id)  # Assumes a method returning stats per junction
            evaluation_data[run_key]["junctions"][junc_id] = {
                "total_vehicles": junction_stats["total_vehicles"],
                "vehicle_types": junction_stats["vehicle_types"],
                "from_to_lanes": junction_stats["from_to_lanes"]
            }

        # Store vehicle_path_data for this run
        vehicle_path_data_collection[run_key] = env.vehicle_path_data

        avg_wait, per_junction_avg_wait = env.monitor.evaluate()

        # Append junction-level results
        for junc_id, avg_wait_time in per_junction_avg_wait.items():
            all_junction_wait_times[junc_id].append(avg_wait_time)

        # Append overall results
        results.append((avg_wait))
        evaluation_time = time.time() - evaluation_start
        print(f"{rv_rate}: Evaluation {i + 1}/{times} completed: avg_wait={avg_wait}, time={evaluation_time:.2f}s")

    # 获取当前时间的时间戳
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    print("Original: Saving all evaluation data to a single JSON file")
    # 文件名中加入时间戳
    with open(f"{args.save_dir}/evaluation_results_{timestamp}.json", "w") as json_file:
        json.dump(evaluation_data, json_file, indent=4)

    # 将每次运行的数据结构中的集合转换为列表，以便 JSON 序列化
    for run_key, vehicle_data in vehicle_path_data_collection.items():
        for veh_id, path_data in vehicle_data.items():
            path_data["incoming_lanes"] = list(path_data["incoming_lanes"])
            path_data["outgoing_lanes"] = list(path_data["outgoing_lanes"])

    print("Original: Saving vehicle path data")
    # 另一个文件名也加入时间戳
    with open(f"{args.save_dir}/vehicle_path_data_{timestamp}.json", "w") as json_file:
        json.dump(vehicle_path_data_collection, json_file, indent=4)

    total_time = time.time() - start_time
    print(f"\n{rv_rate}: {times} evaluations completed in {total_time:.2f}s.")

    # Unified statistics function
    def compute_stats(data, name):
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

    # Compute per-junction statistics
    print("\n--- Per Junction Statistics ---")
    for junc_id in all_junction_wait_times.keys():
        print(f"Junction {junc_id} - Waiting Time:")
        compute_stats(all_junction_wait_times[junc_id], f"Junction {junc_id} - Waiting Time")

    # Compute overall statistics
    avg_wait_results = [r for r in results]

    print(f"\n{rv_rate}: Overall Average Wait Time:")
    compute_stats(avg_wait_results, "Average Wait Time")

    algo.stop()
    ray.shutdown()
