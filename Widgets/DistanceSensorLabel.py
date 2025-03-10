from PySide6.QtWidgets import QLabel
from PySide6.QtCore import Qt, Signal
from NetworkTableManager import NetworkTableManager


class DistanceSensorLabel(QLabel):
    def __init__(self, parent = None):
        super().__init__(parent)

        self.distSensorStatusNTManager = NetworkTableManager(tableName ="Sensors", entryName ="Intake Distance Sensor")
        self.distSensorStatusNTManager.new_value_available.connect(self.setStatus)
        self.timeleft = 300
        self.setAlignment(Qt.AlignCenter)
        self.setAutoFillBackground(True)
        self.generalStyleSheet = "color: white;"\
            "font-weight: bold; font-size: 20px;background-color: rgb(50,50,50);"
        self.setStyleSheet(self.generalStyleSheet)
        self.setText("Distance Sensor:\nNo Data")
        self.manualUpdate()

    def setStatus(self, message: tuple):
        if (message[1]):

            self.setText("Dist Sensor:\nDetected")
            self.setStyleSheet("background-color: rgb(0,50,0);" + self.generalStyleSheet)
        else:
            self.setText("Dist Sensor:\nNot Detected")
            self.setStyleSheet("background-color: rgb(50,50,50);" + self.generalStyleSheet)
    def manualUpdate(self):
        self.setStatus(("init", self.distSensorStatusNTManager.getValue()))

