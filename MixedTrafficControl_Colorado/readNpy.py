import numpy as np
import os
import matplotlib.pyplot as plt
from collections import defaultdict

# 定义数据路径
base_directory = "C:\\Users\\cgchr\\ray_results\\DQN_RV0.2\\histograms"

# 初始化数据存储
all_histograms = defaultdict(lambda: {"counts": [], "bins": None})

# 加载数据
for episode_dir in os.listdir(base_directory):
    episode_path = os.path.join(base_directory, episode_dir)
    if os.path.isdir(episode_path):
        for npy_file in os.listdir(episode_path):
            if npy_file.endswith(".npy"):
                file_path = os.path.join(episode_path, npy_file)
                # 加载 npy 文件内容
                data = np.load(file_path, allow_pickle=True).item()
                junc_id = npy_file.split("_")[1]  # 从文件名中提取路口 ID
                # 存储 bin 和 count 数据
                if all_histograms[junc_id]["bins"] is None:
                    all_histograms[junc_id]["bins"] = data["bins"]
                all_histograms[junc_id]["counts"].append(data["counts"])

# 计算每个路口的平均直方图并绘制
output_directory = "C:\\Users\\cgchr\\ray_results\\DQN_RV0.2\\aggregated_histograms"
os.makedirs(output_directory, exist_ok=True)

for junc_id, data in all_histograms.items():
    if len(data["counts"]) > 0:
        # 计算所有 worker 的平均值
        avg_counts = np.mean(data["counts"], axis=0)
        bins = data["bins"]
        
        # 绘制平均直方图
        plt.figure(figsize=(10, 6))
        plt.bar(bins[:-1], avg_counts, width=(bins[1] - bins[0]), align="edge", alpha=0.7, color="blue")
        plt.title(f"Average Waiting Time Histogram at Junction {junc_id}")
        plt.xlabel("Waiting Time (s)")
        plt.ylabel("Vehicle Count")
        plt.grid(True)
        
        # 保存图片
        output_file = os.path.join(output_directory, f"average_histogram_{junc_id}.jpg")
        plt.savefig(output_file, format="jpg")
        print(f"Saved average histogram for Junction {junc_id} to {output_file}")
        plt.close()
    else:
        print(f"No data available for Junction {junc_id}.")
