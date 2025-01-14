import matplotlib.pyplot as plt

# 数据
data_20 = {
    "Minimum": 1009,
    "Q1": 1111.75,
    "Median": 1150.0,
    "Q3": 1183.25,
    "Maximum": 1310
}

data_60 = {
    "Minimum": 1058,
    "Q1": 1136,
    "Median": 1158,
    "Q3": 1180.25,
    "Maximum": 1245
}

data_80 = {
    "Minimum": 1037,
    "Q1": 1151.75,
    "Median": 1171.5,
    "Q3": 1193.25,
    "Maximum": 1247
}

# 构造箱线图数据
box_data = [
    [data_20["Minimum"], data_20["Q1"], data_20["Median"], data_20["Q3"], data_20["Maximum"]],
    [data_60["Minimum"], data_60["Q1"], data_60["Median"], data_60["Q3"], data_60["Maximum"]],
    [data_80["Minimum"], data_80["Q1"], data_80["Median"], data_80["Q3"], data_80["Maximum"]]
]

# 添加固定值数据
fixed_value = 1312

# 更新箱线图数据
box_data.append([fixed_value])  # 固定值作为独立数据点

# 绘制箱线图
fig, ax = plt.subplots()
ax.boxplot(box_data, vert=True, positions=[20, 60, 80, 120], widths=10, patch_artist=True,
           boxprops=dict(facecolor="lightblue"), medianprops=dict(color="red"))

# boxplot = ax.boxplot(box_data, vert=True, positions=[20, 60, 80, 100], widths=10, patch_artist=True,
#                      boxprops=dict(facecolor="lightblue"), medianprops=dict(color="red"),
#                      flierprops=dict(marker='.'))

# 设置标题和轴标签
plt.title("Average throughput of 100 times Evaluation")
plt.xlabel("RV rate")
plt.ylabel("Number of vehicles")
plt.xticks([20, 60, 80, 120], ["20%", "60%", "80%", "TL"])
plt.grid(axis="y", linestyle="--", alpha=0.7)

# 显示图形
plt.show()