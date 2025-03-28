import matplotlib.pyplot as plt

# 数据
data_20 = {
    "Minimum": 3.81,
    "Q1": 7.31,
    "Median": 8.66,
    "Q3": 10.8,
    "Maximum": 19.57
}

data_60 = {
    "Minimum": 2.77,
    "Q1": 4.72,
    "Median": 5.6,
    "Q3": 6.68,
    "Maximum": 9.82
}

data_70 = {
    "Minimum": 2.64,
    "Q1":  4.4,
    "Median": 5.54,
    "Q3": 6.3,
    "Maximum": 10.85
}

data_80 = {
    "Minimum":3.31,
    "Q1": 4.68,
    "Median": 5.57,
    "Q3": 6.42,
    "Maximum": 8.76
}

data_90 = {
    "Minimum": 5.18,
    "Q1": 6.64,
    "Median": 7.52,
    "Q3": 8.31,
    "Maximum": 12.92
}

data_100 = {
    "Minimum": 7.46,
    "Q1": 7.46,
    "Median": 7.46,
    "Q3": 7.46,
    "Maximum": 7.46
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
fixed_value = 7.26

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
plt.title("Average Wait Time of 100 times Evaluation\ncontrol junction 2052409422 (499)")
plt.xlabel("RV rate")
plt.ylabel("Time (s)")
plt.xticks([20, 60, 70, 80, 90, 100, 120], ["20%", "60%", "70%", "80%", "90%", "100%", "TL"])
plt.grid(axis="y", linestyle="--", alpha=0.7)

# 显示图形
plt.show()