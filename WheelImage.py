import sys
from PySide6.QtWidgets import QApplication, QWidget, QGraphicsView, QGraphicsScene, QVBoxLayout
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt
import NestedNetworkTableManager
from NetworkTableManager import NetworkTableManager
class wheelImage(QWidget):
    def __init__(self):
        super().__init__()
        # Set up the widget layout
        layout = QVBoxLayout()

        # Create a QGraphicsView and QGraphicsScene
        self.view = QGraphicsView(self)
        scene = QGraphicsScene(self)

        # Load an image into a QPixmap
        pixmap = QPixmap('wheeldir.png')

        # Create an item with the pixmap and add it to the scene
        self.pixmap_item = scene.addPixmap(pixmap)
        self.pixmap_item.setTransformOriginPoint(self.pixmap_item.boundingRect().center())

        # Set the scene for the view
        self.view.setScene(scene)

        # Add the view to the layout
        layout.addWidget(self.view)

        # Set the layout for the window
        self.setLayout(layout)
        self.networkStuff("defaultParameter","networkTable","networkTableEntry")
  



    def rotate_image(self, angle):
        """
        Rotates the image by 90 degrees.
        """
        #current_angle = self.pixmap_item.rotation()
        new_angle = angle  # Rotate by 90 degrees each time
        self.pixmap_item.setRotation(new_angle)  # Apply the new rotation
        print("hi")