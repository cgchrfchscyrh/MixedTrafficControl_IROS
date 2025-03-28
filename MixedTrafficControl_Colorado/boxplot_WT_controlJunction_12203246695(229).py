import matplotlib.pyplot as plt

# 数据
data_20 = {
    "Minimum": 0.06,
    "Q1": 0.4,
    "Median":0.6,
    "Q3": 0.91,
    "Maximum": 9.06
}

data_60 = {
    "Minimum": 0.18,
    "Q1": 0.51,
    "Median": 0.88,
    "Q3": 1.21,
    "Maximum": 8.6
}

data_70 = {
    "Minimum": 0.07,
    "Q1": 0.49,
    "Median": 0.79,
    "Q3": 0.94,
    "Maximum": 6.09
}

data_80 = {
    "Minimum": 0.14,
    "Q1": 0.5,
    "Median": 0.75,
    "Q3": 1.08,
    "Maximum": 5.0
}

data_90 = {
    "Minimum": 0.1,
    "Q1": 0.43,
    "Median": 0.83,
    "Q3":  1.18,
    "Maximum": 18.01
}

data_100 = {
    "Minimum": 0.38,
    "Q1": 0.38,
    "Median": 0.38,
    "Q3": 0.38,
    "Maximum": 0.38
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
fixed_value = 5.27

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
plt.title("Average Wait Time of 100 times Evaluation\ncontrol junction 12203246695 (229)")
plt.xlabel("RV rate")
plt.ylabel("Time (s)")
plt.xticks([20, 60, 70, 80, 90, 100, 120], ["20%", "60%", "70%", "80%", "90%", "100%", "TL"])
plt.grid(axis="y", linestyle="--", alpha=0.7)

# 显示图形
plt.show()