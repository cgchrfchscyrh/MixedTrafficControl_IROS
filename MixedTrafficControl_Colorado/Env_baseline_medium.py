from typing import Set
from ray.rllib.utils.typing import AgentID #type:ignore
from core.sumo_interface import SUMO
from core.costomized_data_structures import Vehicle, Container
from core.NetMap import NetMap
import numpy as np #type:ignore
import random, math, traci
# from gym.spaces.box import Box #type:ignore
from gymnasium.spaces.box import Box #type:ignore

from ray.rllib.env.multi_agent_env import MultiAgentEnv #type:ignore
from copy import deepcopy
from core.utils import start_edges, end_edges, dict_tolist, UNCONFLICT_SET
from gymnasium.spaces import Discrete #type:ignore
from core.monitor_medium import DataMonitor #type:ignore

WHITE = (255, 255, 255)
CYAN = (0, 255, 255)
RED = (255, 0, 0)
EPSILON = 0.00001

all_junction_list = ['cluster12203246695_12203246696_430572036_442436239', 
                       'cluster_547498658_547498666_547498756_547498762_#8more', 

                       'cluster_2052409422_2052409707_542824247_542824770_#2more',
                       'cluster_2052409323_2052409733_2052409806_2052409936_#9more',

                       'cluster_2093101229_2093101656_2093101781_2093101915_#8more',
                       'cluster9663732079_J0_J1_J2_#2more',

                       'cluster_439980117_439980118_442435910_442435912',
                       'cluster_1289585639_439979990_8156136067_8156136068_#1more',
                       
                       'cluster_2052409830_2052409981_9356276530_9356276531',
                       'cluster_2052409270_2052409892_2052410135_2052410161_#8more',
                       
                       'cluster_2040873690_2040873694_2040873705_2040873709_#8more',
                       'cluster428692206_428692253_9650210478_9650210479_#2more',
                       'cluster_1334947864_1334947865_1334947879_1334947882',
                       'cluster_2048655723_2048656743_2048656762_2048657045_#8more']

class Env(MultiAgentEnv):
    def __init__(self, config) -> None:
        ## TODO: use config to pass parameters

        super().__init__()
        self.config = config
        self.print_debug = True
        self.cfg = config['cfg']
        self.map_xml = config['map_xml']
        self.keywords_order = ['topstraight', 'topleft','rightstraight', 'rightleft','bottomstraight', 'bottomleft', 'leftstraight', 'leftleft']
        self._max_episode_steps = 10000000 ## unlimited simulation horizon   
        if 'max_episode_steps' in config.keys():
            self._max_episode_steps = self.config['max_episode_steps']
        self.traffic_light_program = self.config['traffic_light_program']

        self.junction_list = self.config['junction_list']
        self.sumo_interface = SUMO(self.cfg, render=self.config['render'])

        self.map = NetMap(self.map_xml, all_junction_list)
        # self.map = NetMap(self.map_xml, self.junction_list)

        self.spawn_rl_prob = config['spawn_rl_prob']
        self.default_rl_prob = config['probablity_RL']
        self.rl_prob_list = config['rl_prob_range'] if 'rl_prob_range' in config.keys() else None

        # self.start_edges = start_edges
        # self.end_edges = end_edges

        self.max_acc = 100
        self.min_acc = -100
        self.control_distance = 30
        self.control_zone_length = 100
        self.max_wait_time = 200
        self.vehicle_len = 5.0

        self.total_departed_count  = 0  # 记录进入网络的车辆数
        self.total_arrived_count = 0  # 记录离开网络的车辆数
        # self.traffic_flow_history = []  # 用于记录历史的车流量数据
        
        #新增，记录每个路口按方向的等待时间分布
        # self.all_waiting_time_histograms = {JuncID: {kw: [] for kw in self.keywords_order} for JuncID in all_junction_list}

        # self.junction_waiting_histograms = {junc: [] for junc in all_junction_list}

        # self.junction_traffic_throughput = {JuncID: 0 for JuncID in all_junction_list}
        # self.all_junction_incoming_edges = {}  # 存储每个路口的入边
        # self.all_junction_outgoing_edges = {}  # 存储每个路口的出边
        # self.all_junction_outgoing_edges['cluster12203246695_12203246696_430572036_442436239'] = ['1318569361#0',  '1318569361#1', '1318565916#0', '1318565916#1', '978613917#0', '978613917#1', '1318569357']
        # self.all_junction_outgoing_edges['cluster_2052409422_2052409707_542824247_542824770_#2more'] = ['978615348#0',  '978615345#1', '978615347#1', '38520914#0']
        # self.all_junction_outgoing_edges['cluster_2093101229_2093101656_2093101781_2093101915_#8more'] = ['229489592#2',  '223369741#1', '229489595#2', '223369742#1']
        # self.all_junction_outgoing_edges['cluster_439980117_439980118_442435910_442435912'] = ['229489602#1',  '436475433#5', '229489593#1', '37552734#10']

        self.all_junction_outgoing_edges = {
            'cluster12203246695_12203246696_430572036_442436239': ['1318569361#0', '1318569361#1', '1318565916#0', '1318565916#1', '978613917#0', '978613917#1', '1318569357'],
            'cluster_2052409422_2052409707_542824247_542824770_#2more': ['978615348#0', '978615345#1', '978615347#1', '38520914#0'],
            'cluster_2093101229_2093101656_2093101781_2093101915_#8more': ['229489592#2', '223369741#1', '229489595#2', '223369742#1'],
            'cluster_439980117_439980118_442435910_442435912': ['229489602#1', '436475433#5', '229489593#1', '37552734#10'],
            'cluster_547498658_547498666_547498756_547498762_#8more':['43417383#22','229357868#1','892145086#1','1318568287#2'],
            'cluster_2052409323_2052409733_2052409806_2052409936_#9more':['43417383#2','39829020#2','877763367#1','877763350#2'],
            'cluster9663732079_J0_J1_J2_#2more':['858377714#6','223369741#12','-858377714#2','36870636#13'],
            'cluster_1289585639_439979990_8156136067_8156136068_#1more':['858378009#3','436475433#12','-858378009#0','37552734#2'],
            'cluster_2052409830_2052409981_9356276530_9356276531':['894433359#1','193565552#1','597941702#1'],
            'cluster_2052409270_2052409892_2052410135_2052410161_#8more':['39829020#7','194732292#5','877763348#5'],
            'cluster_2040873690_2040873694_2040873705_2040873709_#8more':['193565557#2','847829715#1','193565552#18','39829697#7'],
            'cluster428692206_428692253_9650210478_9650210479_#2more':['194732247#1','223369741#16','36870636#3'],
            'cluster_1334947864_1334947865_1334947879_1334947882':['892137985#3','37693888#5','193565552#27','118756783#9'],
            'cluster_2048655723_2048656743_2048656762_2048657045_#8more':['223369752#7','37657919#6','833739973#4','37657924#14']
        }

        self.incoming_traffic_counts = {junc: 0 for junc in all_junction_list}
        self.outgoing_traffic_counts = {junc: 0 for junc in all_junction_list}

        self.incoming_vehicle_history = {junc: set() for junc in all_junction_list}
        self.outgoing_vehicle_history = {junc: set() for junc in all_junction_list}

        # self.junction_vehicle_types = {junc_id: {'RL': 0, 'IDM': 0} for junc_id in self.junction_list}
        self.incoming_vehicle_types = {junc_id: {"RL": 0, "IDM": 0} for junc_id in all_junction_list}
        self.outgoing_vehicle_types = {junc_id: {"RL": 0, "IDM": 0} for junc_id in all_junction_list}

        self.vehicle_path_data = {}
        self.vehicle_lane_stats = {
            junc_id: {}  # 每个路口一个字典，用于记录车辆的 origin 和 destination lane
            for junc_id in all_junction_list
        }

        self.init_env()
        self.previous_global_waiting = dict()
        self.all_previous_global_waiting = dict()
        self.global_obs = dict()

        # # 初始化每个路口的 incoming 和 outgoing edges，但排除掉以 ":" 开头的内部 ID
        # for junc_id in self.junction_list:
        #     # 获取并过滤 incoming edges
        #     all_incoming = traci.junction.getIncomingEdges(junc_id)
        #     # facing_junction_id = self.map.get_facing_intersection(veh.road_id)
        #     self.all_junction_incoming_edges[junc_id] = [edge for edge in all_incoming if not edge.startswith(":")]

        #     # 获取并过滤 outgoing edges
        #     all_outgoing = traci.junction.getOutgoingEdges(junc_id)
        #     self.all_junction_outgoing_edges[junc_id] = [edge for edge in all_outgoing if not edge.startswith(":")]

        # 初始化每个 edge 的车辆历史
        # for junc_id, outgoing_edges in self.all_junction_outgoing_edges.items():
        #     for edge_id in outgoing_edges:
        #         self.vehicle_history[edge_id] = set()  # 每个边一个独立的 set
        # print("incoming edges: ", self.all_junction_incoming_edges)
        print("outgoing edges: ", self.all_junction_outgoing_edges)

        for JuncID in all_junction_list:
            self.all_previous_global_waiting[JuncID] = dict()
            for keyword in self.keywords_order:
                self.all_previous_global_waiting[JuncID][keyword] = 0
                self.all_previous_global_waiting[JuncID]['sum'] = 0
        
        for JuncID in self.junction_list:
            self.previous_global_waiting[JuncID] = dict() # 与global reward和conflict mechanism相关
            self.global_obs[JuncID] = 0 # global_obs实际上即为global reward的值，但paper中并未采用global reward，只用了ego_reward
            for keyword in self.keywords_order:
                self.previous_global_waiting[JuncID][keyword] = 0
                self.previous_global_waiting[JuncID]['sum'] = 0
        
        ## off, standard, flexible
        if 'conflict_mechanism' in config:
            self.conflict_resolve_mechanism_type = config['conflict_mechanism']
        else:
            self.conflict_resolve_mechanism_type = 'off'

        ## ego_only, wait_only, PN_ego
        # self.reward_mode = 'ego_only'
        # self.reward_mode = 'PN_ego'
        # self.reward_mode = 'wait_only'
        self.observation_space = Box(
            low=-1,
            high=1,
            shape=(self.n_obs, ),
            dtype=np.float32)
        
    @property
    def n_obs(self):
        ## TODO defination of obs
        return 80+16
    
    @property
    def action_space(self):
        return Discrete(2)
    
    @property
    def env_step(self):
        return self._step

    def _print_debug(self, fun_str):
        if self.print_debug:
            print('exec: '+fun_str+' at time step: '+str(self._step))

    def get_agent_ids(self) -> Set[AgentID]:
        rl_veh_ids = []
        for veh in self.rl_vehicles:
            rl_veh_ids.extend([veh.id])
        return set(rl_veh_ids)
    
    def update_traffic_flow(self):
        """
        在每个时间步调用，分别更新到达路口和经过路口的车流量，同时记录车辆的 origin 和 destination lane
        """

        # 获取当前所有车辆 ID
        all_vehicle_ids = traci.vehicle.getIDList()

        for veh_id in all_vehicle_ids:
            current_lane_id = traci.vehicle.getLaneID(veh_id)  # 获取车辆当前的 lane ID
            veh_edge_id = traci.vehicle.getRoadID(veh_id)  # 获取车辆当前的 edge ID
            facing_junction_id = self.map.get_facing_intersection(veh_edge_id)  # 计算车辆将到达的 junction ID

            # 检查 facing_junction_id 是否在 junction_list 中
            if not facing_junction_id or facing_junction_id not in self.junction_list:
                continue  # 如果不在 junction_list 中，跳过该车辆

            # 初始化该 junction 的数据结构
            if facing_junction_id not in self.vehicle_lane_stats:
                self.vehicle_lane_stats[facing_junction_id] = {}
            if facing_junction_id not in self.incoming_vehicle_history:
                self.incoming_vehicle_history[facing_junction_id] = set()
            if facing_junction_id not in self.incoming_traffic_counts:
                self.incoming_traffic_counts[facing_junction_id] = 0
            if facing_junction_id not in self.incoming_vehicle_types:
                self.incoming_vehicle_types[facing_junction_id] = {"RL": 0, "IDM": 0}

            # 初始化该车辆的统计数据
            if veh_id not in self.vehicle_lane_stats[facing_junction_id]:
                self.vehicle_lane_stats[facing_junction_id][veh_id] = {"origin": None, "destination": None}

            # 如果 origin 尚未记录，设置为当前 lane
            if self.vehicle_lane_stats[facing_junction_id][veh_id]["origin"] is None:
                self.vehicle_lane_stats[facing_junction_id][veh_id]["origin"] = current_lane_id

            # 如果车辆尚未被统计，记录到达路口信息
            if veh_id not in self.incoming_vehicle_history[facing_junction_id]:
                self.incoming_vehicle_history[facing_junction_id].add(veh_id)
                self.incoming_traffic_counts[facing_junction_id] += 1

                # 获取车辆类型
                vehicle_type = self.vehicles[veh_id].type if veh_id in self.vehicles else "Unknown"
                if vehicle_type in self.incoming_vehicle_types[facing_junction_id]:
                    self.incoming_vehicle_types[facing_junction_id][vehicle_type] += 1
                else:
                    self.incoming_vehicle_types[facing_junction_id][vehicle_type] = 1

        # # 遍历所有路口的incoming edges
        # for junc_id, incoming_edges in self.all_junction_incoming_edges.items():
        #     for edge_id in incoming_edges:
        #         # 获取当前边上的车辆 ID
        #         vehicle_ids = traci.edge.getLastStepVehicleIDs(edge_id)
        #         for veh_id in vehicle_ids:
        #             current_lane_id = traci.vehicle.getLaneID(veh_id)
        #             veh_edge_id = traci.vehicle.getRoadID(veh_id)
        #             facing_junction_id = self.map.get_facing_intersection(veh_edge_id)

        #             # 如果车辆尚未记录 origin
        #             if veh_id not in self.vehicle_lane_stats[junc_id]:
        #                 self.vehicle_lane_stats[junc_id][veh_id] = {"origin": None, "destination": None}
        #             # 如果 origin 尚未记录，设置为当前 lane
        #             if self.vehicle_lane_stats[junc_id][veh_id]["origin"] is None:
        #                 self.vehicle_lane_stats[junc_id][veh_id]["origin"] = current_lane_id
                    
        #             # 如果车辆尚未被统计，记录到达路口信息
        #             if veh_id not in self.incoming_vehicle_history[junc_id]:
        #                 self.incoming_vehicle_history[junc_id].add(veh_id)
        #                 self.incoming_traffic_counts[junc_id] += 1

        #                 # 获取车辆类型
        #                 self.incoming_vehicle_types[junc_id][self.vehicles[veh_id].type] += 1

        # 遍历所有路口的outgoing edges
        for junc_id, outgoing_edges in self.all_junction_outgoing_edges.items():
            for edge_id in outgoing_edges:
                # 获取当前边上的车辆 ID
                vehicle_ids = traci.edge.getLastStepVehicleIDs(edge_id)
                for veh_id in vehicle_ids:
                    # 如果车辆尚未被统计，记录到达路口信息
                    if veh_id not in self.outgoing_vehicle_history[junc_id]:
                        self.outgoing_vehicle_history[junc_id].add(veh_id)
                        self.outgoing_traffic_counts[junc_id] += 1

                        # 获取车辆类型
                        self.outgoing_vehicle_types[junc_id][self.vehicles[veh_id].type] += 1

                    current_lane_id = traci.vehicle.getLaneID(veh_id)

                    if veh_id not in self.vehicle_lane_stats[junc_id]:
                        # 如果 veh_id 未被记录，初始化其数据
                        self.vehicle_lane_stats[junc_id][veh_id] = {"origin": None, "destination": None}

                    # 设置 destination 为当前 lane
                    self.vehicle_lane_stats[junc_id][veh_id]["destination"] = current_lane_id

                    # 检查并补全 origin
                    if self.vehicle_lane_stats[junc_id][veh_id]["origin"] is None:
                        # 查询车辆的完整 route
                        route = traci.vehicle.getRoute(veh_id)
                        
                        # 查找当前 edge 在 route 中的位置
                        if edge_id in route:
                            current_index = route.index(edge_id)
                            if current_index > 0:  # 确保有前一个 edge
                                # 将前一个 edge 记录为 origin
                                prev_edge = route[current_index - 1]
                                self.vehicle_lane_stats[junc_id][veh_id]["origin"] = prev_edge

                        if veh_id not in self.incoming_vehicle_history[junc_id]:
                            self.incoming_vehicle_history[junc_id].add(veh_id)
                            self.incoming_traffic_counts[junc_id] += 1

                            # 获取车辆类型
                            self.incoming_vehicle_types[junc_id][self.vehicles[veh_id].type] += 1

    # def update_vehicle_path_data(self):
    #     """
    #     记录每辆车当前所在的路段和车道，并分类为 incoming edges 或 outgoing edges
    #     仅在车辆位于控制路口的相关边时保存数据。
    #     """
    #     # 获取当前所有车辆的ID
    #     vehicle_ids = traci.vehicle.getIDList()

    #     # 遍历每一辆车
    #     for veh_id in vehicle_ids:
    #         # 获取车辆当前所在的边和车道
    #         current_edge_id = traci.vehicle.getRoadID(veh_id)
    #         current_lane_id = traci.vehicle.getLaneID(veh_id)

    #         facing_junction_id = self.map.get_facing_intersection(current_edge_id)
    #         # current_time = traci.simulation.getTime()  # 获取当前时间步
    #         # # print(f"Current timestep: {current_time}")  # 打印当前时间步
    #         # if veh_id == "13":
    #         #     print("13: ", current_time, current_edge_id)
                
    #         # 如果当前边不属于任何控制路口的 incoming 或 outgoing edges，跳过
    #         is_control_edge = False
    #         for junc_id in self.junction_list:
    #             if (current_edge_id in self.all_junction_incoming_edges[junc_id] or 
    #                 current_edge_id in self.all_junction_outgoing_edges[junc_id]):
    #                 is_control_edge = True
    #                 break

    #         if not is_control_edge:
    #             continue

    #         # 初始化车辆路径记录
    #         if veh_id not in self.vehicle_path_data:
    #             self.vehicle_path_data[veh_id] = {
    #                 "incoming_lanes": set(),
    #                 "outgoing_lanes": set()
    #             }

    #         # 遍历控制路口，检查车辆是否在这些路口的 incoming 或 outgoing edges 上
    #         for junc_id in self.junction_list:
    #             # 检查是否在当前路口的 incoming edges 上
    #             if current_edge_id in self.all_junction_incoming_edges[junc_id]:
    #                 self.vehicle_path_data[veh_id]["incoming_lanes"].add(current_lane_id)
                    
    #                 # 检查是否在当前路口的 outgoing edges 上
    #                 if current_edge_id in self.all_junction_outgoing_edges[junc_id]:
    #                     self.vehicle_path_data[veh_id]["outgoing_lanes"].add(current_lane_id)

    def get_junction_stats(self, junc_id):
        """
        获取指定路口的统计信息, 包括到达车辆总数、车辆类型分布, 以及每辆车的出发和到达lane。
        """
        # 到达/经过路口的车辆总数
        total_vehicles_enter = self.incoming_traffic_counts.get(junc_id, 0)
        total_vehicles_pass = self.outgoing_traffic_counts.get(junc_id, 0)

        # 到达/经过车辆的类型分布
        vehicle_types_enter = self.incoming_vehicle_types.get(junc_id, {"RL": 0, "IDM": 0})
        vehicle_types_pass = self.outgoing_vehicle_types.get(junc_id, {"RL": 0, "IDM": 0})

        # 每辆车的来源和去向
        vehicle_paths = {}
        for veh_id, stats in self.vehicle_lane_stats.get(junc_id, {}).items():
            vehicle_paths[veh_id] = {
                "origin": stats["origin"],
                "destination": stats["destination"]
            }

        return {
            "total_vehicles_enter": total_vehicles_enter,
            "total_vehicles_pass": total_vehicles_pass,
            "vehicle_types_enter": vehicle_types_enter,
            "vehicle_types_pass": vehicle_types_pass,
            "vehicle_paths": vehicle_paths
        }

    def init_env(self):
        ## vehicle level
        self.vehicles = Container()
        self.rl_vehicles = Container()
        self.reward_record = dict()            
        self.veh_waiting_clock = dict()
        self.veh_waiting_juncs = dict()
        self.veh_name_mapping_table = dict()
        self.conflict_vehids=[]

        # env level
        self._step = 0
        self.previous_obs = {}
        self.previous_action = {}
        self.previous_reward = {}
        self.previous_dones = {}

        # occupancy map
        self.inner_lane_obs = dict()
        self.inner_lane_occmap = dict()
        self.inner_lane_newly_enter = dict()
        for JuncID in self.junction_list:
            self.inner_lane_obs[JuncID] = dict()
            self.inner_lane_newly_enter[JuncID] = dict()
            self.inner_lane_occmap[JuncID] = dict()
            for keyword in self.keywords_order:
                self.inner_lane_obs[JuncID][keyword] = []
                self.inner_lane_newly_enter[JuncID][keyword] = []
                self.inner_lane_occmap[JuncID][keyword] = [0 for _ in range(10)]

        # vehicle queue and control queue
        self.control_queue = dict()
        self.control_queue_waiting_time = dict()        
        self.queue = dict()
        self.queue_waiting_time = dict()
        self.head_of_control_queue = dict()
        self.inner_speed = dict()

        for JuncID in all_junction_list:
            self.queue[JuncID] = dict()
            self.queue_waiting_time[JuncID] = dict()
            for keyword in self.keywords_order:
                self.queue[JuncID][keyword] = []
                self.queue_waiting_time[JuncID][keyword] = []

        for JuncID in self.junction_list:
            self.control_queue[JuncID] = dict()
            self.control_queue_waiting_time[JuncID] = dict()
            # self.queue[JuncID] = dict()
            # self.queue_waiting_time[JuncID] = dict()
            self.head_of_control_queue[JuncID] = dict()
            self.inner_speed[JuncID] = []
            for keyword in self.keywords_order:
                self.control_queue[JuncID][keyword] = []
                self.control_queue_waiting_time[JuncID][keyword] = []
                # self.queue[JuncID][keyword] = []
                # self.queue_waiting_time[JuncID][keyword] = []
                self.head_of_control_queue[JuncID][keyword] = []

        ## global reward related        
        self.previous_global_waiting = dict()
        for JuncID in self.junction_list:
            self.previous_global_waiting[JuncID] = dict()
            for keyword in self.keywords_order:
                self.previous_global_waiting[JuncID][keyword] = 0
                self.previous_global_waiting[JuncID]['sum'] = 0

        ## data monitor
        self.monitor = DataMonitor(self)

        # self._print_debug('init_env')

    def get_avg_wait_time(self, JuncID, Keyword, mode = 'all'):
        ## mode = all, rv
        if mode == 'all':
            return np.mean(np.array(self.queue_waiting_time[JuncID][Keyword])) if len(self.queue_waiting_time[JuncID][Keyword])>0 else 0
        elif mode == 'rv':
            return np.mean(np.array(self.control_queue_waiting_time[JuncID][Keyword])) if len(self.control_queue_waiting_time[JuncID][Keyword])>0 else 0
        else:
            print('Error Mode in Queue Waiting time Calculation')
            return 0

    def get_queue_len(self, JuncID, Keyword, mode='all'):
        ## mode = all, rv
        if mode == 'all':
            return len(self.queue[JuncID][Keyword])
        elif mode == 'rv':
            return len(self.control_queue[JuncID][Keyword])
        else:
            print('Error Mode in Queue Length Calculation')
            return 0

    # soft control to the stop line
    def soft_deceleration(self, veh):
        front_distance = self.map.edge_length(veh.road_id) - veh.laneposition
        exhibition = True
        if exhibition:
            front_distance = front_distance-3
            if front_distance < 5:
                return self.min_acc
            else:
                return -((veh.speed**2)/(2*front_distance+EPSILON))
        else:
            if front_distance < 16:
                return self.min_acc
            else:
                return -((veh.speed**2)/(2*front_distance+EPSILON))*10

    def rotated_keywords_order(self, veh):
        if veh.road_id[0] != ':':
            facing_junction_id = self.map.get_facing_intersection(veh.road_id)
            if len(facing_junction_id) == 0:
                print('error in rotating')
                return self.keywords_order
            else:
                dir, label = self.map.qurey_edge_direction(veh.road_id, veh.lane_index)
                if not label:
                    print("error in qurey lane direction and edge lable")
                    return self.keywords_order
                else:
                    ego_keyword = label+dir
                    index = self.keywords_order.index(ego_keyword)
                    rotated_keyword = []
                    for i in range(len(self.keywords_order)):
                        rotated_keyword.extend([self.keywords_order[(i+index)%(len(self.keywords_order)-1)]])
                    return rotated_keyword
        else:
            for ind in range(len(veh.road_id)):
                if veh.road_id[len(veh.road_id)-1-ind] == '_':
                    break
            last_dash_ind = len(veh.road_id)-1-ind
            facing_junction_id = veh.road_id[1:last_dash_ind]
            dir, label = self.map.qurey_inner_edge_direction(veh.road_id, veh.lane_index)
            if not label:
                print("error in qurey lane direction and edge lable")
                return self.keywords_order
            else:
                ego_keyword = label+dir
                index = self.keywords_order.index(ego_keyword)
                rotated_keyword = []
                for i in range(len(self.keywords_order)):
                    rotated_keyword.extend([self.keywords_order[(i+index)%(len(self.keywords_order)-1)]])
                return rotated_keyword
            
    def change_conflict_mechanism_type(self, new_type):
        if not new_type in ['off', 'flexible', 'standard']:
            return False
        else:
            self.conflict_resolve_mechanism_type = new_type
            return True            
        
    def change_veh_route(self, veh_id, route):
        ## route should be a list of edge id
        self.sumo_interface.set_veh_route(veh_id, route)

    def change_rl_prob(self, rl_prob):
        ## assign all existing RL vehicle first
        changed_list = []
        if rl_prob < self.default_rl_prob:
            for veh in self.rl_vehicles:
                # route = self.routes[tc.vehicle.getRouteID(veh_id)]
                if random.random()>(rl_prob/self.default_rl_prob):
                    changed_list.extend([deepcopy(veh)])
                    self.vehicles[veh.id].type = 'IDM'
                    self.sumo_interface.set_color(self.vehicles[veh.id], WHITE)
            for veh in changed_list:
                self.rl_vehicles.pop(veh.id)
            self.change_default_spawn_rl_prob(rl_prob)
        else:
            self.change_default_spawn_rl_prob(rl_prob)
        return changed_list

    def change_default_spawn_rl_prob(self, prob):
        self.default_rl_prob = prob

    # def change_spawn_rl_prob(self, edge_id, prob):
    #     self.spawn_rl_prob[edge_id] = prob

    def conflict_predetection(self, junc, ori):
        # detect potential conflict, refer to conflict resolving mechanism
        # input: junc:junction id, ori: moving direction
        # output: True: conflict or potential conflict, False: no conflict detected
        allowing_ori=[ori]
        for pair_set in UNCONFLICT_SET:
            if ori in pair_set:
                for k in pair_set:
                    if k!= ori:
                        allowing_ori.extend([k])
        if self.conflict_resolve_mechanism_type=='flexible':
            if ori in self.previous_global_waiting[junc]['largest']:
                for key in self.inner_lane_occmap[junc].keys():
                    if max(self.inner_lane_occmap[junc][key][:3])>0 and key not in allowing_ori:
                        return True
            else:
                for key in self.inner_lane_occmap[junc].keys():
                    if max(self.inner_lane_occmap[junc][key][:8])>0 and key not in allowing_ori:
                        return True
        elif self.conflict_resolve_mechanism_type=='standard':
            for key in self.inner_lane_occmap[junc].keys():
                if max(self.inner_lane_occmap[junc][key][:8])>0 and key not in allowing_ori:
                    return True
        elif self.conflict_resolve_mechanism_type=='off':
            pass
        else:
            pass
        return False

    def virtual_id_assign(self, veh_id):
        if not veh_id in self.veh_name_mapping_table.keys():
            self.veh_name_mapping_table[veh_id] = (veh_id, False)
            return veh_id
        else:
            if self.veh_name_mapping_table[veh_id][1]:
                virtual_new_id = veh_id+'@'+str(10*random.random())
                self.veh_name_mapping_table[veh_id] = (virtual_new_id, False)
                return virtual_new_id
            else:
                return self.veh_name_mapping_table[veh_id][0]
    
    def convert_virtual_id_to_real_id(self, virtual_id):
        return virtual_id.split('@')[0]

    def terminate_veh(self, virtual_id):
        real_id = virtual_id.split('@')[0]
        self.veh_name_mapping_table[real_id] = (self.veh_name_mapping_table[real_id][0], True)

    def need_to_control(self, veh):
        # determine whether the vehicles is inside the control zone
        return True if self.map.check_veh_location_to_control(veh) and \
                (self.map.edge_length(veh.road_id) - veh.laneposition) < self.control_distance \
                    else False

    def norm_value(self, value_list, max, min):
        for idx in range(len(value_list)):
            value_list[idx] = value_list[idx] if value_list[idx]<max else max
            value_list[idx] = value_list[idx] if value_list[idx]>min else min
        return np.array(value_list)/max

    def reward_compute(self, rl_veh, waiting_lst, action, junc, ori):
        self.reward_record[rl_veh.id] = dict()
        total_veh_control_queue = self._compute_total_num_control_queue(self.control_queue[junc])
        if not total_veh_control_queue:
            ## avoid empty queue at the beginning
            total_veh_control_queue = 1

        if action == 1:
            egoreward = waiting_lst[0]
        else:
            egoreward = -waiting_lst[0]

        ## global reward negative is bad, positive is good
        globalreward = self.global_obs[junc]
        self.reward_record[rl_veh.id]['ego'] = egoreward
        self.reward_record[rl_veh.id]['global'] = globalreward
        self.reward_record[rl_veh.id]['sum'] = egoreward + globalreward
        if egoreward > 1:
            print('too large ego reward')
        
        if math.isnan(egoreward + globalreward):
            print('nan')
        if rl_veh.id in self.conflict_vehids:
            ## punishing conflicting action
            self.reward_record[rl_veh.id]['ego'] = egoreward-1
            return egoreward-1
        else:
            return egoreward

    def _traffic_light_program_update(self):
        if self._step> self.traffic_light_program['disable_light_start']:
            self.sumo_interface.disable_all_trafficlight(self.traffic_light_program['disable_state'])
  
    def compute_max_len_of_control_queue(self, JuncID):
        control_queue_len = []
        junc_info = self.control_queue[JuncID]
        for keyword in self.keywords_order:
            control_queue_len.extend([len(junc_info[keyword])])
        return np.array(control_queue_len).max()

    def _compute_total_num_control_queue(self, junc_info):
        control_queue_len = []
        for keyword in self.keywords_order:
            control_queue_len.extend([len(junc_info[keyword])])
        return sum(control_queue_len)

    def _update_obs(self):
        # clear the queues
        for JuncID in self.junction_list:
            self.inner_speed[JuncID] = []
            for keyword in self.keywords_order:
                self.control_queue[JuncID][keyword] = []
                self.queue[JuncID][keyword] = []
                self.head_of_control_queue[JuncID][keyword] = []
                self.control_queue_waiting_time[JuncID][keyword] = []
                self.queue_waiting_time[JuncID][keyword] = []
        
        # occupancy map
        self.inner_lane_obs = dict()
        self.inner_lane_occmap = dict()
        self.inner_lane_newly_enter = dict()
        for JuncID in self.junction_list:
            self.inner_lane_obs[JuncID] = dict()
            self.inner_lane_newly_enter[JuncID] = dict()
            self.inner_lane_occmap[JuncID] = dict()
            for keyword in self.keywords_order:
                self.inner_lane_obs[JuncID][keyword] = []
                self.inner_lane_newly_enter[JuncID][keyword] = []
                self.inner_lane_occmap[JuncID][keyword] = [0 for _ in range(10)]

        # one_vehicle = True
        # for veh in self.vehicles:
        #     if len(veh.road_id) == 0:
        #         continue # 忽略无效车辆信息

        #     if veh.road_id[0] == ':':  # 判断车辆是否在路口内部
        #         junc_id = veh.road_id[1:].split('_')[0]  # 去掉 ":" 并提取路口 ID

        #         if junc_id in all_junction_list:
        #             if self.print_debug and one_vehicle:
        #                 print("veh:", veh, " road_id:", veh.road_id, " junc_id:", junc_id)
        #                 # print("counts:", self.intersection_traffic_counts)
        #                 # one_vehicle = False

        #             # 初始化车辆历史
        #             if veh not in self.vehicle_history:
        #                 self.vehicle_history[veh] = set()

        #             # 如果车辆尚未被记录经过该路口，更新流量计数
        #             if junc_id not in self.vehicle_history[veh]:
        #                 self.vehicle_history[veh].add(junc_id)

        #                 # 确保路口计数器初始化
        #                 if junc_id not in self.intersection_traffic_counts:
        #                     self.intersection_traffic_counts[junc_id] = 0

        #                 self.intersection_traffic_counts[junc_id] += 1

        for veh in self.vehicles:
            if len(veh.road_id)==0:
                ## avoid invalid vehicle information
                continue
            if veh.road_id[0] == ':':
                ## inside intersection: update inner obs and occmap
                direction, edge_label = self.map.qurey_inner_edge_direction(veh.road_id, veh.lane_index)
                for ind in range(len(veh.road_id)):
                    if veh.road_id[len(veh.road_id)-1-ind] == '_':
                        break
                last_dash_ind = len(veh.road_id)-1-ind
                if edge_label and veh.road_id[1:last_dash_ind] in self.junction_list:
                    self.inner_lane_obs[veh.road_id[1:last_dash_ind]][edge_label+direction].extend([veh])
                    self.inner_lane_occmap[veh.road_id[1:last_dash_ind]][edge_label+direction][min(int(10*veh.laneposition/self.map.edge_length(veh.road_id)), 9)] = 1
                    if veh not in self.prev_inner[veh.road_id[1:last_dash_ind]][edge_label+direction]:
                        self.inner_lane_newly_enter[veh.road_id[1:last_dash_ind]][edge_label+direction].extend([veh])
                    self.inner_speed[veh.road_id[1:last_dash_ind]].extend([veh.speed])
            else:
                ## update waiting time
                ## 该逻辑确保每辆车的等待时间仅反映在它所在的特定路口，而不是累积到多个路口的总和。
                ## 新车：如果车辆第一次进入网络中任何一个路口，直接记录它的累计等待时间。
                ## 已有记录的车：如果车辆之前经过了其他路口，则减去先前路口的等待时间，从而得到当前路口的等待时间
                JuncID, keyword = self.map.get_veh_moving_direction(veh)
                accumulating_waiting = veh.wait_time

                if len(JuncID) > 0:
                    if veh.id not in self.veh_waiting_juncs.keys(): #该车辆尚未进入过任何路口
                        self.veh_waiting_juncs[veh.id] = dict()
                        self.veh_waiting_juncs[veh.id][JuncID] = accumulating_waiting
                        # 更新直方图数据
                        # self.junction_waiting_histograms[JuncID].append(accumulating_waiting)
                    else:
                        prev_wtm = 0 #存储车辆在其他路口的等待时间
                        for prev_JuncID in self.veh_waiting_juncs[veh.id].keys(): #遍历该车辆在veh_waiting_juncs中的所有已记录路口ID（prev_JuncID）
                            if prev_JuncID != JuncID:
                                prev_wtm += self.veh_waiting_juncs[veh.id][prev_JuncID]
                        if accumulating_waiting - prev_wtm >= 0:
                            #当前累计等待时间比之前路口的等待时间总和更大，说明车辆在当前路口确实有等待时间
                            self.veh_waiting_juncs[veh.id][JuncID] = accumulating_waiting - prev_wtm
                            # 更新直方图数据
                            # self.junction_waiting_histograms[JuncID].append(accumulating_waiting - prev_wtm)
                        else:
                            self.veh_waiting_juncs[veh.id][JuncID] = accumulating_waiting
                            # self.junction_waiting_histograms[JuncID].append(accumulating_waiting)

                    # print("veh:", veh.id, "Junc:", JuncID, "WT:", self.veh_waiting_juncs[veh.id][JuncID])
            
                ## updating control queue and waiting time of queue
                if self.map.get_distance_to_intersection(veh)<=self.control_zone_length:
                    self.queue[JuncID][keyword].extend([veh])
                    self.queue_waiting_time[JuncID][keyword].extend([self.veh_waiting_juncs[veh.id][JuncID]])
                    
                    if veh.type == 'RL' and JuncID in self.junction_list:
                        self.control_queue[JuncID][keyword].extend([veh])
                        self.control_queue_waiting_time[JuncID][keyword].extend([self.veh_waiting_juncs[veh.id][JuncID]])

                    # # 新增：记录每个路口的等待时间分布（直方图）
                    # if JuncID not in self.all_waiting_time_histograms:
                    #     self.all_waiting_time_histograms[JuncID] = {kw: [] for kw in self.keywords_order}
                    # self.all_waiting_time_histograms[JuncID][keyword].extend([self.veh_waiting_juncs[veh.id][JuncID]])
                    
        for JuncID in all_junction_list:
            weighted_sum = 0
            for Keyword in self.keywords_order:
                waiting_time = self.get_avg_wait_time(JuncID, Keyword, 'all')
                self.all_previous_global_waiting[JuncID][Keyword] = waiting_time
                weighted_sum += waiting_time

            self.all_previous_global_waiting[JuncID]['sum'] = weighted_sum

        ## update previous global waiting for next step reward calculation
        for JuncID in self.junction_list:
            weighted_sum = 0
            largest = 0
            for Keyword in self.keywords_order:
                # control_queue_length = self.get_queue_len(JuncID, Keyword, 'rv')
                waiting_time = self.get_avg_wait_time(JuncID, Keyword, 'rv')
                self.previous_global_waiting[JuncID][Keyword] = waiting_time
                if waiting_time >= largest:
                    self.previous_global_waiting[JuncID]['largest'] = [Keyword]
                    largest = waiting_time
                weighted_sum += waiting_time

            # 计算前一个时间步的总等待时间与当前时间步的总等待时间之间的差值。
            # 如果结果为正，表示当前时间步的总等待时间减少了，交通流量改善。
            # 如果结果为负，表示当前时间步的总等待时间增加了，交通流量变差。
            self.global_obs[JuncID] = (self.previous_global_waiting[JuncID]['sum'] - weighted_sum)/(self.previous_global_waiting[JuncID]['sum']*10+EPSILON)
            if self.global_obs[JuncID] < -1:
                self.global_obs[JuncID] = -1
            if self.global_obs[JuncID] > 1:
                self.global_obs[JuncID] = 1

            self.previous_global_waiting[JuncID]['sum'] = weighted_sum

    def step_once(self, action={}, eval=False):
        # self._print_debug('step')
        self.new_departed = set()
        self.sumo_interface.set_max_speed_all(10)
        self._traffic_light_program_update()
        # check if the action input is valid
        if not (isinstance(action, dict) and len(action) == len(self.previous_obs)- sum(dict_tolist(self.previous_dones))):
            print('error!! action dict is invalid')
            return dict()

        # execute action in the sumo env
        for virtual_id in action.keys():
            veh_id = self.convert_virtual_id_to_real_id(virtual_id)
            if action[virtual_id] == 1:
                JuncID, ego_dir = self.map.get_veh_moving_direction(self.rl_vehicles[veh_id])
                if self.conflict_predetection(JuncID, ego_dir):
                    ## conflict
                    self.sumo_interface.accl_control(self.rl_vehicles[veh_id], self.soft_deceleration(self.rl_vehicles[veh_id]))
                    self.conflict_vehids.extend([veh_id])
                else:
                    self.sumo_interface.accl_control(self.rl_vehicles[veh_id], self.max_acc)
            elif action[virtual_id] == 0:
                self.sumo_interface.accl_control(self.rl_vehicles[veh_id], self.soft_deceleration(self.rl_vehicles[veh_id]))

        # sumo step
        self.sumo_interface.step() # self.tc.simulationStep()

        # 获取当前所有车辆的位置信息
        # all_vehicle_ids = self.sumo_interface.tc.vehicle.getIDList()
        # one_vehicle = True
        # sim_res = self.sumo_interface.get_sim_info()
        # for veh_id in sim_res.departed_vehicles_ids:
        #     road_id = self.sumo_interface.get_vehicle_edge(veh_id)
        #     # print("veh_id:", veh_id, " road_id:", road_id)
        #     if len(road_id) == 0:
        #         continue # 忽略无效车辆信息

        #     if road_id[0] == ':':  # 判断车辆是否在路口内部
        #         junc_id = road_id[1:].split('_')[0]  # 去掉 ":" 并提取路口 ID

        #         if junc_id in all_junction_list:
        #             if self.print_debug and one_vehicle:
        #                 print("veh:", veh_id, " road_id:", road_id, " junc_id:", junc_id)
        #                 # print("counts:", self.intersection_traffic_counts)
        #                 # one_vehicle = False

        #             # 初始化车辆历史
        #             if veh_id not in self.vehicle_history:
        #                 self.vehicle_history[veh_id] = set()

        #             # 如果车辆尚未被记录经过该路口，更新流量计数
        #             if junc_id not in self.vehicle_history[veh_id]:
        #                 self.vehicle_history[veh_id].add(junc_id)

        #                 # 确保路口计数器初始化
        #                 if junc_id not in self.intersection_traffic_counts:
        #                     self.intersection_traffic_counts[junc_id] = 0

        #                 self.intersection_traffic_counts[junc_id] += 1

        # 使用 SUMO API 获取当前步进入和离开网络的车辆数量
        current_departed = self.sumo_interface.tc.simulation.getDepartedNumber()
        current_arrived = self.sumo_interface.tc.simulation.getArrivedNumber()

        # 更新累计统计数据
        self.total_departed_count += current_departed
        self.total_arrived_count += current_arrived

        # gathering states from sumo 
        sim_res = self.sumo_interface.get_sim_info()
        
        # setup for new departed vehicles    
        for veh_id in sim_res.departed_vehicles_ids:
            self.sumo_interface.subscribes.veh.subscribe(veh_id)
            length = self.sumo_interface.tc.vehicle.getLength(veh_id)
            route = self.sumo_interface.tc.vehicle.getRoute(veh_id)
            road_id  = self.sumo_interface.get_vehicle_edge(veh_id)
            if (road_id in self.spawn_rl_prob.keys() and random.random()<self.spawn_rl_prob[road_id]) or \
                (random.random()<self.default_rl_prob):
                self.rl_vehicles[veh_id] = veh = Vehicle(id=veh_id, type="RL", route=route, length=length)
                self.vehicles[veh_id] = veh = Vehicle(id=veh_id, type="RL", route=route, length=length, wait_time=0)
            else:
                self.vehicles[veh_id] = veh = Vehicle(id=veh_id, type="IDM", route=route, length=length, wait_time=0)
                
            self.sumo_interface.set_color(veh, WHITE if veh.type=="IDM" else RED)

            self.new_departed.add(veh)

        self.new_arrived = {self.vehicles[veh_id] for veh_id in sim_res.arrived_vehicles_ids}
        self.new_collided = {self.vehicles[veh_id] for veh_id in sim_res.colliding_vehicles_ids}
        self.new_arrived -= self.new_collided # Don't count collided vehicles as "arrived"

        # remove arrived vehicles from Env
        for veh in self.new_arrived:
            if veh.type == 'RL':
                self.rl_vehicles.pop(veh.id)
            self.vehicles.pop(veh.id)

        # self._print_debug('before updating vehicles')
        # update vehicles' info for Env
        for veh_id, veh in self.vehicles.items():
            veh.prev_speed = veh.get('speed', None)
            veh.update(self.sumo_interface.subscribes.veh.get(veh_id))
            if veh.type == 'RL':
                self.rl_vehicles[veh_id].update(self.sumo_interface.subscribes.veh.get(veh_id))
            wt, _ = self.sumo_interface.get_veh_waiting_time(veh)
            if wt > 0:
                self.vehicles[veh_id].wait_time +=1

        ## update obs 
        self._update_obs()

        if eval:
            self.update_traffic_flow()
        # self.update_vehicle_path_data()

        obs = {}
        rewards = {}
        dones = {}
        for rl_veh in self.rl_vehicles:
            virtual_id = self.virtual_id_assign(rl_veh.id)
            if len(rl_veh.road_id) == 0:
                if virtual_id in action.keys():
                    ## collision occured and teleporting, I believe it should be inside the intersection
                    obs[virtual_id] = self.check_obs_constraint(self.previous_obs[virtual_id])
                    dones[virtual_id] = True
                    rewards[virtual_id] =  0
                    self.terminate_veh(virtual_id)
                    continue
                else:
                    ## then do nothing
                    continue
            JuncID, ego_dir = self.map.get_veh_moving_direction(rl_veh)
            if len(JuncID) == 0 or JuncID not in self.junction_list:
                # skip the invalid JuncID 
                continue
        
            obs_control_queue_length = []
            obs_waiting_lst = []
            obs_inner_lst = []
            control_queue_max_len = self.compute_max_len_of_control_queue(JuncID) + EPSILON
            if self.need_to_control(rl_veh):
                ## need to control 
                ## average waiting time 
                for keyword in self.rotated_keywords_order(rl_veh):
                    obs_control_queue_length.extend([self.get_queue_len(JuncID, keyword, 'rv')/control_queue_max_len])
                    obs_waiting_lst.extend([self.get_avg_wait_time(JuncID, keyword, 'rv')])
                    obs_inner_lst.append(self.inner_lane_occmap[JuncID][keyword])
                
                obs_waiting_lst = self.norm_value(obs_waiting_lst, self.max_wait_time, 0)
                if virtual_id in action.keys():
                    ## reward
                    rewards[virtual_id] = self.reward_compute(rl_veh, obs_waiting_lst, action[virtual_id], JuncID, ego_dir)
                obs[virtual_id] = self.check_obs_constraint(np.concatenate((obs_control_queue_length, np.array(obs_waiting_lst), np.reshape(np.array(obs_inner_lst), (80,)))))
                dones[virtual_id] = False
            elif virtual_id in action.keys():
                ## update reward for the vehicle already enter intersection
                if rl_veh.road_id[0]==':':
                    ## inside the intersection
                    for keyword in self.rotated_keywords_order(rl_veh):
                        obs_control_queue_length.extend([self.get_queue_len(JuncID, keyword, 'rv')/control_queue_max_len])
                        obs_waiting_lst.extend([self.get_avg_wait_time(JuncID, keyword, 'rv')])
                        obs_inner_lst.append(self.inner_lane_occmap[JuncID][keyword])
                    obs_waiting_lst = self.norm_value(obs_waiting_lst, self.max_wait_time, 0)
                    rewards[virtual_id] = self.reward_compute(rl_veh, obs_waiting_lst, action[virtual_id], JuncID, ego_dir)
                    dones[virtual_id] = True
                    obs[virtual_id] = self.check_obs_constraint(np.concatenate((obs_control_queue_length, np.array(obs_waiting_lst), np.reshape(np.array(obs_inner_lst), (80,)))))
                    self.terminate_veh(virtual_id)
                else:
                    ## change to right turn lane and no need to control
                    for keyword in self.rotated_keywords_order(rl_veh):
                        obs_control_queue_length.extend([self.get_queue_len(JuncID, keyword, 'rv')/control_queue_max_len])
                        obs_waiting_lst.extend([self.get_avg_wait_time(JuncID, keyword, 'rv')])
                        obs_inner_lst.append(self.inner_lane_occmap[JuncID][keyword])
                    obs_waiting_lst = self.norm_value(obs_waiting_lst, self.max_wait_time, 0)
                    rewards[virtual_id] = 0
                    dones[virtual_id] = True
                    obs[virtual_id] = self.check_obs_constraint(np.concatenate((obs_control_queue_length, np.array(obs_waiting_lst), np.reshape(np.array(obs_inner_lst), (80,)))))
                    self.terminate_veh(virtual_id)    
        dones['__all__'] = False

        infos = {}
        # infos["departed_count"] = departed_count
        # infos["arrived_count"] = arrived_count

        truncated = {}
        truncated['__all__'] = False
        if self._step >= self._max_episode_steps:
            for key in dones.keys():
                truncated[key] = True
        self._step += 1
        self.previous_obs, self.previous_reward, self.previous_action, self.previous_dones, self.prev_inner\
              = deepcopy(obs), deepcopy(rewards), deepcopy(action), deepcopy(dones), deepcopy(self.inner_lane_obs)
        self.monitor.step(self)

        self.conflict_vehids=[]
        # self._print_debug('finish process step')
        # if len(dict_tolist(rewards))>0 and self.print_debug:
        #     print('avg reward: '+str(np.array(dict_tolist(rewards)).mean())+' max reward: '+str(np.array(dict_tolist(rewards)).max())+' min reward: '+str(np.array(dict_tolist(rewards)).min()))

        return obs, rewards, dones, truncated, infos

    def step(self, action={}, eval=False):
        if len(action) == 0:
            print("empty action")

        obs, rewards, dones, truncated, infos = self.step_once(action, eval)

        # COMMENT OUT THE FOLLOWING LINES IF DOING BASELINE SCRIPTS
        # avoid empty obs or all agents are done during simulation
        # all_done = True
        # for id in dones.keys():
        #     if not dones[id] and id!='__all__':
        #         all_done = False
        
        # if all_done:
        #     new_obs = {}
        #     while len(new_obs)==0:
        #         new_obs, new_rewards, new_dones, new_truncated, new_infos = self.step_once()
        #     for id in new_obs.keys():
        #         obs[id] = new_obs[id]
        #         dones[id] = new_dones[id]

        return obs, rewards, dones, truncated, infos

    def reset(self, *, seed=None, options=None):
        # self._print_debug('reset')
        # soft reset
        # 清空每次评估需要重新记录的数据
        self.incoming_traffic_counts = {junc: 0 for junc in all_junction_list}
        self.outgoing_traffic_counts = {junc: 0 for junc in all_junction_list}
        self.incoming_vehicle_history = {junc: set() for junc in all_junction_list}
        self.outgoing_vehicle_history = {junc: set() for junc in all_junction_list}
        self.incoming_vehicle_types = {junc_id: {"RL": 0, "IDM": 0} for junc_id in all_junction_list}
        self.outgoing_vehicle_types = {junc_id: {"RL": 0, "IDM": 0} for junc_id in all_junction_list}

        # 重置 vehicle_lane_stats
        self.vehicle_lane_stats = {junc_id: {} for junc_id in all_junction_list}

        self.vehicle_path_data = {}

        self.total_arrived_count = 0

        while not self.sumo_interface.reset_sumo():
            pass

        if self.rl_prob_list:
            self.default_rl_prob = random.choice(self.rl_prob_list)
            print("new RV percentage = "+str(self.default_rl_prob))

        self.init_env()
        obs = {}
        if options:
            if options['mode'] == 'HARD':
                obs, _, _, _, infos = self.step_once()
                return obs, infos

        while len(obs)==0:
            obs, _, _, _, infos = self.step_once()
        return obs, infos

    def close(self):
        ## close env
        self.sumo_interface.close()

    def action_space_sample(self, agent_ids: list = None):
        # self._print_debug('action sample')
        """Returns a random action for each environment, and potentially each
            agent in that environment.

        Args:
            agent_ids: List of agent ids to sample actions for. If None or
                empty list, sample actions for all agents in the
                environment.

        Returns:
            A random action for each environment.
        """

        if agent_ids is None:
            agent_ids = self.get_agent_ids()
        return {
            agent_id: self.action_space.sample()
            for agent_id in agent_ids
            if agent_id != "__all__"
        }

    def observation_space_sample(self, agent_ids: list = None):
        # self._print_debug('obs sample')
        if agent_ids is None:
            agent_ids = self.get_agent_ids()
        return {
            agent_id: self.observation_space.sample()
            for agent_id in agent_ids
            if agent_id != "__all__"
        }

    def check_obs_constraint(self, obs):
        if not self.observation_space.contains(obs):
            obs= np.asarray([x if x>= self.observation_space.low[0] else self.observation_space.low[0] for x in obs]\
                                    , dtype=self.observation_space.dtype)
            obs = np.asarray([x if x<= self.observation_space.high[0] else self.observation_space.high[0] for x in obs]\
                                    , dtype=self.observation_space.dtype)
            if not self.observation_space.contains(obs):
                print('dddd')
                raise ValueError(
                    "Observation is invalid, got {}".format(obs)
                )
        return obs