from PySide6.QtWidgets import QLabel
from PySide6.QtCore import Qt, Signal
from NetworkTableManager import NetworkTableManager


class ElevatorLimitSwitchLabel(QLabel):
    def __init__(self, parent = None):
        super().__init__(parent)

        self.distSensorStatusNTManager = NetworkTableManager(tableName ="Sensors", entryName ="Elevator Limit Switch")
        self.distSensorStatusNTManager.new_value_available.connect(self.setStatus)
        self.timeleft = 300
        self.setAlignment(Qt.AlignCenter)
        self.setAutoFillBackground(True)
        self.generalStyleSheet = "color: white;"\
            "font-weight: bold; font-size: 20px;"
        self.setStyleSheet(self.generalStyleSheet)
        self.setText("Limit Switch:\nNo Data")


    def setStatus(self, message: tuple):
        if (message[1]):
            self.setText("Limit Switch:\nNot Detected")
            self.setStyleSheet("background-color: rgb(50,50,50);" + self.generalStyleSheet)

        else:
            self.setText("Limit Switch:\nDetected")
            self.setStyleSheet("background-color: rgb(0,50,0);" + self.generalStyleSheet)


