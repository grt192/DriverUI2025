"""
This file defines a customized text widget that displays "Hello World".
"""
from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout, QSizePolicy
from NetworkTableManager import NetworkTableManager
from PySide6.QtCore import Qt

class TextWidget(QWidget):

  def __init__(self):
    super().__init__()
    # Qlabel is the basic component, it can be customized for different
    # purposes.
    self.textLabel = QLabel("Hello World", self)
    layout = QVBoxLayout()
    # Add the view to the layout
    layout.addWidget(self.textLabel)

    # Set the layout for the window
    self.setLayout(layout)
    self.textLabel.setText("0.0")
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
      pass
        #self.textLabel.setText(str(message))
        #self.setText(self.parameterName + str(message))

