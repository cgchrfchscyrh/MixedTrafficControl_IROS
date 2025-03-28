import matplotlib.pyplot as plt

# 数据
data_20 = {
    "Minimum": 4.55,
    "Q1": 5.11,
    "Median": 5.47,
    "Q3":  5.7,
    "Maximum": 6.79
}

data_60 = {
    "Minimum": 4.41,
    "Q1": 5.07,
    "Median": 5.24,
    "Q3": 5.48,
    "Maximum": 6.86
}

data_70 = {
    "Minimum": 4.58,
    "Q1": 5.19,
    "Median": 5.47,
    "Q3": 5.75,
    "Maximum": 6.77
}

data_80 = {
    "Minimum":  4.87,
    "Q1": 5.56,
    "Median": 5.92,
    "Q3":  6.37,
    "Maximum": 7.26
}

data_90 = {
    "Minimum": 4.68,
    "Q1": 5.15,
    "Median": 5.45,
    "Q3": 5.69,
    "Maximum": 7.2
}

data_100 = {
    "Minimum": 5.07,
    "Q1": 5.07,
    "Median": 5.07,
    "Q3": 5.07,
    "Maximum": 5.07
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
fixed_value = 3.07

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
plt.title("Average Wait Time of 100 times Evaluation\ junction 547498658")
plt.xlabel("RV rate")
plt.ylabel("Time (s)")
plt.xticks([20, 60, 70, 80, 90, 100, 120], ["20%", "60%", "70%", "80%", "90%", "100%", "TL"])
plt.grid(axis="y", linestyle="--", alpha=0.7)

# 显示图形
plt.show()