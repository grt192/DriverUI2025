from networktables import NetworkTables
from PySide6.QtCore import Signal, QObject
import time
connected = False
class NetworkTableManager(QObject):
    new_value_available = Signal(tuple)
    def __init__(self, tableName, entryName, parent = None):
        super().__init__(parent)
        if (connected):
            NetworkTables.initialize(server='10.1.92.2') #Robot IP
        else:
            NetworkTables.initialize(server='localhost') #Local IP for Simulation
        print("Connecting to " + tableName + "-> " + entryName + ":")
        while not NetworkTables.isConnected():
            print("#", end="")
            time.sleep(0.2)

        print("Connected!")

        self.tableName = tableName
        self.entryName = entryName
        self.table = NetworkTables.getTable(self.tableName)
        self.entry = self.table.getEntry(self.entryName)
        self.entry.addListener(self.valueChanged, NetworkTables.NotifyFlags.UPDATE)

    def valueChanged(self, table, key, value, isNew):
        self.new_value_available.emit((self.entryName,value))

    def getValue(self):
        #return self.table.getValue(self.entryName, None)
        return self.table.getValue(self.entryName, None)

    def putString(self, value):
        self.entry.setString(value)