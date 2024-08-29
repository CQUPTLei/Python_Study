import control as ctrl
import numpy as np

# 假设传递函数数据
numerators = [4, 2, 10, 10, 2, 4, 10, 10, 10, 9, 2, 10, 4]
denominators = [
    [1, 2, 0], [1, 10, 0], [1, 9, 0], [1, 2, 11], [1, 0.5, 0],
    [1, 2, 0], [1, 1.6, 4], [1, 5, 24], [1, 2.5, 24], [1, 2, 9],
    [1, 0.25, 0], [1, 5, 4], [1, 0.15, 0]
]
H_values = [10, 10, 5, 1, 1, 1, 5, 3, 1, 1, 0.5, 5, 10]
Kp_values = [
    [1, 5, 10], [1, 4, 10], [1, 4, 10], [1, 10, 100], [0.1, 1, 10],
    [0.5, 5, 50], [1, 10, 50], [2, 20, 200], [1, 25, 250], [1, 25, 250],
    [0.2, 20, 200], [1, 10, 50], [1, 5, 10]
]

# 保存闭环传递函数
closed_loop_transfer_functions = []

for i in range(13):
    G1 = ctrl.TransferFunction(numerators[i], denominators[i])
    H = H_values[i]

    for Kp in Kp_values[i]:
        G_OL = Kp * G1
        T = ctrl.feedback(G_OL, H)

        # 保存闭环传递函数
        closed_loop_transfer_functions.append({
            'System': i + 1,
            'Kp': Kp,
            'Closed Loop Transfer Function': T
        })

# 打印每个系统的闭环传递函数
for entry in closed_loop_transfer_functions:
    print(f"System {entry['System']}, Kp = {entry['Kp']}:")
    print(entry['Closed Loop Transfer Function'])
    print()

