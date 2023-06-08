from PySide6.QtWidgets import QApplication

from common.widgets import BWidget
from cputemp.data import CPUTemp


class CPUTempWidget(BWidget):
    def __init__(self):
        super().__init__(CPUTemp)
        self.label_pos = [90, 35]  # 文字位置
        self.data_thread.data_signal.connect(self.update_label)


if __name__ == "__main__":
    app = QApplication([])
    app.setQuitOnLastWindowClosed(False)  # 防止程序在關閉最後一個窗口時退出
    window = CPUTempWidget()
    window.show()
    app.exec()
