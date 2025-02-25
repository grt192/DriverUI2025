"""
This file creates an empty window with the title "Hello World".
Run this file to see the window.
"""
import sys
from PySide6.QtWidgets import *
# from PySide6.QtWidgets import QApplication, QMainWindow
# from PySide6.QtWidgets import QLabel, QVBoxLayout, QWidget
# from PySide6.QtWidgets import QLabel, QHBoxLayout, QWidget

# from PySide6.QtWidgets import QGridLayout

from WheelImage import wheelImage
from Widgets.TimeLeftLabel import TimeLeftLabel
from Widgets.VisionCamConnectivityWidget import VisionCamConnectivityWidget
from Widgets.DistanceSensorLabel import DistanceSensorLabel
from Widgets.CameraWidget import CameraWidget
from Widgets.PushButtonWidget import PushButtonWidget
from Widgets.FieldWidget import MapWidget
from Widgets.AllianceLabel import AllianceLabel
# Every UI has a MainWindows that contains everything. 
class GRT2025DriverUI(QMainWindow):


  # We setup the window's title, size, and show it.
  def __init__(self):
    super().__init__()
    self.setWindowTitle("GRT 2025 Driver UI")
    self.resize(1920, 630)
    self.setMaximumHeight(630)

    self.centralWidget = QWidget(self)#omagic
    self.mainLayout = QHBoxLayout(self)
    self.centralWidget.setLayout(self.mainLayout)
    self.setCentralWidget(self.centralWidget)
    
    #vertical section for all the info boxes
    self.infoBoxWidget = QWidget(self)
    self.infoBoxLayout = QVBoxLayout(self)
    self.infoBoxLayout.addWidget(AllianceLabel(self))
    self.infoBoxWidget.setFixedWidth(200)
    self.infoBoxLayout.addWidget(TimeLeftLabel(self))
    self.infoBoxLayout.addWidget(DistanceSensorLabel(self))
    self.infoBoxWidget.setLayout(self.infoBoxLayout)

    self.cam1Connectivity = VisionCamConnectivityWidget("10.1.92.12")
    # self.cam2Connectivity = VisionCamConnectivityWidget("10.1.92.13")
    # self.cam3Connectivity = VisionCamConnectivityWidget("10.1.92.14")
    # self.cam4Connectivity = VisionCamConnectivityWidget("10.1.92.15")

    self.mapWidget = MapWidget(500)

    self.cameraWidget = CameraWidget()

    self.displayBoxWidget = QWidget(self)
    self.displayBoxLayout = QVBoxLayout()
    self.displayBoxLayout.addWidget(self.mapWidget)
    #self.displayBoxLayout.addWidget(self.cameraWidget)
    self.displayBoxWidget.setLayout(self.displayBoxLayout)
    self.displayBoxWidget.setMaximumWidth(550)
    # self.topRightWheel = wheelImage()
    # self.mainLayout.addWidget(self.topRightWheel,0,0)#y x

    # self.buttonWidget = PushButtonWidget()
    # self.buttonWidget.buttonClass =self.bottomLeftWheel
    # self.mainLayout.addWidget(self.buttonWidget,0,3)
    self.mainLayout.addWidget(self.infoBoxWidget)
    self.mainLayout.addWidget(self.displayBoxWidget)
    self.cameraStuffWidget = QWidget(self)
    self.cameraStuffLayout = QVBoxLayout()
    self.cameraStuffWidget.setLayout(self.cameraStuffLayout)
    self.mainLayout.addWidget(self.cameraStuffWidget)
    self.cameraStuffLayout.addWidget(self.cameraWidget)
    self.cameraStuffLayout.addWidget(self.cam1Connectivity)
    # self.cameraStuffLayout.addWidget(self.cam2Connectivity)
    # self.cameraStuffLayout.addWidget(self.cam3Connectivity)
    # self.cameraStuffLayout.addWidget(self.cam4Connectivity)


    self.show()

# This is the tamplate to start the UI, just copy it.
if __name__ == "__main__":
  app = QApplication(sys.argv)
  window = GRT2025DriverUI()
  window.showFullScreen()
  window.setGeometry(0, 0, 1920, 780)

    # Replace this with the URL of your image stream
    # stream_url = "https://via.placeholder.com/800x600.png"

    # # Create and show the widget
    # viewer = ImageStreamWidget(stream_url, refresh_interval=1000)
    # viewer.resize(800, 600)
    # viewer.show()

  sys.exit(app.exec())


