import matplotlib.pyplot as plt
import numpy as np

directions = ['topstraight', 'topleft','rightstraight', 'rightleft','bottomstraight', 'bottomleft', 'leftstraight', 'leftleft']

# 设定 14 个 intersection 对应的 2 个数据点（示例数据）
data_points = [
    (30.47, 16.69), (9.79, 18.88), (5.5, 15.78), (4.46, 7.90),
    (29.34, 14.64), (0.0, 0.0), (16.06, 20.98), (22.5, 26.25)
]

# TL
# --- JuncID 334 Keyword-wise Wait Times ---
# Direction topstraight: 16.69s
# Direction topleft: 18.88s
# Direction rightstraight: 15.78s
# Direction rightleft: 7.90s
# Direction bottomstraight: 14.64s
# Direction bottomleft: 0.00s
# Direction leftstraight: 20.98s
# Direction leftleft: 26.25s

# 提取数据
values1, values2 = zip(*data_points)

# 设置柱状图的宽度
bar_width = 0.35  
x = np.arange(len(directions))  # x 轴位置

# 创建图形
fig, ax = plt.subplots(figsize=(12, 4))

# 绘制柱状图
bars1 = ax.bar(x - bar_width/2, values1, bar_width, color='blue', label='Ours')
bars2 = ax.bar(x + bar_width/2, values2, bar_width, color='orange', label='TL')

# 设置 x 轴
ax.set_xticks(x)
ax.set_xticklabels(directions, fontsize=28)

# 设置 y 轴
ax.set_ylabel("Avg. Waiting Time (s)", fontsize=30)
ax.set_xlabel("Direction", fontsize=32)
plt.yticks(fontsize=30)

# 显示图例
ax.legend(fontsize=30)

# 调整布局
plt.tight_layout()

# 显示图像
plt.show()