from tensorboard.backend.event_processing.event_file_loader import EventFileLoader
import matplotlib.pyplot as plt
import numpy as np

all_junction_list = ['cluster12203246695_12203246696_430572036_442436239', 
                       'cluster_547498658_547498666_547498756_547498762_#8more', 
                       'cluster_2052409830_2052409981_9356276530_9356276531', 
                       'cluster_1021221509_11808122037_11808122038_11808122040_#4more',
                       'cluster_2052409422_2052409707_542824247_542824770_#2more',
                       'cluster_2052409323_2052409733_2052409806_2052409936_#9more',
                       'cluster_2052409270_2052409892_2052410135_2052410161_#8more',
                       'cluster_2040873690_2040873694_2040873705_2040873709_#8more',
                       '55760356',
                       'cluster_2093101229_2093101656_2093101781_2093101915_#8more',
                       'cluster9663732079_J0_J1_J2_#2more',
                       'cluster428692206_428692253_9650210478_9650210479_#2more',
                       'cluster_1334947864_1334947865_1334947879_1334947882',
                       'cluster12092955396_1334947859',
                       'cluster_439980117_439980118_442435910_442435912',
                       'cluster_1289585639_439979990_8156136067_8156136068_#1more',
                       'cluster_2048655723_2048656743_2048656762_2048657045_#8more',
                       'cluster1478663503_1478663508_cluster_12092966426_12092966445_1478663506_2515541702']

# 指定 TensorBoard 文件路径和直方图的 tag
PATH_OF_FILE = "events.out.tfevents.1736010382.DESKTOP-EJH5JRT"
HISTOGRAM_PREFIX = "ray/tune/hist_stats/WTH_"  # Histogram tag 前缀

# 初始化 event loader
loader = EventFileLoader(PATH_OF_FILE)

# 遍历每个 Junction ID 并提取数据
for junc_id in all_junction_list:
    HISTOGRAM_TAG = f"{HISTOGRAM_PREFIX}{junc_id}"
    hist_data = None
    steps = []

    # 遍历 event 文件加载数据
    for event in loader.Load():
        step = event.step
        if len(event.summary.value) > 0:
            summary = event.summary.value[0]
            if summary.tag == HISTOGRAM_TAG:
                # 保存步数
                steps.append(step)
                # 保存直方图数据
                bucket_limits = np.array(summary.histo.bucket_limit)
                bucket_counts = np.array(summary.histo.bucket)

                # 计算每个 bin 的中心
                bin_centers = (bucket_limits[:-1] + bucket_limits[1:]) / 2

                # 记录为 hist_data
                hist_data = (bin_centers, bucket_counts)

    # 如果找到数据，绘制直方图
    if hist_data:
        bin_centers, bucket_counts = hist_data

        # 绘制直方图
        plt.figure(figsize=(10, 6))
        plt.bar(bin_centers, bucket_counts, width=10, alpha=0.7, color='blue')
        plt.title(f"Waiting Time Histogram at Junction {junc_id}")
        plt.xlabel("Waiting Time (s)")
        plt.ylabel("Vehicle Count")
        plt.grid(True)

        # 显示图像
        plt.show()
    else:
        print(f"No data found for Junction ID {junc_id}")