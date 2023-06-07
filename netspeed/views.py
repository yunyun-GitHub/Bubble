from PySide6.QtCore import Qt
from PySide6.QtGui import QGuiApplication
from PySide6.QtWidgets import QApplication, QLabel

from common.widgets import BaseWidget
from netspeed.data import NetSpeed


class NetSpeedWidget(BaseWidget):
    def __init__(self):
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
        self.netspeed_thread = NetSpeed()
        self.netspeed_thread.netspeed_signal.connect(self.update_netspeed)
        self.netspeed_thread.start()

    def update_netspeed(self, netspeed):
        """更新系统信息,以右上角为锚点，设置位置，以及内容"""

        self.label.setText(netspeed)
        self.label.adjustSize()  # QLabel自适应内容大小
        self.label.move(self.size[0] - self.label_pos[0] - self.label.width() - 20,
                        self.size[1] - self.label_pos[1] - self.label.height() - 20)

    def closeEvent(self, event):
        self.netspeed_thread.stop()


if __name__ == "__main__":
    app = QApplication([])
    app.setQuitOnLastWindowClosed(False)  # 防止程序在關閉最後一個窗口時退出
    window = NetSpeedWidget()
    window.show()
    app.exec()
