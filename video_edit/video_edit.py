#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PyQt6 + OpenCV + FFmpeg 的单文件视频工具：
- 实时预览（播放/暂停、拖动进度、画幅裁剪矩形、旋转预览、倍速预览）
- 格式转换（容器/编码/CRF/码率/帧率/缩放）
- 时长裁剪（-ss/-to 或 -t）
- 画幅裁剪（w:h:x:y，支持鼠标拖拽 ROI）
- 旋转（90/180/270 或任意角度）
- 倍速（视频 setpts + 音频 atempo 自动分段）
- 转 GIF（palettegen/paletteuse）
- 拼接（无损 copy 或重编码）
- 音频（提取/去除）
- 实时日志（解析 ffmpeg 输出进度 time=）

要求：
- 已安装 ffmpeg/ffprobe 并加入 PATH（或把可执行路径填到设置里）
- Python 3.9+，pip install opencv-python PyQt6

许可：MIT
"""
from __future__ import annotations
import os
import sys
import math
import time
import tempfile
import shlex
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Optional, List

import cv2
from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtCore import Qt, QTimer, QThread, pyqtSignal
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QFileDialog, QStyle, QSlider, QLabel, QPushButton,
    QWidget, QHBoxLayout, QVBoxLayout, QGridLayout, QComboBox, QSpinBox, QDoubleSpinBox,
    QLineEdit, QCheckBox, QTabWidget, QGroupBox, QPlainTextEdit, QMessageBox, QListWidget,
    QListWidgetItem
)

# ---------------------- 工具函数 ----------------------

def shell_quote(x: str) -> str:
    return shlex.quote(str(x))


def which(cmd: str) -> Optional[str]:
    exts = [""]
    if os.name == "nt":
        exts = os.environ.get("PATHEXT", ".EXE;.BAT;.CMD").split(";")
    for p in os.environ.get("PATH", "").split(os.pathsep):
        p = p.strip('"')
        if not p:
            continue
        for e in exts:
            cand = Path(p) / (cmd + e)
            if cand.exists():
                return str(cand)
    return None


FFMPEG = which("ffmpeg") or "ffmpeg"
FFPROBE = which("ffprobe") or "ffprobe"


def ffmpeg_available() -> bool:
    try:
        subprocess.run([FFMPEG, "-version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
        subprocess.run([FFPROBE, "-version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
        return True
    except Exception:
        return False


# ---------------------- 预览控件（可画 ROI） ----------------------
class VideoPreview(QtWidgets.QLabel):
    roiChanged = QtCore.pyqtSignal(int, int, int, int)  # x,y,w,h
    clicked = QtCore.pyqtSignal()

    def __init__(self):
        super().__init__("预览区")
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setMinimumSize(480, 270)
        self.setScaledContents(False)
        self.frame = None  # 原始 BGR 帧
        self.display_img = None
        self.dragging = False
        self.roi = None  # (x,y,w,h) 基于原始帧像素
        self._start_pt = None
        self._img_rect_in_widget = QtCore.QRect()  # 视频映射到控件后的矩形

    def setFrame(self, frame_bgr, roi: Optional[tuple[int,int,int,int]], angle_deg: float = 0.0):
        self.frame = frame_bgr
        self.roi = roi
        # 旋转预览（仅预览，不改变源帧）
        if angle_deg % 360 != 0:
            self.frame = self.rotate_image(self.frame, angle_deg)
        self.repaint()

    @staticmethod
    def rotate_image(img, angle_deg: float):
        (h, w) = img.shape[:2]
        center = (w/2, h/2)
        M = cv2.getRotationMatrix2D(center, angle_deg, 1.0)
        cos = abs(M[0, 0]); sin = abs(M[0, 1])
        nW = int((h * sin) + (w * cos))
        nH = int((h * cos) + (w * sin))
        M[0, 2] += (nW / 2) - center[0]
        M[1, 2] += (nH / 2) - center[1]
        return cv2.warpAffine(img, M, (nW, nH))

    def paintEvent(self, ev: QtGui.QPaintEvent) -> None:
        super().paintEvent(ev)
        if self.frame is None:
            return
        rgb = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb.shape
        qimg = QtGui.QImage(rgb.data, w, h, ch * w, QtGui.QImage.Format.Format_RGB888)
        pix = QtGui.QPixmap.fromImage(qimg)

        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.SmoothPixmapTransform)

        # 等比缩放至控件
        target = pix.scaled(self.size(), Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
        x = (self.width() - target.width()) // 2
        y = (self.height() - target.height()) // 2
        self._img_rect_in_widget = QtCore.QRect(x, y, target.width(), target.height())
        painter.drawPixmap(self._img_rect_in_widget, target)

        # ROI 覆盖绘制
        if self.roi:
            rx, ry, rw, rh = self.roi
            # 将原图坐标映射到控件坐标
            scale_x = target.width() / w
            scale_y = target.height() / h
            rr = QtCore.QRect(int(x + rx * scale_x), int(y + ry * scale_y), int(rw * scale_x), int(rh * scale_y))
            pen = QtGui.QPen(QtGui.QColor(0, 255, 0), 2, Qt.PenStyle.DashLine)
            painter.setPen(pen)
            painter.drawRect(rr)
            # 半透明遮罩
            overlay = QtGui.QColor(0, 0, 0, 80)
            painter.setBrush(overlay)
            # 上下左右遮罩
            painter.drawRect(QtCore.QRect(x, y, target.width(), rr.top() - y))
            painter.drawRect(QtCore.QRect(x, rr.bottom(), target.width(), y + target.height() - rr.bottom()))
            painter.drawRect(QtCore.QRect(x, rr.top(), rr.left() - x, rr.height()))
            painter.drawRect(QtCore.QRect(rr.right(), rr.top(), x + target.width() - rr.right(), rr.height()))

        painter.end()

    def mousePressEvent(self, ev: QtGui.QMouseEvent) -> None:
        if self.frame is None or not self._img_rect_in_widget.contains(ev.pos()):
            return
        self.dragging = True
        self._start_pt = ev.position().toPoint()

    def mouseMoveEvent(self, ev: QtGui.QMouseEvent) -> None:
        if not self.dragging or self.frame is None:
            return
        x0, y0 = self._start_pt.x(), self._start_pt.y()
        x1, y1 = ev.position().toPoint().x(), ev.position().toPoint().y()
        rr = QtCore.QRect(min(x0, x1), min(y0, y1), abs(x1 - x0), abs(y1 - y0))
        # 反算为原图坐标
        rx, ry, rw, rh = self._widgetRect_to_imageRect(rr)
        self.roi = (rx, ry, rw, rh)
        self.repaint()
        self.roiChanged.emit(rx, ry, rw, rh)

    def mouseReleaseEvent(self, ev: QtGui.QMouseEvent) -> None:
        self.dragging = False
        self.clicked.emit()

    def _widgetRect_to_imageRect(self, r: QtCore.QRect) -> tuple[int,int,int,int]:
        if self.frame is None:
            return (0,0,0,0)
        img_h, img_w = self.frame.shape[:2]
        x, y, w, h = self._img_rect_in_widget.x(), self._img_rect_in_widget.y(), self._img_rect_in_widget.width(), self._img_rect_in_widget.height()
        if w == 0 or h == 0:
            return (0,0,0,0)
        scale_x = img_w / w
        scale_y = img_h / h
        rx = max(0, min(img_w, int((r.x() - x) * scale_x)))
        ry = max(0, min(img_h, int((r.y() - y) * scale_y)))
        rw = max(2, min(img_w - rx, int(r.width() * scale_x))) // 2 * 2
        rh = max(2, min(img_h - ry, int(r.height() * scale_y))) // 2 * 2
        return (rx, ry, rw, rh)


# ---------------------- FFmpeg 后台任务 ----------------------
class FFmpegWorker(QThread):
    line = pyqtSignal(str)
    progress = pyqtSignal(float)  # 秒
    finished_ok = pyqtSignal()
    finished_fail = pyqtSignal(int)

    def __init__(self, cmd: List[str]):
        super().__init__()
        self.cmd = cmd

    def run(self):
        self.line.emit("命令：" + " ".join(shell_quote(c) for c in self.cmd))
        proc = subprocess.Popen(self.cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, bufsize=1, universal_newlines=True)
        for ln in proc.stdout:
            s = ln.rstrip()
            self.line.emit(s)
            # 解析 time=00:00:12.34 进度
            if "time=" in s:
                try:
                    t = s.split("time=")[-1].split()[0]
                    h, m, sec = t.split(":")
                    sec = float(sec) + int(h) * 3600 + int(m) * 60
                    self.progress.emit(sec)
                except Exception:
                    pass
        proc.wait()
        if proc.returncode == 0:
            self.finished_ok.emit()
        else:
            self.finished_fail.emit(proc.returncode)


# ---------------------- 主窗口 ----------------------
@dataclass
class ExportOptions:
    container: str = "mp4"
    vcodec: str = "libx264"
    acodec: str = "aac"
    crf: int = 23
    preset: str = "medium"
    v_bitrate: str = ""  # 例 "2500k"
    scale: str = ""      # 例 "1280:720" 或 "-2:1080"
    fps: str = ""        # 例 "30"
    remove_audio: bool = False

    # 时长
    t_start: str = ""     # "00:00:05"
    t_end: str = ""       # "00:00:15"
    t_dur: str = ""       # "10"

    # 画幅裁剪
    crop_x: int = 0
    crop_y: int = 0
    crop_w: int = 0
    crop_h: int = 0

    # 旋转
    rotate_mode: str = "none"  # none|t0|t2|t180|angle
    rotate_angle: float = 0.0

    # 倍速
    speed: float = 1.0

    # GIF
    gif_fps: int = 12
    gif_scale: str = ""  # "480:-1"
    gif_loop: int = 0

    # 拼接
    concat_files: List[str] = None
    concat_reencode: bool = False


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PyQt 视频编辑器 (实时预览)")
        self.resize(1280, 800)

        self.input_path: Optional[str] = None
        self.cap: Optional[cv2.VideoCapture] = None
        self.frame_timer = QTimer(self)
        self.frame_timer.timeout.connect(self._on_timer)
        self.playing = False
        self.cur_fps = 25.0
        self.speed = 1.0
        self.duration_sec = 0.0

        # 预览与控制条
        self.preview = VideoPreview()
        self.slider = QSlider(Qt.Orientation.Horizontal)
        self.slider.setEnabled(False)
        self.slider.sliderMoved.connect(self._on_seek_slider)

        self.btn_open = QPushButton("打开…")
        self.btn_play = QPushButton(self.style().standardIcon(QStyle.StandardPixmap.SP_MediaPlay), "")
        self.btn_play.clicked.connect(self.toggle_play)
        self.btn_open.clicked.connect(self.open_file)
        self.btn_frame_prev = QPushButton("◀︎帧")
        self.btn_frame_next = QPushButton("帧▶︎")
        self.btn_frame_prev.clicked.connect(lambda: self.step_frame(-1))
        self.btn_frame_next.clicked.connect(lambda: self.step_frame(+1))

        top = QWidget(); top_l = QVBoxLayout(top)
        top_l.addWidget(self.preview)
        ctr = QHBoxLayout();
        ctr.addWidget(self.btn_open); ctr.addWidget(self.btn_play)
        ctr.addWidget(self.btn_frame_prev); ctr.addWidget(self.btn_frame_next)
        ctr.addWidget(QLabel("进度:")); ctr.addWidget(self.slider, 1)
        top_l.addLayout(ctr)

        # 右侧参数面板
        self.tabs = QTabWidget()
        self._build_tab_basic()
        self._build_tab_trim()
        self._build_tab_crop()
        self._build_tab_rotate()
        self._build_tab_speed()
        self._build_tab_gif()
        self._build_tab_concat()
        self._build_tab_audio()

        # 日志+导出
        self.log = QPlainTextEdit(); self.log.setReadOnly(True)
        self.btn_export = QPushButton("开始导出")
        self.btn_export.clicked.connect(self.export_video)

        right = QWidget(); right_l = QVBoxLayout(right)
        right_l.addWidget(self.tabs)
        right_l.addWidget(self.btn_export)
        right_l.addWidget(QLabel("日志:"))
        right_l.addWidget(self.log, 1)

        # 主布局
        central = QWidget(); lay = QHBoxLayout(central)
        lay.addWidget(top, 2)
        lay.addWidget(right, 1)
        self.setCentralWidget(central)

        # 信号
        self.preview.roiChanged.connect(self._on_roi_changed)

        if not ffmpeg_available():
            QMessageBox.warning(self, "提示", "未检测到 ffmpeg/ffprobe，请确保已安装并在 PATH 中。")

    # ---------------- UI 构建 ----------------
    def _build_tab_basic(self):
        w = QWidget(); g = QGridLayout(w)
        self.cb_container = QComboBox(); self.cb_container.addItems(["mp4","mkv","mov","webm","avi","m4v","ts"]) ; self.cb_container.setCurrentText("mp4")
        self.cb_vcodec = QComboBox(); self.cb_vcodec.addItems(["libx264","libx265","libvpx-vp9","libaom-av1","mpeg4","copy"]) ; self.cb_vcodec.setCurrentText("libx264")
        self.cb_acodec = QComboBox(); self.cb_acodec.addItems(["aac","libopus","libmp3lame","ac3","copy"]) ; self.cb_acodec.setCurrentText("aac")
        self.sp_crf = QSpinBox(); self.sp_crf.setRange(0,51); self.sp_crf.setValue(23)
        self.cb_preset = QComboBox(); self.cb_preset.addItems(["ultrafast","superfast","veryfast","faster","fast","medium","slow","slower","veryslow"]) ; self.cb_preset.setCurrentText("medium")
        self.ed_bitrate = QLineEdit(); self.ed_bitrate.setPlaceholderText("例: 2500k，可留空用CRF")
        self.ed_scale = QLineEdit(); self.ed_scale.setPlaceholderText("例: 1280:720 或 -2:1080")
        self.ed_fps = QLineEdit(); self.ed_fps.setPlaceholderText("例: 30")
        self.ck_remove_audio = QCheckBox("去音频")

        r=0
        for label, widget in [("容器", self.cb_container),("视频编码", self.cb_vcodec),("音频编码", self.cb_acodec),("CRF", self.sp_crf),("preset", self.cb_preset),("视频码率", self.ed_bitrate),("scale", self.ed_scale),("fps", self.ed_fps)]:
            g.addWidget(QLabel(label+"："), r, 0); g.addWidget(widget, r, 1); r+=1
        g.addWidget(self.ck_remove_audio, r, 0, 1, 2)
        self.tabs.addTab(w, "格式转换")

    def _build_tab_trim(self):
        w = QWidget(); g = QGridLayout(w)
        self.ed_ss = QLineEdit(); self.ed_ss.setPlaceholderText("起始 -ss，例 00:00:05")
        self.ed_to = QLineEdit(); self.ed_to.setPlaceholderText("结束 -to，例 00:00:15")
        self.ed_t = QLineEdit(); self.ed_t.setPlaceholderText("时长 -t，例 10")
        self.ck_copy = QCheckBox("尽量流复制(快速切段)"); self.ck_copy.setChecked(True)
        g.addWidget(QLabel("-ss："),0,0); g.addWidget(self.ed_ss,0,1)
        g.addWidget(QLabel("-to："),1,0); g.addWidget(self.ed_to,1,1)
        g.addWidget(QLabel("-t："),2,0); g.addWidget(self.ed_t,2,1)
        g.addWidget(self.ck_copy,3,0,1,2)
        self.tabs.addTab(w, "时长裁剪")

    def _build_tab_crop(self):
        w = QWidget(); g = QGridLayout(w)
        self.sp_cx = QSpinBox(); self.sp_cy = QSpinBox(); self.sp_cw = QSpinBox(); self.sp_ch = QSpinBox()
        for sp in (self.sp_cx, self.sp_cy, self.sp_cw, self.sp_ch):
            sp.setRange(0, 10000)
        g.addWidget(QLabel("x："),0,0); g.addWidget(self.sp_cx,0,1)
        g.addWidget(QLabel("y："),1,0); g.addWidget(self.sp_cy,1,1)
        g.addWidget(QLabel("w："),2,0); g.addWidget(self.sp_cw,2,1)
        g.addWidget(QLabel("h："),3,0); g.addWidget(self.sp_ch,3,1)
        self.tabs.addTab(w, "画幅裁剪")

    def _build_tab_rotate(self):
        w = QWidget(); g = QGridLayout(w)
        self.cb_rotate = QComboBox(); self.cb_rotate.addItems(["none","t0(顺时针90)","t2(逆时针90)","t180(180°)","angle(任意角度)"])
        self.sb_angle = QDoubleSpinBox(); self.sb_angle.setRange(-360.0, 360.0); self.sb_angle.setDecimals(3)
        self.sb_angle.setSingleStep(1.0)
        g.addWidget(QLabel("旋转："),0,0); g.addWidget(self.cb_rotate,0,1)
        g.addWidget(QLabel("角度°："),1,0); g.addWidget(self.sb_angle,1,1)
        self.tabs.addTab(w, "旋转")

    def _build_tab_speed(self):
        w = QWidget(); g = QGridLayout(w)
        self.ds_speed = QDoubleSpinBox(); self.ds_speed.setRange(0.1, 8.0); self.ds_speed.setSingleStep(0.1); self.ds_speed.setValue(1.0)
        self.ds_speed.valueChanged.connect(self._on_speed_changed)
        g.addWidget(QLabel("倍速："),0,0); g.addWidget(self.ds_speed,0,1)
        self.tabs.addTab(w, "倍速")

    def _build_tab_gif(self):
        w = QWidget(); g = QGridLayout(w)
        self.sp_gif_fps = QSpinBox(); self.sp_gif_fps.setRange(1, 60); self.sp_gif_fps.setValue(12)
        self.ed_gif_scale = QLineEdit(); self.ed_gif_scale.setPlaceholderText("例: 480:-1")
        self.sp_gif_loop = QSpinBox(); self.sp_gif_loop.setRange(-1, 9999); self.sp_gif_loop.setValue(0)
        g.addWidget(QLabel("fps："),0,0); g.addWidget(self.sp_gif_fps,0,1)
        g.addWidget(QLabel("scale："),1,0); g.addWidget(self.ed_gif_scale,1,1)
        g.addWidget(QLabel("loop："),2,0); g.addWidget(self.sp_gif_loop,2,1)
        self.tabs.addTab(w, "转GIF")

    def _build_tab_concat(self):
        w = QWidget(); v = QVBoxLayout(w)
        self.list_concat = QListWidget(); self.list_concat.setSelectionMode(QtWidgets.QAbstractItemView.SelectionMode.ExtendedSelection)
        hv = QHBoxLayout();
        btn_add = QPushButton("添加…"); btn_up = QPushButton("上移"); btn_down = QPushButton("下移"); btn_del = QPushButton("删除")
        btn_add.clicked.connect(self._ct_add)
        btn_up.clicked.connect(lambda: self._ct_move(-1))
        btn_down.clicked.connect(lambda: self._ct_move(+1))
        btn_del.clicked.connect(self._ct_del)
        hv.addWidget(btn_add); hv.addWidget(btn_up); hv.addWidget(btn_down); hv.addWidget(btn_del); hv.addStretch(1)
        self.ck_concat_reencode = QCheckBox("强制转码再拼接")
        v.addWidget(self.list_concat, 1)
        v.addLayout(hv)
        v.addWidget(self.ck_concat_reencode)
        self.tabs.addTab(w, "拼接")

    def _build_tab_audio(self):
        w = QWidget(); g = QGridLayout(w)
        self.ck_extract = QCheckBox("提取音频"); self.ck_remove = QCheckBox("去除音频")
        self.cb_aformat = QComboBox(); self.cb_aformat.addItems(["mp3","aac","m4a","opus","wav","flac"]) ; self.cb_aformat.setCurrentText("mp3")
        g.addWidget(self.ck_extract,0,0); g.addWidget(QLabel("格式："),0,1); g.addWidget(self.cb_aformat,0,2)
        g.addWidget(self.ck_remove,1,0)
        self.tabs.addTab(w, "音频/其它")

    # ---------------- 打开/预览 ----------------
    def open_file(self):
        f, _ = QFileDialog.getOpenFileName(self, "选择视频", "", "视频文件 (*.mp4 *.mkv *.mov *.avi *.webm *.m4v *.ts *.flv);;所有文件 (*.*)")
        if not f:
            return
        self.load_video(f)

    def load_video(self, path: str):
        if self.cap is not None:
            self.cap.release()
            self.cap = None
        self.input_path = path
        cap = cv2.VideoCapture(path)
        if not cap.isOpened():
            QMessageBox.critical(self, "错误", "无法打开视频")
            return
        self.cap = cap
        self.cur_fps = cap.get(cv2.CAP_PROP_FPS) or 25.0
        self.duration_sec = (cap.get(cv2.CAP_PROP_FRAME_COUNT) or 0) / max(self.cur_fps, 1e-3)
        self.slider.setRange(0, int(self.duration_sec * 1000))
        self.slider.setValue(0)
        self.slider.setEnabled(True)
        self.playing = True
        self.btn_play.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_MediaPause))
        self._update_timer()

    def toggle_play(self):
        if self.cap is None:
            return
        self.playing = not self.playing
        self.btn_play.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_MediaPause if self.playing else QStyle.StandardPixmap.SP_MediaPlay))
        self._update_timer()

    def _update_timer(self):
        if not self.cap:
            self.frame_timer.stop(); return
        # 预览倍速调整：周期 = 1000 / (fps * speed)
        sp = max(0.1, float(self.ds_speed.value()))
        interval = max(5, int(1000.0 / max(1e-3, self.cur_fps * sp)))
        if self.playing:
            self.frame_timer.start(interval)
        else:
            self.frame_timer.stop()

    def _on_speed_changed(self):
        self._update_timer()

    def _on_timer(self):
        if not self.cap: return
        ret, frame = self.cap.read()
        if not ret:
            # 循环
            self.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
            return
        # 应用 ROI 预览裁剪
        rx, ry, rw, rh = self._current_crop()
        if rw > 0 and rh > 0:
            H, W = frame.shape[:2]
            x1 = max(0, min(W, rx)); y1 = max(0, min(H, ry))
            x2 = max(0, min(W, rx+rw)); y2 = max(0, min(H, ry+rh))
            if x2 > x1 and y2 > y1:
                frame = frame[y1:y2, x1:x2]
        # 旋转预览
        angle = 0.0
        mode = self.cb_rotate.currentText()
        if mode.startswith("t0"): angle = -90
        elif mode.startswith("t2"): angle = 90
        elif mode.startswith("t180"): angle = 180
        elif mode.startswith("angle"): angle = float(self.sb_angle.value())
        self.preview.setFrame(frame, (rx, ry, rw, rh) if self.input_path else None, angle_deg=angle)

        # 更新 slider
        pos_ms = int((self.cap.get(cv2.CAP_PROP_POS_MSEC) or 0))
        self.slider.blockSignals(True)
        self.slider.setValue(min(self.slider.maximum(), pos_ms))
        self.slider.blockSignals(False)

    def _on_seek_slider(self, ms: int):
        if not self.cap: return
        # 定位帧
        self.cap.set(cv2.CAP_PROP_POS_MSEC, ms)

    def step_frame(self, delta: int):
        if not self.cap: return
        cur = int(self.cap.get(cv2.CAP_PROP_POS_FRAMES) or 0)
        self.cap.set(cv2.CAP_PROP_POS_FRAMES, max(0, cur + delta))
        ret, frame = self.cap.read()
        if ret:
            rx, ry, rw, rh = self._current_crop()
            if rw>0 and rh>0:
                frame = frame[ry:ry+rh, rx:rx+rw]
            angle = float(self.sb_angle.value()) if self.cb_rotate.currentText().startswith("angle") else 0.0
            self.preview.setFrame(frame, (rx, ry, rw, rh), angle)

    def _on_roi_changed(self, x,y,w,h):
        self.sp_cx.blockSignals(True); self.sp_cy.blockSignals(True); self.sp_cw.blockSignals(True); self.sp_ch.blockSignals(True)
        self.sp_cx.setValue(x); self.sp_cy.setValue(y); self.sp_cw.setValue(w); self.sp_ch.setValue(h)
        self.sp_cx.blockSignals(False); self.sp_cy.blockSignals(False); self.sp_cw.blockSignals(False); self.sp_ch.blockSignals(False)

    def _current_crop(self) -> tuple[int,int,int,int]:
        return (self.sp_cx.value(), self.sp_cy.value(), self.sp_cw.value(), self.sp_ch.value())

    # ---------------- 导出 ----------------
    def gather_options(self) -> ExportOptions:
        opt = ExportOptions()
        opt.container = self.cb_container.currentText()
        opt.vcodec = self.cb_vcodec.currentText()
        opt.acodec = self.cb_acodec.currentText()
        opt.crf = int(self.sp_crf.value())
        opt.preset = self.cb_preset.currentText()
        opt.v_bitrate = self.ed_bitrate.text().strip()
        opt.scale = self.ed_scale.text().strip()
        opt.fps = self.ed_fps.text().strip()
        opt.remove_audio = self.ck_remove_audio.isChecked()

        opt.t_start = self.ed_ss.text().strip()
        opt.t_end = self.ed_to.text().strip()
        opt.t_dur = self.ed_t.text().strip()

        opt.crop_x, opt.crop_y, opt.crop_w, opt.crop_h = self._current_crop()

        rot = self.cb_rotate.currentText()
        if rot.startswith("t0"): opt.rotate_mode = "t0"
        elif rot.startswith("t2"): opt.rotate_mode = "t2"
        elif rot.startswith("t180"): opt.rotate_mode = "t180"
        elif rot.startswith("angle"): opt.rotate_mode = "angle"; opt.rotate_angle = float(self.sb_angle.value())
        else: opt.rotate_mode = "none"

        opt.speed = float(self.ds_speed.value())

        opt.gif_fps = int(self.sp_gif_fps.value())
        opt.gif_scale = self.ed_gif_scale.text().strip()
        opt.gif_loop = int(self.sp_gif_loop.value())

        opt.concat_files = [self.list_concat.item(i).text() for i in range(self.list_concat.count())]
        opt.concat_reencode = self.ck_concat_reencode.isChecked()
        return opt

    def export_video(self):
        if not self.input_path and not self.list_concat.count():
            QMessageBox.warning(self, "提示", "请先打开一个视频或添加拼接文件。")
            return
        opt = self.gather_options()

        # 弹出保存路径
        if self.list_concat.count() > 1 and (not self.input_path):
            # 纯拼接
            default = "concat_out.mp4"
        else:
            stem = Path(self.input_path).stem if self.input_path else "output"
            default = f"{stem}_export.{opt.container}"
        out, _ = QFileDialog.getSaveFileName(self, "保存输出", default, f"*.{opt.container}")
        if not out:
            return

        cmd = self.build_ffmpeg_cmd(opt, out)
        self.run_ffmpeg(cmd)

    def build_ffmpeg_cmd(self, opt: ExportOptions, out_path: str) -> List[str]:
        # 如果是拼接优先处理
        if opt.concat_files and len(opt.concat_files) >= 2:
            tmp = Path(tempfile.gettempdir()) / f"concat_{int(time.time())}.txt"
            with open(tmp, "w", encoding="utf-8") as f:
                for p in opt.concat_files:
                    f.write(f"file {shell_quote(Path(p).resolve())}\n")
            if not opt.concat_reencode:
                return [FFMPEG, "-y", "-hide_banner", "-f", "concat", "-safe", "0", "-i", str(tmp), "-c", "copy", out_path]
            else:
                return [FFMPEG, "-y", "-hide_banner", "-f", "concat", "-safe", "0", "-i", str(tmp), "-c:v", opt.vcodec, "-c:a", ("aac" if opt.acodec=="copy" else opt.acodec), out_path]

        if not self.input_path:
            raise RuntimeError("没有输入文件")

        args: List[str] = [FFMPEG, "-y", "-hide_banner"]
        # 时间裁剪，-ss 放前面快但关键帧精度差，这里采用放后面更准
        if opt.t_start:
            args += ["-ss", opt.t_start]
        args += ["-i", self.input_path]
        if opt.t_end:
            args += ["-to", opt.t_end]
        if opt.t_dur:
            args += ["-t", opt.t_dur]

        # 滤镜
        vfilters = []
        if opt.crop_w > 0 and opt.crop_h > 0:
            vfilters.append(f"crop={opt.crop_w}:{opt.crop_h}:{opt.crop_x}:{opt.crop_y}")
        if opt.rotate_mode == "t0":
            vfilters.append("transpose=0")
        elif opt.rotate_mode == "t2":
            vfilters.append("transpose=2")
        elif opt.rotate_mode == "t180":
            vfilters.append("hflip,vflip")
        elif opt.rotate_mode == "angle":
            th = opt.rotate_angle * math.pi / 180.0
            vfilters.append(f"rotate={th}:c=black@0:ow=rotw({th}):oh=roth({th})")
        if opt.scale:
            vfilters.append(f"scale={opt.scale}")
        if opt.fps:
            vfilters.append(f"fps={opt.fps}")

        # 倍速
        sp = max(0.1, opt.speed)
        if abs(sp - 1.0) > 1e-6:
            vfilters.append(f"setpts={1.0/sp}*PTS")

        if vfilters:
            args += ["-vf", ",".join(vfilters)]

        # 音频
        if opt.remove_audio:
            args += ["-an"]
        else:
            # 倍速下的音频 atempo 拆分到 0.5~2 范围
            afs = []
            if abs(sp - 1.0) > 1e-6:
                remain = sp
                while remain > 2.0 + 1e-9:
                    afs.append("atempo=2.0"); remain /= 2.0
                while remain < 0.5 - 1e-9:
                    afs.append("atempo=0.5"); remain /= 0.5
                afs.append(f"atempo={remain:.6f}")
            if afs:
                args += ["-af", ",".join(afs)]
            args += ["-c:a", opt.acodec]

        # 视频编码参数
        vcodec = opt.vcodec
        if vcodec == "copy" and vfilters:
            # 不能滤镜+copy
            vcodec = "libx264"
        args += ["-c:v", vcodec]
        if vcodec in ("libx264","libx265","libaom-av1","libvpx-vp9"):
            if opt.v_bitrate:
                args += ["-b:v", opt.v_bitrate]
            else:
                args += ["-crf", str(opt.crf), "-preset", opt.preset]
        elif opt.v_bitrate:
            args += ["-b:v", opt.v_bitrate]

        # 输出容器
        out_ext = Path(out_path).suffix.lower().lstrip(".")
        if not out_ext:
            out_path = str(Path(out_path).with_suffix(f".{opt.container}"))
        return args + [out_path]

    def run_ffmpeg(self, cmd: List[str]):
        self.log.clear()
        self._append_log("==== 开始任务 ====")
        self.worker = FFmpegWorker(cmd)
        self.worker.line.connect(self._append_log)
        self.worker.progress.connect(self._on_progress)
        self.worker.finished_ok.connect(lambda: self._task_done(True))
        self.worker.finished_fail.connect(lambda rc: self._task_done(False, rc))
        self.btn_export.setEnabled(False)
        self.worker.start()

    def _on_progress(self, sec: float):
        # 将进度映射到 slider
        if self.slider.isEnabled():
            ms = int(sec * 1000)
            self.slider.setValue(min(self.slider.maximum(), ms))

    def _task_done(self, ok: bool, rc: int = 0):
        self.btn_export.setEnabled(True)
        if ok:
            self._append_log("[完成] 任务成功")
            QMessageBox.information(self, "完成", "导出完成")
        else:
            self._append_log(f"[失败] 返回码 {rc}")
            QMessageBox.critical(self, "失败", f"导出失败，返回码 {rc}")

    def _append_log(self, s: str):
        self.log.appendPlainText(s)
        self.log.verticalScrollBar().setValue(self.log.verticalScrollBar().maximum())

    # ---------------- 拼接管理 ----------------
    def _ct_add(self):
        files, _ = QFileDialog.getOpenFileNames(self, "选择要拼接的视频", "", "视频文件 (*.mp4 *.mkv *.mov *.webm *.ts *.m4v);;所有文件 (*.*)")
        for f in files:
            if f:
                self.list_concat.addItem(QListWidgetItem(f))

    def _ct_move(self, delta: int):
        items = self.list_concat.selectedItems()
        if not items:
            return
        for it in items:
            row = self.list_concat.row(it)
            new_row = min(max(0, row + delta), self.list_concat.count()-1)
            if new_row != row:
                it = self.list_concat.takeItem(row)
                self.list_concat.insertItem(new_row, it)
                self.list_concat.setCurrentItem(it)

    def _ct_del(self):
        for it in self.list_concat.selectedItems():
            row = self.list_concat.row(it)
            self.list_concat.takeItem(row)


# ---------------------- 入口 ----------------------
def main():
    app = QApplication(sys.argv)
    app.setApplicationName("PyQt Video Editor")
    win = MainWindow()
    win.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
