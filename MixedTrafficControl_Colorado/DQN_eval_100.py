from ray.rllib.algorithms.algorithm import Algorithm
import argparse
import ray
# from ray.rllib.utils.framework import try_import_tf

from Env import Env  # Assuming Env is your custom environment class

parser = argparse.ArgumentParser()
parser.add_argument("--run", type=str, default="DQN", help="The RLlib-registered algorithm to use.")
parser.add_argument("--num-cpus", type=int, default=1)
parser.add_argument("--stop-timesteps", type=int, default=1000, help="Number of timesteps to test.")
parser.add_argument("--model-dir", type=str, required=True, help="Path to the RL model for evaluation")
parser.add_argument("--rv-rate", type=float, default=0.2, help="RV percentage. 0.0-1.0")
parser.add_argument(
    "--explore-during-inference",
    action="store_true",  # Default is False
    help="Whether the trained policy should use exploration during action inference.",
)

if __name__ == "__main__":
    args = parser.parse_args()

    ray.init(local_mode=True)

    rv_rate = args.rv_rate
    print("rv_rate: ", rv_rate)
    checkpoint_path = args.model_dir
    print("checkpoint_path: ", checkpoint_path)

    algo = Algorithm.from_checkpoint(checkpoint_path)

    env_config = {
        "junction_list": [
            'cluster12203246695_12203246696_430572036_442436239',
            'cluster_2052409422_2052409707_542824247_542824770_#2more',
            'cluster_2093101229_2093101656_2093101781_2093101915_#8more',
            'cluster_439980117_439980118_442435910_442435912',
        ],
        "spawn_rl_prob": {},
        "probablity_RL": rv_rate,
        "cfg": 'sumo_networks/colorado/colorado.sumocfg',
        "render": False,
        "map_xml": 'sumo_networks/colorado/colorado.net.xml',
        "max_episode_steps": args.stop_timesteps,
        "conflict_mechanism": 'off',  # 'flexible',
        "traffic_light_program": {
            "disable_state": 'G',
            "disable_light_start": 0
        }
    }

    # Store results for 100 evaluations
    avg_wait_results = []
    total_arrived_results = []

    for eval_run in range(100):
        print(f"Running evaluation {eval_run + 1}/100")
        env = Env(env_config)
        episode_reward = 0
        dones = truncated = {}
        dones['__all__'] = truncated['__all__'] = False

        obs, info = env.reset()

        while not dones['__all__'] and not truncated['__all__']:
            actions = {}
            for agent_id, agent_obs in obs.items():
                actions[agent_id] = algo.compute_single_action(
                    agent_obs, explore=args.explore_during_inference, policy_id="shared_policy"
                )
            obs, reward, dones, truncated, info = env.step(actions)
            for key, done in dones.items():
                if done:
                    obs.pop(key)
            if dones['__all__']:
                obs, info = env.reset()

        # Collect evaluation results
        avg_wait, total_arrived = env.monitor.evaluate(env)
        avg_wait_results.append(avg_wait)
        total_arrived_results.append(total_arrived)

        env.close()

    # Print all results
    print("Results for 100 evaluations:")
    for i in range(100):
        print(f"Evaluation {i + 1}: avg_wait={avg_wait_results[i]}, total_arrived={total_arrived_results[i]}")

    # Print averages
    print("\nAverages over 100 evaluations:")
    print(f"Average avg_wait: {sum(avg_wait_results) / 100}")
    print(f"Average total_arrived: {sum(total_arrived_results) / 100}")

    algo.stop()
    ray.shutdown()