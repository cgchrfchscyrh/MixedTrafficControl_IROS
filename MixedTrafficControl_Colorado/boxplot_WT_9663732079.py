import matplotlib.pyplot as plt

# 数据
data_20 = {
    "Minimum": 2.68,
    "Q1": 4.38,
    "Median": 4.76,
    "Q3": 5.26,
    "Maximum": 6.58
}

data_60 = {
    "Minimum": 2.56,
    "Q1": 3.71,
    "Median": 4.51,
    "Q3": 5.09,
    "Maximum": 6.09
}

data_70 = {
    "Minimum": 2.66,
    "Q1": 3.74,
    "Median":  4.46,
    "Q3": 5.29,
    "Maximum": 6.4
}

data_80 = {
    "Minimum": 3.18,
    "Q1": 4.4,
    "Median": 4.94,
    "Q3": 5.62,
    "Maximum": 7.02
}

data_90 = {
    "Minimum": 2.65,
    "Q1": 4.21,
    "Median": 4.62,
    "Q3": 5.18,
    "Maximum": 6.81
}

data_100 = {
    "Minimum": 5.35,
    "Q1": 5.35,
    "Median": 5.35,
    "Q3": 5.35,
    "Maximum": 5.35
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
fixed_value = 5.10

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
plt.title("Average Wait Time of 100 times Evaluation\n9663732079")
plt.xlabel("RV rate")
plt.ylabel("Time (s)")
plt.xticks([20, 60, 70, 80, 90, 100, 120], ["20%", "60%", "70%", "80%", "90%", "100%", "TL"])
plt.grid(axis="y", linestyle="--", alpha=0.7)

# 显示图形
plt.show()