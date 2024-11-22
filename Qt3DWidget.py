class Qt3DWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        # Create a Qt3D Window
        self.view = Qt3DWindow()
        self.container = self.createWindowContainer(self.view)

        # Create a layout to hold the 3D view
        layout = QVBoxLayout(self)
        layout.addWidget(self.container)
        self.setLayout(layout)

        # Create a root entity
        self.root_entity = QEntity()

        # Add a 3D object (cube)
        self.add_3d_cube(self.root_entity)

        # Configure the camera
        self.setup_camera()

        # Set the root entity
        self.view.setRootEntity(self.root_entity)

    def add_3d_cube(self, parent_entity):
        # Create a cube mesh
        cube_mesh = QCuboidMesh()

        # Create a material
        material = QPhongMaterial()
        material.setDiffuse(Qt.blue)

        # Create an entity for the cube
        cube_entity = QEntity(parent_entity)
        cube_entity.addComponent(cube_mesh)
        cube_entity.addComponent(material)

    def setup_camera(self):
        # Access the camera in the view
        camera = self.view.camera()

        # Set camera position and look-at point
        camera.setPosition(Qt3DCore.QVector3D(0, 0, 10))
        camera.setViewCenter(Qt3DCore.QVector3D(0, 0, 0))

        # Add an orbit camera controller
        cam_controller = QOrbitCameraController(self.root_entity)
        cam_controller.setCamera(camera)
