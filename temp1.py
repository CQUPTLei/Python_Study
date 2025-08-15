import os
import time
import json
import re
import traceback
from datetime import datetime
from enum import Enum
import threading


class PlayState(Enum):
    STOPPED = 0
    PLAYING = 1
    PAUSED = 2
    EXITED = 3


class NeteaseMusicMonitor:
    def __init__(self, log_path: str = None):
        # 默认网易云音乐日志路径
        if log_path is None:
            log_path = r"C:\Users\14134\AppData\Local\NetEase\CloudMusic\cloudmusic.elog"
        self.log_path = log_path

        # 播放状态
        self.play_state = PlayState.STOPPED
        self.current_position = 0.0  # 当前播放位置（秒）
        self.last_resume_time = 0.0  # 上次恢复播放的时间戳
        self.last_reported_state = None  # 上次报告的状态，避免重复输出

        # 歌曲信息
        self.current_song_id = None
        self.current_song_name = "未知歌曲"
        self.current_artist = "未知艺术家"
        self.song_duration = 0  # 歌曲总时长（毫秒）
        self.last_song_info = None  # 上次的歌曲信息，避免重复输出

        # 日志监控
        self.log_file = None
        self.file_size = 0
        self.last_log_line = ""
        self.modified_time = 0

        # 运行状态
        self.is_running = False
        self.monitor_thread = None
        self.is_initializing = True  # 初始化标志

        # 输出控制
        self.last_output_time = 0  # 上次输出时间
        self.output_interval = 1.0  # 输出间隔（秒）
        self.progress_displayed = False  # 是否已显示进度条

    def start_monitoring(self):
        """开始监控"""
        if not os.path.exists(self.log_path):
            print(f"日志文件不存在: {self.log_path}")
            return False

        self.is_running = True
        self.monitor_thread = threading.Thread(target=self._monitor_loop)
        self.monitor_thread.daemon = True
        self.monitor_thread.start()

        print(f"开始监控网易云音乐播放进度...")
        print(f"日志文件: {self.log_path}")
        print("-" * 60)
        return True

    def stop_monitoring(self):
        """停止监控"""
        self.is_running = False
        if self.log_file:
            self.log_file.close()
        print("\n" + "=" * 60)
        print("停止监控")

    def _monitor_loop(self):
        """主监控循环"""
        # 初始化时读取更多日志来获取当前状态
        self._initialize_log_with_current_state()

        while self.is_running:
            try:
                # 检查文件是否被修改
                if os.path.exists(self.log_path):
                    modified_time = os.path.getmtime(self.log_path)
                    if self.modified_time < modified_time:
                        self.modified_time = modified_time
                        self._analyze_log()

                # 只有在播放状态时才更新和显示进度
                current_time = time.time()
                if self.play_state == PlayState.PLAYING:
                    self._update_current_position()
                    # 控制输出频率，避免过于频繁的刷新
                    if current_time - self.last_output_time >= self.output_interval:
                        self._output_progress()
                        self.last_output_time = current_time

                time.sleep(0.2)  # 检查间隔

            except Exception as e:
                print(f"监控循环错误: {e}")
                traceback.print_exc()
                time.sleep(1)

    def _initialize_log_with_current_state(self):
        """初始化日志并尝试获取当前播放状态"""
        try:
            if self.log_file:
                self.log_file.close()

            # 读取更多的日志内容来获取当前状态
            self.log_file = open(self.log_path, "rb")
            self.file_size = os.path.getsize(self.log_path)

            # 从文件末尾读取更多内容
            read_size = min(self.file_size, 32768)  # 读取32KB
            self.log_file.seek(max(0, self.file_size - read_size))

            # 尝试解析最近的日志来获取当前状态
            raw_data = self.log_file.read()
            if raw_data:
                decoded_content = self._decode_elog(raw_data)
                if decoded_content:
                    lines = decoded_content.split('\n')
                    # 反向遍历日志，找到最新的歌曲信息和播放状态
                    for line in reversed(lines):
                        line = line.strip()
                        if line:
                            self._process_log_line(line)

            # 重新定位到文件末尾
            self.log_file.seek(0, 2)
            self.is_initializing = False

            # 初始化完成后，如果有歌曲信息，显示当前状态
            if self.current_song_name != "未知歌曲":
                self._display_current_song_info()

        except Exception as e:
            print(f"初始化日志失败: {e}")
            self.is_initializing = False

    def _analyze_log(self):
        """分析日志内容"""
        try:
            if not self.log_file:
                self._initialize_log_with_current_state()
                return

            # 读取二进制数据
            raw_data = self.log_file.read()
            if not raw_data:
                return

            # 解码.elog格式
            decoded_content = self._decode_elog(raw_data)
            if not decoded_content:
                return

            # 按行分割
            lines = decoded_content.split('\n')

            # 处理新的日志行
            for line in lines:
                line = line.strip()
                if line and line != self.last_log_line:
                    self._process_log_line(line)
                    self.last_log_line = line

        except Exception as e:
            print(f"分析日志失败: {e}")
            traceback.print_exc()
            self._initialize_log_with_current_state()

    def _decode_elog(self, data: bytes) -> str:
        """解码.elog文件的特殊编码格式"""
        try:
            # 尝试原始解码逻辑
            decoded = self._try_original_decode(data)
            if decoded:
                return decoded

            # 尝试简单的解码方法
            decoded = self._try_simple_decode(data)
            if decoded:
                return decoded

            # 尝试直接转换为字符串
            for encoding in ['utf-8', 'gbk', 'gb2312', 'latin-1']:
                try:
                    decoded = data.decode(encoding, errors='ignore')
                    if decoded:
                        return decoded
                except:
                    continue

            return ""

        except Exception as e:
            print(f"解码.elog文件失败: {e}")
            return ""

    def _try_original_decode(self, data: bytes) -> str:
        """尝试原始解码逻辑"""
        try:
            decoded = bytearray()

            for byte_val in data:
                if byte_val == 0:  # 跳过空字节
                    continue

                # 根据原始代码的解码逻辑
                hexs_digit = ((byte_val // 16) ^ (byte_val % 16) + 8) % 16
                bytes_data = hexs_digit * 16 + (byte_val // 64) * 4 + (~(byte_val // 16)) % 4

                # 确保字节值在有效范围内
                if 0 <= bytes_data <= 255:
                    decoded.append(bytes_data)

            # 尝试解码为UTF-8
            return decoded.decode('utf-8', errors='ignore')

        except Exception as e:
            return ""

    def _try_simple_decode(self, data: bytes) -> str:
        """尝试简单的解码方法"""
        try:
            # 简单的XOR解码
            decoded = bytearray()
            for i, byte_val in enumerate(data):
                # 尝试不同的XOR键
                for key in [0x5A, 0x77, 0x88, 0x99, 0xAA]:
                    decoded_byte = byte_val ^ key
                    if 32 <= decoded_byte <= 126:  # 可打印ASCII范围
                        decoded.append(decoded_byte)
                        break
                else:
                    decoded.append(byte_val)

            return decoded.decode('utf-8', errors='ignore')

        except Exception as e:
            return ""

    def _process_log_line(self, line: str):
        """处理单行日志"""
        try:
            # 检查是否是播放相关的日志
            if "【playing】" in line:
                if "setPlaying" in line:
                    self._handle_set_playing(line)
                elif "resume" in line:
                    self._handle_resume(line)
                elif "pause" in line:
                    self._handle_pause(line)
                elif "native播放state" in line:
                    self._handle_play_state(line)
                elif "setPlayingPosition" in line:
                    self._handle_set_position(line)
                elif "seekEnd" in line:
                    self._handle_seek_end(line)
            elif "【PlayProgress】" in line and "dragEnd" in line:
                # 处理拖动进度条结束
                self._handle_drag_end(line)
            elif "DoSeek pos:" in line:
                # 处理Seek操作
                self._handle_do_seek(line)
            elif "exitApp" in line:
                self._handle_exit_app(line)
            elif "song:" in line and "artist:" in line:
                self._handle_song_info(line)
            elif "title_name:" in line:
                # 从窗口标题获取歌曲信息
                self._handle_title_info(line)
            elif "seek:" in line and "cur_progress:" in line:
                # 处理audio_stream中的seek信息
                self._handle_audio_seek(line)
            elif '"duration":' in line:
                # 提取歌曲时长信息
                self._handle_duration_info(line)

        except Exception as e:
            print(f"处理日志行失败: {e}")
            traceback.print_exc()

    def _handle_duration_info(self, line: str):
        """处理歌曲时长信息"""
        try:
            # 提取时长信息
            duration_match = re.search(r'"duration":(\d+)', line)
            if duration_match:
                duration = int(duration_match.group(1))
                if duration > 0:
                    self.song_duration = duration
                    # 如果正在显示歌曲信息，更新时长显示
                    if not self.is_initializing and self.current_song_name != "未知歌曲":
                        print(f"⏱️ 更新时长: {self._format_time(self.song_duration / 1000)}")
        except Exception as e:
            print(f"处理时长信息失败: {e}")

    def _handle_set_playing(self, line: str):
        """处理设置播放歌曲的日志"""
        try:
            song_changed = False

            # 提取歌曲名称
            name_match = re.search(r'"name":"([^"]+)"', line)
            if name_match:
                new_song_name = name_match.group(1)
                if new_song_name != self.current_song_name:
                    self.current_song_name = new_song_name
                    song_changed = True

            # 提取艺术家信息
            artist_match = re.search(r'"artists":\[.*?"name":"([^"]+)"', line)
            if artist_match:
                new_artist = artist_match.group(1)
                if new_artist != self.current_artist:
                    self.current_artist = new_artist
                    song_changed = True

            # 提取时长信息
            duration_match = re.search(r'"duration":(\d+)', line)
            if duration_match:
                self.song_duration = int(duration_match.group(1))

            # 如果歌曲发生变化，重置状态
            if song_changed:
                self.current_position = 0.0
                self.play_state = PlayState.STOPPED
                self.last_reported_state = None
                self.progress_displayed = False

                if not self.is_initializing:
                    self._display_current_song_info()

        except Exception as e:
            print(f"处理播放设置失败: {e}")

    def _handle_title_info(self, line: str):
        """从窗口标题获取歌曲信息"""
        try:
            # 跳过包含文件路径的标题
            if "Python_Study" in line or ".py" in line or "temp" in line:
                return

            # 从日志中提取窗口标题信息
            title_match = re.search(r'title_name:([^,]+)', line)
            if title_match:
                title = title_match.group(1).strip()

                # 跳过非音乐相关的标题
                if any(skip in title.lower() for skip in ["python", "temp", "study", ".py", "untitled"]):
                    return

                song_changed = False

                # 解析歌曲名称和艺术家
                if ' - ' in title:
                    parts = title.split(' - ', 1)
                    new_song_name = parts[0].strip()
                    new_artist = parts[1].strip()
                else:
                    new_song_name = title
                    new_artist = "未知艺术家"

                # 检查是否是新歌曲
                if new_song_name != self.current_song_name or new_artist != self.current_artist:
                    self.current_song_name = new_song_name
                    self.current_artist = new_artist
                    song_changed = True

                if song_changed and not self.is_initializing:
                    self._display_current_song_info()

        except Exception as e:
            print(f"处理标题信息失败: {e}")

    def _handle_song_info(self, line: str):
        """处理歌曲信息日志"""
        try:
            song_changed = False

            # 从日志中提取歌曲信息
            song_match = re.search(r'song:\s*([^,]+)', line)
            artist_match = re.search(r'artist:\s*([^,\s]+)', line)

            if song_match:
                new_song_name = song_match.group(1).strip()
                if new_song_name != self.current_song_name:
                    self.current_song_name = new_song_name
                    song_changed = True

            if artist_match:
                new_artist = artist_match.group(1).strip()
                if new_artist != self.current_artist:
                    self.current_artist = new_artist
                    song_changed = True

            if song_changed and not self.is_initializing:
                self._display_current_song_info()

        except Exception as e:
            print(f"处理歌曲信息失败: {e}")

    def _display_current_song_info(self):
        """显示当前歌曲信息"""
        if self.current_song_name != "未知歌曲":
            print(f"🎵 当前歌曲: {self.current_song_name}")
            print(f"🎤 艺术家: {self.current_artist}")
            if self.song_duration > 0:
                print(f"⏱️ 时长: {self._format_time(self.song_duration / 1000)}")
            print("-" * 60)
            self.progress_displayed = False

    def _handle_resume(self, line: str):
        """处理恢复播放日志"""
        try:
            # 从日志中提取歌曲ID
            id_match = re.search(r'"(\d+)"', line)
            if id_match:
                self.current_song_id = id_match.group(1)

            # 避免重复输出
            if self.last_reported_state != "playing":
                self.play_state = PlayState.PLAYING
                self.last_resume_time = time.time()
                self.last_reported_state = "playing"
                self.progress_displayed = False
                if not self.is_initializing:
                    print(f"▶️ 开始播放")
            else:
                self.play_state = PlayState.PLAYING
                self.last_resume_time = time.time()

        except Exception as e:
            print(f"处理恢复播放失败: {e}")

    def _handle_pause(self, line: str):
        """处理暂停播放日志"""
        try:
            if self.play_state == PlayState.PLAYING:
                # 更新当前位置
                self.current_position += time.time() - self.last_resume_time

            # 避免重复输出
            if self.last_reported_state != "paused":
                self.play_state = PlayState.PAUSED
                self.last_reported_state = "paused"
                if not self.is_initializing:
                    print(f"⏸️ 暂停播放")
                    self._output_progress()  # 显示暂停时的进度
            else:
                self.play_state = PlayState.PAUSED

        except Exception as e:
            print(f"处理暂停播放失败: {e}")

    def _handle_play_state(self, line: str):
        """处理播放状态改变的日志"""
        try:
            # 从日志中提取状态码
            state_match = re.search(r'"native播放state",(\d+)', line)
            if state_match:
                state_code = int(state_match.group(1))

                if state_code == 1:  # 播放
                    if self.last_reported_state != "playing":
                        self.play_state = PlayState.PLAYING
                        self.last_resume_time = time.time()
                        self.last_reported_state = "playing"
                        self.progress_displayed = False
                        if not self.is_initializing:
                            print(f"▶️ 开始播放")
                    else:
                        self.play_state = PlayState.PLAYING
                        self.last_resume_time = time.time()

                elif state_code == 2:  # 暂停
                    if self.play_state == PlayState.PLAYING:
                        self.current_position += time.time() - self.last_resume_time

                    if self.last_reported_state != "paused":
                        self.play_state = PlayState.PAUSED
                        self.last_reported_state = "paused"
                        if not self.is_initializing:
                            print(f"⏸️ 暂停播放")
                            self._output_progress()  # 显示暂停时的进度
                    else:
                        self.play_state = PlayState.PAUSED

        except Exception as e:
            print(f"处理播放状态失败: {e}")

    def _handle_drag_end(self, line: str):
        """处理拖动进度条结束"""
        try:
            # 从日志中提取位置信息
            position_match = re.search(r'setPosition::,(\d+(?:\.\d+)?)', line)
            if position_match:
                position = float(position_match.group(1))
                self.current_position = position

                # 更新最后恢复时间
                if self.play_state == PlayState.PLAYING:
                    self.last_resume_time = time.time()

                if not self.is_initializing:
                    print(f"⏩ 拖动到 {self._format_time(self.current_position)}")
                    self.progress_displayed = False

        except Exception as e:
            print(f"处理拖动结束失败: {e}")

    def _handle_do_seek(self, line: str):
        """处理DoSeek操作"""
        try:
            # 从日志中提取位置信息
            position_match = re.search(r'DoSeek pos:(\d+(?:\.\d+)?)', line)
            if position_match:
                position = float(position_match.group(1))
                self.current_position = position

                # 更新最后恢复时间
                if self.play_state == PlayState.PLAYING:
                    self.last_resume_time = time.time()

                if not self.is_initializing:
                    print(f"⏩ 跳转到 {self._format_time(self.current_position)}")
                    self.progress_displayed = False

        except Exception as e:
            print(f"处理DoSeek失败: {e}")

    def _handle_set_position(self, line: str):
        """处理设置播放位置的日志"""
        try:
            # 从日志中提取位置信息
            position_match = re.search(r'"setPlayingPosition",(\d+(?:\.\d+)?)', line)
            if position_match:
                position = float(position_match.group(1))
                self.current_position = position

                # 更新最后恢复时间
                if self.play_state == PlayState.PLAYING:
                    self.last_resume_time = time.time()

        except Exception as e:
            print(f"处理位置设置失败: {e}")

    def _handle_audio_seek(self, line: str):
        """处理音频流中的seek信息"""
        try:
            # 从audio_stream的seek日志中提取位置信息
            progress_match = re.search(r'cur_progress:(\d+)', line)
            if progress_match:
                # cur_progress是毫秒
                position_ms = float(progress_match.group(1))
                self.current_position = position_ms / 1000

                # 更新最后恢复时间
                if self.play_state == PlayState.PLAYING:
                    self.last_resume_time = time.time()

        except Exception as e:
            print(f"处理audio_seek失败: {e}")

    def _handle_seek_end(self, line: str):
        """处理seekEnd日志"""
        try:
            # seekEnd通常没有位置信息，只是表示seek操作结束
            pass
        except Exception as e:
            print(f"处理seekEnd失败: {e}")

    def _handle_exit_app(self, line: str):
        """处理应用退出的日志"""
        if self.play_state == PlayState.PLAYING:
            self.current_position += time.time() - self.last_resume_time
        self.play_state = PlayState.EXITED
        self.last_reported_state = "exited"
        if not self.is_initializing:
            print(f"❌ 网易云音乐已退出")

    def _update_current_position(self):
        """更新当前播放位置"""
        if self.play_state == PlayState.PLAYING:
            current_time = time.time()
            self.current_position += current_time - self.last_resume_time
            self.last_resume_time = current_time

    def _output_progress(self):
        """输出播放进度"""
        if self.current_song_name == "未知歌曲":
            return

        # 计算进度
        if self.song_duration > 0:
            duration_seconds = self.song_duration / 1000
            progress_percent = min(100, (self.current_position / duration_seconds) * 100)
        else:
            # 如果没有歌曲时长，估算
            estimated_duration = max(self.current_position * 1.5, 180)
            duration_seconds = estimated_duration
            progress_percent = min(100, (self.current_position / duration_seconds) * 100)

        # 创建进度条
        progress_bar_length = 40
        filled_length = int(progress_bar_length * progress_percent / 100)
        bar = "█" * filled_length + "░" * (progress_bar_length - filled_length)

        # 格式化时间
        current_time_str = self._format_time(self.current_position)
        total_time_str = self._format_time(duration_seconds) if self.song_duration > 0 else "??:??"

        # 播放状态图标
        if self.play_state == PlayState.PLAYING:
            status_icon = "▶️"
        elif self.play_state == PlayState.PAUSED:
            status_icon = "⏸️"
        else:
            status_icon = "⏹️"

        # 如果还没有显示过进度条，或者状态发生变化，则显示完整信息
        if not self.progress_displayed:
            print(f"{status_icon} {self.current_song_name} - {self.current_artist}")
            print(f"[{bar}] {current_time_str}/{total_time_str} ({progress_percent:.1f}%)")
            self.progress_displayed = True
        else:
            # 已经显示过，只更新进度条
            print(f"\r[{bar}] {current_time_str}/{total_time_str} ({progress_percent:.1f}%)", end='', flush=True)

    def _format_time(self, seconds: float) -> str:
        """格式化时间显示"""
        minutes = int(seconds // 60)
        seconds = int(seconds % 60)
        return f"{minutes:02d}:{seconds:02d}"

    def get_current_status(self) -> dict:
        """获取当前播放状态"""
        return {
            "song_name": self.current_song_name,
            "artist": self.current_artist,
            "duration": self.song_duration,
            "position": self.current_position,
            "play_state": self.play_state.name,
            "progress_percent": (self.current_position / (
                    self.song_duration / 1000)) * 100 if self.song_duration > 0 else 0
        }


def main():
    # 使用示例
    log_path = r"C:\Users\14134\AppData\Local\NetEase\CloudMusic\cloudmusic.elog"
    monitor = NeteaseMusicMonitor(log_path)

    try:
        if monitor.start_monitoring():
            print("监控已启动，按 Ctrl+C 停止")
            while True:
                time.sleep(1)
    except KeyboardInterrupt:
        print("\n收到退出信号")
    finally:
        monitor.stop_monitoring()


if __name__ == "__main__":
    main()