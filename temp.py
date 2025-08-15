import asyncio
import time
import os
from datetime import datetime

try:
    import pymem
    import pymem.process

    PYMEM_AVAILABLE = True
    print("✅ pymem 库已加载")
except ImportError:
    print("❌ pymem 库不可用，请安装: pip install pymem")
    PYMEM_AVAILABLE = False


class MusicProgressMonitor:
    def __init__(self):
        self.pm = None
        self.module_base = None

        # ==================== 在这里填入您的最终成果 ====================
        #
        #   请用您找到的真实地址替换下面的占位符。
        #   地址前面的 `0x` 代表这是一个十六进制数。
        #
        # ===============================================================
        self.memory_pointers = {
            'cloudmusic': {
                'process_name': 'cloudmusic.exe',
                'module_name': 'cloudmusic.dll',

                # 假设您找到的是播放进度
                'time_offset': 0x1C153A4,  # <--- 您找到的地址！
                'time_type': 'double',  # <--- 'float' 或 'double'

                # 您还需要找到总时长的地址！这里用0作为占位符
                'duration_offset': 0x0,  # <--- ！！请找到并替换这里！！
                'duration_type': 'double'  # <--- 'float' 或 'double'
            }
        }

    def get_media_info_from_memory(self, app_key='cloudmusic'):
        if not PYMEM_AVAILABLE or app_key not in self.memory_pointers:
            return None

        config = self.memory_pointers[app_key]
        process_name = config['process_name']
        module_name = config['module_name']

        try:
            # 附加到进程，如果尚未附加
            if self.pm is None or not self.pm.process_handle:
                self.pm = pymem.Pymem(process_name)
                self.module_base = pymem.process.module_from_name(self.pm.process_handle, module_name).lpBaseOfDll

            # --- 读取播放进度 ---
            time_address = self.module_base + config['time_offset']
            if config['time_type'] == 'float':
                current_pos = self.pm.read_float(time_address)
            else:
                current_pos = self.pm.read_double(time_address)

            # --- 读取总时长 ---
            if config['duration_offset'] == 0x0:  # 如果没填写总时长地址
                total_duration = 0
            else:
                duration_address = self.module_base + config['duration_offset']
                if config['duration_type'] == 'float':
                    total_duration = self.pm.read_float(duration_address)
                else:
                    total_duration = self.pm.read_double(duration_address)

            if total_duration > 1:  # 简单判断数据有效
                return {
                    'title': f"歌曲 (来自内存)",
                    'artist': process_name,
                    'position': current_pos,
                    'duration': total_duration,
                    'is_playing': current_pos > 0 and current_pos < total_duration,
                    'is_paused': False,  # 无法精确判断
                    'app_name': '网易云音乐',
                    'app_icon': '🧠',
                    'source': 'memory'
                }

        except pymem.exception.ProcessNotFound:
            self.pm = None
            return None
        except Exception:
            return None

        return None

    # (这里是您其他的类方法，比如 format_time, create_progress_bar, print_dynamic_info, run, monitor_music_progress 等)
    # (这些函数基本不需要改动，可以直接复用)

    def format_time(self, seconds):
        if seconds < 0: seconds = 0
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = seconds % 60
        if hours > 0:
            return f"{hours:02d}:{minutes:02d}:{secs:05.2f}"
        else:
            return f"{minutes:02d}:{secs:05.2f}"

    def create_progress_bar(self, position, duration, is_playing=True, width=60):
        if duration <= 0: duration = 1
        position = min(max(0, position), duration)
        percentage = (position / duration) * 100
        filled_length = int(width * percentage / 100)
        bar = '█' * filled_length + '░' * (width - filled_length)
        return f"[{bar}] {percentage:05.2f}% {self.format_time(position)}/{self.format_time(duration)}"

    def clear_line(self):
        print('\r' + ' ' * 120 + '\r', end='', flush=True)

    def print_dynamic_info(self, media_info):
        status = "▶️" if media_info['is_playing'] else "⏸️"
        song_info = f"{media_info['title']} - {media_info['artist']}"
        progress_bar = self.create_progress_bar(media_info['position'], media_info['duration'],
                                                media_info['is_playing'])
        info_line = f"{media_info['app_icon']} {media_info['app_name']} {status} {song_info}"
        self.clear_line()
        print(f"{info_line}\n{progress_bar}", end='', flush=True)

    async def monitor_music_progress(self):
        print("\n🎵 音乐播放进度监控器 (内存读取模式)")
        print("=" * 80)
        print(
            f"使用的进度地址: {self.memory_pointers['cloudmusic']['module_name']}+{hex(self.memory_pointers['cloudmusic']['time_offset'])}")
        print("=" * 80)

        last_media_info = None

        while True:
            media_info = self.get_media_info_from_memory('cloudmusic')
            if media_info:
                self.print_dynamic_info(media_info)
                update_interval = 0.05
            else:
                if self.pm is None and last_media_info is not None:
                    self.clear_line()
                    print("\n⏹️ 网易云音乐进程未找到...", end='')
                    last_media_info = None
                update_interval = 1.0

            last_media_info = media_info
            await asyncio.sleep(update_interval)

    def run(self):
        try:
            if os.name == 'nt': os.system('color')
            asyncio.run(self.monitor_music_progress())
        except KeyboardInterrupt:
            print("\n程序已退出")


def main():
    if not PYMEM_AVAILABLE:
        exit(1)
    # 提醒需要管理员权限
    import ctypes
    try:
        is_admin = os.getuid() == 0
    except AttributeError:
        is_admin = ctypes.windll.shell32.IsUserAnAdmin() != 0

    if not is_admin:
        print("❌ 错误：内存读取需要管理员权限。请以管理员身份运行此脚本。")
        exit(1)

    monitor = MusicProgressMonitor()
    monitor.run()


if __name__ == "__main__":
    main()