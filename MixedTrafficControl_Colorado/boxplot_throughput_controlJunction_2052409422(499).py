import matplotlib.pyplot as plt

# 数据
data_20 = {
    "Minimum": 651,
    "Q1": 989.5,
    "Median": 1020,
    "Q3": 1032,
    "Maximum": 1044
}

data_60 = {
    "Minimum": 664,
    "Q1": 1240.0,
    "Median": 1250.0,
    "Q3": 1284.0,
    "Maximum": 1289
}

data_70 = {
    "Minimum": 767,
    "Q1": 1225.0,
    "Median": 1272.0,
    "Q3": 1279.0,
    "Maximum": 1282
}

data_80 = {
    "Minimum": 821,
    "Q1": 1310.75,
    "Median": 1346.0,
    "Q3": 1355.0,
    "Maximum": 1357
}

# 构造箱线图数据
box_data = [
    [data_20["Minimum"], data_20["Q1"], data_20["Median"], data_20["Q3"], data_20["Maximum"]],
    [data_60["Minimum"], data_60["Q1"], data_60["Median"], data_60["Q3"], data_60["Maximum"]],
    [data_70["Minimum"], data_70["Q1"], data_70["Median"], data_70["Q3"], data_70["Maximum"]],
    [data_80["Minimum"], data_80["Q1"], data_80["Median"], data_80["Q3"], data_80["Maximum"]]
]

# 添加固定值数据
fixed_value = 956

# 更新箱线图数据
box_data.append([fixed_value])  # 固定值作为独立数据点

# 绘制箱线图
fig, ax = plt.subplots()
ax.boxplot(box_data, vert=True, positions=[20, 60, 70, 80, 120], widths=5, patch_artist=True,
           boxprops=dict(facecolor="lightblue"), medianprops=dict(color="red"))

# boxplot = ax.boxplot(box_data, vert=True, positions=[20, 60, 80, 100], widths=10, patch_artist=True,
#                      boxprops=dict(facecolor="lightblue"), medianprops=dict(color="red"),
#                      flierprops=dict(marker='.'))

# 设置标题和轴标签
plt.title("Throughput of 100 times Evaluation\ncontrol junction 2052409422 (499)")
plt.xlabel("RV rate")
plt.ylabel("Number of vehicles")
plt.xticks([20, 60, 70, 80, 120], ["20%", "60%", "70%", "80%", "TL"])
plt.grid(axis="y", linestyle="--", alpha=0.7)

# 显示图形
plt.show()