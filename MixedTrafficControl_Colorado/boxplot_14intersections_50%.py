import matplotlib.pyplot as plt
import numpy as np

# 生成 14 个 intersection，每个有 2 个数据点
intersections = [f"{i}" for i in range(1, 15)]

# 设定 14 个 intersection 对应的 2 个数据点（示例数据）
data_points = [
    (0.53, 5.27), (4.92, 3.07), (6.24, 7.26), (0.81, 0.95), (9.65, 9.74),
    (0.1, 5.10), (13.22, 12.89), (4.2, 7.62), (1.95, 1.91), (0.01, 0.28),
    (15.91, 17.83), (0.15, 0.79), (4.94, 4.19), (8.2, 9.49)
]

# 提取数据
values1, values2 = zip(*data_points)

# 设置柱状图的宽度
bar_width = 0.35  
x = np.arange(len(intersections))  # x 轴位置

# 创建图形
fig, ax = plt.subplots(figsize=(12, 4))

# 绘制柱状图
bars1 = ax.bar(x - bar_width/2, values1, bar_width, color='blue', label='Ours')
bars2 = ax.bar(x + bar_width/2, values2, bar_width, color='red', label='TL')

# 设置 x 轴
ax.set_xticks(x)
ax.set_xticklabels(intersections, fontsize=20)

# 设置 y 轴
ax.set_ylabel("Avg. Waiting Time (s)", fontsize=20)
ax.set_xlabel("Intersection", fontsize=22)
plt.yticks(fontsize=20)

# 添加网格线
# ax.grid(axis="y", linestyle="--", alpha=0.7)

# 显示图例
ax.legend(fontsize=20)

# 调整布局
plt.tight_layout()

# 显示图像
plt.show()