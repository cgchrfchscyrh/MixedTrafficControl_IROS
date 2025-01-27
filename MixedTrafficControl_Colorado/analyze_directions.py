import xml.etree.ElementTree as ET
import matplotlib.pyplot as plt
import pandas as pd

# 定义每个控制路口的方向组合
junction_directions_original = {
    "229": {
        "NS": ["978613907#0", "978613917#1"],
        "NE": ["978613907#0", "gneE31"],
        "NW": ["978613907#0", "gneE411"],
        "WN": ["gneE41", "978613912#1"],
        "WE": ["gneE41", "gneE31"],
        "WS": ["gneE41", "978613917#1"],
        "SW": ["978613913#0", "gneE411"],
        "SN": ["978613913#0", "978613912#1"],
        "SE": ["978613914", "229488614#0"],
        "EN": ["229357869#4", "229488615#0"],
        "EW": ["229357869#5", "gneE411"],
        "ES": ["229357869#5", "978613917#1"],
    },
    "499": {
        "NS": ["978615349#0", "978615347#1"],
        "NE": ["978615349#0", "978615345#1"],
        "NW": ["718258596-AddedOffRampEdge", "38521030"],
        "WN": ["877763365#6", "978615348#0"],
        "WE": ["877763365#6", "978615345#1"],
        "WS": ["877763365#5", "38521026#0"],
        "SW": ["877763364#0", "38520914#0"],
        "SN": ["877763364#0", "978615348#0"],
        "SE": ["229489592#3-AddedOffRampEdge", "43076383#0"],
        "EN": ["877763350#4", "43076363"],
        "EW": ["877763350#5", "38520914#0"],
        "ES": ["877763350#5", "978615347#1"],
    },
    "332": {
        "NS": ["877763351#0", "229489595#1"],
        "NE": ["877763351#0", "223369741#0"],
        "NW": ["229489601-AddedOffRampEdge", "36913237"],
        "WN": ["36870615#1", "229489592#1"],
        "WE": ["36870615#1", "223369741#0"],
        "WS": ["36870615#0", "229489600"],
        "SW": ["229489602#4", "223369742#0"],
        "SN": ["229489602#4", "229489592#1"],
        "SE": ["229489602#3-AddedOffRampEdge", "36913198"],
        "EN": ["36870636#10", "36913228"],
        "EW": ["36870636#12", "223369742#0"],
        "ES": ["36870636#12", "229489595#1"],
    },
    "334": {
        "NS": ["229489595#4", "229489593#1"],
        "NE": ["229489595#4", "436475433#6"],
        "NW": ["229489595#3-AddedOffRampEdge", "37723144"],
        "WN": ["436475433#2", "229489602#1"],
        "WE": ["436475433#2", "436475433#6"],
        "WS": ["436475433#1", "37723147"],
        "SW": ["229489781#11", "37552734#10"],
        "SN": ["229489781#11", "229489602#1"],
        "SE": ["229489781#10-AddedOffRampEdge", "37722940"],
        "EN": ["37552734#6", "37722941"],
        "EW": ["37552734#6.62", "37552734#10"],
        "ES": ["37552734#6.62", "229489593#1"],
    },
}

junction_directions_smaller = {
    "229": {
        "NS": ["978613907#1 978613917#0"],
        "NE": ["978613907#1 1318565916#0"],
        "NW": ["978613907#1 1318569357", "978613908 229488609#0"],
        "WN": ["1318568290#1 1318569361#0"],
        "WE": ["1318568290#1 1318565916#0"],
        "WS": ["1318568290#1 978613917#0", "1318568291 229488611#0"],
        "SW": ["978613913#1 1318569357"],
        "SN": ["978613913#1 1318569361#0"],
        "SE": ["978613913#1 1318565916#0", "978613914 229488614#0"],
        "EN": ["1318569356#1 1318569361#0", "1318568288#1 229488615#0"],
        "EW": ["1318569356#1 1318569357"],
        "ES": ["1318569356#1 978613917#0"],
    },
    "499": {
        "NS": ["978615349#0 978615347#1"],
        "NE": ["978615349#0 978615345#1"],
        "NW": ["978615349#0 38520914#0", "718258596-AddedOffRampEdge 38521030"],
        "WN": ["877763365#3 978615348#0"],
        "WE": ["877763365#3 978615345#1"],
        "WS": ["877763365#2-AddedOffRampEdge 38521026#0"],
        "SW": ["877763364#0 38520914#0"],
        "SN": ["877763364#0 978615348#0"],
        "SE": ["229489592#3-AddedOffRampEdge 43076383#0"],
        "EN": ["877763350#4-AddedOffRampEdge 43076363"],
        "EW": ["877763350#5 38520914#0"],
        "ES": ["877763350#5 978615347#1"],
    },
    "332": {
        "NS": ["877763351#0 229489595#2"],
        "NE": ["877763351#0 223369741#1"],
        "NW": ["978613907#0 223369742#1", "229489601-AddedOffRampEdge 36913237#0"],
        "WN": ["36870615#1 229489592#2"],
        "WE": ["36870615#1 223369741#1"],
        "WS": ["36870615#1 229489595#2", "36870615#0 229489600#0"],
        "SW": ["229489602#4 223369742#1"],
        "SN": ["229489602#4 229489592#2"],
        "SE": ["229489602#4 223369741#1", "229489602#3-AddedOffRampEdge 36913198#0"],
        "EN": ["36870636#19 229489592#2", "36870636#17 36913228#0"],
        "EW": ["36870636#19 223369742#1"],
        "ES": ["36870636#19 229489595#2"],
    },
    "334": {
        "NS": ["229489595#4 229489593#1"],
        "NE": ["229489595#4 436475433#5"],
        "NW": ["229489595#4 37552734#10", "229489595#3-AddedOffRampEdge 37723144"],
        "WN": ["436475433#1 229489602#1"],
        "WE": ["436475433#1 436475433#5"],
        "WS": ["436475433#1 229489593#1", "436475433#0 37723147"],
        "SW": ["229489781#5 37552734#10"],
        "SN": ["229489781#5 229489602#1"],
        "SE": ["229489781#5 436475433#5", "229489781#0-AddedOffRampEdge 37722940"],
        "EN": ["37552734#6 229489602#1", "37552734#5 37722941"],
        "EW": ["37552734#6 37552734#10"],
        "ES": ["37552734#6 229489593#1"],
    },
}

# 定义控制路口列表
control_junctions = ["229", "499", "332", "334"]

# # 统计结果存储
junction_counts_original = {junc_id: {dir_label: 0 for dir_label in directions.keys()} for junc_id, directions in junction_directions_original.items()}

# 解析XML文件
def parse_vehicle_routes_original(xml_file, junction_directions, max_depart=1000):
    tree = ET.parse(xml_file)
    root = tree.getroot()
    for vehicle in root.findall("vehicle"):
        depart_time = float(vehicle.get("depart"))  # 获取车辆的 depart 时间
        if depart_time >= max_depart:
            break  # depart 单调递增，超过 max_depart 的直接停止解析

        route_edges = vehicle.find("route").get("edges").split()  # 获取车辆路线
        matched_directions = []  # 记录每辆车的匹配方向

        for junc_id, directions in junction_directions.items():
            for dir_label, edge_combo in directions.items():
                if all(edge in route_edges for edge in edge_combo):
                    junction_counts_original[junc_id][dir_label] += 1
                    matched_directions.append((junc_id, dir_label))
                    break  # 一旦匹配了一个方向，停止检查当前 junction 的其他方向

        # 打印每辆车的分析结果
        if matched_directions:
            print(f"{vehicle.get('id')}: {matched_directions}")
        else:
            print(f"{vehicle.get('id')} - No matches.")

def parse_vehicle_directions_smaller(xml_file, junction_directions, max_depart=1000):
    """
    解析车辆路线并统计每个 junction 的各方向车流量。
    """
    tree = ET.parse(xml_file)
    root = tree.getroot()

    # 初始化每个 junction 的方向计数
    junction_counts = {
        junc_id: {direction: 0 for direction in directions}
        for junc_id, directions in junction_directions.items()
    }

    # 遍历车辆
    for vehicle in root.findall("vehicle"):
        depart_time = float(vehicle.get("depart"))
        if depart_time >= max_depart:
            break  # 如果 depart 超过限制值，则停止分析

        route_edges = vehicle.find("route").get("edges").split()
        matched_directions = []  # 记录每辆车的匹配方向

        # 检查每个 junction
        for junc_id, directions in junction_directions.items():
            for dir_label, edge_combos in directions.items():
                for combo in edge_combos:
                    combo_edges = combo.split()
                    if all(edge in route_edges for edge in combo_edges):
                        junction_counts[junc_id][dir_label] += 1
                        matched_directions.append((junc_id, dir_label))
                        break  # 一旦匹配一个 combo，停止检查当前方向

        # 打印每辆车的分析结果
        if matched_directions:
            print(f"{vehicle.get('id')}: {matched_directions}")
        else:
            print(f"{vehicle.get('id')} - No matches.")

    return junction_counts

# 读取XML文件并统计
xml_file_original = "newroute1220_start0.xml"
xml_file_smaller = "colorado_smaller_1000s_7911v_1sInterval.rou.xml"  # 替换为你的XML文件路径
parse_vehicle_routes_original(xml_file_original, junction_directions_original)

# junction_counts_smaller = parse_vehicle_directions_smaller(xml_file_smaller, junction_directions_smaller)

# 将统计结果转换为DataFrame以便绘图
dataframes_original = {}
for junc_id, dir_counts in junction_counts_original.items():
    df = pd.DataFrame(list(dir_counts.items()), columns=["Direction", "Vehicle Count"])
    dataframes_original[junc_id] = df

# 绘制每个路口的柱状图
for junc_id, df in dataframes_original.items():
    plt.figure(figsize=(8, 6))
    plt.bar(df["Direction"], df["Vehicle Count"], color="skyblue")
    plt.title(f"Demand Distribution at Junction {junc_id}")
    plt.xlabel("Direction")
    plt.ylabel("Vehicle Count")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

    # 计算并打印总车辆数量
    total_vehicles = df["Vehicle Count"].sum()
    print(f"Total Vehicle Count at Junction {junc_id}: {total_vehicles}")