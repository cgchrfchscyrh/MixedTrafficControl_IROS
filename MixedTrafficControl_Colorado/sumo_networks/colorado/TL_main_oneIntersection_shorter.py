import argparse
import os, sys
# import random
sys.path.append(os.getcwd())
from Env_baseline_oneIntersection_shorter import Env #type:ignore
parser = argparse.ArgumentParser()

parser.add_argument(
    "--stop-iters",
    type=int,
    default=200,
    help="Number of iterations to train before we do inference.",
)
parser.add_argument(
    "--stop-timesteps",
    type=int,
    default=100000,
    help="Number of timesteps to train before we do inference.",
)

parser.add_argument(
    "--explore-during-inference",
    action="store_true",
    help="Whether the trained policy should use exploration during action "
    "inference.",
)
parser.add_argument(
    "--num-episodes-during-inference",
    type=int,
    default=10,
    help="Number of episodes to do inference over after training.",
)

if __name__ == "__main__":
    args = parser.parse_args()

    ## TODO map xml could be parsed from sumocfg file
    env = Env({
            "junction_list":['cluster_2052409422_2052409707_542824247_542824770_#2more'],
            "spawn_rl_prob":{},
            "probablity_RL":0.0,
            "cfg":'sumo_networks/colorado/colorado_oneIntersection_shorter.sumocfg',
            "render":True,
            "map_xml":'sumo_networks/colorado/colorado_oneIntersection_shorter.net.xml',
            "max_episode_steps":1000,
            "traffic_light_program":{
                "disable_state":'G',
                "disable_light_start":20000
            }
        })

    episode_reward = 0
    dones = truncated = {}
    dones['__all__'] = truncated['__all__'] = False

    obs, info = env.reset(options={'mode': 'HARD'})

    while not dones['__all__'] and not truncated['__all__']:
        actions = {}
        obs, reward, dones, truncated, info = env.step(actions)

        for key, done in dones.items():
            if done:
                obs.pop(key)
    
    env.monitor.evaluate(env)