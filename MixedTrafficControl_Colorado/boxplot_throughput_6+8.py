import matplotlib.pyplot as plt

# 数据
data_40 = {
    "Minimum":435.23,
    "Q1": 460.8,
    "Median": 468.89,
    "Q3": 476.06,
    "Maximum": 509.78
}

data_50 = {
    "Minimum": 383.28,
    "Q1": 439.71,
    "Median": 448.86,
    "Q3": 456.02,
    "Maximum": 492.5
}

data_60 = {
    "Minimum": 446.13,
    "Q1": 465.55,
    "Median": 476.72,
    "Q3": 486.91,
    "Maximum":  518.72
}

data_70 = {
    "Minimum": 404.28,
    "Q1": 442.77,
    "Median": 453.9,
    "Q3": 463.02,
    "Maximum": 481.39
}

data_80 = {
    "Minimum": 410.35,
    "Q1": 463.65,
    "Median": 475.76,
    "Q3": 486.94,
    "Maximum": 530.22
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
fixed_value = 454

# 更新箱线图数据
box_data.append([fixed_value])  # 固定值作为独立数据点

# 绘制箱线图
fig, ax = plt.subplots()
ax.boxplot(box_data, vert=True, positions=[40, 50, 60, 70, 80, 120], widths=5, patch_artist=True,
           boxprops=dict(facecolor="lightblue"), medianprops=dict(color="red"))

# boxplot = ax.boxplot(box_data, vert=True, positions=[20, 60, 80, 100], widths=10, patch_artist=True,
#                      boxprops=dict(facecolor="lightblue"), medianprops=dict(color="red"),
#                      flierprops=dict(marker='.'))

# 设置标题和轴标签
plt.title("Average throughput of 100 times Evaluation")
plt.xlabel("RV rate")
plt.ylabel("Number of vehicles")
plt.xticks([40, 50, 60, 70, 80, 120], ["40%", "50%", "60%", "70%", "80%", "TL"])
plt.grid(axis="y", linestyle="--", alpha=0.7)

# 显示图形
plt.show()