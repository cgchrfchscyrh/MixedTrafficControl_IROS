import matplotlib.pyplot as plt

# 数据
data_20 = {
    "Minimum": 728,
    "Q1": 1066,
    "Median": 1272,
    "Q3": 1279,
    "Maximum": 1297
}

data_60 = {
    "Minimum": 563,
    "Q1": 1340,
    "Median": 1356,
    "Q3": 1391,
    "Maximum": 1400
}

data_70 = {
    "Minimum": 890,
    "Q1": 1335.0,
    "Median": 1394.0,
    "Q3": 1413.0,
    "Maximum": 1425
}

data_80 = {
    "Minimum": 524,
    "Q1": 1327.0,
    "Median": 1359.0,
    "Q3": 1410.0,
    "Maximum": 1419
}

# 构造箱线图数据
box_data = [
    [data_20["Minimum"], data_20["Q1"], data_20["Median"], data_20["Q3"], data_20["Maximum"]],
    [data_60["Minimum"], data_60["Q1"], data_60["Median"], data_60["Q3"], data_60["Maximum"]],
    [data_70["Minimum"], data_70["Q1"], data_70["Median"], data_70["Q3"], data_70["Maximum"]],
    [data_80["Minimum"], data_80["Q1"], data_80["Median"], data_80["Q3"], data_80["Maximum"]]
]

# 添加固定值数据
fixed_value = 988

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
plt.title("Throughput of 100 times Evaluation\ncontrol junction 2093101229 (332)")
plt.xlabel("RV rate")
plt.ylabel("Number of vehicles")
plt.xticks([20, 60, 70, 80, 120], ["20%", "60%", "70%", "80%", "TL"])
plt.grid(axis="y", linestyle="--", alpha=0.7)

# 显示图形
plt.show()