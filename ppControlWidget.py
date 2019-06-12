import sys
from PySide2.QtWidgets import QApplication, QListWidgetItem, QListWidget
from PySide2.QtWidgets import QHBoxLayout, QPushButton, QWidget, QLabel
from PySide2.QtWidgets import QGroupBox, QFrame,QDialog,QLineEdit, QVBoxLayout
from PySide2.QtCore import Signal, Slot, QThread, QMargins, QPoint
from PySide2.QtGui import QPainter,QIcon

import time
from ppDevice import *
import pygame
import json

try:
    with open('control_config.txt', 'r') as outfile:  
        joytofunc=json.load(outfile)
        print ("control config file loaded")
except:
    print ("default control config loaded")
    joytofunc={'funcreverse':{'gaz':-1,
                              'yaw':1,
                              'pitch':-1,
                              'roll':1},
               'functoaxis':{'pitch':3,
                             'roll':2,
                             'gaz':1,
                             'yaw':0},
               'functoswitch':{'start':0,
                               'rth':2}}
joytofunc['switchtofunc']={y:x for x,y in joytofunc['functoswitch'].items()}
bindaxis=None

def bindtopitch():
    global bindaxis
    bindaxis='pitch'
def bindtoroll():
    global bindaxis
    bindaxis='roll'
def bindtoyaw():
    global bindaxis
    bindaxis='yaw'
def bindtogaz():
    global bindaxis
    bindaxis='gaz'
def bindtostart():
    global bindaxis
    bindaxis='start'
def bindtorth():
    global bindaxis
    bindaxis='rth'
def bindsave():
    with open('control_config.txt', 'w') as outfile:  
        json.dump(joytofunc, outfile)
        outfile.close()

class ppConfigControlWindow(QDialog):
    def __init__(self, parent=None):
        super(ppConfigControlWindow, self).__init__(parent)
        # Create widgets
        s=self.parent().Sticks
        self.btPitch = QPushButton("pitch: 0")
        self.btRoll = QPushButton("roll: 0")
        self.btYaw = QPushButton("Yaw: 0")
        self.btGaz = QPushButton("Thrust: 0")
        self.btTakeoff = QPushButton("Takeoff/Landing: 0")
        self.btRth = QPushButton("RTH: 0")
        self.btSave = QPushButton("Save")
        # Create layout and add widgets
        layout = QVBoxLayout()
        layout.addWidget(self.btPitch)
        layout.addWidget(self.btRoll)
        layout.addWidget(self.btYaw)
        layout.addWidget(self.btGaz)
        layout.addWidget(self.btTakeoff)
        layout.addWidget(self.btRth)
        layout.addWidget(self.btSave)
        # Set dialog layout
        self.setLayout(layout)
        # Add button signal to slot
        self.btPitch.clicked.connect(bindtopitch)
        self.btRoll.clicked.connect(bindtoroll)
        self.btYaw.clicked.connect(bindtoyaw)
        self.btGaz.clicked.connect(bindtogaz)
        self.btTakeoff.clicked.connect(bindtostart)
        self.btRth.clicked.connect(bindtorth)
        self.btSave.clicked.connect(bindsave)

    def freshValues(self,p,r,y,g,to,rt):
        self.btPitch.setText("pitch: %d"%p)
        self.btRoll.setText("roll: %d"%r)
        self.btYaw.setText("Yaw: %d"%y)
        self.btGaz.setText("Thrust: %d"%g)
        self.btTakeoff.setText("Takeoff/Landing: %d"%to)
        self.btRth.setText("RTH: %d"%rt)


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
            self._Sticks={'gaz':self._joystick.get_axis(joytofunc['functoaxis']['gaz'])*joytofunc['funcreverse']['gaz'],
                          'yaw':self._joystick.get_axis(joytofunc['functoaxis']['yaw'])*joytofunc['funcreverse']['yaw'],
                          'pitch':self._joystick.get_axis(joytofunc['functoaxis']['pitch'])*joytofunc['funcreverse']['pitch'],
                          'roll':self._joystick.get_axis(joytofunc['functoaxis']['roll'])*joytofunc['funcreverse']['roll']}
            self._Switchs={'start':self._joystick.get_button(joytofunc['functoswitch']['start']),
                           'rth':self._joystick.get_button(joytofunc['functoswitch']['rth'])}
        else:
            self._joystick = None
            self._Sticks={'gaz':0,
                          'yaw':0,
                          'pitch':0,
                          'roll':0}
            self._Switchs={'start':0,
                           'rth':0}
        self.btconfig.clicked.connect(self.config)
        self.ConfigDialog=ppConfigControlWindow(parent=self)
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
        c1=QPoint(r.width()/4+(self._Sticks['yaw']*r1),r.height()/2-(self._Sticks['gaz']*r1))
        c2=QPoint(3*r.width()/4+(self._Sticks['roll']*r1),r.height()/2-(self._Sticks['pitch']*r1))
        painter.drawEllipse(c1,rc,rc)
        painter.drawEllipse(c2,rc,rc)

    def resizeEvent(self,event):
        pass
    
    def run(self):
        global bindaxis
        while(self._running):
            pygame.event.pump()
            if(self._joycnt>0):
                self._Sticks={'gaz':self._joystick.get_axis(joytofunc['functoaxis']['gaz'])*joytofunc['funcreverse']['gaz'],
                              'yaw':self._joystick.get_axis(joytofunc['functoaxis']['yaw'])*joytofunc['funcreverse']['yaw'],
                              'pitch':self._joystick.get_axis(joytofunc['functoaxis']['pitch'])*joytofunc['funcreverse']['pitch'],
                              'roll':self._joystick.get_axis(joytofunc['functoaxis']['roll'])*joytofunc['funcreverse']['roll']}
                self._Switchs={'start':self._joystick.get_button(joytofunc['functoswitch']['start']),
                               'rth':self._joystick.get_button(joytofunc['functoswitch']['rth'])}
                
            p=round(100*self._Sticks['pitch'])
            r=round(100*self._Sticks['roll'])
            y=round(100*self._Sticks['yaw'])
            t=round(100*self._Sticks['gaz'])
            to=self._Switchs['start']
            rt=self._Switchs['rth']
                           
            self.ConfigDialog.freshValues(p,r,y,t,to,rt)

            if(self._instance is not None):
                self._instance.PCMD(p,r,y,t)

                    
            for event in pygame.event.get(): # User did something
                if not (bindaxis == None):
                    if event.type == pygame.JOYAXISMOTION:
                        if abs(event.value)>0.5:
                            joytofunc['functoaxis'][bindaxis]=event.axis
                            bindaxis=None
                    if event.type == pygame.JOYBUTTONDOWN:
                        joytofunc['functoswitch'][bindaxis]=event.button
                        bindaxis=None

                        

                
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
        w=self.ConfigDialog
        w.show()

    @property
    def Sticks(self):
        return self._Sticks
    
    @property
    def device(self):
        return self._instance

    @device.setter
    def device(self,dev):
        if dev is not None:
            self._instance=dev
