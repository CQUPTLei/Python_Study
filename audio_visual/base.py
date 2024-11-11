import sounddevice as sd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib
import sys
import matplotlib.cm as cm

# 设置 matplotlib 后端
matplotlib.use('TkAgg')

# 设置音频流参数
RATE = 48000
CHUNK = 1024
n_bars = 50  # 频谱的条数

# 初始化图形
fig, ax = plt.subplots()

# x轴表示不同的频段
x = np.linspace(0, 80, n_bars)

bars = ax.bar(x, np.zeros(n_bars), width=1)  # 设置宽度大于1，使其更可视化

ax.set_ylim(0, 1)  # 设置y轴范围
ax.set_xlim(0, n_bars)  # x轴显示的频段数量
plt.title("Real-time Frequency Spectrum (Grouped)")

# 使用对数刻度进行频率划分
freq_bands = np.logspace(np.log10(20), np.log10(20000 // 2), n_bars + 1)  # 对数刻度划分频率区间
freq_bands = np.int32(freq_bands)  # 转为整数，方便索引


# 获取默认输出设备的音频流
def audio_callback(indata, frames, time, status):
    if status:
        print(status, file=sys.stderr)

    # 转换为 numpy 数组
    samples = np.frombuffer(indata, dtype=np.int16)

    # 执行快速傅里叶变换 (FFT)
    fft_data = np.fft.rfft(samples)
    fft_magnitude = np.abs(fft_data)  # 频谱的幅值

    # 对 FFT 数据进行分组计算每个频段的能量
    band_magnitudes = []
    for i in range(n_bars):
        start_idx = freq_bands[i]  # 获取当前频段的起始索引
        end_idx = freq_bands[i + 1]  # 获取当前频段的结束索引
        band_magnitude = np.sum(fft_magnitude[start_idx:end_idx])  # 计算该频段的总能量
        band_magnitudes.append(band_magnitude)  # 存储频段的能量

    # 归一化到 [0, 1]
    min_magnitude = min(band_magnitudes)
    max_magnitude = max(band_magnitudes)
    # print(min_magnitude,max_magnitude)
    if max_magnitude > min_magnitude+2500:  # 避免除以零
        band_magnitudes = [(magnitude - min_magnitude) / (max_magnitude - min_magnitude) for magnitude in band_magnitudes]
    else:
        band_magnitudes = [0] * len(band_magnitudes)  # 如果所有幅值相同，设置为 0
    # 获取一个颜色映射器
    norm = plt.Normalize(min(band_magnitudes), max(band_magnitudes))  # 根据幅值范围进行归一化
    cmap = matplotlib.colormaps['rainbow']  # 使用rainbow色图

    # 更新柱状图数据并设置颜色
    for i, bar in enumerate(bars):
        bar.set_height(band_magnitudes[i])  # 设置每个柱子的高度
        bar.set_color(cmap(norm(band_magnitudes[i])))  # 根据频段的能量设置颜色


# 打开音频流（从系统输出捕获音频）
stream = sd.InputStream(callback=audio_callback, channels=2, samplerate=RATE, blocksize=CHUNK, dtype='int16', device='Input (VB-Audio Point)')

stream.start()

# 初始化动画
ani = animation.FuncAnimation(fig, lambda frame: None, interval=100, cache_frame_data=False)

plt.show(block=True)  # 保证窗口保持打开状态

# 关闭音频流
stream.stop()
stream.close()
