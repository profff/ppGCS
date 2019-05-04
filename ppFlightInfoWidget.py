import sys
from PySide2.QtWidgets import QApplication, QListWidgetItem, QListWidget
from PySide2.QtWidgets import QVBoxLayout, QPushButton, QWidget, QLabel
from PySide2.QtWidgets import QHBoxLayout
from PySide2.QtGui import QPalette,QColor
from PySide2.QtCore import Signal, Slot, QThread
import time
from ppGraphWidget import *
from ppHorizonWidget import *

class ppFlightInfoWidget(QWidget, QThread):
    def __init__(self):
        QWidget.__init__(self)
        QThread.__init__(self)
        layout = QHBoxLayout()
        layout.setSpacing(0);
        layout.setMargin(0);
        self._running=True
        self._instance=None
        self._periodicity=0.1 #time period between loops
        self._altgraph=ppGraphWidget(self._periodicity)
        self._horizon=ppHorizonWidget()
        self.setMinimumHeight(50)
        layout.addWidget(self._altgraph)
        layout.addWidget(self._horizon)
        
        self.setLayout(layout)
        self.start()
        
    def __del__(self):
        self._running=False

    def paintEvent(self, paintEvent):
        # painter = QPainter(self)
        # r=self.rect()
        # r-=QMargins(0,0,1,1)
        # painter.drawRoundedRect(r,5,5)
        pass
    
    def run(self):
        while(self._running):
            if(self._instance is not None):
                fst=self._instance.flystate
                self._altgraph.addValue(self._instance.altitude)
                self._horizon.roll=self._instance.roll
                self._horizon.pitch=self._instance.pitch
            time.sleep(self._periodicity)

    @property
    def device(self):
        return self._instance

    @device.setter
    def device(self,dev):
        if dev is not None:
            self._instance=dev
