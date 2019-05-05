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
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.lconnected)
        self.layout.addWidget(self.lFlyState)
        self.layout.addWidget(self.bTakeoff)
        self.layout.addWidget(self.bCircle)
        self.layout.addWidget(self.bRTH)
        self.setLayout(self.layout)
        self.bTakeoff.clicked.connect(self.takeoff)
        self.bCircle.clicked.connect(self.circle)
        self.bRTH.clicked.connect(self.rth)

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
                    self.bCircle.setDisabled(True)
                    self.bCircle.setText('Circle')
                    self.bRTH.setDisabled(True)
                    self.bRTH.setText('RTH')
                elif fst==1: # takingoff
                    self.bTakeoff.setDisabled(False)
                    self.bTakeoff.setText('stop')
                    self.bCircle.setDisabled(True)
                    self.bCircle.setText('Circle')
                    self.bRTH.setDisabled(True)
                    self.bRTH.setText('RTH')
                elif fst==2: # hovering
                    self.bTakeoff.setDisabled(False)
                    self.bTakeoff.setText('Land')
                    self.bCircle.setDisabled(True)
                    self.bCircle.setText('Circle')
                    self.bRTH.setDisabled(False)
                    self.bRTH.setText('RTH')
                elif fst==3: # flying
                    self.bTakeoff.setDisabled(False)
                    self.bTakeoff.setText('Land')
                    self.bCircle.setDisabled(False)
                    self.bCircle.setText('Circle')
                    self.bRTH.setDisabled(False)
                    self.bRTH.setText('RTH')
                else:
                    self.bTakeoff.setDisabled(False)
                    self.bTakeoff.setText('stop')
                    self.bCircle.setDisabled(False)
                    self.bCircle.setText('Circle')
                    self.bRTH.setDisabled(False)
                    self.bRTH.setText('RTH')

            time.sleep(0.2)

    def takeoff(self):
        self._instance.tkof_lnd_emcy()
    def circle(self):
        self._instance.circle()
    def rth(self):
        self._instance.rth()
    
            
    @property
    def device(self):
        return self._instance

    @device.setter
    def device(self,dev):
        if dev is not None:
            self._instance=dev
