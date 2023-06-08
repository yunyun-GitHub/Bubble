import os
import clr
import time
from PySide6.QtCore import QThread, Signal
from Bubble.settings import BASE_DIR

# 加载OpenHardwareMonitorLib.dll文件
clr.AddReference(os.path.join(BASE_DIR, "cputemp", "OpenHardwareMonitorLib.dll"))
from OpenHardwareMonitor.Hardware import *


class CPUTemp(QThread):
    data_signal = Signal(str)

    def __init__(self):
        super().__init__()
        self.running = True
        self.computer = Computer()  # 创建Computer类的实例
        self.computer.CPUEnabled = True  # 设置需要获取的硬件信息
        self.computer.Open()  # 打开硬件监控功能

    def run(self):
        while self.running:
            cputemp_list = []
            for hardware in self.computer.Hardware:
                if hardware.HardwareType == HardwareType.CPU:
                    hardware.Update()
                    for sensor in hardware.Sensors:
                        if sensor.SensorType == SensorType.Temperature:
                            cputemp_list.append([sensor.Name, sensor.Value])
            cputemp = self.conversion(cputemp_list)
            self.data_signal.emit(cputemp)
            time.sleep(1)  # 暂停1秒
            # print(cputemp)

    @staticmethod
    def conversion(matrix, column_index=1):
        """获取二维列表中第一列的最大值"""
        max_value = matrix[0][column_index]  # 初始化最大值为第一个元素
        for row in matrix:
            if row[column_index] > max_value:
                max_value = row[column_index]
        return str(round(max_value)) + "°C"

    def stop(self):
        self.running = False
        self.wait()  # 等待子線程結束


if __name__ == "__main__":
    cpu_temp = CPUTemp()
    cpu_temp.start()
    time.sleep(10)
