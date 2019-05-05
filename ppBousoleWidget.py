import sys
import math
from PySide2.QtWidgets import QApplication, QListWidgetItem, QListWidget
from PySide2.QtWidgets import QVBoxLayout, QPushButton, QWidget, QLabel
from PySide2.QtWidgets import QGroupBox, QFrame, QHBoxLayout
from PySide2.QtCore import Signal, Slot, QThread, QMargins, QPoint
from PySide2.QtGui import QPainter

class ppBousoleWidget(QWidget):

    def __init__(self):
        QWidget.__init__(self)
        self._y=0
        self._frame=QFrame()
        self._lYaw=QLabel(str(0))
        self._lYaw.setMaximumWidth(35)
        self.setMaximumSize(85,50)
        llayout = QVBoxLayout()
        llayout.setSpacing(0);
        llayout.setMargin(0);
        llayout.addWidget(self._lYaw)
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
        painter.drawLine(0,r.height()/3,0,-r.height()/3)
        painter.rotate(self._y)
        painter.drawLine(0,-r.height()/2,3,-r.height()/2+7)
        painter.drawLine(-3,-r.height()/2+7,3,-r.height()/2+7)
        painter.drawLine(-3,-r.height()/2+7,0,-r.height()/2)

        painter.drawLine(-r.height()/2,0,-r.height()/2+5,0)
        painter.drawLine(r.height()/2,0,r.height()/2-5,0)
        painter.drawLine(0,r.height()/2,0,r.height()/2-5)
        for i in range (0,360,10):
            painter.drawLine(0,-r.height()/2,0,-r.height()/2+3)
            painter.rotate(10)

    @property
    def yaw(self):
        return self._y

    @yaw.setter
    def yaw(self,v):
        self._y=v
        self._lYaw.setText(str(round(v)))
        self.update()
        
    def resizeEvent(self,event):
        pass
