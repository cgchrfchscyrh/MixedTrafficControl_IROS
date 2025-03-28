import matplotlib.pyplot as plt

# 数据
data_40 = {
    "Minimum":5.0,
    "Q1": 5.62,
    "Median": 5.94,
    "Q3": 6.28,
    "Maximum": 8.45
}

data_50 = {
    "Minimum": 5.39,
    "Q1": 6.73,
    "Median": 7.02,
    "Q3": 7.32,
    "Maximum": 8.57
}

data_60 = {
    "Minimum": 4.76,
    "Q1": 5.24,
    "Median": 5.51,
    "Q3": 5.78,
    "Maximum":  7.54
}

data_70 = {
    "Minimum": 4.76,
    "Q1": 5.64,
    "Median": 6.23,
    "Q3": 6.69,
    "Maximum": 8.34
}

data_80 = {
    "Minimum": 4.66,
    "Q1": 5.55,
    "Median": 5.95,
    "Q3": 6.35,
    "Maximum": 8.03
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
ax.boxplot(box_data, vert=True, positions=[40, 50, 60, 70, 80, 120], widths=5, patch_artist=True,
           boxprops=dict(facecolor="lightblue"), medianprops=dict(color="red"))

# ax.boxplot(box_data, vert=True, positions=[20, 60, 70, 80, 90, 100, 120], widths=5, patch_artist=True,
#            boxprops=dict(facecolor="lightblue"), medianprops=dict(color="red"))

# 设置标题和轴标签
plt.title("Average Wait Time of 100 times Evaluation")
plt.xlabel("RV rate")
plt.ylabel("Time (s)")
plt.xticks([40, 50, 60, 70, 80, 120], ["40%", "50%", "60%", "70%", "80%", "TL"])
plt.grid(axis="y", linestyle="--", alpha=0.7)

# 显示图形
plt.show()