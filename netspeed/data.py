import time
import psutil
from PySide6.QtCore import QThread, Signal


class NetSpeed(QThread):
    netspeed_signal = Signal(str)

    def __init__(self):
        super().__init__()
        self.running = True

    def run(self):
        sent_before = psutil.net_io_counters().bytes_sent  # 已发送的流量
        recv_before = psutil.net_io_counters().bytes_recv  # 已接收的流量
        while self.running:
            time.sleep(1)  # 暂停1秒
            sent_now = psutil.net_io_counters().bytes_sent
            recv_now = psutil.net_io_counters().bytes_recv

            # 算出1秒后的差值,并转换
            sent = self.conversion(sent_now - sent_before)
            recv = self.conversion(recv_now - recv_before)

            sent_before = sent_now
            recv_before = recv_now

            self.netspeed_signal.emit(f"{sent} ↑\n{recv} ↓")
            # print(f"{sent} ↑\n{recv} ↓")

    @staticmethod
    def conversion(bit):
        if bit < 1024:
            speed = '%sB' % bit
        elif bit < 1048576:
            speed = '%sK' % round(bit / 1024, 2)
        else:
            speed = '%sM' % round(bit / 1048576, 2)
        return speed + "/s"

    def stop(self):
        self.running = False
        self.wait()  # 等待子線程結束


if __name__ == "__main__":
    netspeed = NetSpeed()
    netspeed.start()
    time.sleep(10)
