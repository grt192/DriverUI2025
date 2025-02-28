import sys
from PySide6 import QtCore
from PySide6.QtWidgets import QLabel, QWidget, QPushButton, QVBoxLayout, QHBoxLayout
from PySide6.QtWidgets import QApplication, QSizePolicy,QGraphicsPixmapItem
from PySide6.QtGui import QImage, QPixmap
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication,QGraphicsView, QGraphicsScene
from PySide6.QtGui import QKeySequence, QShortcut

import cv2
import requests

from NetworkTableManager import NetworkTableManager

class CameraWidget(QWidget):
    camURl = "http://10.1.92.2:1181/stream.mjpg"
    camTestURL = "http://10.1.92.2:1181"
    #320*240@120fps for fisheye
    resolutionX = 160
    resolutionY = 120
    
    FPS = 30
    #resolutionX = 320
    #resolutionY = 240
    # FPS = 120
    scale = 1.5
    #The actual video size on the UI
    windowWidth = resolutionX * scale
    windowHeight = resolutionY * scale

    connected = False
    def __init__(self, parent=None):
        super(CameraWidget, self).__init__(parent)
        self.scene =  QGraphicsScene(self)
        self.view = QGraphicsView(self.scene)

        self.view.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        self.view.setSceneRect(0,0,self.windowWidth,self.windowHeight)

        print("cameraWidget Start")
        #use this time to call the DisplayStream method to retrieve and display frames.
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.displayStream)
        # self.timer.timeout.connect(self.testDisplay)
        self.timer.setSingleShot(True)

        if self.checkDriver():
            self.setDriverCap()
            self.timer.start(1)
            self.connected = True
        self.reconnectButton = QPushButton("Reconnect")
        self.reconnectButton.clicked.connect(self.reconnect)
        self.reconnectButton.setFixedWidth(480)

        self.camera = True#true is front camera false is back camera
        self.cameraSwitch = QPushButton("switchCamera")
        self.cameraSwitch.clicked.connect(self.switchCamera)
        self.cameraSwitch.setFixedWidth(480)
        layout = QVBoxLayout(self)
        #Add everything layout.
        layout.addWidget(self.view)
        layout.addWidget(self.cameraSwitch)

        layout.addWidget(self.reconnectButton)
        self.setLayout(layout)
        
        self.cameraItem = QGraphicsPixmapItem()
        self.scene.addItem(self.cameraItem)

        self.cameraSelectNTmanager = NetworkTableManager(tableName ="testTable", entryName ="cameraSelection")#assuming position is a (entryname, [Xcord,Ycord,angle])
        
        self.hud = QPixmap('./Images/hud.png')
        self.hud = self.hud.scaled(
                self.resolutionX*2,#self.scale,
                self.resolutionY*2,#self.scale,
                Qt.KeepAspectRatio,  # Maintains aspect ratio
                Qt.SmoothTransformation  # High-quality scaling
            )

        self.hudItem = QGraphicsPixmapItem()
        self.hudItem.setPixmap(self.hud)
        self.scene.addItem(self.hudItem)
        switch_cam_shortcut = QShortcut(QKeySequence("Space"), self)
        switch_cam_shortcut.activated.connect(self.switchCamera)
        print ('cameraWidget done')
    def setDriverCap(self):
        self.driverCap = cv2.VideoCapture(self.camURl)
        #self.driverCap = cv2.VideoCapture(0)

        self.driverCap.set(cv2.CAP_PROP_FRAME_WIDTH, self.resolutionX)
        self.driverCap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.resolutionY)
        self.driverCap.set(cv2.CAP_PROP_FPS, self.FPS)
        # self.driverCap.set(cv2.CAP_PROP_EXPOSURE, 0.5)
        # self.driverCap.set(cv2.CAP_PROP_CONVERT_RGB, 1)
    def switchCamera(self):
        self.camera = not self.camera
        print("camera switch pressed")
        self.cameraSelectNTmanager.entry.setBoolean(self.camera)
    def reconnect(self):
        if self.checkDriver():
            self.setDriverCap()
            self.timer.start(1)
            self.connected = True
        else:
            self.connected = False
            print("Network Issue!")
    def checkDriver(self):
        try:
            response = requests.get(self.camTestURL, timeout=1)
            if response.status_code != 200:
                print("Driver cam not accessable! Status Code: " + str(response.status_code))
                return False
            response.close()
        except Exception as e:
            print("Check Driver exception in the following line:")
            print(e)
            return False
        return True
    def testDisplay(self):
        ret, frame = self.driverCap.read()
        cv2.imshow("frame", frame)
        cv2.waitKey(1)
        self.timer.start(1)

    def displayStream(self):
        if not self.connected:
            return
        elif not self.driverCap.isOpened():
            print("Can't access driver camera")
            return
        else:
            ret, frame = self.driverCap.read()
            # Convert the image to Qt format
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            h, w, ch = frame.shape
            bytesPerLine = ch * w
            cvtToQtFormat = QImage(
                frame.data, w, h, bytesPerLine, QImage.Format_RGB888
            )
            pixmap = QPixmap.fromImage(cvtToQtFormat)
            self.cameraItem.setPixmap(pixmap)
            #self.cameraDisplay.setAlignment(Qt.AlignCenter)

            self.timer.start(1)
    