import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import minimize
import networkx as nx

# 定义障碍物
obstacles = [(500, 500, 50), (1500, 1500, 100)]  # (x, y, radius)

# 机器人起点和终点
start_points = [(52, 186), (540, 492), (1619, 696), (1256, 840), (205, 1070),
                (1586, 51), (1007, 733), (294, 730), (715, 1661), (1000, 300)]
goal_points = [(9834, 8725), (7206, 9726), (6085, 6203), (8425, 6240), (9594, 6414),
               (6115, 6981), (5940, 9179), (5054, 5625), (8906, 6377), (8000, 8000)]


# A*算法路径规划函数（简化版）
def astar(start, goal):
    path = [start, goal]  # 简化路径规划为直线
    return path


# 速度优化目标函数
def optimize_speed(x, *params):
    # x是速度向量，params包含起点、终点和路径
    speed = x[0]
    return np.sum(speed)  # 简单优化目标: 最小化总速度


# 计算路径并优化速度
def plan_path_and_optimize():
    paths = []
    speeds = []
    times = []

    for start, goal in zip(start_points, goal_points):
        path = astar(start, goal)
        paths.append(path)

        # 简单优化: 使用固定速度
        initial_speed = [5]  # 初始速度
        result = minimize(optimize_speed, initial_speed, args=(start, goal, path))
        speeds.append(result.x[0])

        # 计算时间（假设路径长度为常量）
        distance = np.linalg.norm(np.array(goal) - np.array(start))
        time = distance / result.x[0]
        times.append(time)

    return paths, speeds, times


# 可视化结果
def visualize_results(paths, speeds, times):
    plt.figure(figsize=(10, 10))

    # 绘制路径
    for i, (path, speed, time) in enumerate(zip(paths, speeds, times)):
        path = np.array(path)
        plt.plot(path[:, 0], path[:, 1], label=f'Robot {i + 1} Path (Speed: {speed:.2f}, Time: {time:.2f})')
        plt.scatter(*path[0], color='red')  # 起点
        plt.scatter(*path[-1], color='green')  # 终点

    # 绘制障碍物
    for (x, y, r) in obstacles:
        circle = plt.Circle((x, y), r, color='gray', alpha=0.5)
        plt.gca().add_artist(circle)

    plt.xlabel('North')
    plt.ylabel('East')
    plt.title('Robot Paths and Obstacles')
    plt.legend()
    plt.grid(True)
    plt.show()


# 主程序
paths, speeds, times = plan_path_and_optimize()
visualize_results(paths, speeds, times)
