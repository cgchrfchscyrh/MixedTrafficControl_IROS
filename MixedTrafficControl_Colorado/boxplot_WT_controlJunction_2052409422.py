import matplotlib.pyplot as plt

# 数据
data_20 = {
    "Minimum": 18.60839019609089,
    "Q1": 31.708931159616817,
    "Median": 37.93214541035352,
    "Q3": 47.45475540908301,
    "Maximum": 151.41330706387112
}

data_60 = {
    "Minimum": 11.338547974219821,
    "Q1": 18.36278154261314,
    "Median": 20.40202532833113,
    "Q3": 24.29049724372278,
    "Maximum": 51.26370071753913
}

data_80 = {
    "Minimum": 8.273041826594458,
    "Q1": 13.930932613918056,
    "Median": 16.784105261675734,
    "Q3": 20.118448170453256,
    "Maximum": 34.807810945198426
}

# 构造箱线图数据
box_data = [
    [data_20["Minimum"], data_20["Q1"], data_20["Median"], data_20["Q3"], data_20["Maximum"]],
    [data_60["Minimum"], data_60["Q1"], data_60["Median"], data_60["Q3"], data_60["Maximum"]],
    [data_80["Minimum"], data_80["Q1"], data_80["Median"], data_80["Q3"], data_80["Maximum"]]
]

# 添加固定值数据
fixed_value = 10.89

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
plt.title("Average Wait Time of 100 times Evaluation\ncontrol junction 2052409422")
plt.xlabel("RV rate")
plt.ylabel("Time (s)")
plt.xticks([20, 60, 80, 120], ["20%", "60%", "80%", "TL"])
plt.grid(axis="y", linestyle="--", alpha=0.7)

# 显示图形
plt.show()