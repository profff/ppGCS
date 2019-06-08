#!/usr/bin/env python3
import sys
import random
from PySide2.QtWidgets import QApplication, QMainWindow, QHBoxLayout
from PySide2.QtWidgets import QVBoxLayout, QPushButton, QWidget, QTabWidget
from PySide2.QtWebEngineWidgets import QWebEngineView
from PySide2.QtQuick import QQuickView
from PySide2.QtCore import QUrl
from PySide2.QtGui import QFont
import time
from ppDevice import *
from ppDiscoverWidget import *
from ppVideoWidget import *
from ppDeviceInfoWidget import *
from ppFlightInfoWidget import *
from ppControlWidget import *

class ppGCSMain(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("pppGCS : Plural Python Parrot GCS")

        self.DeviceInfo=ppDeviceInfoWidget()
        self.DeviceList=ppDiscoverWidget()
        self.leftcol_layout = QVBoxLayout()
        self.leftcol_layout.addWidget(self.DeviceInfo)
        self.leftcol_layout.addWidget(self.DeviceList)

        self.VideoViewer=ppVideoWidget()

        self.tabs=QTabWidget()
        self.tabs.addTab(self.VideoViewer,"Video stream")
        self.mapview = QQuickView()
        self.mapcontainer=QWidget.createWindowContainer(self.mapview,self)
        url = QUrl("map.qml")
        self.mapview.setSource(url)
        self.mapview.show()
        self.tabs.addTab(self.mapcontainer,"map view")
        

        self.FlightInfo=ppFlightInfoWidget()
        self.ControlInfo=ppControlWidget()
        self.rightcol_layout = QVBoxLayout()
        self.rightcol_layout.addWidget(self.tabs)
        self.lowrightcol_layout = QHBoxLayout()
        self.lowrightcol_layout.addWidget(self.FlightInfo)
        self.lowrightcol_layout.addWidget(self.ControlInfo)
        self.rightcol_layout.addLayout(self.lowrightcol_layout)

        self.layout = QHBoxLayout()
        self.layout.addLayout(self.leftcol_layout)
        self.layout.addLayout(self.rightcol_layout)

        self.setLayout(self.layout)

        self.DeviceList.DeviceChanged.connect(self.on_device_changed)
        
    def on_device_changed(self,device):
        self.VideoViewer.close_video()
        self.VideoViewer.open_video(device.sdpfile)
        self.DeviceInfo.device=device
        self.FlightInfo.device=device
        self.ControlInfo.device=device
        
if __name__ == "__main__":
    app = QApplication([])

    win = QMainWindow()
    font=QFont()
    font.setFamily('Courier')
    font.setPointSize(8)
    win.setFont(font)
    pp=ppGCSMain()
    win.setCentralWidget(pp)
    win.resize(1200, 600)
    win.show()
    sys.exit(app.exec_())
