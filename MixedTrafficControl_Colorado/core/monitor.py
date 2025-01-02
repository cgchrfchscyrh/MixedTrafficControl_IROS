import numpy as np
import pickle

## For colorado.net.xml without roundabouts/one-way streets
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

class DataMonitor(object):
    def __init__(self, env) -> None:
        # self.junction_list = env.junction_list
        self.junction_list = all_junction_list
        self.keywords_order = env.keywords_order
        self.clear_data()

    def clear_data(self):
        self.conduct_traj_recorder()
        self.conduct_data_recorder()

    def conduct_traj_recorder(self):
        self.traj_record = dict()
        for JuncID in self.junction_list:
            self.traj_record[JuncID] = dict()
            for Keyword in self.keywords_order:
                self.traj_record[JuncID][Keyword] = dict()
        self.max_t = 0
        self.max_x = 0

    def conduct_data_recorder(self):
        self.data_record = dict()
        self.conflict_rate = []
        initial_size = 5000  # 5000 --> 10000 初始化更大的数组
        for JuncID in self.junction_list:
            self.data_record[JuncID] = dict()
            for Keyword in self.keywords_order :
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
        for JuncID in self.junction_list:
            for Keyword in self.keywords_order:
                self.data_record[JuncID][Keyword]['queue_length'][t] = env.get_queue_len(JuncID, Keyword, 'all')
                self.data_record[JuncID][Keyword]['queue_wait'][t] = env.get_avg_wait_time(JuncID, Keyword, 'all')
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

    def evaluate(self, min_step=500, max_step=1000):
        # 初始化统计变量
        total_wait = []  # 所有车辆的等待时间
        total_arrivals = 0  # 到达目的地的总车辆数
        intersection_throughput = {}  # 每个路口的车流量统计

        # 初始化每个路口的统计数据
        for JuncID in self.junction_list:
            intersection_throughput[JuncID] = 0

        # 遍历每个路口并统计数据
        for JuncID in self.junction_list:
            junction_wait = []  # 当前路口的等待时间

            for keyword in self.keywords_order:
                # 计算当前路口和方向的平均等待时间
                avg_wait = np.mean(self.data_record[JuncID][keyword]['queue_wait'][min_step:max_step])
                junction_wait.append(avg_wait)

                # 累加车流量
                throughput = sum(self.data_record[JuncID][keyword]['throughput'][min_step:max_step])
                intersection_throughput[JuncID] += throughput

                # 打印每个方向的等待时间
                print(f"Avg waiting time at {JuncID} {keyword}: {avg_wait:.2f}")

            # 累计所有路口的总数据
            total_wait.extend(junction_wait)

            # 打印当前路口的总平均等待时间
            print(f"Total avg wait time at junction {JuncID}: {np.mean(junction_wait):.2f}")

        # 统计总到达车辆数量
        total_arrivals = sum(intersection_throughput.values())

        # 打印整个网络的统计结果
        print("\n--- Network Statistics ---")
        print(f"Total Avg Wait Time: {np.mean(total_wait):.2f}")
        print(f"Total Arrivals: {total_arrivals}")

        # 打印每个路口的车流量
        print("\n--- Per Intersection Throughput ---")
        for JuncID, throughput in intersection_throughput.items():
            print(f"Intersection {JuncID} - Traffic Throughput: {throughput}")

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
