import matplotlib.pyplot as plt

# 数据
data_20 = {
    "Minimum": 4.78,
    "Q1": 6.94,
    "Median": 7.51,
    "Q3":8.77,
    "Maximum": 12.18
}

data_60 = {
    "Minimum": 4.93,
    "Q1": 7.36,
    "Median": 7.89,
    "Q3": 8.79,
    "Maximum": 11.17
}

data_70 = {
    "Minimum": 6.6,
    "Q1": 8.11,
    "Median": 9.11,
    "Q3": 10.35,
    "Maximum": 15.46
}

data_80 = {
    "Minimum": 7.77,
    "Q1": 10.14,
    "Median": 11.18,
    "Q3": 12.91,
    "Maximum": 21.66
}

data_90 = {
    "Minimum": 5.67,
    "Q1": 7.35,
    "Median": 7.97,
    "Q3": 8.93,
    "Maximum": 13.06
}

data_100 = {
    "Minimum": 14.12,
    "Q1": 14.12,
    "Median": 14.12,
    "Q3": 14.12,
    "Maximum": 14.12
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
fixed_value = 7.62

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
plt.title("Average Wait Time of 100 times Evaluation\n1289585639")
plt.xlabel("RV rate")
plt.ylabel("Time (s)")
plt.xticks([20, 60, 70, 80, 90, 100, 120], ["20%", "60%", "70%", "80%", "90%", "100%", "TL"])
plt.grid(axis="y", linestyle="--", alpha=0.7)

# 显示图形
plt.show()