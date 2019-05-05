import sys
from PySide2.QtWidgets import QApplication, QListWidgetItem, QListWidget
from PySide2.QtWidgets import QVBoxLayout, QPushButton, QWidget, QLabel
from PySide2.QtCore import Signal, Slot, QThread
import time
import inspect
from os.path import join

sys.path.append('./bybop/src')
from Bybop_Discovery import *
import Bybop_Device

def strFlyState(v):
    stfs=['LANDED','TAKINGOFF','HOVERING','FLYING','LANDING',
          'EMERGENCY','USERTAKEOFF','MOTOR_RAMPPING',
          'EMERGENCY_LANDING']
    return stfs[v] 


class ppDevice(QListWidgetItem):
    def __init__(self, device):
        self._dev=device
        self._instance=None
        super().__init__(get_name(device))
        fullPath = inspect.getfile(ppDevice)
        shortPathIndex = fullPath.rfind("/")
        if (shortPathIndex == -1):
            # handle Windows paths
            shortPathIndex = fullPath.rfind("\\")
        shortPath = fullPath[0:shortPathIndex]
        ip=get_ip(self._dev)
        sdpPath = join(shortPath, "sdps")
        self._sdpfile = sdpPath+"/"+ip+".sdp"
        f= open(self.sdpfile,"w+")
        f.write("c=IN IP4 "+ip+"\n")
        f.write("m=video 55004 RTP/AVP 96"+"\n")
        f.write("a=rtpmap:96 H264/90000"+"\n")
        f.close()

    @property
    def isconnected(self):
        return self.drone.is_connected()
    @property
    def name(self):
        return get_name(self._dev)
    @property
    def ip(self):
        return get_ip(self._dev)
    @property
    def id(self):
        return get_device_id(self._dev)
    @property
    def port(self):
        return get_port(self._dev)
    @property
    def sdpfile(self):
        return self._sdpfile
    @property
    def drone(self):
        return self._instance
    
    @property
    def flystate(self):
        #return self.strFlyState[self.drone.get_flystatus()['state']]
        return self.drone.get_flystatus()['state']
    @property
    def altitude(self):
        return self.drone.get_altitude()['altitude']
    @property
    def roll(self):
        return self.drone.get_attitude()['roll']
    @property
    def pitch(self):
        return self.drone.get_attitude()['pitch']
    @property
    def yaw(self):
        return self.drone.get_attitude()['yaw']
    @property
    def batt(self):
        return self.drone.get_battery()
    @property
    def heading(self):
        return self.drone.get_heading()
        
    def connect(self):
        d2c_port = 54321
        controller_type = "PC"
        controller_name = "ppGCS"
        print('Connecting to ' + self.name +" ...")
        self._instance = Bybop_Device.create_and_connect(
            self._dev, d2c_port, controller_type, controller_name)
    def start_stream(self):
        self.drone.start_streaming()
    def stop_stream(self):
        self.drone.stop_streaming()
    
    def tkof_lnd_emcy(self):
        fs=self.flystate
        if fs==0 : # landed
            return self.drone.take_off()
        elif fs==2 or fs==3: #hovering or flying
            return self.drone.land()
        else: # every thing else
            return self.drone.emergency()
        
    def land(self):
        return self.drone.land()
    def rth(self):
        return self.drone.RTH()
    def circle(self):
        return self.drone.circle()
    def emcy(self):
        return self.drone.emergency()
    
    def PCMD(self,pitch,roll,yaw,gaz):
        return self.drone.PCMD(pitch,roll,yaw,gaz)
    
    
        
    
    
