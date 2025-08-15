import asyncio
import time
import os
import re
from datetime import datetime

# 导入需要的库
try:
    from winsdk.windows.media.control import GlobalSystemMediaTransportControlsSessionManager as MediaManager

    SMTC_AVAILABLE = True
except ImportError:
    SMTC_AVAILABLE = False

try:
    import psutil
    import win32gui
    import win32process

    WINDOW_MONITOR_AVAILABLE = True
except ImportError:
    WINDOW_MONITOR_AVAILABLE = False
    print("❌ 需要安装: pip install psutil pywin32")


class MusicMonitor:
    def __init__(self):
        self.stop_monitoring = False
        self.last_media_info = None

    async def get_smtc_info(self):
        """获取SMTC信息（QQ音乐等）"""
        if not SMTC_AVAILABLE:
            return None

        try:
            sessions = await MediaManager.request_async()
            current_session = sessions.get_current_session()

            if not current_session:
                return None

            media_properties = await current_session.try_get_media_properties_async()
            playback_info = current_session.get_playback_info()
            timeline_properties = current_session.get_timeline_properties()

            if timeline_properties and media_properties:
                position = timeline_properties.position.total_seconds()
                duration = timeline_properties.end_time.total_seconds() - timeline_properties.start_time.total_seconds()
                is_playing = playback_info.playback_status == 4 if playback_info else False

                return {
                    'source': 'SMTC',
                    'app': current_session.source_app_user_model_id,
                    'title': media_properties.title,
                    'artist': media_properties.artist,
                    'album': media_properties.album_title or '',
                    'position': position,
                    'duration': duration,
                    'is_playing': is_playing
                }
        except Exception as e:
            pass
        return None

    def get_window_titles(self):
        """获取所有窗口标题"""
        if not WINDOW_MONITOR_AVAILABLE:
            return []

        windows = []

        def enum_callback(hwnd, windows):
            if win32gui.IsWindowVisible(hwnd):
                title = win32gui.GetWindowText(hwnd)
                if title:
                    try:
                        _, pid = win32process.GetWindowThreadProcessId(hwnd)
                        proc = psutil.Process(pid)
                        windows.append({
                            'title': title,
                            'process': proc.name(),
                            'pid': pid
                        })
                    except:
                        pass
            return True

        try:
            win32gui.EnumWindows(enum_callback, windows)
        except:
            pass

        return windows

    def parse_netease_title(self, title):
        """解析网易云音乐窗口标题"""
        # 网易云音乐可能的标题格式
        patterns = [
            r'^(.+?) - (.+?) - 网易云音乐$',  # 歌名 - 歌手 - 网易云音乐
            r'^网易云音乐 - (.+?) - (.+?)$',  # 网易云音乐 - 歌名 - 歌手
            r'^(.+?) — (.+?) — 网易云音乐$',  # 使用长破折号
            r'^(.+?) - (.+?)$',  # 简单格式：歌名 - 歌手
        ]

        for pattern in patterns:
            match = re.match(pattern, title)
            if match:
                return {
                    'title': match.group(1).strip(),
                    'artist': match.group(2).strip()
                }

        # 如果包含网易云音乐但格式不匹配，尝试提取
        if '网易云音乐' in title:
            clean_title = title.replace('网易云音乐', '').strip(' -—')
            if ' - ' in clean_title:
                parts = clean_title.split(' - ', 1)
                return {
                    'title': parts[0].strip(),
                    'artist': parts[1].strip()
                }

        return None

    def get_netease_info(self):
        """获取网易云音乐信息"""
        windows = self.get_window_titles()

        # 查找网易云相关窗口
        netease_windows = []
        for window in windows:
            if 'cloudmusic' in window['process'].lower() or 'netease' in window['process'].lower():
                netease_windows.append(window)

        # 只在调试模式或新歌时显示窗口信息
        debug_mode = False  # 设为True开启调试

        if netease_windows and debug_mode:
            print(f"🔍 发现网易云窗口:")
            for w in netease_windows:
                print(f"  PID:{w['pid']} - '{w['title']}'")

        # 尝试解析标题
        for window in netease_windows:
            parsed = self.parse_netease_title(window['title'])
            if parsed:
                # 只在新歌时显示解析成功信息
                if (not self.last_media_info or
                        parsed['title'] != self.last_media_info.get('title') or
                        parsed['artist'] != self.last_media_info.get('artist')):
                    pass  # 不再每次都打印解析成功

                # 模拟播放时间（基于系统时间）
                if not hasattr(self, 'netease_start_time'):
                    self.netease_start_time = time.time()
                elif (self.last_media_info and
                      (parsed['title'] != self.last_media_info.get('title') or
                       parsed['artist'] != self.last_media_info.get('artist'))):
                    # 新歌，重置计时
                    self.netease_start_time = time.time()

                current_position = time.time() - self.netease_start_time

                return {
                    'source': '窗口标题',
                    'app': '网易云音乐',
                    'title': parsed['title'],
                    'artist': parsed['artist'],
                    'album': '',
                    'position': current_position,
                    'duration': 0,  # 无法获取总时长
                    'is_playing': True
                }

        return None

    async def get_current_info(self):
        """获取当前播放信息"""
        # 优先尝试SMTC
        smtc_info = await self.get_smtc_info()
        if smtc_info:
            return smtc_info

        # 尝试网易云窗口标题
        netease_info = self.get_netease_info()
        if netease_info:
            return netease_info

        return None

    def format_time(self, seconds):
        """格式化时间"""
        if seconds <= 0:
            return "00:00"
        minutes = int(seconds // 60)
        secs = int(seconds % 60)
        return f"{minutes:02d}:{secs:02d}"

    def create_progress_bar(self, position, duration, width=50):
        """创建进度条"""
        if duration <= 0:
            return f"播放中: {self.format_time(position)}"

        percentage = (position / duration) * 100
        filled = int(width * percentage / 100)
        bar = "█" * filled + "░" * (width - filled)

        return f"[{bar}] {percentage:4.1f}% {self.format_time(position)}/{self.format_time(duration)}"

    def display_info(self, info):
        """显示播放信息"""
        if not info:
            if self.last_media_info:  # 只在从有音乐变为无音乐时显示
                print(f"\n⏹️ 未检测到播放")
                self.last_media_info = None
            return

        # 检查是否是新歌
        is_new_song = (not self.last_media_info or
                       info['title'] != self.last_media_info.get('title') or
                       info['artist'] != self.last_media_info.get('artist') or
                       info['app'] != self.last_media_info.get('app'))

        if is_new_song:
            print(f"\n🎵 {info['title']}")
            print(f"👤 {info['artist']}")
            if info['album']:
                print(f"💿 {info['album']}")
            print(f"📱 {info['app']} [{info['source']}]")
            print("-" * 60)

        # 显示进度
        if info['duration'] > 0:
            # 有完整时间信息
            progress = self.create_progress_bar(info['position'], info['duration'])
            status = "▶️" if info['is_playing'] else "⏸️"
            print(f"\r{status} {progress}", end="", flush=True)
        else:
            # 只有播放时间
            status = "▶️" if info['is_playing'] else "⏸️"
            time_str = self.format_time(info['position'])
            print(f"\r{status} 播放中: {time_str} (无总时长信息)", end="", flush=True)

    async def run(self):
        """运行监控"""
        print("🎵 音乐播放监控器")
        print("=" * 50)
        print("支持: QQ音乐(SMTC) + 网易云音乐(窗口标题)")
        print("按 Ctrl+C 停止")
        print("=" * 50)

        while not self.stop_monitoring:
            try:
                info = await self.get_current_info()
                self.display_info(info)
                self.last_media_info = info

                # 根据信息源调整更新频率
                if info and info['source'] == 'SMTC':
                    await asyncio.sleep(0.5)  # SMTC更新
                elif info and info['source'] == '窗口标题':
                    await asyncio.sleep(1.0)  # 窗口标题更新
                else:
                    await asyncio.sleep(3.0)  # 无音乐时低频检测

            except KeyboardInterrupt:
                print(f"\n🛑 监控停止")
                break
            except Exception as e:
                await asyncio.sleep(1.0)


def main():
    print("🎵 简化音乐监控器")
    print("支持QQ音乐完整功能 + 网易云音乐基础功能")
    print()

    if not WINDOW_MONITOR_AVAILABLE:
        print("⚠️ 窗口监控不可用，只能监控SMTC应用")
        print("安装: pip install psutil pywin32")
        print()

    monitor = MusicMonitor()
    try:
        asyncio.run(monitor.run())
    except KeyboardInterrupt:
        print("程序退出")


if __name__ == "__main__":
    main()