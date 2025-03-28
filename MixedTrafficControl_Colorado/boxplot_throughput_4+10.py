import matplotlib.pyplot as plt

# 数据
data_40 = {
    "Minimum":401.23,
    "Q1": 442.8,
    "Median": 452.89,
    "Q3": 462.06,
    "Maximum": 508.78
}

data_50 = {
    "Minimum": 420.28,
    "Q1": 449.71,
    "Median": 459.86,
    "Q3": 471.02,
    "Maximum": 508.5
}

data_60 = {
    "Minimum": 427.13,
    "Q1": 454.55,
    "Median": 468.72,
    "Q3": 478.91,
    "Maximum":  504.72
}

data_70 = {
    "Minimum": 411.28,
    "Q1": 445.77,
    "Median": 457.9,
    "Q3": 467.02,
    "Maximum": 497.39
}

data_80 = {
    "Minimum": 380.35,
    "Q1": 458.65,
    "Median": 466.76,
    "Q3": 479.94,
    "Maximum": 497.22
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