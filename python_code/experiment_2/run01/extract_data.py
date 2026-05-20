"""
批量读取 run01 目录下所有CSV文件，
提取：每文件最后一行数据、1/3位置的数据、2/3位置的数据，
输出到 summary.md
"""

import os
import csv

data_dir = os.path.dirname(os.path.abspath(__file__))
csv_files = sorted([f for f in os.listdir(data_dir) if f.endswith(".csv")])

# 准备输出
md_lines = ["# 双摆模拟数据汇总\n", f"**目录**: `{data_dir}`\n", f"**文件数**: {len(csv_files)}\n", "---\n"]

for fname in csv_files:
    fpath = os.path.join(data_dir, fname)
    with open(fpath, "r") as f:
        reader = list(csv.reader(f))

    header = reader[0]  # ["theta_1", "theta_2"]
    data_rows = reader[1:]  # 跳过表头
    total = len(data_rows)

    # 各位置索引
    last_row = data_rows[-1]
    pos_1_3 = data_rows[int(total * 1 / 3)]
    pos_2_3 = data_rows[int(total * 2 / 3)]

    # 从文件名提取方法和时间步
    # 例如: run_01_data_001_RK4_0.2000_15s.csv
    parts = fname.replace(".csv", "").split("_")
    # parts: ['run', '01', 'data', '001', 'RK4', '0.2000', '15s']
    method = parts[4]
    dt = parts[5]

    md_lines.append(f"## {fname}\n")
    md_lines.append(f"- **方法**: {method}  |  **dt**: {dt}  |  **总行数(不含表头)**: {total}\n\n")
    md_lines.append(f"| 位置 | theta_1 | theta_2 |\n")
    md_lines.append(f"|------|---------|---------|\n")
    md_lines.append(f"| 最后一行 (索引 {total-1}) | {last_row[0]} | {last_row[1]} |\n")
    md_lines.append(f"| 1/3 处 (索引 {int(total*1/3)}) | {pos_1_3[0]} | {pos_1_3[1]} |\n")
    md_lines.append(f"| 2/3 处 (索引 {int(total*2/3)}) | {pos_2_3[0]} | {pos_2_3[1]} |\n")
    md_lines.append("\n")

# 写入 MD
md_path = os.path.join(data_dir, "summary.md")
with open(md_path, "w") as f:
    f.writelines(md_lines)

print(f"✅ 已完成！输出文件: {md_path}")
