from PySide6.QtCore import Qt
from PySide6.QtGui import QCursor
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout


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


if __name__ == '__main__':
    app = QApplication([])
    app.setQuitOnLastWindowClosed(False)  # 防止程序在關閉最後一個窗口時退出
    window = BaseWidget()
    window.show()
    app.exec()
