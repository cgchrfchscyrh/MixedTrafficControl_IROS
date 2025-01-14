import matplotlib.pyplot as plt

# 数据
data_20 = {
    "Minimum": 8.054311579841233,
    "Q1": 10.73909994819803,
    "Median": 12.055528408178597,
    "Q3": 13.877800155165549,
    "Maximum": 19.195333890515037
}

data_60 = {
    "Minimum": 6.863474861278062,
    "Q1": 9.180230215454328,
    "Median": 10.155860389935619,
    "Q3": 11.79450894809004,
    "Maximum": 16.113811496293604
}

data_80 = {
    "Minimum": 6.831750183899727,
    "Q1": 8.47543334675992,
    "Median": 9.475127227981632,
    "Q3": 10.455469971221824,
    "Maximum": 18.71397201915452
}

# 构造箱线图数据
box_data = [
    [data_20["Minimum"], data_20["Q1"], data_20["Median"], data_20["Q3"], data_20["Maximum"]],
    [data_60["Minimum"], data_60["Q1"], data_60["Median"], data_60["Q3"], data_60["Maximum"]],
    [data_80["Minimum"], data_80["Q1"], data_80["Median"], data_80["Q3"], data_80["Maximum"]]
]

# 添加固定值数据
fixed_value = 8.56

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
plt.title("Average Wait Time of 100 times Evaluation")
plt.xlabel("RV rate")
plt.ylabel("Time (s)")
plt.xticks([20, 60, 80, 120], ["20%", "60%", "80%", "TL"])
plt.grid(axis="y", linestyle="--", alpha=0.7)

# 显示图形
plt.show()