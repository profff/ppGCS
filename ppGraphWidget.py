import sys
from PySide2.QtWidgets import QApplication, QListWidgetItem, QListWidget
from PySide2.QtWidgets import QVBoxLayout, QPushButton, QWidget, QLabel
from PySide2.QtWidgets import QGroupBox, QFrame, QHBoxLayout
from PySide2.QtCore import Signal, Slot, QThread, QMargins, QPoint
from PySide2.QtGui import QPainter

class ppGraphWidget(QWidget):

    def __init__(self,p):
        QWidget.__init__(self)
        self._frame=QFrame()
        self._lMax=QLabel(str(0))
        self._lMax.setMaximumWidth(35)
        self._lVal=QLabel(str(0))
        self._lVal.setMaximumWidth(35)
        self.setMaximumSize(200,50)
        llayout = QVBoxLayout()
        llayout.setSpacing(0);
        llayout.setMargin(0);
        llayout.addWidget(self._lMax)
        llayout.addWidget(self._lVal)
        layout = QHBoxLayout()
        layout.setSpacing(0);
        layout.setMargin(0);
        layout.addWidget(self._frame)
        layout.addLayout(llayout)
        
        self.setLayout(layout)
        self._history=[]
        self._length=10 # time to display in sec
        self._max=0.1
        self._min=-0.1
        self._val=0
        self._maxoflength=0
        self._periodicity=p #time period between value in sec
        
    def __del__(self):
        pass
    @property
    def period(self):
        return self._periodicity
    @period.setter
    def period(self,v):
        self._periodicity=v
    
    def paintEvent(self, paintEvent):
        painter = QPainter(self)
        r=self._frame.rect()
        r-=QMargins(3,3,3,4)
#        painter.drawRect(r)
        h=len(self._history)
        if(h>5):
            csmp=round(self._length/self._periodicity)
            xr=r.width()/(self._length/self._periodicity)
            yr=r.height()/(self._max-self._min)
            i=csmp #sample count to display
            c=h-1 #index to display
            while(c>0 and i>0):
                x1=r.left()+xr*i
                x2=r.left()+xr*(i-1)
                v1=self._history[c]-self._min
                v2=self._history[c-1]-self._min
                y1=r.top()+r.height()-v1*yr
                y2=r.top()+r.height()-v2*yr
                painter.drawLine(x1,y1,x2,y2)
        #        print(x1,y1,x2,y2)
                i-=1
                c-=1
        
        
    def resizeEvent(self,event):
        pass
    
    def addValue(self,v):
        self._max=max(v,self._max)
        self._min=min(v,self._min)
        self._val=v
        self._lMax.setText(str(round(self._max)))
        self._lVal.setText(str(round(self._val)))
        self._history.append(v)
        self.update()

if __name__ == "__main__":
    app = QApplication([])

    widget = ppGraphWidget()
    widget.resize(800, 600)
    widget.show()
    
    sys.exit(app.exec_())
