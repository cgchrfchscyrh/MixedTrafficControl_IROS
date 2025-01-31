import xml.etree.ElementTree as ET
import random

# 输入和输出文件
filename = 'file/colorado_medium.trips.xml'  # trips 文件名
output_file = 'medium_trips_NSSN.trips.xml'  # 输出文件名

# 入口和出口 edge ID 列表
other_entrance_edges = [
    "978613905", "237596041#0", "877763365#0", "1317319994", "-436475432#1",
    "229489781#0", "1206873710#0","194878477#0",
    "-894433359#1","39829697#2-AddedOffRampEdge","118756783#6-AddedOffRampEdge",
    "37657924#10","223369752#0"
]

north_entrance_edges = ["978613905"]
north_exit_edges = ["978613906"]

other_exit_edges = [
    "-237596041#0", "38520914#1", "-1317319994", "436475432#1",
    "-1206873710#0","194878410#4", "978613906", "229489593#3",
    "894433359#1","847829715#2-AddedOnRampEdge","37693888#6-AddedOnRampEdge",
    "37657919#7","833739973#4"
]

south_exit_edges = ["229489593#3"]
south_entrance_edges = ["229489781#0"]

# 加载 trips 文件
tree = ET.parse(filename)
routes = tree.getroot()

# 统计车辆总数
total_vehicles = len(routes.findall('trip'))

# 计算每种分配方式的车辆数量
north_to_south_count = int(total_vehicles * 0.27)
south_to_north_count = int(total_vehicles * 0.235)
other_count = total_vehicles - north_to_south_count - south_to_north_count

# 修改所有 trip 的起点和终点
trip_list = routes.findall('trip')

# 分配从 north_entrance_edges 到 south_exit_edges 的车辆
for trip in trip_list[:north_to_south_count]:
    source = random.choice(north_entrance_edges)
    destination = random.choice(south_exit_edges)
    trip.set('from', source)
    trip.set('to', destination)

# 分配从 south_entrance_edges 到 north_exit_edges 的车辆
for trip in trip_list[north_to_south_count:north_to_south_count + south_to_north_count]:
    source = random.choice(south_entrance_edges)
    destination = random.choice(north_exit_edges)
    trip.set('from', source)
    trip.set('to', destination)

# 分配从 other_entrance_edges 到 other_exit_edges 的车辆
other_trips = trip_list[north_to_south_count + south_to_north_count:]
for trip in other_trips:
    source = random.choice(other_entrance_edges)
    destination = random.choice(other_exit_edges)
    while destination == source:  # 确保起点和终点不相同
        destination = random.choice(other_exit_edges)
    trip.set('from', source)
    trip.set('to', destination)

# 保存修改后的 trips 文件
tree.write(output_file, encoding="utf-8", xml_declaration=True)
print(f"Updated trips file saved to {output_file}")