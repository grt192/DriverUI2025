"""
This file defines a customized text widget that displays "Hello World".
"""
import time
from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout, QSizePolicy
from NetworkTableManager import NetworkTableManager
from PySide6.QtCore import Qt, QTimer
from pythonping import ping
import threading

class VisionCamConnectivityWidget(QWidget):


  def __init__(self, ip):
    super().__init__()
    self.ip = ip
    # Qlabel is the basic component, it can be customized for different
    # purposes.
    self.textLabel = QLabel("Checking Connectivity" , self)
    layout = QVBoxLayout()
    # Add the view to the layout
    layout.addWidget(self.textLabel)

    # Set the layout for the window
    self.setLayout(layout)
    #self.textLabel.setText("0.0")
    #self.networkStuff("defaultParameter","networkTable","networkTableEntry")
    self.textLabel.setAutoFillBackground(True)
    self.textLabel.setFixedWidth(480)

    self.textLabel.generalStyleSheet = "color: black;"\
            "font-weight: bold; font-size: 20px;"

    self.timer = QTimer()
    self.timer.timeout.connect(self.checkConnectivity)
    self.timer.start(3000)  # Update every 1000 ms (1 second)

  def checkConnectivity(self):
    self.t1 = threading.Thread(target =self.threadedPing)

    self.t1.start()

  def threadedPing(self):
      
      result = ping(self.ip,timeout=0.1)
      if (result.success()):
        self.textLabel.setText(str(self.ip) + " Connected")
        self.textLabel.setStyleSheet("background-color: rgb(0,255,0);" + self.textLabel.generalStyleSheet)

      else:
        self.textLabel.setText(str(self.ip) + " Not Connected!")
        self.textLabel.setStyleSheet("background-color: rgb(255,0,0);" + self.textLabel.generalStyleSheet)
