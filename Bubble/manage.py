import os

from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QWidget, QApplication

from Bubble.settings import BASE_DIR
from Bubble.systemtray import TrayIcon
from cputemp.views import CPUTempWidget
from netspeed.views import NetSpeedWidget


class ManageWin(QWidget):
    def __init__(self):
        super().__init__()

        # 創建一個托盤對象，並把它設置為類的屬性
        self.tray = TrayIcon(QIcon(os.path.join(BASE_DIR, "Bubble/img/bubble.png")), self)
        self.tray.setVisible(True)  # 設置托盤對象的可見性

        self.netspeed = NetSpeedWidget()
        self.netspeed.show()
        self.cputemp = CPUTempWidget()
        self.cputemp.show()

    def show_front(self):
        # 顯示在屏幕最前面,取代show()函數
        flags = self.windowFlags()
        self.setWindowFlags(flags | Qt.WindowStaysOnTopHint)
        self.show()
        self.setWindowFlags(flags)
        self.show()


if __name__ == "__main__":
    app = QApplication([])
    app.setQuitOnLastWindowClosed(False)  # 防止程序在關閉最後一個窗口時退出
    window = ManageWin()
    window.show()  # 主窗口一開始不可見
    app.exec()
