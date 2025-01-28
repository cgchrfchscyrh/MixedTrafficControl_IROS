import numpy as np
import matplotlib
matplotlib.use('Agg')  # 设置为非交互模式后端
import matplotlib.pyplot as plt
import os, threading
from datetime import datetime
# from collections import defaultdict

# import ray #type:ignore
# from ray import tune #type:ignore
# from ray.rllib.env import BaseEnv #type:ignore
# from ray.rllib.policy import Policy #type:ignore
# from ray.rllib.policy.sample_batch import SampleBatch #type:ignore
# from ray.rllib.evaluation import MultiAgentEpisode, RolloutWorker #type:ignore
from ray.rllib.algorithms.callbacks import DefaultCallbacks #type:ignore

all_junction_list = ['cluster12203246695_12203246696_430572036_442436239', 
                       'cluster_547498658_547498666_547498756_547498762_#8more', 

                       'cluster_2052409422_2052409707_542824247_542824770_#2more',
                       'cluster_2052409323_2052409733_2052409806_2052409936_#9more',

                       'cluster_2093101229_2093101656_2093101781_2093101915_#8more',
                       'cluster9663732079_J0_J1_J2_#2more',

                       'cluster_439980117_439980118_442435910_442435912',
                       'cluster_1289585639_439979990_8156136067_8156136068_#1more']

class CustomLoggerCallback(DefaultCallbacks):
    def __init__(self):
        super().__init__()
        self.episode_count = 0  # 初始化计数器

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
        # self.episode_total = episode_total
        # episode_total += 1

        env = worker.env
        env.total_departed_count = 0  # 重置进入车辆统计
        env.total_arrived_count = 0  # 重置离开车辆统计
        
        episode.user_data["conflict_rate"] = []
        episode.user_data["avg_wait"] = []
        episode.user_data["total_departed"] = 0  # 初始化进入网络的车辆总数
        episode.user_data["total_arrived"] = 0   # 初始化离开网络的车辆总数

        # 初始化每个路口的等待时间统计
        for JuncID in all_junction_list:
            metric_name = f"avg_wait_{JuncID}"
            episode.user_data[metric_name] = []

        # env.junction_waiting_histograms = {junc: [] for junc in all_junction_list}

        # # for JuncID in env.junction_waiting_histograms.keys():
        # #     env.junction_waiting_histograms[JuncID] = []
        
        # env.junction_vehicle_history = {junc: set() for junc in all_junction_list}

        # for junc_id in env.junction_traffic_counts:
        #     env.junction_traffic_counts[junc_id] = 0  # 重置每个路口的车流量

        # episode.hist_data = {}

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
        for JuncID in worker.env.previous_global_waiting.keys():
            total_wait += worker.env.previous_global_waiting[JuncID]['sum']
        episode.user_data["avg_wait"].extend([total_wait])

        # 当前JuncID的所有方向Keyword上的所有在control zone之内的车辆的等待时间的平均值
        for JuncID in worker.env.all_previous_global_waiting.keys():
            waiting_time = worker.env.all_previous_global_waiting[JuncID]['sum']
            metric_name = f"avg_wait_{JuncID}"
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
        #增加计数器
        self.episode_count += 1

        # 获取当前系统时间，仅小时和分钟
        # current_time = datetime.now().strftime("%H:%M")
        # 获取当前线程 ID 和系统时间
        thread_id = threading.get_ident()  # 获取线程 ID
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")  # 系统时间，精确到秒

        # global_episode_count = increment_episode_count()

        episode.custom_metrics["conflict_rate"] = np.mean(episode.user_data["conflict_rate"])
        episode.custom_metrics["avg_wait"] = np.mean(episode.user_data["avg_wait"])

        total_departed = worker.env.total_departed_count
        total_arrived = worker.env.total_arrived_count

        episode.custom_metrics["episode_departed"] = total_departed
        episode.custom_metrics["episode_arrived"] = total_arrived

        # 记录每个路口的平均等待时间
        for JuncID in all_junction_list:
            metric_name = f"avg_wait_{JuncID}"  # 自定义每个路口的metric名称
            episode.custom_metrics[metric_name] = np.mean(episode.user_data[metric_name])

        # 创建一个字典，用于存储每个路口的等待时间
        junction_waiting_times = {junc: [] for junc in all_junction_list}

        # 从 veh_waiting_juncs 中提取等待时间
        for _, junctions in worker.env.veh_waiting_juncs.items():
            for JuncID, waiting_time in junctions.items():
                junction_waiting_times[JuncID].append(waiting_time)

        # # 存储到tensorboard的histogram中
        # for JuncID, waiting_times in junction_waiting_times.items():
        #     histogram, bins = np.histogram(waiting_times, bins=20, range=(0, 1000))
        #     metric_name = f"WTH_{JuncID}"
        #     episode.hist_data[metric_name] = (bins[:-1].tolist(), histogram.tolist())

        # for JuncID in worker.env.junction_waiting_histograms.keys():
        #     metric_name = f"WT_{JuncID}"
        #     # 确保数据是数值类型，且范围合理
        #     histogram, bins = np.histogram(
        #         worker.env.junction_waiting_histograms[JuncID], bins=20, range=(0, 1000)
        #     )
        #     episode.hist_data[metric_name] = (bins[:-1].tolist(), histogram.tolist())
        #     print(f"Junction {JuncID} waiting times: {worker.env.junction_waiting_histograms[JuncID]}")

        # 遍历所有路口
        # for JuncID, waiting_times in junction_waiting_times.items():
        #     # 计算直方图数据
        #     histogram, _ = np.histogram(
        #         waiting_times, bins=20, range=(0, 1000)
        #     )

        #     # 自定义 metric name，包含时间戳和路口 ID
        #     metric_name = f"WTH_{JuncID}_{current_time}"

        #     # 将 counts 数据存储到 custom metrics
        #     episode.custom_metrics[metric_name] = histogram.tolist()

        # 定义保存文件的路径
        # base_directory = "C:\\Users\\sliu78\\ray_results\\DQN_RV0.2\\histograms"
        # base_directory = "C:\\Users\\cgchr\\ray_results\\DQN_RV0.2\\histograms"
        # save_directory = os.path.join(base_directory, f"episode_{self.episode_count:04d}_thread_{thread_id}_{timestamp}")
        # # save_directory = os.path.join(base_directory, f"episode_{self.episode_count:04d}")

        # if not os.path.exists(save_directory):
        #     os.makedirs(save_directory)

        # # 每个路口动态更新直方图
        # for JuncID, waiting_times in junction_waiting_times.items():
        #     histogram, bins = np.histogram(waiting_times, bins=20, range=(0, 1000))
        #     # 保存直方图数据为 .npy 文件
        #     npy_file = os.path.join(save_directory, f"junction_{JuncID}_episode_{self.episode_count:04d}_thread_{thread_id}.npy")
        #     np.save(npy_file, {"bins": bins, "counts": histogram})
        #     print(f"Saved histogram data for Junction {JuncID} to {npy_file}")

        #     # 绘制直方图
        #     plt.figure()
        #     plt.hist(waiting_times, bins=20, range=(0, 1000), alpha=0.7, color='blue')
        #     plt.title(f"Waiting Time Distribution at Junction \n{JuncID} \n(Episode {self.episode_count:04d})")
        #     plt.xlabel("Waiting Time (s)")
        #     plt.ylabel("Vehicle Count")
        #     plt.grid(True)

        #     # 保存直方图到磁盘，以路口ID和Episode为命名
        #     file_name = os.path.join(save_directory, f"junction_{JuncID}_episode_{self.episode_count:04d}_thread_{thread_id}.jpg")
        #     plt.savefig(file_name, format='jpg')
        #     print(f"Saved histogram for Junction {JuncID} to {file_name}")
        #     plt.close()  # 关闭图表，防止内存泄漏

        # # 每个路口动态更新直方图
        # for JuncID, waiting_times in junction_waiting_times.items():
        #     # 绘制直方图
        #     plt.figure()
        #     plt.hist(waiting_times, bins=20, range=(0, 1000), alpha=0.7, color='blue')
        #     plt.title(f"Waiting Time Distribution at Junction \n{JuncID} \n(Episode {self.episode_count:04d})")
        #     plt.xlabel("Waiting Time (s)")
        #     plt.ylabel("Vehicle Count")
        #     plt.grid(True)

        #     # 保存直方图到磁盘，以路口ID和Episode为命名
        #     file_name = os.path.join(save_directory, f"junction_{JuncID}_episode_{self.episode_count:04d}.jpg")
        #     plt.savefig(file_name, format='jpg')
        #     # print(f"Saved histogram for Junction {JuncID} to {file_name}")
        #     plt.close()  # 关闭图表，防止内存泄漏

        # for JuncID in worker.env.junction_waiting_histograms.keys():
        #     # 添加直方图数据
        #     metric_name = f"WT_{JuncID}"
        #     histogram, _ = np.histogram(
        #     worker.env.junction_waiting_histograms[JuncID], bins=20, range=(0, 1000)
        #     )
        #     episode.custom_metrics[metric_name] = histogram.tolist()  # 转换为列表记录
            # episode.custom_metrics[metric_name] = np.histogram(
            #     worker.env.junction_waiting_histograms[JuncID], bins=10
            # )[0].tolist()  # 将直方图转换为可记录的列表

        # 将路口流量数据存储为 histogram custom metric
        # for junc_id, count in worker.env.junction_traffic_counts.items():
        #     episode.custom_metrics[f"throughput_{junc_id}"] = count

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
