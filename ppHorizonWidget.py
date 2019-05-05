import sys
import math
from PySide2.QtWidgets import QApplication, QListWidgetItem, QListWidget
from PySide2.QtWidgets import QVBoxLayout, QPushButton, QWidget, QLabel
from PySide2.QtWidgets import QGroupBox, QFrame, QHBoxLayout
from PySide2.QtCore import Signal, Slot, QThread, QMargins, QPoint
from PySide2.QtGui import QPainter

class ppHorizonWidget(QWidget):

    def __init__(self):
        QWidget.__init__(self)
        self._r=0
        self._p=0
        self._y=0
        
        self._frame=QFrame()
        self._lRoll=QLabel(str(0))
        self._lRoll.setMaximumWidth(35)
        self._lPitch=QLabel(str(0))
        self._lPitch.setMaximumWidth(35)
        self.setMaximumSize(150,50)
        llayout = QVBoxLayout()
        llayout.setSpacing(0);
        llayout.setMargin(0);
        llayout.addWidget(self._lPitch)
        llayout.addWidget(self._lRoll)
        layout = QHBoxLayout()
        layout.setSpacing(0);
        layout.setMargin(0);
        layout.addWidget(self._frame)
        layout.addLayout(llayout)
        self.setLayout(layout)
        
    def __del__(self):
        pass
            
    def paintEvent(self, paintEvent):
        painter = QPainter(self)
        r=self._frame.rect()
        r-=QMargins(3,3,3,4)
        painter.drawRect(r)
        painter.translate(r.width()/2+r.left(),r.height()/2+r.top())
        dp=math.degrees(self._p)
        pr=r.height()/90
        painter.translate(0,pr*dp)
        d=math.degrees(self._r)
        painter.rotate(d)
        painter.drawLine(-r.width()/2,0,r.width()/2,0)
        painter.drawLine(0,r.height()/2,0,-r.height()/2)


    @property
    def roll(self):
        return self._r
    @property
    def pitch(self):
        return self._p
    @property
    def yaw(self):
        return self._y

    @roll.setter
    def roll(self,v):
        self._r=v
        self._lRoll.setText(str(round(math.degrees(v)))+'°')
        self.update()
    @pitch.setter
    def pitch(self,v):
        self._p=v
        self._lPitch.setText(str(round(math.degrees(v)))+'°')
        self.update()
    @yaw.setter
    def yaw(self,v):
        self._y=v
        self.update()
        
    def resizeEvent(self,event):
        pass
