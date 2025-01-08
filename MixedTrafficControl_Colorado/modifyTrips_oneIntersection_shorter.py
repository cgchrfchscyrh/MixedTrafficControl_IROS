import xml.etree.ElementTree as ET
import random

# 输入和输出文件
filename = 'file/colorado_oneIntersection_shorter.trips.xml'  # trips 文件名
output_file = 'shorter_trips.trips.xml'  # 输出文件名

# 入口和出口 edge ID 列表
entrance_edges = [
    "229489592#3-AddedOffRampEdge", "877763350#4-AddedOffRampEdge", "877763365#2-AddedOffRampEdge", "718258596-AddedOffRampEdge"
]

exit_edges = [
    "229489601-AddedOnRampEdge", "877763366#0-AddedOnRampEdge", "38520914#1-AddedOnRampEdge", "229489597-AddedOnRampEdge"
]

# 加载 trips 文件
tree = ET.parse(filename)
routes = tree.getroot()

# 修改所有 trip 的起点和终点
for trip in routes.iter('trip'):
    # 随机选择入口边的索引
    source_index = random.randint(0, len(entrance_edges) - 1)
    source = entrance_edges[source_index]

    # 随机选择出口边，但不能与入口边索引相同
    destination_candidates = [edge for i, edge in enumerate(exit_edges) if i != source_index]
    destination = random.choice(destination_candidates)

    trip.set('from', source)
    trip.set('to', destination)

# 保存修改后的 trips 文件
tree.write(output_file, encoding="utf-8", xml_declaration=True)
print(f"Updated trips file saved to {output_file}")