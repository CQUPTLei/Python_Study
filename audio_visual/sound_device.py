import sounddevice as sd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib
import sys
import matplotlib.cm as cm

# 设置 matplotlib 后端
matplotlib.use('TkAgg')


class RealTimeSpectrum:
    def __init__(self, rate=48000, chunk=1024, n_bars=50, device=None):
        self.rate = rate
        self.chunk = chunk
        self.n_bars = n_bars
        self.device = device
        self.fig, self.ax = plt.subplots()
        self.x = np.linspace(0, 80, self.n_bars)
        self.bars = self.ax.bar(self.x, np.zeros(self.n_bars), width=1)
        self.ax.set_ylim(0, 1200000)
        self.ax.set_xlim(0, self.n_bars)
        plt.title("Real-time Frequency Spectrum (Grouped)")

        # 设置频率分段
        self.freq_bands = np.logspace(np.log10(20), np.log10(20000 // 2), self.n_bars + 1).astype(int)

        # 打开音频流
        self.stream = sd.InputStream(callback=self.audio_callback, channels=2, samplerate=self.rate,
                                     blocksize=self.chunk, dtype='int16', device=self.device)

    def audio_callback(self, indata, frames, time, status):
        if status:
            print(status, file=sys.stderr)

        # 转换为 numpy 数组
        samples = np.frombuffer(indata, dtype=np.int16)

        # 执行快速傅里叶变换 (FFT)
        fft_data = np.fft.rfft(samples)
        fft_magnitude = np.abs(fft_data)

        # 计算每个频段的能量
        band_magnitudes = []
        for i in range(self.n_bars):
            start_idx = self.freq_bands[i]
            end_idx = self.freq_bands[i + 1]
            band_magnitude = np.sum(fft_magnitude[start_idx:end_idx])
            band_magnitudes.append(band_magnitude)

        # 颜色映射器
        norm = plt.Normalize(min(band_magnitudes), max(band_magnitudes))
        cmap = matplotlib.colormaps['rainbow']

        # 更新柱状图
        for i, bar in enumerate(self.bars):
            bar.set_height(band_magnitudes[i])
            bar.set_color(cmap(norm(band_magnitudes[i])))

    def start(self):
        self.stream.start()
        ani = animation.FuncAnimation(self.fig, lambda frame: None, interval=100, cache_frame_data=False)
        plt.show(block=True)

        # 关闭流
        self.stream.stop()
        self.stream.close()


# 使用类
spectrum = RealTimeSpectrum(device=68)
spectrum.start()
