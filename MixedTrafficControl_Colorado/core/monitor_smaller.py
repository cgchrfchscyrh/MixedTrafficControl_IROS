import numpy as np
import pickle, os
import matplotlib.pyplot as plt

## For colorado.net.xml without roundabouts/one-way streets
all_junction_list = ['cluster12203246695_12203246696_430572036_442436239', 
                       'cluster_547498658_547498666_547498756_547498762_#8more', 

                       'cluster_2052409422_2052409707_542824247_542824770_#2more',
                       'cluster_2052409323_2052409733_2052409806_2052409936_#9more',

                       'cluster_2093101229_2093101656_2093101781_2093101915_#8more',
                       'cluster9663732079_J0_J1_J2_#2more',

                       'cluster_439980117_439980118_442435910_442435912',
                       'cluster_1289585639_439979990_8156136067_8156136068_#1more']

class DataMonitor(object):
    def __init__(self, env) -> None:
        self.junction_list = env.junction_list
        self.keywords_order = env.keywords_order
        # self.veh_waiting_juncs = env.veh_waiting_juncs
        # self.all_previous_global_waiting = env.all_previous_global_waiting
        # self.total_arrived_count = env.total_arrived_count
        # self.junction_traffic_counts = env.junction_traffic_counts
        self.clear_data()

    def clear_data(self):
        self.conduct_traj_recorder()
        self.conduct_data_recorder()

    def conduct_traj_recorder(self):
        self.traj_record = dict()
        # for JuncID in self.junction_list:
        for JuncID in all_junction_list:
            self.traj_record[JuncID] = dict()
            for Keyword in self.keywords_order:
                self.traj_record[JuncID][Keyword] = dict()
        self.max_t = 0
        self.max_x = 0

    def conduct_data_recorder(self):
        self.data_record = dict()
        self.conflict_rate = []
        initial_size = 5000

        for JuncID in all_junction_list:
            self.data_record[JuncID] = dict()
            for Keyword in self.keywords_order:
                self.data_record[JuncID][Keyword] = dict()
                self.data_record[JuncID][Keyword]['queue_wait'] = np.zeros(initial_size)
                self.data_record[JuncID][Keyword]['queue_length'] = np.zeros(initial_size)

        for JuncID in self.junction_list:
            self.data_record[JuncID] = dict()
            for Keyword in self.keywords_order:
                self.data_record[JuncID][Keyword] = dict()
                self.data_record[JuncID][Keyword]['t'] = [i for i in range(initial_size)]
                self.data_record[JuncID][Keyword]['queue_wait'] = np.zeros(initial_size)
                self.data_record[JuncID][Keyword]['queue_length'] = np.zeros(initial_size)
                self.data_record[JuncID][Keyword]['control_queue_wait'] = np.zeros(initial_size)
                self.data_record[JuncID][Keyword]['control_queue_length'] = np.zeros(initial_size)
                self.data_record[JuncID][Keyword]['throughput_av'] = np.zeros(initial_size)
                self.data_record[JuncID][Keyword]['throughput'] = np.zeros(initial_size)
                self.data_record[JuncID][Keyword]['throughput_hv'] = np.zeros(initial_size)
                self.data_record[JuncID][Keyword]['conflict'] = np.zeros(initial_size)
                self.data_record[JuncID][Keyword]['global_reward'] = np.zeros(initial_size)

    def step(self, env):
        t = env.env_step

        for JuncID in all_junction_list:
            for Keyword in self.keywords_order:
                self.data_record[JuncID][Keyword]['queue_length'][t] = env.get_queue_len(JuncID, Keyword, 'all')
                self.data_record[JuncID][Keyword]['queue_wait'][t] = env.get_avg_wait_time(JuncID, Keyword, 'all')

        for JuncID in self.junction_list:
            for Keyword in self.keywords_order:
                # self.data_record[JuncID][Keyword]['queue_length'][t] = env.get_queue_len(JuncID, Keyword, 'all')
                # self.data_record[JuncID][Keyword]['queue_wait'][t] = env.get_avg_wait_time(JuncID, Keyword, 'all')
                self.data_record[JuncID][Keyword]['control_queue_length'][t] = env.get_queue_len(JuncID, Keyword, 'rv')
                self.data_record[JuncID][Keyword]['control_queue_wait'][t] = env.get_avg_wait_time(JuncID, Keyword, 'rv')
                self.data_record[JuncID][Keyword]['throughput'][t] = len(env.inner_lane_newly_enter[JuncID][Keyword])
                self.data_record[JuncID][Keyword]['conflict'][t] = len(env.conflict_vehids)
                self.data_record[JuncID][Keyword]['global_reward'][t] = env.global_obs[JuncID]
        self.conflict_rate.extend(
            [len(env.conflict_vehids)/len(env.previous_action) if len(env.previous_action) else 0]
            )

    # def evaluate(self, min_step = 500, max_step = 1000):
    #     total_wait = []
    #     for JuncID in self.junction_list:
    #         for keyword in self.keywords_order:
    #             avg_wait = np.mean(self.data_record[JuncID][keyword]['queue_wait'][min_step:max_step])
    #             total_wait.extend([avg_wait])
    #             print("Avg waiting time at" + JuncID +" "+keyword+": "+str(avg_wait))
    #         print("Total avg wait time at junction "+JuncID+": " +str(np.mean(total_wait)))

    # def evaluate(self, env, min_step=500, max_step=1000):
    #     # 初始化统计变量
    #     total_wait = []  # 所有车辆的等待时间

    #     # 创建一个字典，用于存储每个路口的等待时间
    #     junction_waiting_times = {junc: [] for junc in all_junction_list}

    #     # 从 veh_waiting_juncs 中提取等待时间
    #     for _, junctions in env.veh_waiting_juncs.items():
    #         for JuncID, waiting_time in junctions.items():
    #             junction_waiting_times[JuncID].append(waiting_time)

    #     # 当前JuncID的所有方向Keyword上的所有在control zone之内的车辆的等待时间的平均值
    #     # for JuncID in self.all_previous_global_waiting.keys():
    #     #     waiting_time = self.all_previous_global_waiting[JuncID]['sum']
    #     #     metric_name = f"avg_wait_{JuncID}"
    #     #     episode.user_data[metric_name].extend([waiting_time])

    #     # 遍历每个路口并统计数据
    #     for JuncID in all_junction_list:
    #         junction_wait = []  # 当前路口的等待时间
    #         for keyword in self.keywords_order:
    #             # 计算当前路口和方向的平均等待时间
    #             avg_wait = np.mean(self.data_record[JuncID][keyword]['queue_wait'][min_step:max_step])
    #             junction_wait.append(avg_wait)

    #             # 打印每个方向的等待时间
    #             # print(f"Avg waiting time at {JuncID} {keyword}: {avg_wait:.2f}")

    #         # 累计所有路口的总数据
    #         total_wait.extend(junction_wait)

    #         # 2. 打印当前路口的总平均等待时间
    #         print(f"Total avg wait time at junction {JuncID}: {np.mean(junction_wait):.2f}\n")

    #     # 打印整个网络的统计结果
    #     print("\n--- Network statistics ---")
    #     # 1. 打印所有路口的平均等待时间
    #     print(f"Total Avg Wait Time: {np.mean(total_wait):.2f}")

    #     # 2.5 每个路口的直方图，不受min_step和max_step限制，只要是在路口有过等待时间的车辆都会被计算
    #     for JuncID, waiting_times in junction_waiting_times.items():
    #         plt.figure()
    #         plt.hist(waiting_times, bins=20, range=(0, 1000), alpha=0.7, color='blue')
    #         plt.title(f"Waiting Time Histogram \n{JuncID}")
    #         plt.xlabel("Waiting Time (s)")
    #         plt.ylabel("Vehicle Count")
    #         plt.grid(True)

    #         # 保存直方图到磁盘，以路口ID为命名
    #         file_name = os.path.join(f"WTH_{JuncID}.jpg")
    #         plt.savefig(file_name, format='jpg')
    #         print(f"Saved histogram for Junction {JuncID} to {file_name}")
    #         plt.close()  # 关闭图表，防止内存泄漏

    #     # 3. 打印到达目的地的车辆数量
    #     print(f"Total Arrivals: {env.total_arrived_count}")

    #     # 4. 打印每个路口的车流量
    #     print("\n--- Per junction throughput ---")
    #     for junc_id, count in env.junction_traffic_counts.items():
    #         print(f"{junc_id} - Throughput: {count}")

    #     return np.mean(total_wait), env.total_arrived_count
    
    def evaluate(self, env, min_step=500, max_step=1000):
        # 初始化统计变量
        total_wait = []  # 所有车辆的等待时间

        # 创建一个字典，用于存储每个路口的等待时间
        junction_waiting_times = {junc: [] for junc in all_junction_list}

        # 从 veh_waiting_juncs 中提取等待时间
        for _, junctions in env.veh_waiting_juncs.items():
            for JuncID, waiting_time in junctions.items():
                junction_waiting_times[JuncID].append(waiting_time)

        # 存储每个路口的平均等待时间和车流量
        per_junction_avg_wait = {}
        per_junction_throughput = {}

        # 遍历每个路口并统计数据
        for JuncID in all_junction_list:
            junction_wait = []  # 当前路口的等待时间
            for keyword in self.keywords_order:
                # 计算当前路口和方向的平均等待时间
                avg_wait = np.mean(self.data_record[JuncID][keyword]['queue_wait'][min_step:max_step])
                junction_wait.append(avg_wait)

            # 累计所有路口的总数据
            total_wait.extend(junction_wait)

            # 记录当前路口的平均等待时间
            per_junction_avg_wait[JuncID] = np.mean(junction_wait)

            # 打印当前路口的总平均等待时间
            print(f"Total avg wait time at junction {JuncID}: {per_junction_avg_wait[JuncID]:.2f}")

        # 打印整个网络的统计结果
        print("\n--- Network statistics ---")
        print(f"Total Avg Wait Time: {np.mean(total_wait):.2f}")

        # 每个路口的直方图，不受 min_step 和 max_step 限制
        for JuncID, waiting_times in junction_waiting_times.items():
            plt.figure()
            plt.hist(waiting_times, bins=20, range=(0, 1000), alpha=0.7, color='blue')
            plt.title(f"Waiting Time Histogram \n{JuncID}")
            plt.xlabel("Waiting Time (s)")
            plt.ylabel("Vehicle Count")
            plt.grid(True)

            # 保存直方图到磁盘，以路口ID为命名
            file_name = os.path.join(f"WTH_{JuncID}.jpg")
            plt.savefig(file_name, format='jpg')
            print(f"Saved histogram for Junction {JuncID} to {file_name}")
            plt.close()  # 关闭图表，防止内存泄漏

        # 打印到达目的地的车辆数量
        print(f"Total Arrivals: {env.total_arrived_count}")

        # 打印每个路口的车流量
        print("\n--- Per junction throughput ---")
        for junc_id, count in env.junction_traffic_counts.items():
            per_junction_throughput[junc_id] = count
            print(f"{junc_id} - Throughput: {count}")

        # 返回所有统计数据
        return (
            np.mean(total_wait),  # 整个网络的平均等待时间
            env.total_arrived_count,  # 到达目的地的车辆数量
            per_junction_avg_wait,  # 每个路口的平均等待时间
            per_junction_throughput,  # 每个路口的车流量
        )

    def eval_traffic_flow(self, JuncID, time_range):
        inflow_intersection = []
        for t in range(time_range[0], time_range[1]):
            inflow_intersection.extend([0])
            for Keyword in self.keywords_order:
                 inflow_intersection[-1] += self.data_record[JuncID][Keyword]['throughput'][t]
        return inflow_intersection, max(inflow_intersection), sum(inflow_intersection)/len(inflow_intersection)

    def save_to_pickle(self, file_name):
        saved_dict = {'data_record':self.data_record, 'junctions':self.junction_list, 'keyword':self.keywords_order}
        with open(file_name, "wb") as f:
            pickle.dump(saved_dict, f)
