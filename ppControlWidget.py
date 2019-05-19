import sys
from PySide2.QtWidgets import QApplication, QListWidgetItem, QListWidget
from PySide2.QtWidgets import QVBoxLayout, QPushButton, QWidget, QLabel
from PySide2.QtWidgets import QGroupBox, QFrame
from PySide2.QtCore import Signal, Slot, QThread, QMargins, QPoint
from PySide2.QtGui import QPainter

import time
from ppDevice import *
import pygame

axistostick={'lv':1,
             'lh':0,
             'rv':3,
             'rh':2}

axisreverse={'lv':-1,
             'lh':1,
             'rv':-1,
             'rh':1}

sticktofunc={'pitch':'rv',
             'roll':'rh',
             'gaz':'lv',
             'yaw':'rh'}
switchtofunc={0:'start',
              2:'rth'}

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
        self._periodicity=0.05 #time period between loops
        self.frame=QFrame()
        self.setFixedSize(100,50)
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.frame)
        self.setLayout(self.layout)
        pygame.event.pump()
        self._Sticks={'lv':self._joystick.get_axis(axistostick['lv'])*axisreverse['lv'],
                      'lh':self._joystick.get_axis(axistostick['lh'])*axisreverse['lh'],
                      'rv':self._joystick.get_axis(axistostick['rv'])*axisreverse['rv'],
                      'rh':self._joystick.get_axis(axistostick['rh'])*axisreverse['rh']}
        self.start()
        
    def __del__(self):
        self._running=False
        pygame.quit()

    def paintEvent(self, paintEvent):
        painter = QPainter(self)
        r=self.rect()
        r-=QMargins(0,0,1,1)
        painter.drawRect(r)
        c1=QPoint(r.width()/4,r.height()/2)
        c2=QPoint(3*r.width()/4,r.height()/2)
        r1=(r.height()*0.90)/2
        rc=(r.height()*0.1)/2
        painter.drawEllipse(c1,r1,r1)
        painter.drawEllipse(c2,r1,r1)
        global axistostick
        c1=QPoint(r.width()/4+(self._Sticks['lh']*r1),r.height()/2-(self._Sticks['lv']*r1))
        c2=QPoint(3*r.width()/4+(self._Sticks['rh']*r1),r.height()/2-(self._Sticks['rv']*r1))
        painter.drawEllipse(c1,rc,rc)
        painter.drawEllipse(c2,rc,rc)

    def resizeEvent(self,event):
        pass
    
    def run(self):
        while(self._running):
            pygame.event.pump()
            self._Sticks={'lv':self._joystick.get_axis(axistostick['lv'])*axisreverse['lv'],
                          'lh':self._joystick.get_axis(axistostick['lh'])*axisreverse['lh'],
                          'rv':self._joystick.get_axis(axistostick['rv'])*axisreverse['rv'],
                          'rh':self._joystick.get_axis(axistostick['rh'])*axisreverse['rh']}

            if(self._instance is not None):
                p=round(100*self._Sticks[sticktofunc['pitch']])
                r=round(100*self._Sticks[sticktofunc['roll']])
                y=round(100*self._Sticks[sticktofunc['yaw']])
                t=round(100*self._Sticks[sticktofunc['gaz']])
                self._instance.PCMD(p,r,y,t)

                for event in pygame.event.get(): # User did something
                    if event.type == pygame.JOYBUTTONDOWN:
                        if(event.button in switchtofunc.keys()):
                            if(switchtofunc[event.button]=='start'):
                                try: 
                                    self._instance.tkof_lnd_emcy()
                                except:
                                    print("no device selected")
                            if(switchtofunc[event.button]=='rth'):
                                try: 
                                    self._instance.rth()
                                except:
                                    print("no device selected")

            self.update()
            time.sleep(self._periodicity)

    @property
    def device(self):
        return self._instance

    @device.setter
    def device(self,dev):
        if dev is not None:
            self._instance=dev
