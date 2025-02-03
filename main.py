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
from Widgets.TextWidget import TextWidget
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

    self.centralWidget = QWidget(self)#magic
    self.mainLayout = QHBoxLayout(self)
    self.centralWidget.setLayout(self.mainLayout)
    self.setCentralWidget(self.centralWidget)
    
    self.infoBoxWidget = QWidget(self)
    self.infoBoxLayout = QVBoxLayout(self)
    self.infoBoxLayout.addWidget(AllianceLabel(self))
    self.infoBoxWidget.setMaximumWidth(200)

    self.infoBoxWidget.setLayout(self.infoBoxLayout)

    self.topRightText = TextWidget()
    self.infoBoxLayout.addWidget(self.topRightText)

    self.t = TextWidget()
    self.infoBoxLayout.addWidget(self.t)

    self.mainLayout.addWidget(self.infoBoxWidget)

    self.mapWidget = MapWidget()
    self.mainLayout.addWidget(self.mapWidget)

    # self.cameraWidget = CameraWidget()
    # self.mainLayout.addWidget(self.cameraWidget)

    # self.topRightWheel = wheelImage()
    # self.mainLayout.addWidget(self.topRightWheel,0,0)#y x

    # self.buttonWidget = PushButtonWidget()
    # self.buttonWidget.buttonClass =self.bottomLeftWheel
    # self.mainLayout.addWidget(self.buttonWidget,0,3)
    

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


