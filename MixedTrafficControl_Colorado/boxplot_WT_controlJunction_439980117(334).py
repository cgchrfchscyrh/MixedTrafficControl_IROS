import matplotlib.pyplot as plt

# 数据
data_20 = {
    "Minimum": 14.9,
    "Q1": 21.52,
    "Median": 24.34,
    "Q3": 28.13,
    "Maximum": 44.14
}

data_60 = {
    "Minimum": 10.14,
    "Q1": 14.17,
    "Median": 16.31,
    "Q3": 19.88,
    "Maximum": 32.42
}

data_70 = {
    "Minimum": 9.13,
    "Q1": 14.16,
    "Median": 15.96,
    "Q3": 21.15,
    "Maximum": 44.24
}

data_80 = {
    "Minimum": 9.95,
    "Q1": 14.35,
    "Median": 16.01,
    "Q3": 18.46,
    "Maximum": 37.23
}

data_90 = {
    "Minimum": 12.85,
    "Q1": 16.23,
    "Median": 17.76,
    "Q3": 20.01,
    "Maximum": 27.56
}

data_100 = {
    "Minimum": 13.37,
    "Q1": 13.37,
    "Median": 13.37,
    "Q3": 13.37,
    "Maximum": 13.37
}

# 构造箱线图数据
box_data = [
    # [data_20["Minimum"], data_20["Q1"], data_20["Median"], data_20["Q3"], data_20["Maximum"]],
    # [data_60["Minimum"], data_60["Q1"], data_60["Median"], data_60["Q3"], data_60["Maximum"]],
    [data_70["Minimum"], data_70["Q1"], data_70["Median"], data_70["Q3"], data_70["Maximum"]],
    [data_80["Minimum"], data_80["Q1"], data_80["Median"], data_80["Q3"], data_80["Maximum"]],
    [data_90["Minimum"], data_90["Q1"], data_90["Median"], data_90["Q3"], data_90["Maximum"]],
    [data_100["Minimum"], data_100["Q1"], data_100["Median"], data_100["Q3"], data_100["Maximum"]]
]

# 添加固定值数据
TL = 15.14

# 更新箱线图数据
box_data.append([TL])  # 固定值作为独立数据点

# 绘制箱线图
fig, ax = plt.subplots()
ax.boxplot(box_data, vert=True, positions=[70, 80, 90, 100, 120], widths=5, patch_artist=True,
           boxprops=dict(facecolor="lightblue"), medianprops=dict(color="red"))

# 设置标题和轴标签
plt.title("Average Wait Time of junction 334")
plt.xlabel("RV rate")
plt.ylabel("Time (s)")
plt.xticks([70, 80, 90, 100, 120], ["RV: 70%", "RV: 80%", "RV: 90%", "RV: 100%", "TL"], rotation=60, fontsize=16)
plt.grid(axis="y", linestyle="--", alpha=0.7)

# 显示图形
plt.show()