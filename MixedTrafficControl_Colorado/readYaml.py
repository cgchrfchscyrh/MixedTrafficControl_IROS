import yaml

# YAML 文件路径（按顺序存放）
yaml_files = [
    "medium_2control_40%.yaml",
    "medium_4control_40%.yaml",
    "medium_6control_40%.yaml",
    "medium_8control_40%.yaml",
    "medium_10control_40%.yaml"
]

# 解析 YAML 文件
def parse_yaml(file_path):
    file_path = "yaml/40%/" + file_path
    with open(file_path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    return data

def group_intersections(data):
    """
    将一个 YAML 文件的数据按 intersection 分组。
    假设每个 intersection 对应两条 key:
      - "Junction {name} - Waiting Time:"  
      - "Junction {name} - Throughput:"  
    返回一个有序列表，每一项是 (intersection_name, { "Waiting Time": waiting_median, "Throughput": throughput_median })
    """
    intersections = {}
    # 为了保持 YAML 文件中的自然顺序，根据文件中 key 的出现次序构造有序列表
    ordered_names = []
    for key, value in data.items():
        # 只处理以 "Junction " 开头的 key
        if not key.startswith("Junction "):
            continue
        # 去掉前缀 "Junction "，并去除尾部的冒号（如果有）
        key_body = key[len("Junction "):].strip()
        if key_body.endswith(":"):
            key_body = key_body[:-1]
        # 按 " - " 分割，第一部分为 intersection 的名称，第二部分为类型
        parts = key_body.split(" - ")
        if len(parts) < 2:
            continue
        inter_name = parts[0].strip()
        inter_type = parts[1].strip()  # 例如 "Waiting Time" 或 "Throughput"
        # 记录自然出现顺序
        if inter_name not in intersections:
            intersections[inter_name] = {}
            ordered_names.append(inter_name)
        # 保存该项的 Median 数值
        intersections[inter_name][inter_type] = value.get("Median")
    # 返回有序列表
    ordered_list = [(name, intersections[name]) for name in ordered_names]
    return ordered_list

# 依次读取 5 个 YAML 文件，并对每个文件进行分组
grouped_data_list = []
for file in yaml_files:
    data = parse_yaml(file)
    grouped = group_intersections(data)
    grouped_data_list.append(grouped)

# 假设所有 YAML 文件中 intersection 的数量和顺序一致
num_intersections = len(grouped_data_list[0])
num_files = len(yaml_files)

# 生成 LaTeX 代码
for i in range(num_intersections):
    # 第一列：intersection 编号（1 到 num_intersections）
    print(f"{i+1}")
    # 对于每个 YAML 文件，取当前 intersection 的 waiting time 和 throughput 的 median
    line_parts = []
    for file_idx in range(num_files):
        # 每个 grouped_data_list[file_idx] 是一个列表，每项为 (name, data_dict)
        # data_dict 包含键 "Waiting Time" 和 "Throughput"
        inter_data = grouped_data_list[file_idx][i][1]
        waiting = inter_data.get("Waiting Time", "N/A")
        throughput = inter_data.get("Throughput", "N/A")
        line_parts.append(f"        & {waiting} & {throughput}")
    # 将所有部分拼接起来，以 LaTeX 换行符结束
    line = "\n".join(line_parts) + " \\\\"
    print(line)
    print("\n        \\hline")