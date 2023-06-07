from PySide6.QtGui import QIcon, QAction
from PySide6.QtWidgets import QApplication, QSystemTrayIcon, QMenu


class TrayIcon(QSystemTrayIcon):
    def __init__(self, icon, parent=None):
        super().__init__(icon, parent)
        self.manage_win = parent

        # Create the menu
        self.menu = QMenu()
        self.action = QAction("退出(Exit)")
        # QApplication.instance()這個靜態方法能獲取當前的應用對象,調用它的quit方法,就不需要在類裏引用app變量了
        self.action.triggered.connect(QApplication.instance().quit)  # 當點擊退出時，退出程序
        self.menu.addAction(self.action)
        # 设置右擊時彈出菜單
        self.setContextMenu(self.menu)

        # 連接托盤圖標的activated信號和activate方法
        self.activated.connect(self.activate)

    def activate(self, reason):
        """
        ActivationReason.Trigger  左键单击
        ActivationReason.DoubleClick  左键双击
        ActivationReason.Context  右键单击
        """
        # 如果鼠標左擊托盤圖標，切換主窗口的可見性
        if reason == self.ActivationReason.Trigger:
            if self.manage_win is not None:
                if self.manage_win.isVisible():
                    self.manage_win.hide()
                else:
                    self.manage_win.show_front()


if __name__ == "__main__":
    app = QApplication([])
    app.setQuitOnLastWindowClosed(False)  # 防止程序在關閉最後一個窗口時退出
    tray = TrayIcon(QIcon("img/bubble.png"))
    tray.setVisible(True)
    app.exec()
