"""Example of using RLlib's debug callbacks.

Here we use callbacks to track the average CartPole pole angle magnitude as a
custom metric.
"""

from typing import Dict
import argparse
import numpy as np

import ray #type:ignore
from ray import tune #type:ignore
from ray.rllib.env import BaseEnv #type:ignore
from ray.rllib.policy import Policy #type:ignore
from ray.rllib.policy.sample_batch import SampleBatch #type:ignore
from ray.rllib.evaluation import MultiAgentEpisode, RolloutWorker #type:ignore
from ray.rllib.algorithms.callbacks import DefaultCallbacks #type:ignore

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
        
        # 获取等待时间直方图数据
        if hasattr(worker.env, "all_waiting_time_histograms"):
            all_histograms = worker.env.all_waiting_time_histograms
            # 添加直方图数据到 episode.hist_data
            for junc_id, hist_data in all_histograms.items():
                for keyword, waiting_times in hist_data.items():
                    hist_key = f"waiting_time_histogram_{junc_id}_{keyword}"
                    episode.hist_data[hist_key] = waiting_times

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--num-iters", type=int, default=2000)
    args = parser.parse_args()

    ray.init()
    trials = tune.run(
        "PG",
        stop={
            "training_iteration": args.num_iters,
        },
        config={
            "env": "CartPole-v0",
            "callbacks": MyCallbacks, #type:ignore
        },
        return_trials=True)

    # verify custom metrics for integration tests
    custom_metrics = trials[0].last_result["custom_metrics"]
    print(custom_metrics)
    assert "pole_angle_mean" in custom_metrics
    assert "pole_angle_min" in custom_metrics
    assert "pole_angle_max" in custom_metrics
    assert "num_batches_mean" in custom_metrics
    assert "callback_ok" in trials[0].last_result
