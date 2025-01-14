import matplotlib.pyplot as plt

# 数据
data_20 = {
    "Minimum": 16.726626582894816,
    "Q1": 28.61619894392581,
    "Median": 35.16374614690252,
    "Q3": 43.565698565262956,
    "Maximum": 133.01489790965823
}

data_60 = {
    "Minimum": 12.20274290816981,
    "Q1": 18.574400038577956,
    "Median": 20.726034597656263,
    "Q3": 24.235838162956455,
    "Maximum": 44.374888420751915
}

data_80 = {
    "Minimum": 12.310039543694439,
    "Q1": 16.515489343412064,
    "Median": 19.97640613067425,
    "Q3": 23.47871508783438,
    "Maximum": 50.97839412937961
}

# 构造箱线图数据
box_data = [
    [data_20["Minimum"], data_20["Q1"], data_20["Median"], data_20["Q3"], data_20["Maximum"]],
    [data_60["Minimum"], data_60["Q1"], data_60["Median"], data_60["Q3"], data_60["Maximum"]],
    [data_80["Minimum"], data_80["Q1"], data_80["Median"], data_80["Q3"], data_80["Maximum"]]
]

# 添加固定值数据
fixed_value = 15.24

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
plt.title("Average Wait Time of 100 times Evaluation\ncontrol junction 2093101229")
plt.xlabel("RV rate")
plt.ylabel("Time (s)")
plt.xticks([20, 60, 80, 120], ["20%", "60%", "80%", "TL"])
plt.grid(axis="y", linestyle="--", alpha=0.7)

# 显示图形
plt.show()