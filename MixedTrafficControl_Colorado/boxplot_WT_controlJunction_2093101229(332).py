import matplotlib.pyplot as plt

# 数据
data_20 = {
    "Minimum": 7.92,
    "Q1": 14.48,
    "Median": 17.91,
    "Q3": 21.17,
    "Maximum": 40.97
}

data_60 = {
    "Minimum": 5.59,
    "Q1": 8.64,
    "Median": 9.98,
    "Q3": 12.95,
    "Maximum": 20.57
}

data_70 = {
    "Minimum": 5.65,
    "Q1": 7.77,
    "Median": 9.13,
    "Q3": 11.18,
    "Maximum": 15.42
}

data_80 = {
    "Minimum": 5.3,
    "Q1": 7.19,
    "Median": 8.83,
    "Q3": 10.75,
    "Maximum": 18.56
}

data_90 = {
    "Minimum": 5.11,
    "Q1": 7.04,
    "Median": 8.12,
    "Q3": 9.63,
    "Maximum":  15.73
}

data_100 = {
    "Minimum": 8.97,
    "Q1": 8.97,
    "Median": 8.97,
    "Q3": 8.97,
    "Maximum": 8.97
}

# 构造箱线图数据
box_data = [
    [data_20["Minimum"], data_20["Q1"], data_20["Median"], data_20["Q3"], data_20["Maximum"]],
    [data_60["Minimum"], data_60["Q1"], data_60["Median"], data_60["Q3"], data_60["Maximum"]],
    [data_70["Minimum"], data_70["Q1"], data_70["Median"], data_70["Q3"], data_70["Maximum"]],
    [data_80["Minimum"], data_80["Q1"], data_80["Median"], data_80["Q3"], data_80["Maximum"]],
    [data_90["Minimum"], data_90["Q1"], data_90["Median"], data_90["Q3"], data_90["Maximum"]],
    [data_100["Minimum"], data_100["Q1"], data_100["Median"], data_100["Q3"], data_100["Maximum"]]
]

# 添加固定值数据
fixed_value = 9.74

# 更新箱线图数据
box_data.append([fixed_value])  # 固定值作为独立数据点

# 绘制箱线图
fig, ax = plt.subplots()
ax.boxplot(box_data, vert=True, positions=[20, 60, 70, 80, 90, 100, 120], widths=5, patch_artist=True,
           boxprops=dict(facecolor="lightblue"), medianprops=dict(color="red"))

# boxplot = ax.boxplot(box_data, vert=True, positions=[20, 60, 80, 100], widths=10, patch_artist=True,
#                      boxprops=dict(facecolor="lightblue"), medianprops=dict(color="red"),
#                      flierprops=dict(marker='.'))

# 设置标题和轴标签
plt.title("Average Wait Time of 100 times Evaluation\ncontrol junction 2093101229 (332)")
plt.xlabel("RV rate")
plt.ylabel("Time (s)")
plt.xticks([20, 60, 70, 80, 90, 100, 120], ["20%", "60%", "70%", "80%", "90%", "100%", "TL"])
plt.grid(axis="y", linestyle="--", alpha=0.7)

# 显示图形
plt.show()