import matplotlib.pyplot as plt

# 数据
data_20 = {
    "Minimum": 1.26,
    "Q1": 1.79,
    "Median": 1.96,
    "Q3": 2.14,
    "Maximum": 2.9
}

data_60 = {
    "Minimum": 1.27,
    "Q1": 1.59,
    "Median": 1.84,
    "Q3": 2.07,
    "Maximum": 2.77
}

data_70 = {
    "Minimum": 1.27,
    "Q1": 1.8,
    "Median": 2.08,
    "Q3": 2.24,
    "Maximum": 3.62
}

data_80 = {
    "Minimum": 2.72,
    "Q1": 4.73,
    "Median": 5.8,
    "Q3": 7.05,
    "Maximum": 10.7
}

data_90 = {
    "Minimum": 1.42,
    "Q1": 1.84,
    "Median": 2.1,
    "Q3": 2.38,
    "Maximum": 3.1
}

data_100 = {
    "Minimum": 2.45,
    "Q1": 2.45,
    "Median": 2.45,
    "Q3": 2.45,
    "Maximum": 2.45
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
fixed_value = 0.95

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
plt.title("Average Wait Time of 100 times Evaluation\n2052409323")
plt.xlabel("RV rate")
plt.ylabel("Time (s)")
plt.xticks([20, 60, 70, 80, 90, 100, 120], ["20%", "60%", "70%", "80%", "90%", "100%", "TL"])
plt.grid(axis="y", linestyle="--", alpha=0.7)

# 显示图形
plt.show()