# from typing import Dict
import argparse
import numpy as np

import ray #type:ignore
from ray import tune #type:ignore
# from ray.rllib.env import BaseEnv #type:ignore
# from ray.rllib.policy import Policy #type:ignore
# from ray.rllib.policy.sample_batch import SampleBatch #type:ignore
# from ray.rllib.evaluation import MultiAgentEpisode, RolloutWorker #type:ignore
from ray.rllib.algorithms.callbacks import DefaultCallbacks #type:ignore

all_junction_list = ['cluster12203246695_12203246696_430572036_442436239', 
                       'cluster_547498658_547498666_547498756_547498762_#8more', 
                       'cluster_2052409830_2052409981_9356276530_9356276531', 
                       'cluster_1021221509_11808122037_11808122038_11808122040_#4more',
                       'cluster_2052409422_2052409707_542824247_542824770_#2more',
                       'cluster_2052409323_2052409733_2052409806_2052409936_#9more',
                       'cluster_2052409270_2052409892_2052410135_2052410161_#8more',
                       'cluster_2040873690_2040873694_2040873705_2040873709_#8more',
                       '55760356',
                       'cluster_2093101229_2093101656_2093101781_2093101915_#8more',
                       'cluster9663732079_J0_J1_J2_#2more',
                       'cluster428692206_428692253_9650210478_9650210479_#2more',
                       'cluster_1334947864_1334947865_1334947879_1334947882',
                       'cluster12092955396_1334947859',
                       'cluster_439980117_439980118_442435910_442435912',
                       'cluster_1289585639_439979990_8156136067_8156136068_#1more',
                       'cluster_2048655723_2048656743_2048656762_2048657045_#8more',
                       'cluster1478663503_1478663508_cluster_12092966426_12092966445_1478663506_2515541702']

class CustomLoggerCallback(DefaultCallbacks):
    def on_episode_start(
            self,
            *,
            worker,
            base_env,
            policies,
            episode,
            env_index = None,
            **kwargs,
        ):
        env = worker.env
        env.total_departed_count = 0  # 重置进入车辆统计
        env.total_arrived_count = 0  # 重置离开车辆统计
        
        episode.user_data["conflict_rate"] = []
        episode.user_data["avg_wait"] = []
        # episode.user_data["traffic_flow_rate"] = []  # 新增车流量列表
        episode.user_data["total_departed"] = 0  # 初始化进入网络的车辆总数
        episode.user_data["total_arrived"] = 0   # 初始化离开网络的车辆总数

        # 新增：初始化每个路口的等待时间统计
        for JuncID in all_junction_list:
            metric_name = f"avg_wait_{JuncID}"
            episode.user_data[metric_name] = []

    def on_episode_step(
            self,
            *,
            worker,
            base_env,
            policies = None,
            episode,
            env_index= None,
            **kwargs,
        ):

        # 检查是否有车辆流量数据
        if hasattr(worker.env, "total_departed_count") and hasattr(worker.env, "total_arrived_count"):
            # 直接更新 episode 内的累计统计
            episode.user_data["total_departed"] = worker.env.total_departed_count
            episode.user_data["total_arrived"] = worker.env.total_arrived_count

        conflict_rate = worker.env.monitor.conflict_rate[-1]
        episode.user_data["conflict_rate"].extend([conflict_rate])

        total_wait = 0
        for id in worker.env.previous_global_waiting.keys():
            total_wait += worker.env.previous_global_waiting[id]['sum']
        episode.user_data["avg_wait"].extend([total_wait])

        for id in worker.env.all_previous_global_waiting.keys():
            waiting_time = worker.env.all_previous_global_waiting[id]['sum']
            metric_name = f"avg_wait_{id}"
            episode.user_data[metric_name].extend([waiting_time])

        # # 记录每个路口的等待时间
        # for JuncID in all_junction_list:
        #     if JuncID in worker.env.all_previous_global_waiting:
        #         # 累加该路口的等待时间到对应的列表
        #         waiting_time = worker.env.all_previous_global_waiting[JuncID]['sum']
        #         if "junction_wait_times" not in episode.user_data:
        #             episode.user_data["junction_wait_times"] = {junc: [] for junc in all_junction_list}
        #         episode.user_data["junction_wait_times"][JuncID].append(waiting_time)

    def on_episode_end(
        self,
        *,
        worker,
        base_env,
        policies,
        episode,
        env_index = None,
        **kwargs,
    ):
        episode.custom_metrics["conflict_rate"] = np.mean(episode.user_data["conflict_rate"])
        episode.custom_metrics["avg_wait"] = np.mean(episode.user_data["avg_wait"])

        # 获取当前 episode 的统计
        total_departed = worker.env.total_departed_count
        total_arrived = worker.env.total_arrived_count

        # 添加为 custom metrics
        episode.custom_metrics["episode_departed"] = total_departed
        episode.custom_metrics["episode_arrived"] = total_arrived

        # 记录每个路口的平均等待时间
        for JuncID in all_junction_list:
            metric_name = f"avg_wait_{JuncID}"  # 自定义每个路口的metric名称
            episode.custom_metrics[metric_name] = np.mean(episode.user_data[metric_name])

        # # 获取等待时间直方图数据
        # if hasattr(worker.env, "all_waiting_time_histograms"):
        #     all_histograms = worker.env.all_waiting_time_histograms
        #     # 添加直方图数据到 episode.hist_data
        #     for junc_id, hist_data in all_histograms.items():
        #         for keyword, waiting_times in hist_data.items():
        #             hist_key = f"waiting_time_histogram_{junc_id}_{keyword}"
        #             episode.hist_data[hist_key] = waiting_times

        # 将路口流量数据存储为 histogram custom metric
        # if hasattr(worker.env, "intersection_traffic_counts"):
        # for junc_id, count in worker.env.intersection_traffic_counts.items():
        #     episode.custom_metrics[f"throughput_{junc_id}"] = count

        # 遍历每个路口，记录交通流量
        for JuncID, throughput in worker.env.junction_traffic_throughput.items():
            metric_name = f"TP_{JuncID}"
            episode.custom_metrics[metric_name] = throughput

# if __name__ == "__main__":
#     parser = argparse.ArgumentParser()
#     parser.add_argument("--num-iters", type=int, default=2000)
#     args = parser.parse_args()

#     ray.init()
#     trials = tune.run(
#         "PG",
#         stop={
#             "training_iteration": args.num_iters,
#         },
#         config={
#             "env": "CartPole-v0",
#             "callbacks": MyCallbacks, #type:ignore
#         },
#         return_trials=True)

#     # verify custom metrics for integration tests
#     custom_metrics = trials[0].last_result["custom_metrics"]
#     print(custom_metrics)
#     assert "pole_angle_mean" in custom_metrics
#     assert "pole_angle_min" in custom_metrics
#     assert "pole_angle_max" in custom_metrics
#     assert "num_batches_mean" in custom_metrics
#     assert "callback_ok" in trials[0].last_result