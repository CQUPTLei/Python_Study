import matplotlib.pyplot as plt
import numpy as np

x = np.linspace(0, 10, 100)
y = np.sin(x)

plt.plot(x, y)
plt.fill_between(x, y, color='blue', alpha=0.3)  # 填充曲线下方区域
plt.show()


plt.plot(x, y)
plt.fill_between(x, y, y.max(), color='red', alpha=0.3)  # 填充曲线上方区域
plt.show()


