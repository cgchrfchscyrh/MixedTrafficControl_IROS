import matplotlib.pyplot as plt

# 数据
data_20 = {
    "Minimum": 24.725960920979446,
    "Q1": 47.431824328846986,
    "Median": 60.79718078025212,
    "Q3": 77.29468525874289,
    "Maximum": 228.37431380576243
}

data_60 = {
    "Minimum": 20.343517910176725,
    "Q1": 40.6815982840844,
    "Median": 57.30810921832051,
    "Q3": 73.48715400183201,
    "Maximum": 183.8451854251091
}

data_80 = {
    "Minimum": 22.734274807582125,
    "Q1": 35.36237580795452,
    "Median": 44.60762556308903,
    "Q3": 64.55983782489835,
    "Maximum": 228.8580035464492
}

# 构造箱线图数据
box_data = [
    [data_20["Minimum"], data_20["Q1"], data_20["Median"], data_20["Q3"], data_20["Maximum"]],
    [data_60["Minimum"], data_60["Q1"], data_60["Median"], data_60["Q3"], data_60["Maximum"]],
    [data_80["Minimum"], data_80["Q1"], data_80["Median"], data_80["Q3"], data_80["Maximum"]]
]

# 添加固定值数据
fixed_value = 13.21

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
plt.title("Average Wait Time of 100 times Evaluation\ncontrol junction 439980117")
plt.xlabel("RV rate")
plt.ylabel("Time (s)")
plt.xticks([20, 60, 80, 120], ["20%", "60%", "80%", "TL"])
plt.grid(axis="y", linestyle="--", alpha=0.7)

# 显示图形
plt.show()