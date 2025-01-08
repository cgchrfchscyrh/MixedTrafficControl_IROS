import xml.etree.ElementTree as ET
import random

# 输入和输出文件
# filename = 'file/colorado_roundabouts_singleLine.trips.xml'         # trips 文件名
# output_file = 'updated_trips_2.trips.xml'  # 输出文件名

filename = 'file/colorado_oneIntersection.trips.xml'         # trips 文件名
output_file = 'updated_trips.trips.xml'  # 输出文件名

# 入口和出口 edge ID 列表
# entrance_edges = [
#     "237596041#0", "877763365#0", "1317319994", "-436475432#1",
#     "229489781#0", "1206873710#0", "223369752#0", "877730942#0",
#     "892128262#0", "194878492#0", "194878477#0", "978613905"
# ]

entrance_edges = [
    "877763365#0", "229489592#3", "877763350#3", "978613918"
]

# exit_edges = [
#     "-237596041#0", "38520914#1", "-1317319994", "436475432#1",
#     "229489593#3", "-1206873710#0", "833739973#4", "657904703#3",
#     "910280335#1", "194878402#1", "194878410#4", "978613906"
# ]

exit_edges = [
    "978613914", "38520914#1", "229489601", "877763366#2"
]

# 加载 trips 文件
tree = ET.parse(filename)
routes = tree.getroot()

# 修改所有 trip 的起点和终点
for trip in routes.iter('trip'):
    # 随机选择入口边和出口边
    source = random.choice(entrance_edges)
    destination = random.choice(exit_edges)
    while destination == source:  # 确保起点和终点不相同
        destination = random.choice(exit_edges)

    trip.set('from', source)
    trip.set('to', destination)

# 保存修改后的 trips 文件
tree.write(output_file, encoding="utf-8", xml_declaration=True)
print(f"Updated trips file saved to {output_file}")