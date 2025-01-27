import json
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import xml.etree.ElementTree as ET

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

def extract_edge_id(lane_id):
    """从 lane_id 提取 edge_id, 去掉下划线及后面的数字"""
    if lane_id:
        return lane_id.split("_")[0]
    return None

# 读取 JSON 数据
with open("smaller_0.8_evaluation_results_20250127_140908.json", "r") as f:
    data = json.load(f)

columns = ['run', 'junction', 'total_vehicles_enter', 'total_vehicles_pass', 'RL_enter', 'IDM_enter', 'RL_pass', 'IDM_pass']
plot_data = []
path_data = []
missing_destinations = []

# 遍历每次运行的数据
for run_name, run_data in data.items():
    run_id = int(run_name.split('_')[-1])  # 获取运行编号
    for junc_id, junc_data in run_data["junctions"].items():
        total_vehicles_enter = junc_data["total_vehicles_enter"]
        total_vehicles_pass = junc_data["total_vehicles_pass"]
        vehicle_types_enter = junc_data["vehicle_types_enter"]
        vehicle_types_pass = junc_data["vehicle_types_pass"]
        rl_count_enter = vehicle_types_enter.get("RL", 0)
        idm_count_enter = vehicle_types_enter.get("IDM", 0)
        rl_count_pass = vehicle_types_pass.get("RL", 0)
        idm_count_pass = vehicle_types_pass.get("IDM", 0)
        
        # 添加到总表格数据中
        plot_data.append([run_id, junc_id, total_vehicles_enter, total_vehicles_pass, rl_count_enter, idm_count_enter, rl_count_pass, idm_count_pass])
        
        # # 提取路径信息并转换为 edge_id
        # vehicle_paths = junc_data["vehicle_paths"]
        # for veh_id, path_info in vehicle_paths.items():
        #     origin = extract_edge_id(path_info["origin"])
        #     destination = extract_edge_id(path_info["destination"])
        #     if origin and destination:  # 只记录有效的 origin-destination 组合
        #         path_data.append([run_id, junc_id, origin, destination])

        # 提取路径信息并检查是否有未抵达的车辆
        vehicle_paths = junc_data["vehicle_paths"]
        for veh_id, path_info in vehicle_paths.items():
            origin = extract_edge_id(path_info["origin"])
            destination = extract_edge_id(path_info["destination"])

            if destination is None:  # 如果没有抵达目的地
                missing_destinations.append(veh_id)

# 转换为 DataFrame
df = pd.DataFrame(plot_data, columns=columns)
# df_paths = pd.DataFrame(path_data, columns=["run", "junction", "origin", "destination"])
# df_paths["origin-destination"] = df_paths["origin"] + " -> " + df_paths["destination"]

# 统计 OD 组合在每次运行中的出现次数
# grouped = df_paths.groupby(["junction", "origin-destination"])["run"].count().reset_index(name="vehicle_count")

# 计算 100 次运行中 OD 组合的总出现次数和平均值
# total_counts = grouped.groupby(["junction", "origin-destination"])["vehicle_count"].sum().reset_index(name="total_count")
# average_counts = total_counts.copy()
# average_counts["average_count"] = average_counts["total_count"] / 100

# # 打印 100 次叠加后的 OD 组合总出现次数
# print("Total OD Combination Counts Over 100 Runs:")
# print(total_counts)

# # 打印 100 次运行后平均的 OD 组合出现次数
# print("\nAverage OD Combination Counts Over 100 Runs:")
# print(average_counts)

# 使用 Seaborn 绘制箱线图
sns.set(style="whitegrid")

# 绘制每个 junction 的统计箱线图
plt.figure(figsize=(12, 6))
sns.boxplot(x="junction", y="total_vehicles_enter", data=df)
plt.title("Total Vehicles Enter per Junction")
plt.xlabel("Junction")
plt.ylabel("Total Vehicles Enter")
plt.show()

plt.figure(figsize=(12, 6))
sns.boxplot(x="junction", y="total_vehicles_pass", data=df)
plt.title("Total Vehicles Pass per Junction")
plt.xlabel("Junction")
plt.ylabel("Total Vehicles Pass")
plt.show()

plt.figure(figsize=(12, 6))
sns.boxplot(x="junction", y="RL_enter", data=df)
plt.title("RL Vehicles Enter per Junction")
plt.xlabel("Junction")
plt.ylabel("Number of RL Vehicles Enter")
plt.show()

plt.figure(figsize=(12, 6))
sns.boxplot(x="junction", y="RL_pass", data=df)
plt.title("RL Vehicles Pass per Junction")
plt.xlabel("Junction")
plt.ylabel("Number of RL Vehicles Pass")
plt.show()

plt.figure(figsize=(12, 6))
sns.boxplot(x="junction", y="IDM_enter", data=df)
plt.title("IDM Vehicles Enter per Junction")
plt.xlabel("Junction")
plt.ylabel("Number of IDM Vehicles Enter")
plt.show()

plt.figure(figsize=(12, 6))
sns.boxplot(x="junction", y="IDM_pass", data=df)
plt.title("IDM Vehicles Pass per Junction")
plt.xlabel("Junction")
plt.ylabel("Number of IDM Vehicles Pass")
plt.show()

# # 绘制每个 junction 的 OD 组合的平均柱状图
# junctions = average_counts["junction"].unique()

# for junction in junctions:
#     plt.figure(figsize=(14, 8))
#     subset = average_counts[average_counts["junction"] == junction]
#     sns.barplot(
#         data=subset, 
#         x="origin-destination", 
#         y="average_count", 
#         palette="viridis"
#     )
#     plt.xticks(rotation=45, ha="right")
#     plt.title(f"Average Vehicle Counts by Origin-Destination at Junction {junction}", fontsize=16)
#     plt.xlabel("Origin-Destination Combination", fontsize=12)
#     plt.ylabel("Average Vehicle Count", fontsize=12)
#     plt.tight_layout()
#     plt.show()

# 定义解析 XML 的函数
def analyze_missing_destinations_original(xml_file, missing_destinations, junction_directions):
    """
    从 XML 文件中查询 missing_destinations 中车辆的路线，并统计各路口方向的未抵达车辆数。
    """
    tree = ET.parse(xml_file)
    root = tree.getroot()

    # 初始化每个路口方向的计数
    junction_counts = {
        junc_id: {direction: 0 for direction in directions}
        for junc_id, directions in junction_directions.items()
    }

    # 遍历所有车辆
    for vehicle in root.findall("vehicle"):
        veh_id = vehicle.get("id")
        if veh_id not in missing_destinations:
            continue  # 跳过不在 missing_destinations 中的车辆

        route_edges = vehicle.find("route").get("edges").split()  # 获取车辆的路线
        matched_directions = []  # 记录每辆车的匹配方向

        for junc_id, directions in junction_directions.items():
            for dir_label, edge_combo in directions.items():
                if all(edge in route_edges for edge in edge_combo):
                    junction_counts[junc_id][dir_label] += 1
                    matched_directions.append((junc_id, dir_label))
                    break  # 一旦匹配了一个方向，停止检查当前 junction 的其他方向

        # # 打印每辆车的分析结果
        # if matched_directions:
        #     print(f"{vehicle.get('id')}: {matched_directions}")
        # else:
        #     print(f"{vehicle.get('id')} - No matches.")

    return junction_counts

def parse_vehicle_directions_smaller(xml_file, missing_destinations, junction_directions):
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

    # 遍历所有车辆
    for vehicle in root.findall("vehicle"):
        veh_id = vehicle.get("id")
        if veh_id not in missing_destinations:
            continue  # 跳过不在 missing_destinations 中的车辆

        route_edges = vehicle.find("route").get("edges").split()  # 获取车辆的路线
        matched_directions = []  # 记录每辆车的匹配方向

        for junc_id, directions in junction_directions.items():
            for dir_label, edge_combos in directions.items():
                for combo in edge_combos:
                    combo_edges = combo.split()
                    if all(edge in route_edges for edge in combo_edges):
                        junction_counts[junc_id][dir_label] += 1
                        matched_directions.append((junc_id, dir_label))
                        break  # 一旦匹配了一个方向，停止检查当前 junction 的其他方向

    return junction_counts

# 示例 missing_destinations 和 XML 文件路径
xml_file_original = "newroute1220_start0.xml"
xml_file_smaller = "colorado_smaller_1000s_7911v.rou.xml"  # 替换为你的XML文件路径

# 调用函数解析 XML 文件
junction_counts = parse_vehicle_directions_smaller(xml_file_smaller, missing_destinations, junction_directions_smaller)

# 将统计结果转换为 DataFrame 以便绘图
dataframes = {}
for junc_id, dir_counts in junction_counts.items():
    df = pd.DataFrame(list(dir_counts.items()), columns=["Direction", "Missing Vehicle Count"])
    dataframes[junc_id] = df

# 绘制每个路口的柱状图
for junc_id, df in dataframes.items():
    plt.figure(figsize=(10, 6))
    plt.bar(df["Direction"], df["Missing Vehicle Count"], color="salmon")
    plt.title(f"Missing Destination Vehicles at Junction {junc_id}")
    plt.xlabel("Direction")
    plt.ylabel("Missing Vehicle Count")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()