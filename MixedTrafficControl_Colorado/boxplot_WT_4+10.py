import matplotlib.pyplot as plt

# 数据
data_40 = {
    "Minimum":5.92,
    "Q1": 6.64,
    "Median": 6.9,
    "Q3": 7.17,
    "Maximum": 8.37
}

data_50 = {
    "Minimum": 5.7,
    "Q1": 6.37,
    "Median": 6.63,
    "Q3": 6.94,
    "Maximum": 8.19
}

data_60 = {
    "Minimum": 5.38,
    "Q1": 5.98,
    "Median": 6.22,
    "Q3": 6.53,
    "Maximum": 7.84
}

data_70 = {
    "Minimum": 5.64,
    "Q1": 6.18,
    "Median": 6.36,
    "Q3": 6.54,
    "Maximum": 7.47
}

data_80 = {
    "Minimum": 5.19,
    "Q1": 5.71,
    "Median": 5.91,
    "Q3":  6.24,
    "Maximum": 10.34
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
ax.boxplot(box_data, vert=True, positions=[40, 50, 60, 70, 80, 90], widths=5, patch_artist=True,
           boxprops=dict(facecolor="lightblue"), medianprops=dict(color="red"), whis=(0,100))

# ax.boxplot(box_data, vert=True, positions=[20, 60, 70, 80, 90, 100, 120], widths=5, patch_artist=True,
#            boxprops=dict(facecolor="lightblue"), medianprops=dict(color="red"))

# 设置标题和轴标签
# plt.title("Average Wait Time of 100 times Evaluation")
# plt.xlabel("RV rate")
plt.ylabel("Avg. Waiting Time (s)", fontsize=16)
plt.xticks([40, 50, 60, 70, 80, 90], ["RV: 40%", "RV: 50%", "RV: 60%", "RV: 70%", "RV: 80%", "TL"], rotation=60, fontsize=16)
plt.yticks(fontsize=16)

plt.grid(axis="y", linestyle="--", alpha=0.7)

# 显示图形
plt.show()