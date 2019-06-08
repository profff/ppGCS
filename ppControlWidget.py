import sys
from PySide2.QtWidgets import QApplication, QListWidgetItem, QListWidget
from PySide2.QtWidgets import QHBoxLayout, QPushButton, QWidget, QLabel
from PySide2.QtWidgets import QGroupBox, QFrame,QDialog,QLineEdit, QVBoxLayout
from PySide2.QtCore import Signal, Slot, QThread, QMargins, QPoint
from PySide2.QtGui import QPainter,QIcon

import time
from ppDevice import *
import pygame
joytofunc={'axistostick':{'lv':1,
                          'lh':0,
                          'rv':3,
                          'rh':2},
           'axisreverse':{'lv':-1,
                          'lh':1,
                          'rv':-1,
                          'rh':1},
           'sticktofunc':{'pitch':'rv',
                          'roll':'rh',
                          'gaz':'lv',
                          'yaw':'lh'},
           'switchtofunc':{0:'start',
                           2:'rth'}
           }

class ppConfigControlWindow(QDialog):
    def __init__(self, parent=None):
        super(ppConfigControlWindow, self).__init__(parent)
        # Create widgets
        self.btPitch = QPushButton("pitch: 0")
        self.btRoll = QPushButton("roll: 0")
        self.btYaw = QPushButton("Yaw: 0")
        self.btGaz = QPushButton("Thrust: 0")
        self.btTakeoff = QPushButton("Takeoff/Landing: 0")
        self.btRth = QPushButton("RTH: 0")
        # Create layout and add widgets
        layout = QVBoxLayout()
        layout.addWidget(self.btPitch)
        layout.addWidget(self.btRoll)
        layout.addWidget(self.btYaw)
        layout.addWidget(self.btGaz)
        layout.addWidget(self.btTakeoff)
        layout.addWidget(self.btRth)
        # Set dialog layout
        self.setLayout(layout)
        # Add button signal to greetings slot



class ppControlWidget(QWidget, QThread):

    def __init__(self):
        QWidget.__init__(self)
        QThread.__init__(self)

        pygame.init()
        pygame.joystick.init()
        self._joycnt=pygame.joystick.get_count()
        print (self._joycnt)
        if(self._joycnt==0):
            print('no joystick found')
            #sys.exit(0)
        else :
            pygame.joystick.Joystick(0).init()
            if(pygame.joystick.Joystick(0).get_numaxes()<4):
                self._joycnt=0

        self._running=True
        self._instance=None
        self._periodicity=0.05 #time period between loops
        self.frame=QFrame()
        self.frame.setFixedSize(100,50)
        self.btconfig=QPushButton(QIcon("res/config.png"),"")
        self.setFixedSize(140,50)
        self.layout = QHBoxLayout()
        self.layout.addWidget(self.frame)
        self.layout.addWidget(self.btconfig)
        self.setLayout(self.layout)
        if(self._joycnt>0):
            self._joystick = pygame.joystick.Joystick(0)
            self._joystick.init()
            print(self._joystick.get_name())
            pygame.event.pump()
            self._Sticks={'lv':self._joystick.get_axis(joytofunc['axistostick']['lv'])*joytofunc['axisreverse']['lv'],
                          'lh':self._joystick.get_axis(joytofunc['axistostick']['lh'])*joytofunc['axisreverse']['lh'],
                          'rv':self._joystick.get_axis(joytofunc['axistostick']['rv'])*joytofunc['axisreverse']['rv'],
                          'rh':self._joystick.get_axis(joytofunc['axistostick']['rh'])*joytofunc['axisreverse']['rh']}
        else:
            self._joystick = None
            self._Sticks={'lv':0,
                          'lh':0,
                          'rv':0,
                          'rh':0}

        self.btconfig.clicked.connect(self.config)
        
        self.start()
        
    def __del__(self):
        self._running=False
        pygame.quit()

    def paintEvent(self, paintEvent):
        painter = QPainter(self)
        r=self.frame.rect()
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
            if(self._joycnt>0):
                self._Sticks={'lv':self._joystick.get_axis(joytofunc['axistostick']['lv'])*joytofunc['axisreverse']['lv'],
                              'lh':self._joystick.get_axis(joytofunc['axistostick']['lh'])*joytofunc['axisreverse']['lh'],
                              'rv':self._joystick.get_axis(joytofunc['axistostick']['rv'])*joytofunc['axisreverse']['rv'],
                              'rh':self._joystick.get_axis(joytofunc['axistostick']['rh'])*joytofunc['axisreverse']['rh']}

            if(self._instance is not None):
                p=round(100*self._Sticks[joytofunc['sticktofunc']['pitch']])
                r=round(100*self._Sticks[joytofunc['sticktofunc']['roll']])
                y=round(100*self._Sticks[joytofunc['sticktofunc']['yaw']])
                t=round(100*self._Sticks[joytofunc['sticktofunc']['gaz']])
                self._instance.PCMD(p,r,y,t)

                for event in pygame.event.get(): # User did something
                    if event.type == pygame.JOYBUTTONDOWN:
                        if(event.button in joytofunc['switchtofunc'].keys()):
                            if(joytofunc['switchtofunc'][event.button]=='start'):
                                try: 
                                    self._instance.tkof_lnd_emcy()
                                except:
                                    print("no device selected")
                            if(joytofunc['switchtofunc'][event.button]=='rth'):
                                try: 
                                    self._instance.rth()
                                except:
                                    print("no device selected")

            self.update()
            time.sleep(self._periodicity)

    def config(self):
        w=ppConfigControlWindow(parent=self)
        w.show()
    @property
    def device(self):
        return self._instance

    @device.setter
    def device(self,dev):
        if dev is not None:
            self._instance=dev
