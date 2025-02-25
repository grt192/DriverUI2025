from PySide6.QtWidgets import QLabel
from PySide6.QtCore import Qt, Signal
from NetworkTableManager import NetworkTableManager


class TimeLeftLabel(QLabel):
    isRedSignal = Signal(bool)
    def __init__(self, parent = None):
        super().__init__(parent)

        self.timeLeftNTManager = NetworkTableManager(tableName ="FMSInfo", entryName ="TimeLeft")
        self.timeLeftNTManager.new_value_available.connect(self.setTimeLeft)
        self.timeleft = 300
        self.setAlignment(Qt.AlignCenter)
        self.setAutoFillBackground(True)
        self.generalStyleSheet = "color: white;"\
            "font-weight: bold; font-size: 20px;"
        self.setStyleSheet(self.generalStyleSheet)
        self.setText("Time Left:\nNo Data")


    def setTimeLeft(self, message: tuple):
        print(message[1])
        
        self.setText("Red " + str(message[1]))
            
