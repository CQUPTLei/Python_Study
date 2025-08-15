# -*- coding = utf-8 -*-
# @TIME : 2025/08/15 11:58
# @Author : Grace
# @File : photo_edit.py
# @Software : PyCharm Professional 2025.1.2
# Introduction：
import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QLabel, QFileDialog, QDockWidget, QListWidget,
    QVBoxLayout, QWidget, QSlider, QPushButton, QLineEdit, QFormLayout,
    QDialog, QDialogButtonBox, QComboBox, QColorDialog, QSpinBox, QGraphicsScene,
    QGraphicsView, QGraphicsPixmapItem, QRubberBand
)
from PyQt6.QtGui import (
    QPixmap, QImage, QPainter, QTransform, QFont, QColor, QIcon, QAction, QPen, QBrush
)
from PyQt6.QtCore import (
    Qt, QSize, QRect, QPoint
)


# 自定义一个QLabel，用于处理鼠标事件以实现裁剪和马赛克功能
class PhotoViewer(QLabel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setScaledContents(False)
        self.setMinimumSize(1, 1)
        self.rubber_band = None
        self.mode = None  # 'CROP', 'ASPECT_CROP', 'MOSAIC'
        self.aspect_ratio = 16 / 9

    def set_mode(self, mode, aspect_ratio=None):
        self.mode = mode
        if aspect_ratio:
            self.aspect_ratio = aspect_ratio
        self.setCursor(Qt.CursorShape.CrossCursor if mode else Qt.CursorShape.ArrowCursor)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton and self.mode:
            self.origin = event.pos()
            if not self.rubber_band:
                self.rubber_band = QRubberBand(QRubberBand.Shape.Rectangle, self)
            self.rubber_band.setGeometry(QRect(self.origin, QSize()))
            self.rubber_band.show()

    def mouseMoveEvent(self, event):
        if self.rubber_band and not self.origin.isNull():
            end_point = event.pos()

            # 限制选框在图片范围内
            pixmap_rect = self.pixmap().rect()
            end_point.setX(max(0, min(end_point.x(), pixmap_rect.width())))
            end_point.setY(max(0, min(end_point.y(), pixmap_rect.height())))

            rect = QRect(self.origin, end_point).normalized()

            if self.mode == 'ASPECT_CROP':
                if rect.width() / self.aspect_ratio > rect.height():
                    rect.setHeight(int(rect.width() / self.aspect_ratio))
                else:
                    rect.setWidth(int(rect.height() * self.aspect_ratio))

                # 再次检查边界
                if rect.right() > pixmap_rect.width():
                    rect.setWidth(pixmap_rect.width() - rect.left())
                    rect.setHeight(int(rect.width() / self.aspect_ratio))
                if rect.bottom() > pixmap_rect.height():
                    rect.setHeight(pixmap_rect.height() - rect.top())
                    rect.setWidth(int(rect.height() * self.aspect_ratio))

            self.rubber_band.setGeometry(rect)

    def mouseReleaseEvent(self, event):
        if self.rubber_band and event.button() == Qt.MouseButton.LeftButton:
            self.parent().apply_selection(self.rubber_band.geometry(), self.mode)
            self.rubber_band.hide()
            self.set_mode(None)
            self.origin = QPoint()


class EditorWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PyQt6 图片编辑器")
        self.setGeometry(100, 100, 1200, 800)

        self.original_pixmap = None
        self.current_pixmap = None

        # --- 中心控件 ---
        self.image_viewer = PhotoViewer(self)
        self.image_viewer.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setCentralWidget(self.image_viewer)

        # --- 菜单栏 ---
        self.create_menus()

        # --- 工具栏 ---
        self.create_toolbar()

        # --- 控制面板 ---
        self.create_controls_dock()

    def create_menus(self):
        menu_bar = self.menuBar()
        # 文件菜单
        file_menu = menu_bar.addMenu("文件")
        open_action = QAction("打开", self)
        open_action.triggered.connect(self.open_image)
        save_action = QAction("保存", self)
        save_action.triggered.connect(self.save_image)
        save_as_action = QAction("另存为...", self)
        save_as_action.triggered.connect(self.save_as_image)
        file_menu.addActions([open_action, save_action, save_as_action])

        # 编辑菜单
        edit_menu = menu_bar.addMenu("编辑")
        reset_action = QAction("重置所有更改", self)
        reset_action.triggered.connect(self.reset_image)
        edit_menu.addAction(reset_action)

    def create_toolbar(self):
        toolbar = self.addToolBar("常用工具")
        open_action = QAction(QIcon.fromTheme("document-open"), "打开", self)
        open_action.triggered.connect(self.open_image)
        save_action = QAction(QIcon.fromTheme("document-save"), "保存", self)
        save_action.triggered.connect(self.save_image)
        reset_action = QAction(QIcon.fromTheme("edit-undo"), "重置", self)
        reset_action.triggered.connect(self.reset_image)
        toolbar.addActions([open_action, save_action, reset_action])

    def create_controls_dock(self):
        dock = QDockWidget("控制面板", self)
        self.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, dock)

        controls_widget = QWidget()
        layout = QVBoxLayout(controls_widget)
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        # 旋转
        layout.addWidget(QLabel("旋转:"))
        self.rotation_slider = QSlider(Qt.Orientation.Horizontal)
        self.rotation_slider.setRange(-180, 180)
        self.rotation_slider.setValue(0)
        self.rotation_slider.valueChanged.connect(self.rotate_image)
        layout.addWidget(self.rotation_slider)

        # 缩放
        layout.addWidget(QLabel("缩放:"))
        scale_btn = QPushButton("调整尺寸")
        scale_btn.clicked.connect(self.show_scale_dialog)
        layout.addWidget(scale_btn)

        # 裁剪
        layout.addWidget(QLabel("裁剪:"))
        crop_btn = QPushButton("自由裁剪")
        crop_btn.clicked.connect(lambda: self.image_viewer.set_mode('CROP'))
        layout.addWidget(crop_btn)

        self.aspect_combo = QComboBox()
        self.aspect_combo.addItems(["16:9", "4:3", "1:1", "3:4", "9:16"])
        aspect_crop_btn = QPushButton("按比例裁剪")
        aspect_crop_btn.clicked.connect(self.start_aspect_crop)
        layout.addWidget(self.aspect_combo)
        layout.addWidget(aspect_crop_btn)

        # 马赛克
        layout.addWidget(QLabel("效果:"))
        mosaic_btn = QPushButton("添加马赛克")
        mosaic_btn.clicked.connect(lambda: self.image_viewer.set_mode('MOSAIC'))
        layout.addWidget(mosaic_btn)

        # 水印
        watermark_btn = QPushButton("添加水印")
        watermark_btn.clicked.connect(self.show_watermark_dialog)
        layout.addWidget(watermark_btn)

        dock.setWidget(controls_widget)

    def open_image(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "打开图片", "", "图片文件 (*.png *.jpg *.jpeg *.bmp)")
        if file_name:
            self.original_pixmap = QPixmap(file_name)
            self.current_pixmap = self.original_pixmap.copy()
            self.image_viewer.setPixmap(self.current_pixmap)
            self.reset_controls()

    def save_image(self):
        self.save_as_image()

    def save_as_image(self):
        if self.current_pixmap:
            file_name, _ = QFileDialog.getSaveFileName(self, "保存图片", "",
                                                       "PNG (*.png);;JPEG (*.jpg *.jpeg);;BMP (*.bmp)")
            if file_name:
                # 对于JPEG格式，可以询问压缩质量
                if file_name.lower().endswith(('.jpg', '.jpeg')):
                    quality, ok = QSpinBox.getInt(self, "JPEG 质量", "质量 (1-100):", 90, 1, 100)
                    if ok:
                        self.current_pixmap.save(file_name, "JPG", quality)
                else:
                    self.current_pixmap.save(file_name)

    def reset_image(self):
        if self.original_pixmap:
            self.current_pixmap = self.original_pixmap.copy()
            self.image_viewer.setPixmap(self.current_pixmap)
            self.reset_controls()

    def reset_controls(self):
        self.rotation_slider.setValue(0)

    def update_preview(self):
        if self.current_pixmap:
            # 基础是原始图片
            temp_pixmap = self.original_pixmap.copy()

            # 1. 应用旋转
            angle = self.rotation_slider.value()
            if angle != 0:
                transform = QTransform().rotate(angle)
                temp_pixmap = temp_pixmap.transformed(transform, Qt.TransformationMode.SmoothTransformation)

            # 更新current_pixmap和预览
            self.current_pixmap = temp_pixmap
            self.image_viewer.setPixmap(self.current_pixmap)

    def rotate_image(self):
        if self.original_pixmap is None: return
        angle = self.rotation_slider.value()
        transform = QTransform().rotate(angle)
        self.current_pixmap = self.original_pixmap.transformed(transform, Qt.TransformationMode.SmoothTransformation)
        self.image_viewer.setPixmap(self.current_pixmap)

    def show_scale_dialog(self):
        if not self.current_pixmap: return

        dialog = QDialog(self)
        dialog.setWindowTitle("调整尺寸")
        form = QFormLayout(dialog)

        width_edit = QLineEdit(str(self.current_pixmap.width()))
        height_edit = QLineEdit(str(self.current_pixmap.height()))

        form.addRow("宽度 (px):", width_edit)
        form.addRow("高度 (px):", height_edit)

        buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        buttons.accepted.connect(dialog.accept)
        buttons.rejected.connect(dialog.reject)
        form.addWidget(buttons)

        if dialog.exec():
            try:
                w = int(width_edit.text())
                h = int(height_edit.text())
                self.current_pixmap = self.current_pixmap.scaled(w, h, Qt.AspectRatioMode.KeepAspectRatio,
                                                                 Qt.TransformationMode.SmoothTransformation)
                self.original_pixmap = self.current_pixmap.copy()  # 缩放后设为新的"原始"图
                self.image_viewer.setPixmap(self.current_pixmap)
            except ValueError:
                pass  # 输入无效则忽略

    def start_aspect_crop(self):
        ratio_str = self.aspect_combo.currentText()
        w, h = map(int, ratio_str.split(':'))
        self.image_viewer.set_mode('ASPECT_CROP', aspect_ratio=w / h)

    def apply_selection(self, rect, mode):
        if not self.current_pixmap: return

        if mode == 'CROP' or mode == 'ASPECT_CROP':
            self.current_pixmap = self.current_pixmap.copy(rect)
            self.original_pixmap = self.current_pixmap.copy()  # 裁剪后设为新的"原始"图
            self.image_viewer.setPixmap(self.current_pixmap)
        elif mode == 'MOSAIC':
            self.apply_mosaic(rect)

    def apply_mosaic(self, rect, block_size=10):
        if not self.current_pixmap: return

        image = self.current_pixmap.toImage()
        # 确保rect在图像范围内
        rect = rect.intersected(image.rect())

        for y in range(rect.top(), rect.bottom(), block_size):
            for x in range(rect.left(), rect.right(), block_size):
                # 定义一个马赛克块的区域
                block_rect = QRect(x, y, min(block_size, rect.right() - x), min(block_size, rect.bottom() - y))

                # 计算块内平均颜色
                r, g, b, a_sum = 0, 0, 0, 0
                count = 0
                for i in range(block_rect.left(), block_rect.right()):
                    for j in range(block_rect.top(), block_rect.bottom()):
                        color = image.pixelColor(i, j)
                        r += color.red()
                        g += color.green()
                        b += color.blue()
                        a_sum += color.alpha()
                        count += 1

                if count > 0:
                    avg_color = QColor(r // count, g // count, b // count, a_sum // count)

                    # 用平均颜色填充整个块
                    painter = QPainter(image)
                    painter.fillRect(block_rect, avg_color)
                    painter.end()

        self.current_pixmap = QPixmap.fromImage(image)
        self.image_viewer.setPixmap(self.current_pixmap)

    def show_watermark_dialog(self):
        if not self.current_pixmap: return

        dialog = QDialog(self)
        dialog.setWindowTitle("添加水印")
        layout = QVBoxLayout(dialog)

        # ... (此处可以添加更复杂的UI让用户选择文字或图片)
        text_edit = QLineEdit("在此输入水印文字")
        opacity_slider = QSlider(Qt.Orientation.Horizontal)
        opacity_slider.setRange(0, 255)
        opacity_slider.setValue(128)

        layout.addWidget(QLabel("水印文字:"))
        layout.addWidget(text_edit)
        layout.addWidget(QLabel("不透明度:"))
        layout.addWidget(opacity_slider)

        buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        buttons.accepted.connect(dialog.accept)
        buttons.rejected.connect(dialog.reject)
        layout.addWidget(buttons)

        if dialog.exec():
            text = text_edit.text()
            opacity = opacity_slider.value()
            self.apply_text_watermark(text, opacity)

    def apply_text_watermark(self, text, opacity):
        if not self.current_pixmap: return

        pixmap = self.current_pixmap.copy()
        painter = QPainter(pixmap)

        font = QFont()
        # 字体大小可以根据图片大小动态调整
        font_size = max(12, int(pixmap.width() / 20))
        font.setPointSize(font_size)
        painter.setFont(font)

        color = QColor(255, 255, 255, opacity)
        painter.setPen(color)

        # 将水印绘制在右下角
        metrics = painter.fontMetrics()
        text_width = metrics.horizontalAdvance(text)
        text_height = metrics.height()
        x = pixmap.width() - text_width - 10
        y = pixmap.height() - text_height

        painter.drawText(x, y, text)
        painter.end()

        self.current_pixmap = pixmap
        self.image_viewer.setPixmap(self.current_pixmap)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = EditorWindow()
    window.show()
    sys.exit(app.exec())