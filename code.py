import numpy as np
import scipy.linalg as la

# 设定参数
T = 1.0  # 时间长度
x_max = 16  # 最大财富
N = 320  # 时间离散化步数
M = 32  # 财富空间离散化步数
p = M + 1  # 财富网格点数量

delta_t = T / N  # 时间步长
delta_x = x_max / (p - 1)  # 财富空间步长

# 风险资产参数
r = np.array([0.05, 0.01])  # 无风险资产利率
mu = np.array([0.13, 0.07])  # 风险资产回报率
sigma = np.array([0.20, 0.30])  # 风险资产波动率

# 跳扩散过程的参数
lambda_ = np.array([0.005, 0.005])  # 跳跃强度
mu_bar = np.array([-0.5, -0.5])  # 跳跃的均值
gamma = np.array([0.45, 0.45])  # 跳跃波动率

# 状态转移矩阵 Q
Q = np.array([[-1 / 3, 1 / 3], [1 / 2, -1 / 2]])

# 初始财富
x_0 = 1.0


# 终端条件和边界条件
def utility(x):
    return 2 * np.sqrt(x)


def phi(t, x_max, j):
    # 终端条件的计算
    return np.exp(np.dot(np.linalg.expm(Q * (T - t)), np.ones(2))) * utility(x_max)


# 初始化财富网格
x_grid = np.linspace(0, x_max, p)

# 初始化价值函数
V = np.zeros((N + 1, p, 2))  # (时间步，财富网格点，状态)

# 初始时刻的价值函数
for j in range(2):
    V[0, :, j] = utility(x_grid)

# 数值解的主循环
for n in range(N - 1, -1, -1):
    for k in range(100):  # 迭代次数，直到收敛
        V_new = np.zeros_like(V[n])

        # 计算 A(pi) 对应的矩阵项（例如 a_i, b_i 等）
        for i in range(1, p - 1):
            for j in range(2):
                # 计算 a_i, b_i 等矩阵项
                a_i = (sigma[j] ** 2 * (mu[j] - r[j]) * x_grid[i] ** 2) / (2 * delta_x ** 2)
                b_i = (sigma[j] ** 2 * x_grid[i] ** 2) / delta_x ** 2

                # 用最优控制策略 pi 来更新 V_new
                V_new[i, j] = V[n, i, j]  # 这里简化为直接复制，可以根据具体公式替换

        # 边界条件
        V_new[0, :] = 0
        V_new[-1, :] = phi(n * delta_t, x_max, 2)

        # 检查收敛性
        if np.max(np.abs(V_new - V[n])) < 1e-5:
            break

        V[n] = V_new  # 更新价值函数

# 输出结果
print("最终的价值函数 V(T, x, j):")
print(V[-1, :, :])

