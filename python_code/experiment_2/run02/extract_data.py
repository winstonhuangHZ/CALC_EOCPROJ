"""
批量读取 run02 目录下所有CSV文件，
提取每文件：最后一行、1/15处、1/3处、2/3处的数据 (theta_1, theta_2, energy)，
输出到 summary_run02.md
"""

import os
import csv

data_dir = os.path.dirname(os.path.abspath(__file__))
csv_files = sorted([f for f in os.listdir(data_dir) if f.endswith(".csv") and f != "extract_data.py"])

md_lines = ["# 双摆模拟数据汇总 — run02\n", f"**目录**: `{data_dir}`\n", f"**文件数**: {len(csv_files)}\n", "---\n"]

for fname in csv_files:
    fpath = os.path.join(data_dir, fname)
    with open(fpath, "r") as f:
        reader = list(csv.reader(f))

    header = reader[0]  # ["theta_1", "theta_2", "energy"]
    data_rows = reader[1:]  # 跳过表头
    total = len(data_rows)

    # 各位置索引
    idx_last = total - 1
    idx_1_15 = int(total * 1 / 15)
    idx_1_3  = int(total * 1 / 3)
    idx_2_3  = int(total * 2 / 3)

    last_row   = data_rows[idx_last]
    pos_1_15   = data_rows[idx_1_15]
    pos_1_3    = data_rows[idx_1_3]
    pos_2_3    = data_rows[idx_2_3]

    # 从文件名提取方法和时间步
    # 例如: run_02_data_001_RK4_0.2000_15s.csv
    parts = fname.replace(".csv", "").split("_")
    method = parts[4]
    dt = parts[5]

    md_lines.append(f"## {fname}\n")
    md_lines.append(f"- **方法**: {method}  |  **dt**: {dt}  |  **总行数(不含表头)**: {total}\n\n")
    md_lines.append(f"| 位置 | theta_1 | theta_2 | energy |\n")
    md_lines.append(f"|------|---------|---------|--------|\n")
    md_lines.append(f"| 最后一行 (idx {idx_last}) | {last_row[0]} | {last_row[1]} | {last_row[2]} |\n")
    md_lines.append(f"| 1/15 处 (idx {idx_1_15}) | {pos_1_15[0]} | {pos_1_15[1]} | {pos_1_15[2]} |\n")
    md_lines.append(f"| 1/3  处 (idx {idx_1_3}) | {pos_1_3[0]} | {pos_1_3[1]} | {pos_1_3[2]} |\n")
    md_lines.append(f"| 2/3  处 (idx {idx_2_3}) | {pos_2_3[0]} | {pos_2_3[1]} | {pos_2_3[2]} |\n")
    md_lines.append("\n---\n")

# 写入 MD
md_path = os.path.join(data_dir, "summary_run02.md")
with open(md_path, "w") as f:
    f.writelines(md_lines)

print(f"✅ 已完成！输出文件: {md_path}")
