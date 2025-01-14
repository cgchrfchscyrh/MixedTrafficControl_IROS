import matplotlib.pyplot as plt

# 数据
data_20 = {
    "Minimum": 2.9915821428571427,
    "Q1": 8.625665313852814,
    "Median": 13.84178013618326,
    "Q3": 23.11536380772006,
    "Maximum": 79.93873187229437
}

data_60 = {
    "Minimum": 5.982695274170274,
    "Q1": 18.000965755772004,
    "Median": 24.698835790945168,
    "Q3": 33.24061631493507,
    "Maximum": 83.67951968836985
}

data_80 = {
    "Minimum": 9.496094660894661,
    "Q1": 17.23777956349206,
    "Median": 22.149869016053394,
    "Q3": 29.229318215118216,
    "Maximum": 57.45423483764859
}

# 构造箱线图数据
box_data = [
    [data_20["Minimum"], data_20["Q1"], data_20["Median"], data_20["Q3"], data_20["Maximum"]],
    [data_60["Minimum"], data_60["Q1"], data_60["Median"], data_60["Q3"], data_60["Maximum"]],
    [data_80["Minimum"], data_80["Q1"], data_80["Median"], data_80["Q3"], data_80["Maximum"]]
]

# 添加固定值数据
fixed_value = 7.17

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
plt.title("Average Wait Time of 100 times Evaluation\ncontrol junction 12203246695")
plt.xlabel("RV rate")
plt.ylabel("Time (s)")
plt.xticks([20, 60, 80, 120], ["20%", "60%", "80%", "TL"])
plt.grid(axis="y", linestyle="--", alpha=0.7)

# 显示图形
plt.show()