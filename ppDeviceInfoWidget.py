import sys
from PySide2.QtWidgets import QApplication, QListWidgetItem, QListWidget
from PySide2.QtWidgets import QVBoxLayout, QPushButton, QWidget, QLabel
from PySide2.QtWidgets import QGroupBox
from PySide2.QtCore import Signal, Slot, QThread
import time
from ppDevice import *

class ppDeviceInfoWidget(QWidget, QThread):
    def __init__(self):
        QWidget.__init__(self)
        QThread.__init__(self)
        self.gbInfos=QGroupBox()
        self.gbCmd=QGroupBox()
        self.infolayout = QVBoxLayout()
        self.cmdlayout = QVBoxLayout()
        self._running=True
        self._instance=None
        self.lconnected = QLabel('')
        self.lFlyState = QLabel('')
        self.bTakeoff = QPushButton('')
        self.bTakeoff.setDisabled(True)
        self.bCircle = QPushButton('')
        self.bCircle.setDisabled(True)
        self.bRTH = QPushButton('')
        self.bRTH.setDisabled(True)
        self.infolayout.addWidget(self.lconnected)
        self.infolayout.addWidget(self.lFlyState)
        self.gbInfos.setLayout(self.infolayout)
        self.cmdlayout.addWidget(self.bTakeoff)
        self.cmdlayout.addWidget(self.bCircle)
        self.cmdlayout.addWidget(self.bRTH)
        self.gbCmd.setLayout(self.cmdlayout)

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.gbInfos)
        self.layout.addWidget(self.gbCmd)
        self.setLayout(self.layout)
        self.start()
        
    def __del__(self):
        self._running=False
        
    def run(self):
        while(self._running):
            if(self._instance is not None):
                self.lFlyState.setText(strFlyState(self._instance.flystate))
                if(self._instance.isconnected):
                    self.lconnected.setText('connected')
                else:
                    self.lconnected.setText('disconnected!')

                fst=self._instance.flystate
                if fst==0 : # landed
                    self.bTakeoff.setDisabled(False)
                    self.bTakeoff.setText('Take Off')
                    self.bCircle.setDisabled(False)
                    self.bCircle.setText('Circle')
                    self.bRTH.setDisabled(False)
                    self.bRTH.setText('RTH')
                else:
                    self.bTakeoff.setDisabled(True)

            time.sleep(0.2)
    @property
    def device(self):
        return self._instance

    @device.setter
    def device(self,dev):
        if dev is not None:
            self._instance=dev
