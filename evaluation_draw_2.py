import json
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

def extract_edge_id(lane_id):
    """从 lane_id 提取 edge_id，去掉下划线及后面的数字"""
    if lane_id:
        return lane_id.split("_")[0]
    return None

# 读取 JSON 数据
with open("smaller_60%_evaluation_results_20250125_131256.json", "r") as f:
    data = json.load(f)

columns = ['run', 'junction', 'total_vehicles_enter', 'total_vehicles_pass', 'RL_enter', 'IDM_enter', 'RL_pass', 'IDM_pass']
plot_data = []
path_data = []

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
        
        # 提取路径信息并转换为 edge_id
        vehicle_paths = junc_data["vehicle_paths"]
        for veh_id, path_info in vehicle_paths.items():
            origin = extract_edge_id(path_info["origin"])
            destination = extract_edge_id(path_info["destination"])
            if origin and destination:  # 只记录有效的 origin-destination 组合
                path_data.append([run_id, junc_id, origin, destination])

# 转换为 DataFrame
df = pd.DataFrame(plot_data, columns=columns)
df_paths = pd.DataFrame(path_data, columns=["run", "junction", "origin", "destination"])
df_paths["origin-destination"] = df_paths["origin"] + " -> " + df_paths["destination"]

# 统计 OD 组合在每次运行中的出现次数
grouped = df_paths.groupby(["junction", "origin-destination"])["run"].count().reset_index(name="vehicle_count")

# 计算 100 次运行中 OD 组合的总出现次数和平均值
total_counts = grouped.groupby(["junction", "origin-destination"])["vehicle_count"].sum().reset_index(name="total_count")
average_counts = total_counts.copy()
average_counts["average_count"] = average_counts["total_count"] / 100

# 打印 100 次叠加后的 OD 组合总出现次数
print("Total OD Combination Counts Over 100 Runs:")
print(total_counts)

# 打印 100 次运行后平均的 OD 组合出现次数
print("\nAverage OD Combination Counts Over 100 Runs:")
print(average_counts)

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

# 绘制每个 junction 的 OD 组合的平均柱状图
junctions = average_counts["junction"].unique()

for junction in junctions:
    plt.figure(figsize=(14, 8))
    subset = average_counts[average_counts["junction"] == junction]
    sns.barplot(
        data=subset, 
        x="origin-destination", 
        y="average_count", 
        palette="viridis"
    )
    plt.xticks(rotation=45, ha="right")
    plt.title(f"Average Vehicle Counts by Origin-Destination at Junction {junction}", fontsize=16)
    plt.xlabel("Origin-Destination Combination", fontsize=12)
    plt.ylabel("Average Vehicle Count", fontsize=12)
    plt.tight_layout()
    plt.show()
