from PySide6.QtWidgets import QHBoxLayout, QVBoxLayout, QWidget
from PySide6.QtWidgets import QApplication,QGraphicsView, QGraphicsScene
from PySide6.QtWidgets import QLabel, QVBoxLayout, QWidget,QPushButton,QGraphicsPixmapItem
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt,QPointF
import struct

from NetworkTableManager import NetworkTableManager
import keyboard
class MapWidget(QWidget):
    #the origin 
        
    #x, y from blue bottom right
    #x direction for the long way of the field
    #angle from the diagram
    def setRobotPos(self,x,y,angle):
        tempAxis = x
        x = y#flip the cordinates 
        y = tempAxis

        
        #if we are blue team on blue side
        if (self.alliance == "BLUE"):
            x = self.fieldWidth*self.conversion - x#flip the axis
            y = self.idealImageHeight - y#flip the axis
        else:
            angle += 180
        x -= self.robotWidth*self.conversion/2#set the origin of transform to the center of the image
        y -= self.robotHeight*self.conversion/2#set the origin of transform to the center of the image

        self.robot.setPos(x,y)
        self.robot.setRotation(angle)
    # def setMap(self,side,alliance):
    #     if side == "BLUE":
    #         if alliance == "BLUE":
    #             self.mapItem = QPixmap('./Images/BlueSide.png')
    #         else:
    #             self.mapItem = QPixmap('./Images/RedSide.png')
    #     else:
    #         if alliance == "BLUE":
    #             self.mapItem = QPixmap('./Images/BlueSide.png')
    #         else:
    #             self.mapItem = QPixmap('./Images/RedSide.png')
    #     self.mapItem = self.mapItem.scaled(
    #             10000,
    #             self.mapHeight,
    #             Qt.KeepAspectRatio,  # Maintains aspect ratio
    #             Qt.SmoothTransformation  # High-quality scaling
    #         )
    def __init__(self, newImageWidth):#if alliance false = red, alliance true = blue
        super().__init__()
        self.alliance = "BLUE"#which alliance team we are  on
        fieldSide = self.alliance#which side of the field we are on

        self.fieldHeight = 690.876#inches long side
        self.fieldWidth = 317.0#inches
        self.robotX = 0#in meters
        self.robotY = 0#in meters
        self.robotRot = 0#
        self.idealImageWidth = newImageWidth#pixels
        self.idealImageHeight = self.idealImageWidth*((self.fieldHeight/2)/self.fieldWidth)
        print("width", self.idealImageWidth)
        print("height", self.idealImageHeight)
        #self.setFixedSize(idealImageWidth, idealImageHeight)

        self.conversion =  self.idealImageWidth/self.fieldWidth#inches to pixels
        print(self.conversion)
        self.robotWidth = 30#inches
        self.robotHeight = 30#inches
        layout = QVBoxLayout()
        #self.alignLayout = QVBoxLayout()

        self.scene =  QGraphicsScene(self)
        self.view = QGraphicsView(self.scene)

        self.view.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        #self.setMaximumHeight(idealImageHeight)
        #self.scene.setSceneRect(0, 0, idealImageWidth, idealImageHeight)  #prevents scrolling
        self.view.setSceneRect(0,0,self.idealImageWidth,self.idealImageHeight)

        #self.setMaximumSize(idealImageWidth+100,idealImageHeight+10)
        #self.view.fitInView(self.scene.sceneRect(), Qt.KeepAspectRatio)
        #self.setFixedSize(idealImageWidth+100,idealImageHeight+10)
        #self.view.setRenderHint(QGraphicsView.RenderHint.Antialiasing)
        #self.setContentsMargins(0,0,0,0)
        #self.pushButton = QPushButton("Click Me")
        self.bluePixmap = QPixmap('./Images/BlueSide.png')
        self.redPixmap = QPixmap('./Images/RedSide.png')
        self.bluePixmap = self.bluePixmap.scaled(
                self.idealImageWidth,
                10000,
                Qt.KeepAspectRatio,  # Maintains aspect ratio
                Qt.SmoothTransformation  # High-quality scaling
            )
        self.redPixmap = self.redPixmap.scaled(
                self.idealImageWidth,
                10000,
                Qt.KeepAspectRatio,  # Maintains aspect ratio
                Qt.SmoothTransformation  # High-quality scaling
            )
        print("width", self.redPixmap.width())
        print("height", self.redPixmap.height())

        self.robotPixmap = QPixmap('./Images/Robot.png')
        if self.robotPixmap.isNull():
            self.setText("Failed to load robot image!")
        self.mapItem = QGraphicsPixmapItem()
        if(self.alliance == "BLUE"):
            self.mapItem.setPixmap(self.bluePixmap)

        elif (self.alliance == "RED"):
            self.mapItem.setPixmap(self.redPixmap)
        # if self.mapItem.isNull():
        #     self.setText("Failed to load map image!")

        center_x = self.bluePixmap.width() / 2
        center_y = self.bluePixmap.height() / 2
        self.mapItem.setTransformOriginPoint(center_x, center_y)

        
        self.robotPixmap = self.robotPixmap.scaled(
                self.robotWidth*self.conversion,
                self.robotHeight*self.conversion,
                Qt.KeepAspectRatio,  # Maintains aspect ratio
                Qt.SmoothTransformation  # High-quality scaling
            )
        map = self.scene.addItem(self.mapItem)
        self.robot = self.scene.addPixmap(self.robotPixmap)
        self.robot.setTransformOriginPoint(self.robotPixmap.width() / 2, self.robotPixmap.height() / 2)

        #map.setPos(QPointF(0,0))
        
        self.updateRobotPose(("sup",[10,1,3.1415926/4]))
        layout.addWidget(self.view)
        self.setLayout(layout)




        #self.robotPoseNTTableNames = ["Shuffleboard", "Auton", "Field"]#xcord,ycord in  inches and angle in deg
        self.robotPoseNTManager = NetworkTableManager(tableName = "SwerveStats",entryName = "estimatedPose")#assuming position is a (entryname, [Xcord,Ycord,angle])
        self.robotPoseNTManager.new_value_available.connect(self.updateRobotPose)
        self.allianceNTManager = NetworkTableManager(tableName ="FMSInfo", entryName ="IsRedAlliance")#assuming position is a (entryname, [Xcord,Ycord,angle])
        self.allianceNTManager.new_value_available.connect(self.updateAllianceColor)

    def updateRobotPose(self, info):
        # print(len(info[1]))
        entryName = info[0]
        entryValue = info[1]
        try:
            try:
                x, y, rotation = struct.unpack("ddd", info[1])
            except:
                rotation = entryValue[2]
                x= entryValue[0]
                y= entryValue[1]
            self.robotRot = rotation#entryValue.degrees()

            rotation = rotation * 180. / 3.1415926

            # print(x)
            # print(y)
            # print(rotation)
            # print()
        
        
            self.robotX = x#entryValue.X()
            self.robotY = y#entryValue.Y()
            # print(str(info))
            #print (info[1])
            x = x*39.3700787*self.conversion#meters to inches
            y = y*39.3700787*self.conversion
            rot = rotation
            if (self.alliance == "BLUE"):
                if (x < self.idealImageHeight):#the robot blue side
                    self.mapItem.setRotation(0)

                    self.mapItem.setPixmap(self.bluePixmap)

                else:
                    x -= self.idealImageHeight
                    self.mapItem.setRotation(180)
                    self.mapItem.setPixmap(self.redPixmap)
            if (self.alliance == "RED"):
                if (x < self.idealImageHeight):#the robot blue side
                    self.mapItem.setRotation(180)
                    self.mapItem.setPixmap(self.bluePixmap)
                else:
                    x -= self.idealImageHeight
                    self.mapItem.setRotation(0)

                    self.mapItem.setPixmap(self.redPixmap)

            self.setRobotPos(x,y,rot)
        except Exception as e:
            print("robot pos fail", e)
            pass
    def updateAllianceColor(self, message: tuple):
            #print(message)
            if message[1]:
                self.alliance = "RED"


            else:
                self.alliance = "BLUE"
            self.updateRobotPose(("hi",[self.robotX,self.robotY,self.robotRot]))
