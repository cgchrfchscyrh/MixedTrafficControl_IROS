import matplotlib.pyplot as plt

# 数据
data_40 = {
    "Minimum":5.66,
    "Q1": 6.16,
    "Median": 6.43,
    "Q3": 6.71,
    "Maximum": 8.1
}

data_50 = {
    "Minimum": 6.6,
    "Q1": 7.55,
    "Median": 7.92,
    "Q3": 8.24,
    "Maximum": 11.51
}

data_60 = {
    "Minimum": 5.12,
    "Q1": 6.03,
    "Median": 6.41,
    "Q3": 6.85,
    "Maximum":  8.11
}

data_70 = {
    "Minimum": 6.82,
    "Q1": 7.6,
    "Median": 7.85,
    "Q3": 8.13,
    "Maximum": 8.94
}

data_80 = {
    "Minimum": 5.26,
    "Q1": 5.83,
    "Median": 6.31,
    "Q3": 6.74,
    "Maximum": 10.16
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