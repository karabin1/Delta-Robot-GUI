import math
import time
from dynamixel       import run_dynamixel
from PyQt5           import QtCore
from PyQt5.QtCore    import QThread

class Thread(QThread):
    send_actualPoseT = QtCore.pyqtSignal(list)
    send_visialisation = QtCore.pyqtSignal(list, list)
    send_finish = QtCore.pyqtSignal(int)
    
    def __init__(self, MainWindow):
        
        QThread.__init__(self)
        self.git_url = ""
        
        MainWindow.send_thread.connect(self.Dynamixel)                       
        MainWindow.send_thread2.connect(self.Visualization)
        
        self.status = 0
        self.visual3d = 0
        self.dataDynamixelT = [0.0, 0.0, -200.0, 0.0]
        self.sleepTime = 0.5
        self.tresh = [0.0, 0.0, 0.0, 0.0]
        
    def Dynamixel(self, speedT, dataDynamixelT):
        self.dataDynamixelT1 = self.dataDynamixelT
        self.speedT = speedT
        self.dataDynamixelT = dataDynamixelT
        self.status = 1
        self.start = time.time()
        
        for i in range(len(dataDynamixelT)):
            self.positionDif = abs(self.dataDynamixelT1[0] - self.dataDynamixelT[0])
            if abs(self.dataDynamixelT1[i] - self.dataDynamixelT[i]) > self.positionDif:
                self.positionDif = abs(self.dataDynamixelT1[i] - self.dataDynamixelT[i])
        
        self.stopTime = self.positionDif / (math.sqrt(self.speedT)*6)
        self.sleepTime = 0.05 

    def Visualization(self, speedV, xyz, theta):
        self.speedV = speedV
        self.xyz = xyz
        self.theta = theta
        self.visual3d = 1
        self.sleepTime = 0.5 

    def run(self):
        while 1:
            if self.status == 1:
                self.presentPoseT = run_dynamixel(self.speedT*10, self.dataDynamixelT)    
                for i in range(len(self.dataDynamixelT)):
                    self.tresh[i] = abs(self.presentPoseT[i] - self.dataDynamixelT[i])
                if self.tresh[0] < 5 and self.tresh[1] < 5 and self.tresh[2] < 5 and self.tresh[3] < 3:
                    self.send_finish.emit(1)
                    self.status = 0
                    
                stop = time.time() - self.start
                self.send_actualPoseT.emit(self.presentPoseT)

                if stop > self.stopTime:
                    self.send_finish.emit(1)
                    self.status = 0
               
            if self.visual3d == 1:    
                self.send_visialisation.emit(self.xyz, self.theta)
                self.send_finish.emit(1)
                self.visual3d = 0  
            
            time.sleep(self.sleepTime)