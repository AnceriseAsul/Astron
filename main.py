#将位移信息转化为坐标并整合时间戳,x,y,z通道
import pandas as pd
def process_routine(routine_path, output_path):
    with open(routine_path, 'r') as file:
        lines = file.readlines()

    x, y, z = 0, 1.5, 0
    count = 0
    step = 0.5
    time = 1715824722

    results = []

    for line in lines:
        command = line.strip()
        if command.startswith('X'):
            target_x = float(command[1:])
            while x != target_x:
                x += step if target_x > x else -step
                x = round(x, 2)  # Ensure precision
                count += 1
                time += 1
                results.append({'Coordinate': f'({x}, {y}, {z})', 'Step Count': count, 'Time': time})

        elif command.startswith('Y'):
            target_y = float(command[1:])
            while y != target_y:
                y += step if target_y > y else -step
                y = round(y, 2)  # Ensure precision
                count += 1
                time += 1
                results.append({'Coordinate': f'({x}, {y}, {z})', 'Step Count': count, 'Time': time})

        elif command.startswith('Z'):
            target_z = float(command[1:])
            while z != target_z:
                z += step if target_z > z else -step
                z = round(z, 2)  # Ensure precision
                count += 1
                time += 1
                results.append({'Coordinate': f'({x}, {y}, {z})', 'Step Count': count, 'Time': time})

        elif command.startswith('P'):
            repeat_count = int(command[1:]) // 1000 
            for _ in range(repeat_count):
                count += 1
                time += 1
                results.append({'Coordinate': f'({x}, {y}, {z})', 'Step Count': count, 'Time': time})

    df_routine = pd.DataFrame(results)
    df_routine.to_csv(output_path, index=False)

def merge_files(routine_path, data_path, output_path):
    # 处理 routine 文件
    routine_output_path = 'processed_routine.csv'
    process_routine(routine_path, routine_output_path)

    # 读取 processed_routine 和 90590-空采 文件
    df_routine = pd.read_csv(routine_output_path)
    df_data = pd.read_csv(data_path, sep="\t", skiprows=1, names=["Index", "Channel_X", "Channel_Y", "Channel_Z", "Time"])

    # 确保 Time 列为相同的数据类型
    df_routine["Time"] = df_routine["Time"].astype(int)
    df_data["Time"] = df_data["Time"].astype(int)

    # 合并数据
    merged = pd.merge(df_routine, df_data, on="Time", how="inner")
    merged = merged[["Time", "Coordinate", "Channel_X", "Channel_Y", "Channel_Z"]]

    # 保存合并后的数据
    merged.to_csv(output_path, sep="\t", index=False, header=False)

# 定义文件路径
routine_file_path = 'routine.txt'
data_file_path = '亮CSV.txt'
#data_file_path = '亮CSV.txt'
output_file_path = '综合2.txt'

# 处理并合并文件
merge_files(routine_file_path, data_file_path, output_file_path)

print("合并完成。请检查 '综合2.txt' 文件。")
