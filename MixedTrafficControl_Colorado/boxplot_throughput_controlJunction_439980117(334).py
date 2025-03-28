import matplotlib.pyplot as plt

# 数据
data_20 = {
    "Minimum": 636,
    "Q1": 798,
    "Median": 838,
    "Q3": 865,
    "Maximum": 874
}

data_60 = {
    "Minimum": 619,
    "Q1": 888.0,
    "Median": 895.0,
    "Q3": 915.25,
    "Maximum": 931
}

data_70 = {
    "Minimum": 643,
    "Q1": 917.75,
    "Median": 943.0,
    "Q3": 965.0,
    "Maximum": 968
}

data_80 = {
    "Minimum": 557,
    "Q1": 910.0,
    "Median": 924.5,
    "Q3": 934.0,
    "Maximum": 937
}

# 构造箱线图数据
box_data = [
    [data_20["Minimum"], data_20["Q1"], data_20["Median"], data_20["Q3"], data_20["Maximum"]],
    [data_60["Minimum"], data_60["Q1"], data_60["Median"], data_60["Q3"], data_60["Maximum"]],
    [data_70["Minimum"], data_70["Q1"], data_70["Median"], data_70["Q3"], data_70["Maximum"]],
    [data_80["Minimum"], data_80["Q1"], data_80["Median"], data_80["Q3"], data_80["Maximum"]]
]

# 添加固定值数据
fixed_value = 781

# 更新箱线图数据
box_data.append([fixed_value])  # 固定值作为独立数据点

# 绘制箱线图
fig, ax = plt.subplots()
ax.boxplot(box_data, vert=True, positions=[20, 60, 70, 80, 120], widths=5, patch_artist=True,
           boxprops=dict(facecolor="lightblue"), medianprops=dict(color="red"))

# boxplot = ax.boxplot(box_data, vert=True, positions=[20, 60, 80, 100], widths=10, patch_artist=True,
#                      boxprops=dict(facecolor="lightblue"), medianprops=dict(color="red"),
#                      flierprops=dict(marker='.'))

# 设置标题和轴标签
plt.title("Throughput of 100 times Evaluation\ncontrol junction 439980117 (334)")
plt.xlabel("RV rate")
plt.ylabel("Number of vehicles")
plt.xticks([20, 60, 70, 80, 120], ["20%", "60%", "70%", "80%", "TL"])
plt.grid(axis="y", linestyle="--", alpha=0.7)

# 显示图形
plt.show()