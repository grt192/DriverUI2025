from PySide6.QtWidgets import  QLabel
from PySide6.QtCore import Qt
from NetworkTableManager import NetworkTableManager


class DoubleDisplayLabel(QLabel):
    def __init__(self):
        super().__init__()

    def networkStuff(self,parameterName,tableName,entryName):
        self.parameterName = parameterName
        self.tableName = tableName
        self.entryName = entryName

        self.NTManager = NetworkTableManager(
            tableName=tableName, entryName=entryName
        )
        self.NTManager.new_value_available.connect(self.updateFromNT)

        if self.NTManager.getValue() is not None:
            self.updateFromNT(self.NTManager.getValue())    
    def updateFromNT(self, message: float):
        self.setText(self.parameterName + str(message))