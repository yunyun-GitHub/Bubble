from PySide6.QtWidgets import QApplication

from common.widgets import BWidget
from netspeed.data import NetSpeed


class NetSpeedWidget(BWidget):
    def __init__(self):
        super().__init__(NetSpeed)
        self.label_pos = [10, 35]  # 文字位置
        self.data_thread.data_signal.connect(self.update_label)


if __name__ == "__main__":
    app = QApplication([])
    app.setQuitOnLastWindowClosed(False)  # 防止程序在關閉最後一個窗口時退出
    window = NetSpeedWidget()
    window.show()
    app.exec()
