import sys
from PySide2.QtWidgets import QApplication, QListWidgetItem, QListWidget
from PySide2.QtWidgets import QVBoxLayout, QPushButton, QWidget, QLabel
from PySide2.QtWidgets import QHBoxLayout, QSplitter
from PySide2.QtGui import QPalette,QColor
from PySide2.QtCore import Signal, Slot, QThread, Qt
import time
import math
from ppGraphWidget import *
from ppHorizonWidget import *
from ppBousoleWidget import *
from geomath import getDistanceClose

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
        self._altgraph=ppGraphWidget(self._periodicity,'Alt')
        self._battgraph=ppGraphWidget(5,'Bat%')
        self._battgraphitt=0
        self._horizon=ppHorizonWidget()
        self._bousole=ppBousoleWidget()
        self._lAirSpeed=QLabel('Air Speed:\t0')
        self._lGroundSpeed=QLabel('Gnd Speed:\t0')
        self._lClimbRate=QLabel('Climb Rate:\t0')
        self._lDistToHome=QLabel('To Home:\t0')
        self.setMinimumHeight(50)
        s=QSplitter()
        s.addWidget(self._altgraph)
        s.addWidget(self._horizon)
        s.addWidget(self._bousole)
        s.addWidget(self._battgraph)
        l=QVBoxLayout()
        l.addWidget(self._lAirSpeed)
        l.addWidget(self._lGroundSpeed)
        l.addWidget(self._lClimbRate)
        l.addWidget(self._lDistToHome)
        layout.addWidget(s)
        layout.addLayout(l)
        layout.setAlignment(Qt.AlignLeft)
       
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
                try:
                    asp=round(self._instance.drone.get_airspeed()*10)
                except:
                    asp=0
                spd=self._instance.drone.get_speeds()
                spdx=spd['speedX']
                spdy=spd['speedY']
                spdz=spd['speedZ']
                cmr=round(-spdz*10) #climb rate is oposite of speed z in NED referential
                spn=math.hypot(spdx, spdy)
                if(spn>1):
                    spdx/=spn
                    spdy/=spn
                    head=math.atan2(spdx,spdy)
                    self._bousole.yaw=head
                else:
                    self._bousole.yaw=-math.degrees(self._instance.yaw)
                    head=0
                gspd=round(spn*10)
                
                self._altgraph.addValue(self._instance.altitude)
                self._battgraphitt+=self._periodicity
                self._battgraphitt=self._battgraphitt % 5
                if(self._battgraphitt==0):
                    self._battgraph.addValue(self._instance.batt)
                self._horizon.roll=self._instance.roll
                self._horizon.pitch=self._instance.pitch
                self._lAirSpeed.setText('Air Speed:\t'+str(asp/10.0))
                self._lClimbRate.setText('Climb Rate:\t'+str(cmr/10.0))
                self._lGroundSpeed.setText('Gnd Speed:\t'+str(gspd/10.0))

            time.sleep(self._periodicity)

    @property
    def device(self):
        return self._instance

    @device.setter
    def device(self,dev):
        if dev is not None:
            self._instance=dev
