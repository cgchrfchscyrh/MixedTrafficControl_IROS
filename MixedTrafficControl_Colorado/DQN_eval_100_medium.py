import time, json, datetime
import numpy as np #type:ignore
from ray.rllib.algorithms.algorithm import Algorithm #type:ignore
import argparse
import ray #type:ignore
from Env_medium import Env
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
        "cfg":'sumo_networks/colorado/colorado_medium.sumocfg',
        "render": False,
        "map_xml":'sumo_networks/colorado/colorado_medium.net.xml',
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
    # Data storage structure
    evaluation_data = {}
    vehicle_path_data_collection = {}
    start_time = time.time()
    times = 100

    # 预初始化变量，确保后续可以安全访问
    avg_wait = 0
    total_arrived = 0
    per_junction_avg_wait = {junc_id: 0 for junc_id in env.junction_list}
    per_junction_throughput = {junc_id: 0 for junc_id in env.junction_list}

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
            obs, reward, dones, truncated, info = env.step(actions, eval=True)
            for key, done in dones.items():
                if done:
                    obs.pop(key)

            # **如果 episode 结束，不管是因 `dones` 还是 `truncated`，先统计数据**
            if dones['__all__'] or truncated['__all__']:
                run_key = f"run_{i + 1}"
                evaluation_data[run_key] = {"junctions": {}}

                for junc_id in env.junction_list:
                    junction_stats = env.get_junction_stats(junc_id)  # **确保 reset 之前统计数据**
                    evaluation_data[run_key]["junctions"][junc_id] = {
                        "total_vehicles_enter": junction_stats["total_vehicles_enter"],
                        "total_vehicles_pass": junction_stats["total_vehicles_pass"],
                        "vehicle_types_enter": junction_stats["vehicle_types_enter"],
                        "vehicle_types_pass": junction_stats["vehicle_types_pass"],
                        "vehicle_paths": junction_stats["vehicle_paths"],
                    }

                vehicle_path_data_collection[run_key] = env.vehicle_path_data
                avg_wait, total_arrived, per_junction_avg_wait, per_junction_throughput = env.monitor.evaluate(env)

            if dones['__all__']:
                obs, info = env.reset()

        # Append junction-level results
        for junc_id, avg_wait_time in per_junction_avg_wait.items():
            all_junction_wait_times[junc_id].append(avg_wait_time)
        for junc_id, throughput in per_junction_throughput.items():
            all_junction_throughputs[junc_id].append(throughput)

        # Append overall results
        results.append((avg_wait, total_arrived))
        evaluation_time = time.time() - evaluation_start
        print(f"Medium {rv_rate}: Evaluation {i + 1}/{times} completed: avg_wait={avg_wait}, total_arrived={total_arrived}, time={evaluation_time:.2f}s")
    
    # 获取当前时间的时间戳
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")

    print("Medium: Saving all evaluation data to a single JSON file")
    # 文件名中加入时间戳
    with open(f"{args.save_dir}/medium_{rv_rate}_evaluation_results_{timestamp}.json", "w") as json_file:
        json.dump(evaluation_data, json_file, indent=4)

    # 将每次运行的数据结构中的集合转换为列表，以便 JSON 序列化
    for run_key, vehicle_data in vehicle_path_data_collection.items():
        for veh_id, path_data in vehicle_data.items():
            path_data["incoming_lanes"] = list(path_data["incoming_lanes"])
            path_data["outgoing_lanes"] = list(path_data["outgoing_lanes"])

    print("Medium: Saving vehicle path data")
    # 另一个文件名也加入时间戳
    with open(f"{args.save_dir}/vehicle_path_data_{timestamp}.json", "w") as json_file:
        json.dump(vehicle_path_data_collection, json_file, indent=4)

    total_time = time.time() - start_time
    print(f"\n{rv_rate}: {times} evaluations completed in {total_time:.2f}s.")

    # Unified statistics function
    def compute_stats(data, name, is_per_junction=False):
        q1 = np.percentile(data, 25)
        median = np.median(data)
        q3 = np.percentile(data, 75)
        # iqr = q3 - q1
        minimum = np.min(data)
        maximum = np.max(data)
        print(f"\n{name} Statistics:")
        print(f"  Minimum: {minimum}")
        print(f"  Q1: {q1}")
        print(f"  Median: {median}")
        print(f"  Q3: {q3}")
        # print(f"  IQR: {iqr}")
        print(f"  Maximum: {maximum}")
        if is_per_junction:
            return {
                "Minimum": round(minimum,2),
                "Q1": round(q1,2),
                "Median": round(median,2),
                "Q3": round(q3,2),
                # "IQR": iqr,
                "Maximum": round(maximum,2)
            }

    # Compute per-junction statistics
    print("\n--- Per Junction Statistics ---")
    junction_stats = {}
    for junc_id in all_junction_wait_times.keys():
        junction_stats[junc_id] = compute_stats(all_junction_wait_times[junc_id], f"Junction {junc_id} - Waiting Time", is_per_junction=True)
        compute_stats(all_junction_throughputs[junc_id], f"Junction {junc_id} - Throughput")

    # Compute overall statistics
    avg_wait_results = [r[0] for r in results]
    total_arrived_results = [r[1] for r in results]

    print(f"\nMedium_{rv_rate}: Overall Average Wait Time:")
    compute_stats(avg_wait_results, "Average Wait Time")
    print(f"\nMedium_{rv_rate}: Overall Total Arrived:")
    compute_stats(total_arrived_results, "Total Arrived")

    algo.stop()
    ray.shutdown()
