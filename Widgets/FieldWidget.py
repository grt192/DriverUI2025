from PySide6.QtWidgets import QHBoxLayout, QVBoxLayout, QWidget
from PySide6.QtWidgets import QApplication,QGraphicsView, QGraphicsScene
from PySide6.QtWidgets import QLabel, QVBoxLayout, QWidget,QPushButton,QGraphicsPixmapItem
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt,QPointF

import NetworkTableManager

class MapWidget(QWidget):
    #the origin 
        
    #x, y from blue bottom right
    #x direction for the long way of the field
    #angle from the diagram
    def setRobotPos(self,x,y,angle):
        tempAxis = x
        x = y#flip the cordinates 
        y = tempAxis
        x = x*self.conversion#convert inches into pixels
        y = y*self.conversion#convert inches into pixels
        
        #if we are blue team on blue side
        if (self.alliance == "BLUE"):
            x = self.fieldWidth*self.conversion - x#flip the axis
            y = self.mapHeight - y#flip the axis
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
    def __init__(self, alliance):#if alliance false = red, alliance true = blue
        super().__init__()
        self.alliance = alliance#which alliance team we are  on
        fieldSide = alliance#which side of the field we are on

        self.fieldHeight = 690.876#inches long side
        self.fieldWidth = 317.0#inches

        idealFieldHeight = 600#pixels
        self.mapHeight = 600
        self.conversion =  600/(self.fieldHeight/2)#inches to pixels
        self.robotWidth = 30#inches
        self.robotHeight = 30#inches
        layout = QVBoxLayout()
        #self.alignLayout = QVBoxLayout()

        self.scene =  QGraphicsScene(self)
        self.view = QGraphicsView(self.scene)
        self.view.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        self.scene.setSceneRect(0, 0, 600, 400)  
        #self.view.setRenderHint(QGraphicsView.RenderHint.Antialiasing)
        #self.setContentsMargins(0,0,0,0)
        #self.pushButton = QPushButton("Click Me")
        self.bluePixmap = QPixmap('./Images/BlueSide.png')
        self.redPixmap = QPixmap('./Images/RedSide.png')
        self.bluePixmap = self.bluePixmap.scaled(
                10000,
                self.mapHeight,
                Qt.KeepAspectRatio,  # Maintains aspect ratio
                Qt.SmoothTransformation  # High-quality scaling
            )
        self.redPixmap = self.redPixmap.scaled(
                10000,
                self.mapHeight,
                Qt.KeepAspectRatio,  # Maintains aspect ratio
                Qt.SmoothTransformation  # High-quality scaling
            )
        
        self.robotPixmap = QPixmap('./Images/Robot.png')
        if self.robotPixmap.isNull():
            self.setText("Failed to load robot image!")
        self.mapItem = QGraphicsPixmapItem()
        if(alliance == "BLUE"):
            self.mapItem.setPixmap(self.bluePixmap)

        elif (alliance == "RED"):
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
        
        self.updateRobotPose(("sup",(10,10,45)))
        layout.addWidget(self.view)
        self.setLayout(layout)




        #self.robotPoseNTTableNames = ["Shuffleboard", "Auton", "Field"]#xcord,ycord in  inches and angle in deg
        #self.robotPoseNTManager = NetworkTableManager("PositionTable","Position")#assuming position is a (entryname, [Xcord,Ycord,angle])
        #self.robotPoseNTManager.new_value_available.connect(self.updateRobotPose)

    def updateRobotPose(self, info: tuple):
        entryName = info[0]
        entryValue = info[1]
        if (self.alliance == "BLUE"):
            if (entryValue[0] < self.fieldHeight/2):#the robot blue side
                
                self.mapItem.setPixmap(self.bluePixmap)
            else:
                self.mapItem.setRotation(180)
                self.mapItem.setPixmap(self.redPixmap)

        self.setRobotPos(entryValue[0],entryValue[1],entryValue[2])




        #self.robotPoseNTTableNames = ["Shuffleboard", "Auton", "Field"]#xcord,ycord in  inches and angle in deg
        #self.robotPoseNTManager = NetworkTableManager("PositionTable","Position")#assuming position is a (entryname, [Xcord,Ycord,angle])
        #self.robotPoseNTManager.new_value_available.connect(self.updateRobotPose)

    def updateRobotPose(self, info: tuple):
        entryName = info[0]
        entryValue = info[1]
        if (self.alliance == "BLUE"):
            if (entryValue[0] < self.fieldHeight/2):#the robot blue side
                
                self.mapItem.setPixmap(self.bluePixmap)
            else:
                self.mapItem.setRotation(180)
                self.mapItem.setPixmap(self.redPixmap)

        self.setRobotPos(entryValue[0],entryValue[1],entryValue[2])
    def updateAllianceColor(self, message: tuple):
            print(message)
            if message[1]:
                print("RED")
            else:
                print("BLUE")