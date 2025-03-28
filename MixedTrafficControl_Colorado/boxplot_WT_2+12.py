import matplotlib.pyplot as plt

# 数据
data_20 = {
    "Minimum":5.36,
    "Q1": 5.79,
    "Median": 5.91,
    "Q3": 6.11,
    "Maximum": 6.73
}

data_30 = {
    "Minimum":5.34,
    "Q1": 5.82,
    "Median": 5.99,
    "Q3": 6.15,
    "Maximum": 7.11
}

data_40 = {
    "Minimum":5.23,
    "Q1": 5.8,
    "Median": 5.89,
    "Q3": 6.06,
    "Maximum": 6.78
}

data_50 = {
    "Minimum": 5.28,
    "Q1": 5.71,
    "Median": 5.86,
    "Q3": 6.02,
    "Maximum": 6.5
}

data_60 = {
    "Minimum": 5.13,
    "Q1": 5.55,
    "Median": 5.72,
    "Q3": 5.91,
    "Maximum":  6.72
}

data_70 = {
    "Minimum": 5.28,
    "Q1": 5.77,
    "Median": 5.9,
    "Q3": 6.02,
    "Maximum": 6.39
}

data_80 = {
    "Minimum": 5.35,
    "Q1": 5.65,
    "Median": 5.76,
    "Q3": 5.94,
    "Maximum": 6.22
}

# data_100 = {
#     "Minimum": 6.05,
#     "Q1": 6.05,
#     "Median": 6.05,
#     "Q3": 6.05,
#     "Maximum": 6.05
# }

# 构造箱线图数据
box_data = [
    [data_20["Minimum"], data_20["Q1"], data_20["Median"], data_20["Q3"], data_20["Maximum"]],
    [data_30["Minimum"], data_30["Q1"], data_30["Median"], data_30["Q3"], data_30["Maximum"]],
    [data_40["Minimum"], data_40["Q1"], data_40["Median"], data_40["Q3"], data_40["Maximum"]],
    [data_50["Minimum"], data_50["Q1"], data_50["Median"], data_50["Q3"], data_50["Maximum"]],
    [data_60["Minimum"], data_60["Q1"], data_60["Median"], data_60["Q3"], data_60["Maximum"]],
    [data_70["Minimum"], data_70["Q1"], data_70["Median"], data_70["Q3"], data_70["Maximum"]],
    [data_80["Minimum"], data_80["Q1"], data_80["Median"], data_80["Q3"], data_80["Maximum"]]
    # [data_90["Minimum"], data_90["Q1"], data_90["Median"], data_90["Q3"], data_90["Maximum"]],
    # [data_100["Minimum"], data_100["Q1"], data_100["Median"], data_100["Q3"], data_100["Maximum"]]
]

# 添加固定值数据
TL = 6.17

# 更新箱线图数据
box_data.append([TL])  # 固定值作为独立数据点

# 绘制箱线图
fig, ax = plt.subplots()
ax.boxplot(box_data, vert=True, positions=[20, 30, 40, 50, 60, 70, 80, 120], widths=5, patch_artist=True,
           boxprops=dict(facecolor="lightblue"), medianprops=dict(color="red"))

# ax.boxplot(box_data, vert=True, positions=[20, 60, 70, 80, 90, 100, 120], widths=5, patch_artist=True,
#            boxprops=dict(facecolor="lightblue"), medianprops=dict(color="red"))

# 设置标题和轴标签
plt.title("Average Wait Time of 100 times Evaluation")
plt.xlabel("RV rate")
plt.ylabel("Time (s)")
plt.xticks([20, 30, 40, 50, 60, 70, 80, 120], ["20%", "30%", "40%", "50%", "60%", "70%", "80%", "TL"])
plt.grid(axis="y", linestyle="--", alpha=0.7)

# 显示图形
plt.show()