# 这个是Gemini写的演示程序，后面我再重构

import numpy as np
import csv

params = {
    "m1": 1.0,  # 摆球1质量 (kg)
    "m2": 1.0,  # 摆球2质量 (kg)
    "l1": 1.0,  # 摆绳1长度 (m)
    "l2": 1.0,  # 摆绳2长度 (m)
    "g": 9.81,  # 重力加速度 (m/s^2)
    "dt": 0.01,  # 时间步长 (s)
    "duration": 25.0,  # 总模拟时间 (s)
    "angle_mode": "DEG",  # 模式选择: 'DEG' (角度) 或 'RAD' (弧度)
    "theta1_0": 90.0,  # 初始角度1
    "theta2_0": 90.0,  # 初始角度2
    "w1_0": 0.0,  # 初始角速度1 (无论模式，建议设为0)
    "w2_0": 0.0,  # 初始角速度2
}




def simulate_double_pendulum(para=None):
    # 如果外部没传参数，使用默认字典
    if para is None:
        para = {
            "m1": 1.0, "m2": 1.0,
            "l1": 1.0, "l2": 1.0,
            "g": 9.81, "dt": 0.01,
            "duration": 5.0,
            "angle_mode": "DEG",
            "theta1_0": 90.0, "theta2_0": 90.0,
            "w1_0": 0.0, "w2_0": 0.0,
        }

    # 1. 预处理：根据 angle_mode 转换初始角度
    if para["angle_mode"].upper() == "DEG":
        t1_run = np.radians(para["theta1_0"])
        t2_run = np.radians(para["theta2_0"])
    else:
        t1_run = para["theta1_0"]
        t2_run = para["theta2_0"]

    # --- 核心物理方程 (保持不变，但使用传入的 para) ---
    def derivatives(state, t, p):
        t1, w1, t2, w2 = state
        m1, m2, l1, l2, g = p["m1"], p["m2"], p["l1"], p["l2"], p["g"]

        delta = t1 - t2
        den = 2 * m1 + m2 - m2 * np.cos(2 * t1 - 2 * t2)

        d_w1 = (-g * (2 * m1 + m2) * np.sin(t1)
                - m2 * g * np.sin(t1 - 2 * t2)
                - 2 * np.sin(delta) * m2 * (w2**2 * l2 + w1**2 * l1 * np.cos(delta))
               ) / (l1 * den)

        d_w2 = (2 * np.sin(delta) * (w1**2 * l1 * (m1 + m2)
                + g * (m1 + m2) * np.cos(t1)
                + w2**2 * l2 * m2 * np.cos(delta))
               ) / (l2 * den)

        return np.array([w1, d_w1, w2, d_w2])

    def rk4_step(state, t, dt, p):
        k1 = derivatives(state, t, p)
        k2 = derivatives(state + 0.5 * dt * k1, t + 0.5 * dt, p)
        k3 = derivatives(state + 0.5 * dt * k2, t + 0.5 * dt, p)
        k4 = derivatives(state + dt * k3, t + dt, p)
        return state + (dt / 6.0) * (k1 + 2 * k2 + 2 * k3 + k4)

    # --- 执行模拟 ---
    num_steps = int(para["duration"] / para["dt"])
    current_state = np.array([t1_run, para["w1_0"], t2_run, para["w2_0"]])

    results = []
    for i in range(num_steps):
        t1_out, t2_out = current_state[0], current_state[2]

        # 2. 后处理：转换回 DEG 模式（如果需要）
        if para["angle_mode"].upper() == "DEG":
            results.append([float(np.degrees(t1_out)), float(np.degrees(t2_out))])
        else:
            results.append([float(t1_out), float(t2_out)])

        # 步进
        current_state = rk4_step(current_state, i * para["dt"], para["dt"], para)

    return results

# 传入字典
sim_results = simulate_double_pendulum(para=params)

# 打印查看
print(f"模拟完成，环境模式: {params['angle_mode']}")
for step_data in sim_results[:5]:
    print(f"角度1: {step_data[0]:.2f}, 角度2: {step_data[1]:.2f}")

csv_filename = "pendulum_data.csv"
with open(csv_filename, mode='w', newline='') as f:
    writer = csv.writer(f)
    # 写入表头
    writer.writerow(["time", "theta1", "theta2"])
    # 写入数据
    writer.writerows(sim_results)

print(f"模拟完成！数据已保存至: {csv_filename}")
