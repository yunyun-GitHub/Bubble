from PySide6.QtWidgets import QApplication

from Bubble.manage import ManageWin

if __name__ == "__main__":
    app = QApplication([])
    app.setQuitOnLastWindowClosed(False)  # 防止程序在關閉最後一個窗口時退出
    window = ManageWin()
    # window.show()  # 主窗口一開始不可見
    app.exec()
