import traci
import xml.etree.ElementTree as ET

# 定义四个控制 junction 的 ID
# junction_list = ['229','499','332','334']
junction_list = ['cluster12203246695_12203246696_430572036_442436239',
            'cluster_2052409422_2052409707_542824247_542824770_#2more',
            'cluster_2093101229_2093101656_2093101781_2093101915_#8more',
            'cluster_439980117_439980118_442435910_442435912',
            'cluster_547498658_547498666_547498756_547498762_#8more',
            'cluster_2052409323_2052409733_2052409806_2052409936_#9more',
            'cluster9663732079_J0_J1_J2_#2more',
            'cluster_1289585639_439979990_8156136067_8156136068_#1more']

# 用于存储每个 junction 的 incoming edges
junction_incoming_edges = {}

# 初始化 SUMO 环境
sumo_binary = "sumo"  # or "sumo-gui" for GUI mode
# sumo_config = "osm.sumocfg"
sumo_config = "colorado_smaller.sumocfg"
traci.start([sumo_binary, "-c", sumo_config])

try:
    # 查询每个 junction 的 incoming edges
    for junc_id in junction_list:
        # 获取所有 incoming edges
        all_incoming = traci.junction.getIncomingEdges(junc_id)
        
        # 过滤掉以 ":" 开头的内部 ID
        filtered_incoming = [edge for edge in all_incoming if not edge.startswith(":")]
        
        # 存储到字典中
        junction_incoming_edges[junc_id] = filtered_incoming

finally:
    # 关闭 SUMO 环境
    traci.close()

# 打印每个 junction 的 incoming edges
print("Junction Incoming Edges:")
for junc_id, edges in junction_incoming_edges.items():
    print(f"{junc_id}: {edges}")

# def parse_vehicle_routes_by_depart(xml_file, junction_incoming_edges, max_depart=1000):
#     """
#     解析 XML 文件中的车辆路线，仅统计 depart 值小于 max_depart 的车辆。
#     确保每辆车只为每个 junction 计数一次。
#     """
#     # 加载 XML 文件
#     tree = ET.parse(xml_file)
#     root = tree.getroot()
    
#     # 存储每个 junction 的车辆计数
#     junction_vehicle_counts = {junc_id: 0 for junc_id in junction_incoming_edges.keys()}
    
#     # 遍历所有车辆的路线
#     for vehicle in root.findall("vehicle"):
#         depart_time = float(vehicle.get("depart"))  # 获取车辆的 depart 时间
#         if depart_time >= max_depart:
#             break  # depart 单调递增，一旦超过 max_depart，直接退出
        
#         route_edges = vehicle.find("route").get("edges").split()  # 获取车辆的 edges 列表
        
#         # 使用集合避免重复计数
#         visited_junctions = set()
        
#         # 遍历每个 junction，检查车辆是否经过其 incoming edges
#         for junc_id, incoming_edges in junction_incoming_edges.items():
#             if junc_id not in visited_junctions and any(edge in route_edges for edge in incoming_edges):  # 检查是否有交集
#                 junction_vehicle_counts[junc_id] += 1
#                 visited_junctions.add(junc_id)  # 标记为已访问
    
#     return junction_vehicle_counts

def parse_vehicle_routes_by_depart(xml_file, junction_incoming_edges, max_depart=1000):
    """
    解析 XML 文件中的车辆路线，仅统计 depart 值小于 max_depart 的车辆。
    确保每辆车只为每个 junction 计数一次，并记录每辆车经过的 junction。
    """
    # 加载 XML 文件
    tree = ET.parse(xml_file)
    root = tree.getroot()
    
    # 存储每个 junction 的车辆计数
    junction_vehicle_counts = {junc_id: 0 for junc_id in junction_incoming_edges.keys()}
    # 存储每辆车经过的 junction 信息
    vehicle_junction_map = {}
    
    # 遍历所有车辆的路线
    for vehicle in root.findall("vehicle"):
        vehicle_id = vehicle.get("id")  # 获取车辆 ID
        depart_time = float(vehicle.get("depart"))  # 获取车辆的 depart 时间
        if depart_time >= max_depart:
            break  # depart 单调递增，一旦超过 max_depart，直接退出
        
        route_edges = vehicle.find("route").get("edges").split()  # 获取车辆的 edges 列表
        
        # 使用集合避免重复计数
        visited_junctions = set()
        
        # 遍历每个 junction，检查车辆是否经过其 incoming edges
        for junc_id, incoming_edges in junction_incoming_edges.items():
            if junc_id not in visited_junctions and any(edge in route_edges for edge in incoming_edges):  # 检查是否有交集
                junction_vehicle_counts[junc_id] += 1
                visited_junctions.add(junc_id)  # 标记为已访问
        
        # 记录该车辆经过的 junction
        vehicle_junction_map[vehicle_id] = list(visited_junctions)
    
    return junction_vehicle_counts, vehicle_junction_map

# 指定 XML 文件路径
# xml_file = "newroute1220_start0.xml"
xml_file = "colorado_smaller_1000s_7911v.rou.xml"
# xml_file = "colorado_smaller_1000s_7911v_1sInterval.rou.xml"

# 调用函数解析文件并统计车辆经过数量
# junction_vehicle_counts = parse_vehicle_routes(xml_file, junction_incoming_edges)

# 调用函数解析文件并统计车辆经过数量，仅统计 depart 小于 1000 的车辆
# junction_vehicle_counts = parse_vehicle_routes_by_depart(xml_file, junction_incoming_edges, max_depart=1000)
junction_vehicle_counts, vehicle_junction_map = parse_vehicle_routes_by_depart(xml_file, junction_incoming_edges, max_depart=1000)

# 输出每辆车的 ID 和经过的 junction
print("\nVehicle Routes by Junction:")
for vehicle_id, junctions in vehicle_junction_map.items():
    print(f"Vehicle {vehicle_id}: {', '.join(junctions) if junctions else 'None'}")

    # 输出结果
print(f"\n{xml_file}")
for junc_id, count in junction_vehicle_counts.items():
    print(f"{junc_id}: {count} vehicles")