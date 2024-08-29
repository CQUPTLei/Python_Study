import numpy as np
import matplotlib.pyplot as plt
from scipy.fftpack import fft2, fftshift

# 生成示例图像（这里使用一个简单的示例）
image = np.random.rand(256, 256)

# 进行二维傅里叶变换
f_transform = fft2(image)
f_transform_shifted = fftshift(f_transform)

# 计算功率谱密度
psd_2d = np.abs(f_transform_shifted)**2

# 绘制原始图像和功率谱密度
plt.figure(figsize=(12, 6))

plt.subplot(1, 2, 1)
plt.title('Original Image')
plt.imshow(image, cmap='gray')
plt.colorbar()

plt.subplot(1, 2, 2)
plt.title('Power Spectral Density')
plt.imshow(np.log(psd_2d), cmap='gray')
plt.colorbar()

plt.show()
