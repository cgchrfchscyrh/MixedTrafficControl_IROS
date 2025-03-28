import matplotlib.pyplot as plt

# 数据
data_20 = {
    "Minimum":424.23,
    "Q1": 455.8,
    "Median": 469.89,
    "Q3": 482.06,
    "Maximum": 507.78
}

data_30 = {
    "Minimum":417.23,
    "Q1": 453.8,
    "Median": 468.89,
    "Q3": 477.06,
    "Maximum": 501.78
}

data_40 = {
    "Minimum":431.23,
    "Q1": 465.8,
    "Median": 477.89,
    "Q3": 486.06,
    "Maximum": 522.78
}

data_50 = {
    "Minimum": 408.28,
    "Q1": 458.71,
    "Median": 471.86,
    "Q3": 481.02,
    "Maximum": 521.5
}

data_60 = {
    "Minimum": 456.13,
    "Q1": 480.55,
    "Median": 494.72,
    "Q3": 511.91,
    "Maximum":  544.72
}

data_70 = {
    "Minimum": 453.28,
    "Q1": 474.77,
    "Median": 490.9,
    "Q3": 500.02,
    "Maximum": 538.39
}

data_80 = {
    "Minimum": 452.35,
    "Q1": 482.65,
    "Median": 493.76,
    "Q3": 505.94,
    "Maximum": 526.22
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
    # [data_20["Minimum"], data_20["Q1"], data_20["Median"], data_20["Q3"], data_20["Maximum"]],
    # [data_30["Minimum"], data_30["Q1"], data_30["Median"], data_30["Q3"], data_30["Maximum"]],
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
ax.boxplot(box_data, vert=True, positions=[40, 50, 60, 70, 80, 90], widths=5, patch_artist=True,
           boxprops=dict(facecolor="lightblue"), medianprops=dict(color="red"), whis=(0,100))

# boxplot = ax.boxplot(box_data, vert=True, positions=[20, 60, 80, 100], widths=10, patch_artist=True,
#                      boxprops=dict(facecolor="lightblue"), medianprops=dict(color="red"),
#                      flierprops=dict(marker='.'))

# 设置标题和轴标签
# plt.title("Average throughput of 100 times Evaluation")
# plt.xlabel("RV rate")
plt.ylabel("Vehicle throughput (v/500s)", fontsize=16)
plt.xticks([40, 50, 60, 70, 80, 90], ["RV: 40%", "RV: 50%", "RV: 60%", "RV: 70%", "RV: 80%", "TL"], rotation=60, fontsize=16)
plt.yticks(fontsize=16)
plt.grid(axis="y", linestyle="--", alpha=0.7)

# 显示图形
plt.show()