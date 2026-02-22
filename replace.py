#!/usr/bin/env python3
import numpy as np

def replace_scientific_timestamps(tum_file, times_file, output_file):
    """
    用科学计数法格式的时间戳替换TUM文件的时间戳
    """
    
    # 读取TUM数据
    tum_data = np.loadtxt(tum_file)
    print(f"原始TUM数据点数: {len(tum_data)}")
    
    # 读取科学计数法格式的时间戳
    scientific_timestamps = []
    with open(times_file, 'r') as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#'):
                try:
                    # 直接使用numpy来解析科学计数法
                    timestamp = float(line)
                    scientific_timestamps.append(timestamp)
                except ValueError:
                    print(f"跳过无法解析的行: {line}")
                    continue
    
    print(f"读取到科学计数法时间戳数量: {len(scientific_timestamps)}")
    
    # 检查长度匹配
    if len(scientific_timestamps) != len(tum_data):
        print(f"警告: 时间戳数量({len(scientific_timestamps)}) ≠ TUM数据点数({len(tum_data)})")
        min_length = min(len(scientific_timestamps), len(tum_data))
        scientific_timestamps = scientific_timestamps[:min_length]
        tum_data = tum_data[:min_length]
        print(f"最终使用数据点数: {min_length}")
    
    # 替换时间戳（保持科学计数法格式）
    tum_data[:, 0] = scientific_timestamps
    
    # 保存为科学计数法格式
    np.savetxt(output_file, tum_data, fmt='%.18e')
    
    print(f"处理完成! 输出文件: {output_file}")
    
    # 显示前几个时间戳对比
    print("\n前3个时间戳对比:")
    print("新时间戳 (科学计数法):")
    for i in range(min(3, len(tum_data))):
        print(f"{tum_data[i, 0]:.18e}")

def check_times_format(times_file):
    """
    检查时间戳文件的格式
    """
    print("检查时间戳文件格式...")
    with open(times_file, 'r') as f:
        lines = f.readlines()
    
    for i, line in enumerate(lines[:5]):  # 检查前5行
        if line.strip() and not line.startswith('#'):
            print(f"第{i+1}行: {line.strip()}")
    
    # 尝试解析第一行
    if lines:
        first_line = lines[0].strip()
        try:
            ts = float(first_line)
            print(f"第一行解析为: {ts}")
            print(f"科学计数法表示: {ts:.18e}")
        except:
            print("无法解析第一行")

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='处理科学计数法时间戳替换')
    parser.add_argument('--tum', type=str, required=True, help='TUM格式轨迹文件')
    parser.add_argument('--times', type=str, required=True, help='科学计数法时间戳文件')
    parser.add_argument('--output', type=str, required=True, help='输出文件')
    
    args = parser.parse_args()
    
    # 先检查时间戳文件格式
    check_times_format(args.times)
    
    # 执行替换
    replace_scientific_timestamps(args.tum, args.times, args.output)
