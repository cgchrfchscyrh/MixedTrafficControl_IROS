import matplotlib.pyplot as plt
import numpy as np

rate = ['10','20','30', '40','50', '60', '70', '80', '90', '100']

data_points = [
    (8.6, 11.88, 0, 1.82), (10.37, 12.63, 1.44, 0), (10.04, 9.33, 1.3, 1.06), (10.36, 10.96, 3, 0), (12.17, 11.89, 1.13, 0),
    (14.36, 9.8, 1.26, 0.84), (9.42, 0.0, 1.18, 0.0), (11.61, 10.51, 1.54, 0), (0, 0, 1.6, 0), (14.06, 0, 1.38, 0)
]

# 提取数据
values1, values2, values3, values4 = zip(*data_points)

# 设置柱状图的宽度
bar_width = 0.35  
x = np.arange(len(rate))  # x 轴位置

# 创建图形
fig, ax = plt.subplots(figsize=(12, 4))

# 绘制柱状图
bars1 = ax.bar(x - bar_width/4, values1, bar_width, color='blue', label='Ori-Flexible')
bars2 = ax.bar(x + bar_width/4, values2, bar_width, color='orange', label='Ori-Standard')
bars3 = ax.bar(x + bar_width/2, values3, bar_width, color='red', label='8U6S-Flexible')
bars4 = ax.bar(x + 3*bar_width/4, values4, bar_width, color='green', label='8U6S-Standard')

# 设置 x 轴
ax.set_xticks(x)
ax.set_xticklabels(rate, fontsize=28)

# 设置 y 轴
ax.set_ylabel("Collision rate (%)", fontsize=30)
ax.set_xlabel("RV rate (%)", fontsize=32)
plt.yticks(fontsize=30)

# 显示图例
ax.legend(fontsize=30)

# 调整布局
plt.tight_layout()

# 显示图像
plt.show()