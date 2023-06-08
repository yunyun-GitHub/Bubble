from PySide6.QtCore import Qt
from PySide6.QtGui import QCursor, QGuiApplication
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel


class BaseWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.relative_position = QCursor.pos() - self.pos()  # 相對位置
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint | Qt.SubWindow)  # 置顶窗口,无边框,隐藏任务栏图标
        self.setAttribute(Qt.WA_TranslucentBackground)  # 使透明效果生效

        # QWidget不是顶层窗口，必须再套一层
        self.widget = QWidget(self)
        self.verticalLayout = QVBoxLayout(self)
        self.verticalLayout.addWidget(self.widget)

    def mouseDoubleClickEvent(self, event):
        """双击隐藏"""
        self.close()

    def mousePressEvent(self, event):
        """左键按下"""
        self.relative_position = QCursor.pos() - self.pos()

    def mouseMoveEvent(self, event):
        """左键移动"""
        self.move(QCursor.pos() - self.relative_position)


class BWidget(BaseWidget):
    def __init__(self, DataThread):
        super().__init__()

        # 背景图片 文字颜色和大小的樣式(qss)
        self.style_sheet = u".QWidget .QLabel {color: #FFFFFF; font-size: 13px;}"
        self.widget.setStyleSheet(self.style_sheet)  # 设置样式

        self.size = [180, 166]  # 窗口大小
        self.label_pos = [10, 35]  # 文字位置
        self.position = [0, 0]  # 窗口位置

        # 创建窗口
        self.resize(self.size[0], self.size[1])  # 设置窗口大小
        screen = QGuiApplication.primaryScreen().size()  # 获得屏幕的尺寸
        self.move(screen.width() - self.position[0] - self.size[0],
                  screen.height() - self.position[1] - self.size[1])  # 调用move移动到右下角位置

        self.label = QLabel("", self.widget)  # 创建文字
        self.label.setAlignment(Qt.AlignRight)  # 右对齐

        # 启动子线程
        self.data_thread = DataThread()
        self.data_thread.start()

    def update_label(self, data):
        """更新系统信息,以右上角为锚点，设置位置，以及内容"""

        self.label.setText(data)
        self.label.adjustSize()  # QLabel自适应内容大小
        self.label.move(self.size[0] - self.label_pos[0] - self.label.width() - 20,
                        self.size[1] - self.label_pos[1] - self.label.height() - 20)

    def closeEvent(self, event):
        self.data_thread.stop()
