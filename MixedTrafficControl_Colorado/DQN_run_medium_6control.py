import argparse
import ray #type:ignore
from ray import air, tune #type:ignore
from ray.rllib.algorithms.dqn import DQNConfig, DQNTorchPolicy #type:ignore
from Env_medium import Env #type:ignore
# from ray.rllib.examples.models.shared_weights_model import ( #type:ignore
#     SharedWeightsModel1,
#     SharedWeightsModel2,
#     TF2SharedWeightsModel,
#     TorchSharedWeightsModel,
# )
# from ray.rllib.utils.framework import try_import_tf #type:ignore
from ray.rllib.utils.test_utils import check_learning_achieved #type:ignore
from core.custom_logger_medium import CustomLoggerCallback #type:ignore
import os
os.environ['RAY_AIR_NEW_OUTPUT'] = '1'
from ray.tune.experimental.output import AirVerbosity, get_air_verbosity #type:ignore

# tf1, tf, tfv = try_import_tf()

parser = argparse.ArgumentParser()
parser.add_argument("--num-cpus", type=int, default=0)
parser.add_argument("--framework",choices=["tf", "tf2", "torch"],default="torch",help="The DL framework specifier.")
parser.add_argument("--as-test",action="store_true",help="Whether this script should be run as a test: --stop-reward must be achieved within --stop-timesteps AND --stop-iters.")
parser.add_argument("--stop-iters", type=int, default=2000, help="Number of iterations to train.")
parser.add_argument("--rv-rate", type=float, default=0.6, help="RV percentage. 0.0-1.0")

if __name__ == "__main__":
    args = parser.parse_args()

    ray.init(num_gpus=1, num_cpus=args.num_cpus)

    dummy_env = Env({
            "junction_list":['cluster12203246695_12203246696_430572036_442436239',
                    'cluster_2052409422_2052409707_542824247_542824770_#2more',
                    'cluster_2093101229_2093101656_2093101781_2093101915_#8more',
                    'cluster_439980117_439980118_442435910_442435912',
                    'cluster_547498658_547498666_547498756_547498762_#8more',
                    'cluster_2052409323_2052409733_2052409806_2052409936_#9more'],
            "TL_list":['J0',
                       'cluster_2052409422_2052409707_542824247_542824770_#2more',
                       'cluster_2093101229_2093101656_2093101781_2093101915_#8more',
                       'GS_cluster_439980117_439980118_442435910_442435912',
                       'cluster_547498658_547498666_547498756_547498762_#8more',
                       'cluster_2052409323_2052409733_2052409806_2052409936_#9more'],
            "spawn_rl_prob":{},
            "probablity_RL":args.rv_rate,
            "cfg":'sumo_networks/colorado/colorado_medium.sumocfg',
            "render":False,    
            "map_xml":'sumo_networks/colorado/colorado_medium.net.xml',
            "max_episode_steps":1000, #1000
            "conflict_mechanism":'flexible',
            "traffic_light_program":{ #交通灯
                "disable_state":'G',
                "disable_light_start":0
            }
        })
    obs_space = dummy_env.observation_space
    act_space = dummy_env.action_space
    dummy_env.close()

    policy = {
        "shared_policy": (
            DQNTorchPolicy,
            obs_space,
            act_space,
            None
        )}
    #将共享策略分配给环境中的每个智能体
    policy_mapping_fn = lambda agent_id, episode, worker, **kwargs: "shared_policy"

    config = (
        DQNConfig()
        .environment(Env, env_config={
            "junction_list":['cluster12203246695_12203246696_430572036_442436239',
                    'cluster_2052409422_2052409707_542824247_542824770_#2more',
                    'cluster_2093101229_2093101656_2093101781_2093101915_#8more',
                    'cluster_439980117_439980118_442435910_442435912',
                    'cluster_547498658_547498666_547498756_547498762_#8more',
                    'cluster_2052409323_2052409733_2052409806_2052409936_#9more'],
            "TL_list":['J0',
                       'cluster_2052409422_2052409707_542824247_542824770_#2more',
                       'cluster_2093101229_2093101656_2093101781_2093101915_#8more',
                       'GS_cluster_439980117_439980118_442435910_442435912',
                       'cluster_547498658_547498666_547498756_547498762_#8more',
                       'cluster_2052409323_2052409733_2052409806_2052409936_#9more'],
            "spawn_rl_prob":{},
            "probablity_RL":args.rv_rate,
            "cfg":'sumo_networks/colorado/colorado_medium.sumocfg',
            "render":False,
            "map_xml":'sumo_networks/colorado/colorado_medium.net.xml',
            # "rl_prob_range": [i*0.1 for i in range(5, 10)], # change RV penetration rate when reset
            "max_episode_steps":1000,
            "conflict_mechanism":'flexible',
            "traffic_light_program":{
                "disable_state":'G',
                "disable_light_start":0 
            }
        }, 
        auto_wrap_old_gym_envs=False)
        .framework(args.framework)
        .training(
            num_atoms=51,
            noisy=False,
            hiddens= [512, 512, 512],
            dueling=True,
            double_q=True,
            replay_buffer_config={
                'type':'MultiAgentPrioritizedReplayBuffer',
                'prioritized_replay_alpha':0.5,
                'capacity':50000,
            }
        )
        .rollouts(num_rollout_workers=args.num_cpus-1, rollout_fragment_length="auto")
        # .rollouts(num_rollout_workers=args.num_cpus-1, rollout_fragment_length=50)

        .multi_agent(policies=policy, policy_mapping_fn=policy_mapping_fn)
        # Use GPUs iff `RLLIB_NUM_GPUS` env var set to > 0.ass 'ray.rllib.policy.policy_template.DQNTorchPolicy'> for PolicyID=shared_policy
        .resources(num_gpus=1, num_cpus_per_worker=1)
        .callbacks(CustomLoggerCallback)
    )

    stop = {
        "training_iteration": args.stop_iters,
    }

    results = tune.Tuner(
        "DQN",
        param_space=config.to_dict(),
        run_config=air.RunConfig(
            name='DQN_6+8_RV'+str(args.rv_rate), 
            storage_path = "/blue/du.j/liusongyang/checkpoints/", 
            stop=stop, 
            # verbose = 3,
            verbose = get_air_verbosity(AirVerbosity.DEFAULT), 
            log_to_file=False, 
            checkpoint_config=air.CheckpointConfig(
                num_to_keep = 40,
                checkpoint_frequency = 10)
        ),
    ).fit()

    if args.as_test:
        check_learning_achieved(results, args.stop_reward)
    ray.shutdown()