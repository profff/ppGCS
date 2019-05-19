import sys
from PySide2.QtWidgets import QApplication, QListWidgetItem, QListWidget
from PySide2.QtWidgets import QVBoxLayout, QPushButton, QWidget
from PySide2.QtCore import Signal, Slot
import time
import inspect
from os.path import join


sys.path.append('./bybop/src')
from Bybop_Discovery import *
import Bybop_Device
from ppDevice import ppDevice    
    

class ppDiscoverWidget(QWidget,Discovery):
    DeviceChanged=Signal(ppDevice)
    def __init__(self):
        QWidget.__init__(self)
        Discovery.__init__(self,DeviceID.BEBOP_FAMILY)
        
        self.button = QPushButton("Refresh Devices")
        self.lst = QListWidget(self)

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.lst)
        self.layout.addWidget(self.button)
        self.setLayout(self.layout)
        self.button.clicked.connect(self.discover)
        self.lst.currentItemChanged.connect(self.on_item_changed)
        self.setFixedWidth(140)
        
    def add_service(self, zeroconf, type, name):
        """ Internal function for zeroconf.ServiceBrowser. """
        info=super().add_service(zeroconf,type,name)
        #        self.devices.append(info)
        item=ppDevice(info)
        self.lst.addItem(item)
        # item2=ppDevice(info)
        # self.lst.addItem(item2)
        print('['+item.name+'-'+item.ip+']')
        item.connect()
        item.start_stream()

    def discover(self,wd=2):
        print("searching devices...")
        self.lst.clear()
        #self.devices = []
        super().start()
        super().wait_for_change(2)
        super().stop()
        print("OK")

    def on_item_changed(self, curr, prev):
        print("switch on "+curr.name)
        self.DeviceChanged.emit(curr)
    
    @property
    def curentDevice(self):
        return self.lst.currentItem()
    
        
if __name__ == "__main__":
    app = QApplication([])

    widget = ppDiscoverWidget()
    widget.resize(800, 600)
    widget.show()
    
    sys.exit(app.exec_())
