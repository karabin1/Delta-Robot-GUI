# Author Dawid Karabon 
# Github karabin1

import sys
import numpy as np
from PyQt5           import QtCore
from PyQt5.QtWidgets import QMainWindow, QApplication, QLabel, QHBoxLayout, QDockWidget
from PyQt5.QtWidgets import QInputDialog, QStackedWidget, QAction, QCheckBox, QMessageBox, QWidget
from PyQt5.QtCore    import Qt, QSettings
from control         import controll_class
from construct       import construct_class
from dataResult      import dataResult_class
from sequence        import sequence_class, sequenceTool_class
from kinematic       import inverse, forward
from dynamixel       import init, torque, close, getPoseInit
from plot            import Plot
from thread          import Thread

class MainWindow(QMainWindow):
    send_control_init   = QtCore.pyqtSignal(list, float)                        
    send_data_result    = QtCore.pyqtSignal(list, float, list)                  
    send_construct_save = QtCore.pyqtSignal(int, list)                          
    send_plotConst      = QtCore.pyqtSignal(list)                               
    send_plotXYZtheta   = QtCore.pyqtSignal(list, list)                         
    send_thread         = QtCore.pyqtSignal(float, list)                        
    send_thread2        = QtCore.pyqtSignal(float, list, list)                  
    send_sequenceActual = QtCore.pyqtSignal(list)                               
    send_sequenceSim    = QtCore.pyqtSignal(int)                                
    send_sequenceSetAct = QtCore.pyqtSignal(int)                                
    send_thread2Reset   = QtCore.pyqtSignal(int)                                
    
    def __init__(self):
        super().__init__()  
        
        self.kardan_min     = -150
        self.kardan_max     = -60
        
        self.online         = False
        self.torqueState    = False
        self.select         = 0                                                    
        self.dataList       = [[], [], [], [], [], []]                             
        self.xyz            = [0.0, 0.0, -100]                                   
        self.alpha          = 0.0
        self.theta          = [0.0, 0.0, 0.0]                                      
        self.sym            = 0
        self.presAngle      = []
        self.sequenceList   = [0.0, 0.0, 0.0, 0.0, 0.0]
        self.speed          = 10.0
        self.sequenceStatus = 0
        self.sequenceCount  = 0
        self.kardanStatus   = 0
        
        self.initWindow()                                                       
        
        self.dockWidget()                                                       
        self.show()                                                             
        
        settings        = QSettings('construct')                                
        select_getSave  = settings.value('select1', type=int)                   
        
        for i in range(len(self.dataList)):
            self.dataList[i] = settings.value('list' + str(i), 1024)            
        
        if self.dataList[0] != 1024:
            self.send_construct_save.emit(select_getSave, self.dataList)        
        
        try:
            sequenceListSave  = QSettings('SequenceList')                                
            self.sequenceData  = sequenceListSave.value('select2', list)                   
            
            if self.sequenceData != None:
                for i in range(len(self.sequenceData)):
                    self.send_sequenceActual.emit(self.sequenceData[i])
        except:
            print("error")
            
        self.git_thread = Thread(self)                                          
        self.git_thread.send_actualPoseT.connect(self.dataFromThread)           
        self.git_thread.send_visialisation.connect(self.Visual)                 
        self.git_thread.send_finish.connect(self.dynamixelFinish)                 
        self.git_thread.start()                                                 
    
    def dataFromThread(self, presAngleT):                                       
        self.xyz = forward(presAngleT, self.dataListActual)                     
        self.presAngle = presAngleT                                             
        self.send_data_result.emit(self.xyz, self.presAngle[3], self.presAngle) 
        
    def Visual(self, xyz, theta):                                               
        self.send_plotXYZtheta.emit(xyz, theta)                                 
        if self.sequenceStatus == 1:
            self.send_data_result.emit(self.xyz, self.alpha, self.theta)            
        
    def initWindow(self):                                                       
        self.setWindowTitle("Delta Robot Studio")                               
        self.setGeometry(0, 0, 790, 470)                                        
        #self.setMaximumSize(790, 470)
        #self.showMaximized()
        mainMenu   = self.menuBar()                                            
        windowMenu = mainMenu.addMenu('Window')                                  
        motorMenu  = mainMenu.addMenu('Connect motors')                   
        kardanMenu = mainMenu.addMenu('Cardan Joint')                   
        
        self.mainLayout = QHBoxLayout()                                         
        
        constructWindow = QAction ('Construct', self, checkable=True)         
        constructWindow.setChecked(True)                                        
        constructWindow.triggered.connect(self.constructWindow)                 
        windowMenu.addAction(constructWindow)                                   
                
        controlWindow = QAction ('Control', self, checkable=True)
        controlWindow.setChecked(True)
        controlWindow.triggered.connect(self.controlWindow)
        windowMenu.addAction(controlWindow)
        
        resultWindow = QAction ('Result', self, checkable=True)
        resultWindow.setChecked(True)
        resultWindow.triggered.connect(self.resultWindow)
        windowMenu.addAction(resultWindow)
        sequToolWindow = QAction ('Sequence tool', self, checkable=True)
        sequToolWindow.setChecked(True)
        sequToolWindow.triggered.connect(self.sequToolWindow)
        windowMenu.addAction(sequToolWindow)
        
        sequWindow = QAction ('Sequence', self, checkable=True)
        sequWindow.setChecked(True)
        sequWindow.triggered.connect(self.sequWindow)
        windowMenu.addAction(sequWindow)
                
        self.onlineWindow = QAction ('Online', self, checkable=True)
        self.onlineWindow.setChecked(False)
        self.onlineWindow.triggered.connect(self.onlineWindowDef)
        motorMenu.addAction(self.onlineWindow)
        
        self.torqueWindow = QAction ('Motor torque', self, checkable=True)
        self.torqueWindow.setChecked(False)
        self.torqueWindow.triggered.connect(self.torqueWindowDef)
        motorMenu.addAction(self.torqueWindow)
        
        kardanEnable = QAction ('Cardan Joint', self, checkable=True)
        kardanEnable.setChecked(False)
        kardanEnable.triggered.connect(self.kardanEnable)
        kardanMenu.addAction(kardanEnable)
        self.kardan_set = QAction ('Cardan settings', self, checkable=False)
        self.kardan_set.triggered.connect(self.kardanSettings)
        kardanMenu.addAction(self.kardan_set)

    def kardanSettings(self, state):  
        min, okPressed = QInputDialog.getDouble(self, "Cardan settings","minimal position:", self.kardan_min, -1000, 0, 2)
        if okPressed:
            self.kardan_min = min
        max, okPressed = QInputDialog.getDouble(self, "Cardan settings","maximal position:", self.kardan_max, -1000, 0, 2)
        if okPressed:
            self.kardan_max = max

    def kardanEnable(self, state): 
        if state: self.kardanStatus = 1
        else:     self.kardanStatus = 0
    
    def constructWindow(self, state):                                           
        if state: self.dockConstruct.show()                                     
        else:     self.dockConstruct.hide()                                     
        
    def controlWindow(self, state):                                             
        if state: self.dockControl.show()
        else:     self.dockControl.hide() 
        
    def resultWindow(self, state):                                              
        if state: self.dockDataResult.show()
        else:     self.dockDataResult.hide()
        
    def sequToolWindow(self, state):                                                
        if state: self.dockSequenceTool.show()                                      
        else:     self.dockSequenceTool.hide()                                      
        
    def sequWindow(self, state):                                                
        if state: self.dockSequence.show()                                      
        else:     self.dockSequence.hide()                                      
        
    def onlineWindowDef(self, state):                                           
        if state:                                                               
            try:    
                init()                                                          
                self.online = True                                              
                self.central_widget.addWidget(self.dockSequenceItem)
                self.central_widget.setCurrentWidget(self.dockSequenceItem)
                self.dockSequence.hide()
                self.send_sequenceSim.emit(0) 
                QMessageBox.about(self, "Succes", "Online mode enable")       
            except: 
                QMessageBox.about(self, "Warning", "Connect converter to port")  
                self.onlineWindow.setChecked(False)                             
        else:
            try:                                                                
                close()                                                         
                self.online = False                                             
                self.torqueState = False
                self.torqueWindow.setChecked(False)                             
                self.central_widget.setCurrentWidget(self.Visualization)
                self.send_sequenceSim.emit(1) 
                self.central_widget.removeWidget(self.dockSequenceItem)
                self.dockSequence.setWidget     (self.dockSequenceItem)
                self.dockSequence.show()
                QMessageBox.about(self, "Succes", "Online mode disable")      
            except: 
                QMessageBox.about(self, "Warning", "Somethong it's wrong")          
            
    def torqueWindowDef(self, state):                                           
        if state:                                                               
            if (self.online == True):                                           
                try:    
                    torque(True)                                                
                    self.torqueState = True                                     
                    self.presAngle   = getPoseInit()                            
                    self.xyz = forward(self.presAngle, self.dataListActual)     
                    self.send_control_init.emit(self.xyz, self.presAngle[3])    
                    self.send_data_result.emit (self.xyz, self.presAngle[3], self.presAngle)    
                    self.send_plotXYZtheta.emit(self.xyz, self.presAngle)                       
                    QMessageBox.about(self, "Succes", "Motor torque enable")               
                    
                except: 
                    QMessageBox.about(self, "Warning", "Connect motors")         
                    self.torqueWindow.setChecked(False)                         
            else:
                self.torqueWindow.setChecked(False)                             
                QMessageBox.about(self, "Warning", "Go online first")   
        else:
            try:    
                torque(False)                                                   
                self.torqueState = False                                        
                QMessageBox.about(self, "Succes", "Motor torque disable")  
            except: 
                QMessageBox.about(self, "Warning", "Somethong it's wrong")          
                self.torqueWindow.setChecked(False)                             
        
    def dockWidget(self):
        self.central_widget = QStackedWidget()                                  
        self.setCentralWidget(self.central_widget)
        
        self.infoText = QLabel("Value out of range")                         
        self.infoText.setStyleSheet('color: black; background-color: rgb(255, 255, 255);')
        self.infoText.setAlignment(QtCore.Qt.AlignCenter | QtCore.Qt.AlignVCenter)
        self.central_widget.addWidget(self.infoText)
        
        self.Visualization = Plot(self)                                         
        self.central_widget.addWidget(self.Visualization)                       
        self.central_widget.setCurrentWidget(self.Visualization)                
        
        
        self.dockConstruct    = QDockWidget("Construct", self)     
        self.dockControl      = QDockWidget("Control"  , self)     
        self.dockDataResult   = QDockWidget("Result"   , self)     
        self.dockSequenceTool = QDockWidget("Tool"     , self)     
        self.dockSequence     = QDockWidget("Sequence" , self)     
        
        self.dockDataResult.setMaximumHeight(35)
        self.dockSequence.setMaximumHeight(62)
        self.dockConstruct.setFeatures   (QDockWidget.DockWidgetMovable)          
        self.dockControl.setFeatures     (QDockWidget.DockWidgetMovable)        
        self.dockDataResult.setFeatures  (QDockWidget.DockWidgetMovable)
        self.dockSequenceTool.setFeatures(QDockWidget.DockWidgetMovable)
        self.dockSequence.setFeatures    (QDockWidget.DockWidgetMovable)
        
        self.dockConstructItem    = construct_class   (self)                          
        self.dockControlItem      = controll_class    (self)
        self.dockDataResultItem   = dataResult_class  (self)
        self.dockSequenceToolItem = sequenceTool_class(self)
        self.dockSequenceItem     = sequence_class    (self)
        
        self.dockConstruct.setWidget    (self.dockConstructItem  )
        self.dockControl.setWidget      (self.dockControlItem    )
        self.dockDataResult.setWidget   (self.dockDataResultItem )
        self.dockSequenceTool.setWidget (self.dockSequenceToolItem)
        self.dockSequence.setWidget     (self.dockSequenceItem   )
        self.dockDataResult.setTitleBarWidget   (QWidget(None))
        self.dockSequence.setTitleBarWidget     (QWidget(None))
        
        self.addDockWidget(Qt.RightDockWidgetArea , self.dockConstruct   )         
        self.addDockWidget(Qt.RightDockWidgetArea , self.dockControl     )
        self.addDockWidget(Qt.BottomDockWidgetArea, self.dockDataResult  )
        self.addDockWidget(Qt.LeftDockWidgetArea  , self.dockSequenceTool)
        self.addDockWidget(Qt.TopDockWidgetArea   , self.dockSequence    )
        self.tabifyDockWidget(self.dockConstruct  , self.dockControl     )
        
        self.dockControlItem.dataControl.connect           (self.send_xyz_return)            
        self.dockConstructItem.send_construct.connect      (self.send_construct_return) 
        self.dockSequenceToolItem.send_sequenceTool.connect(self.sequenceTool_return)
        self.dockSequenceToolItem.send_sequenceToolStart.connect(self.sequenceToolStart) 
        self.dockSequenceToolItem.send_sequenceToolStop.connect(self.sequenceToolStop) 
        self.dockSequenceToolItem.send_sequenceToolSave.connect(self.sequenceToolSave) 
        self.dockSequenceItem.send_sequence.connect        (self.sequence) 
        
        self.setLayout(self.mainLayout)              

    def sequenceToolSave(self, data):
        self.sequenceData = data
        
    def sequenceTool_return(self, delay):
        self.sequenceList[0] = self.xyz[0]
        self.sequenceList[1] = self.xyz[1]
        self.sequenceList[2] = self.xyz[2]
        self.sequenceList[3] = self.alpha
        self.sequenceList[4] = delay
        self.send_sequenceActual.emit(self.sequenceList) 
            
    def dynamixelFinish(self, finish):
        if self.sequenceStatus == 1 and self.online == True and self.torqueState == True:
            if self.sequenceCount < len(self.sequenceData):
                self.xyz[0] = self.sequenceData[self.sequenceCount][0]
                self.xyz[1] = self.sequenceData[self.sequenceCount][1]
                self.xyz[2] = self.sequenceData[self.sequenceCount][2]
                self.alpha  = self.sequenceData[self.sequenceCount][3]
                self.send_xyz_return(self.xyz, self.alpha, self.speed)
                self.send_sequenceSetAct.emit(self.sequenceCount)
                self.sequenceCount +=1
        elif self.sequenceStatus == 1 and (self.online == False or self.torqueState == False):
            self.send_sequenceSetAct.emit(self.sequenceCount-1)
            if self.sequenceCount < len(self.sequenceData):
                self.xyz[0] = self.sequenceData[self.sequenceCount][0]
                self.xyz[1] = self.sequenceData[self.sequenceCount][1]
                self.xyz[2] = self.sequenceData[self.sequenceCount][2]
                self.alpha  = self.sequenceData[self.sequenceCount][3]   
                self.send_xyz_return(self.xyz, self.alpha, self.speed)           
                self.sequenceCount +=1

    def sequenceToolStop(self, stop):
        self.sequenceStatus = 0
        self.sequenceCount = 0
        
    def sequenceToolStart(self, speed, data):
        try:
            self.speed = speed    
            self.sequenceData = data   
            self.send_sequenceSetAct.emit(0)
            self.sequenceStatus = 1
            self.sequenceCount = 1
            self.xyz[0] = self.sequenceData[0][0]
            self.xyz[1] = self.sequenceData[0][1]
            self.xyz[2] = self.sequenceData[0][2]
            self.alpha  = self.sequenceData[0][3]
            self.send_xyz_return(self.xyz, self.alpha, self.speed)
        except:
            QMessageBox.about(self, "Error", "Add points") 

    def sequence(self, data):
        self.xyz[0] = data[0]
        self.xyz[1] = data[1]
        self.xyz[2] = data[2]
        self.alpha  = data[3]
        self.send_xyz_return(self.xyz, self.alpha, self.speed)
              
    def send_construct_return(self, select_ret, dataListRet):                   
        self.select, self.dataList, self.dataListActual = select_ret, dataListRet, []   
        
        for i in range(len(self.dataList)):                                     
            self.dataListActual.append(i)
            self.dataListActual[i] = self.dataList[i][self.select]
        inverse(self.xyz, self.dataListActual)                                  
        self.send_data_result.emit(self.xyz, self.alpha, self.theta)            
        self.send_plotConst.emit(self.dataListActual)                           
        self.send_plotXYZtheta.emit(self.xyz, self.theta)     

    def send_xyz_return(self, xyz_ret, alpha, speed):                           
        self.xyz = xyz_ret 
        self.speed = speed
        self.alpha = alpha
        
        self.status, self.theta = inverse(self.xyz, self.dataListActual)        
        p1 = np.array([0, 0, 0])
        p2 = np.array([self.xyz[0], self.xyz[1], self.xyz[2]])
        squared_dist = np.sum(p1**2 + p2**2, axis=0)
        dist = np.sqrt(squared_dist)
        
        if self.status == 1 or self.alpha < -150 or self.alpha > 150 or (self.kardanStatus == 1 and (dist < -self.kardan_max or dist > -self.kardan_min)):           
            self.central_widget.setCurrentWidget(self.infoText)                 
        else:
            dataDynamixel = [self.theta[0], self.theta[1], self.theta[2], self.alpha]  
            if (self.online == True and self.torqueState == True):              
                self.central_widget.setCurrentWidget(self.dockSequenceItem)
                self.send_thread.emit(speed, dataDynamixel)                     
                self.sym = 0                                                    
            elif (self.sym == 0):
                QMessageBox.about(self, "Warning", "Simulation mode, to exit enable online mode and motor torque")   
                self.central_widget.setCurrentWidget(self.Visualization)        
                self.sym = 1     
            else:
                self.send_thread2.emit(speed, self.xyz, self.theta)                    
                self.central_widget.setCurrentWidget(self.Visualization)
                if self.sequenceStatus == 0:
                    self.send_data_result.emit(self.xyz, self.alpha, self.theta)            
                
    def closeEvent(self, event):                                                
        settings = QSettings('construct')
        settings.setValue('select1', self.select)
                
        for i in range(len(self.dataList)):
            settings.setValue('list' + str(i), self.dataList[i])
        
        sequenceListSave = QSettings('SequenceList')
        sequenceListSave.setValue('select2', self.sequenceData)
        QMainWindow.closeEvent(self, event)
        
        if (self.torqueState == True):
            torque(0)                                                           
    
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWindow()
    sys.exit(app.exec_())
