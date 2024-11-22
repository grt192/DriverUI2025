"""
This file creates an empty window with the title "Hello World".
Run this file to see the window.
"""
import sys
from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtWidgets import QLabel, QVBoxLayout, QWidget
from PySide6.QtWidgets import QGridLayout

from WheelImage import wheelImage
from TextWidget import TextWidget
from PushButtonWidget import PushButtonWidget

# Every UI has a MainWindows that contains everything. 
class HelloWorld(QMainWindow):


  # We setup the window's title, size, and show it.
  def __init__(self):
    super().__init__()
    self.setWindowTitle("Hello World")
    self.resize(400, 400)
    self.centralWidget = QWidget(self)
    self.mainLayout = QGridLayout(self)
    self.mainLayout.horizontalSpacing = 4
    self.mainLayout.verticalSpacing = 4

    self.centralWidget.setLayout(self.mainLayout)
    
    self.topRightText = TextWidget()
    self.mainLayout.addWidget(self.topRightText,1,0)
    self.topRightWheel = wheelImage()
    self.mainLayout.addWidget(self.topRightWheel,0,0)#y x

    self.topLeftText = TextWidget()
    self.mainLayout.addWidget(self.topLeftText,1,1)
    self.topLeftWheel = wheelImage()
    self.mainLayout.addWidget(self.topLeftWheel,0,1)#y x
  
    self.bottomRightText = TextWidget()
    self.mainLayout.addWidget(self.bottomRightText,3,0)
    self.bottomRightWheel = wheelImage()
    self.mainLayout.addWidget(self.bottomRightWheel,2,0)#y x

    self.bottomLeftText = TextWidget()
    self.mainLayout.addWidget(self.bottomLeftText,3,1)
    self.bottomLeftWheel = wheelImage()
    self.mainLayout.addWidget(self.bottomLeftWheel,2,1)#y x

    self.buttonWidget = PushButtonWidget()
    self.buttonWidget.buttonClass =self.bottomLeftWheel
    self.mainLayout.addWidget(self.buttonWidget,0,3)
    
    self.setCentralWidget(self.centralWidget)

    self.show()

# This is the tamplate to start the UI, just copy it.
if __name__ == "__main__":
  app = QApplication(sys.argv)
  window = HelloWorld()

  sys.exit(app.exec())
  