import sys
from PySide2.QtWidgets import QApplication, QListWidgetItem, QListWidget
from PySide2.QtWidgets import QVBoxLayout, QPushButton, QWidget, QLabel
from PySide2.QtWidgets import QGroupBox, QFrame
from PySide2.QtCore import Signal, Slot, QThread, QMargins, QPoint
from PySide2.QtGui import QPainter

import time
from ppDevice import *
import pygame

axistostick={'name':'default',
             'left-vertical':2,
             'left-horizontal':3,
             'right-vertical':1,
             'right-horizontal':0}

sticktofunc={'name':'default',
             'pitch':1,
             'roll':0,
             'gaz':2,
             'yaw':3,
             'takeoff':None,
             'rth':None}

class ppControlWidget(QWidget, QThread):

    def __init__(self):
        QWidget.__init__(self)
        QThread.__init__(self)

        pygame.init()
        pygame.joystick.init()
        cnt=pygame.joystick.get_count()
        if(cnt==0):
            print('no joystick found')
            sys.exit(0)
        self._joystick = pygame.joystick.Joystick(0)
        self._joystick.init()
        print(self._joystick.get_name())
        axes =self._joystick.get_numaxes()

        self._running=True
        self._instance=None
        self.frame=QFrame()
        self.setFixedSize(100,50)
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.frame)
        self.setLayout(self.layout)
        self._LStickV=self._joystick.get_axis(2)
        self._LStickH=self._joystick.get_axis(3)
        self._RStickV=self._joystick.get_axis(1)
        self._RStickH=self._joystick.get_axis(0)
        print(self._LStickV,self._LStickH,self._RStickV,self._RStickH)
        
        self.start()
        
    def __del__(self):
        self._running=False
        pygame.quit()

    def paintEvent(self, paintEvent):
        painter = QPainter(self)
        r=self.rect()
        r-=QMargins(0,0,1,1)
        painter.drawRoundedRect(r,5,5)

        c1=QPoint(r.width()/4,r.height()/2)
        c2=QPoint(3*r.width()/4,r.height()/2)
        
        r1=(r.height()*0.8)/2
        rc=(r.height()*0.1)/2
        painter.drawEllipse(c1,r1,r1)
        painter.drawEllipse(c2,r1,r1)
        global axistostick
        c1=QPoint(r.width()/4-(self._LStickH*r1),r.height()/2-(self._LStickV*r1))
        c2=QPoint(3*r.width()/4-(self._RStickH*r1),r.height()/2-(self._RStickV*r1))
        painter.drawEllipse(c1,rc,rc)
        painter.drawEllipse(c2,rc,rc)

    def resizeEvent(self,event):
        pass
    
    def run(self):
        while(self._running):
            if(self._instance is not None):
                pass
            pygame.event.pump()
            self._LStickV=self._joystick.get_axis(2)
            self._LStickH=self._joystick.get_axis(3)
            self._RStickV=self._joystick.get_axis(1)
            self._RStickH=self._joystick.get_axis(0)

            self.update()
            time.sleep(0.05)
    @property
    def device(self):
        return self._instance

    @device.setter
    def device(self,dev):
        if dev is not None:
            self._instance=dev
