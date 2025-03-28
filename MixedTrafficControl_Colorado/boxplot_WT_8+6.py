import matplotlib.pyplot as plt

# 数据
data_20 = {
    "Minimum":5.85,
    "Q1": 6.66,
    "Median": 7.02,
    "Q3": 7.61,
    "Maximum":9.57
}

data_30 = {
    "Minimum":5.41,
    "Q1": 6.25,
    "Median": 6.58,
    "Q3":  7.09,
    "Maximum": 9.11
}

data_40 = {
    "Minimum":4.63,
    "Q1": 5.52,
    "Median": 5.74,
    "Q3": 6.07,
    "Maximum": 7.95
}

data_50 = {
    "Minimum": 5.15,
    "Q1": 5.79,
    "Median": 6.11,
    "Q3": 6.65,
    "Maximum": 10.08
}

data_60 = {
    "Minimum": 4.49,
    "Q1": 4.94,
    "Median": 5.22,
    "Q3": 5.63,
    "Maximum":  6.44
}

data_70 = {
    "Minimum": 4.11,
    "Q1": 4.73,
    "Median": 4.91,
    "Q3": 5.23,
    "Maximum": 6.79
}

data_80 = {
    "Minimum": 4.4,
    "Q1": 5.3,
    "Median": 5.76,
    "Q3": 6.3,
    "Maximum": 7.32
}

data_90 = {
    "Minimum": 4.35,
    "Q1": 5.03,
    "Median": 5.24,
    "Q3": 5.44,
    "Maximum": 5.95
}

data_100 = {
    "Minimum": 5.05,
    "Q1": 5.05,
    "Median": 5.05,
    "Q3": 5.05,
    "Maximum": 5.05
}

# 构造箱线图数据
box_data = [
    # [data_20["Minimum"], data_20["Q1"], data_20["Median"], data_20["Q3"], data_20["Maximum"]],
    # [data_30["Minimum"], data_30["Q1"], data_30["Median"], data_30["Q3"], data_30["Maximum"]],
    # [data_40["Minimum"], data_40["Q1"], data_40["Median"], data_40["Q3"], data_40["Maximum"]],
    # [data_50["Minimum"], data_50["Q1"], data_50["Median"], data_50["Q3"], data_50["Maximum"]],
    # [data_60["Minimum"], data_60["Q1"], data_60["Median"], data_60["Q3"], data_60["Maximum"]],
    [data_70["Minimum"], data_70["Q1"], data_70["Median"], data_70["Q3"], data_70["Maximum"]],
    [data_80["Minimum"], data_80["Q1"], data_80["Median"], data_80["Q3"], data_80["Maximum"]],
    [data_90["Minimum"], data_90["Q1"], data_90["Median"], data_90["Q3"], data_90["Maximum"]],
    [data_100["Minimum"], data_100["Q1"], data_100["Median"], data_100["Q3"], data_100["Maximum"]]
]

# 添加固定值数据
TL = 6.31

# 更新箱线图数据
box_data.append([TL])  # 固定值作为独立数据点

# 绘制箱线图
fig, ax = plt.subplots()
ax.boxplot(box_data, vert=True, positions=[70, 80, 90, 100, 120], widths=5, patch_artist=True,
           boxprops=dict(facecolor="lightblue"), medianprops=dict(color="red"), whis=(0,100))

# 设置标题和轴标签
# plt.title("Average Wait Time of 100 times Evaluation")
# plt.xlabel("RV rate", fontsize=20, fontweight='bold')
plt.ylabel("Avg. Waiting Time (s)", fontsize=16)
plt.xticks([70, 80, 90, 100, 120], ["RV: 70%", "RV: 80%", "RV: 90%", "RV: 100%", "TL"], rotation=60, fontsize=16)
plt.yticks(fontsize=16)

plt.grid(axis="y", linestyle="--", alpha=0.7)

# 显示图形
plt.show()