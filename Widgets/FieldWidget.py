from PySide6.QtWidgets import QHBoxLayout, QVBoxLayout, QWidget
from PySide6.QtWidgets import QApplication,QGraphicsView, QGraphicsScene
from PySide6.QtWidgets import QLabel, QVBoxLayout, QWidget,QPushButton
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt,QPointF

class MapWidget(QWidget):
    #x, y from blue bottom right
    #x direction for the long way of the field
    #angle from the diagram
    #def setRobotPos(x,y,angle)
    def __init__(self, alliance):#if alliance false = red, alliance true = blue
        super().__init__()

        fieldHeight = 690.876#inches long side
        fieldWidth = 317.0#inches

        idealFieldHeight = 600#pixels
        
        mapHeight = 600
        conversion =  600/(fieldHeight/2)#inches to pixels
        robotWidth = 30#inches
        robotHeight = 30#inches
        layout = QVBoxLayout()
        #self.alignLayout = QVBoxLayout()

        self.scene =  QGraphicsScene(self)
        self.view = QGraphicsView(self.scene)
        self.view.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        self.scene.setSceneRect(0, 0, 600, 400)  
        #self.view.setRenderHint(QGraphicsView.RenderHint.Antialiasing)
        #self.setContentsMargins(0,0,0,0)
        #self.pushButton = QPushButton("Click Me")
        self.robotPixmap = QPixmap('./Images/Robot.png')
        if self.robotPixmap.isNull():
            self.setText("Failed to load robot image!")

        if (alliance == "BLUE"):
            self.mapPixmap = QPixmap('./Images/BlueSide.png')
        elif (alliance == "RED"):
            self.mapPixmap = QPixmap('./Images/RedSide.png')
        if self.mapPixmap.isNull():
            self.setText("Failed to load map image!")

        self.mapPixmap = self.mapPixmap.scaled(
                10000,
                mapHeight,
                Qt.KeepAspectRatio,  # Maintains aspect ratio
                Qt.SmoothTransformation  # High-quality scaling
            )
        self.robotPixmap = self.robotPixmap.scaled(
                robotWidth*conversion,
                robotHeight*conversion,
                Qt.KeepAspectRatio,  # Maintains aspect ratio
                Qt.SmoothTransformation  # High-quality scaling
            )
        map = self.scene.addPixmap(self.mapPixmap)
        robot = self.scene.addPixmap(self.robotPixmap)
        robot.setTransformOriginPoint(self.robotPixmap.width() / 2, self.robotPixmap.height() / 2)

        map.setPos(QPointF(0,0))
        
        robot.setPos(100,100)
        robot.setRotation(45)
        layout.addWidget(self.view)
        self.setLayout(layout)
