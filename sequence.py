from PyQt5            import QtCore
from PyQt5.QtWidgets  import QWidget, QTableWidget, QTableWidgetItem,QVBoxLayout, QPushButton, QButtonGroup,QLabel, QDoubleSpinBox, QMessageBox

global dataSequence
dataSequence = []

class sequenceTool_class(QWidget):
    send_sequenceTool      = QtCore.pyqtSignal(int)
    send_sequenceToolStart = QtCore.pyqtSignal(float, list)
    send_sequenceToolStop  = QtCore.pyqtSignal(int)
    send_sequenceToolSave  = QtCore.pyqtSignal(list)
    
    def __init__(self, parent):                                                 
        super(QWidget, self).__init__(parent)
  
        self.setMaximumSize(185, 275)
        self.sequence_layout = QVBoxLayout(self)                              
        self.dataLayout()                                                       
        self.setLayout(self.sequence_layout)                                  
        
    def dataLayout(self):                                                       
        data_layout = QVBoxLayout()                                             
               
        self.spinSpeed = QDoubleSpinBox()                                    
        self.spinSpeed.setRange   (1,100)                              
        self.spinSpeed.setDecimals(1)                                       
        self.spinSpeed.setValue   (10) 
        self.spinSpeed.setPrefix('v: ')                                   
        self.spinSpeed.setSuffix(' %')                                   
        self.spinDelay = QDoubleSpinBox()                                    
        self.spinDelay.setRange   (0,10)                              
        self.spinDelay.setDecimals(2)                                       
        self.spinDelay.setValue   (0) 
        self.spinDelay.setPrefix('stop: ')                                   
        self.spinDelay.setSuffix(' s')                                   
         
        data_layout.addWidget(self.spinSpeed)
        data_layout.addWidget(self.spinDelay)
        
        self.list = ["Add point", "START", "STOP", "Save"]
        self.buttons = [] 
        
        for i in range(len(self.list)):
            self.buttons.append(i)                                              
            self.buttons[i] = QPushButton(self.list[i], self)                   
            self.buttons[i].setMinimumHeight(35)                                  
            data_layout.addWidget(self.buttons[i])                              
            
        self.buttons[0].clicked.connect(self.butt1)
        self.buttons[1].clicked.connect(self.butt2)
        self.buttons[2].clicked.connect(self.butt3)
        self.buttons[3].clicked.connect(self.butt4)
        self.buttons[0].setStyleSheet('color: black; background-color: yellow;') 
        self.buttons[1].setStyleSheet('color: black; background-color: green;') 
        self.buttons[2].setStyleSheet('color: black; background-color: red;') 
        
        self.author = QLabel("Github: karabin1")
        data_layout.addWidget(self.author)

        self.sequence_layout.addLayout(data_layout)      

    def butt1(self):
        self.send_sequenceTool.emit(self.spinDelay.value())

    def butt2(self):
        self.send_sequenceToolStart.emit(self.spinSpeed.value(), dataSequence)
        
    def butt3(self):
        self.send_sequenceToolStop.emit(1)
    
    def butt4(self):
        self.send_sequenceToolSave.emit(dataSequence)
        
class sequence_class(QWidget):
    send_sequence = QtCore.pyqtSignal(list)
    
    def __init__(self, parent):                                                 
        super(QWidget, self).__init__(parent)
  
        parent.send_sequenceActual.connect(self.addSequence)
        parent.send_sequenceSim.connect(self.simulation)
        parent.send_sequenceSetAct.connect(self.setAct)
    
        self.n = 0
        
        self.buttGo  = []                                                        
        self.buttGoGroup = QButtonGroup()                                     
        self.buttGoGroup.buttonClicked[int].connect(self.buttGoDef)      
        self.buttClear  = []                                                        
        self.buttClearGroup = QButtonGroup()                                     
        self.buttClearGroup.buttonClicked[int].connect(self.buttClearDef)      
        self.sequence_layout = QVBoxLayout(self)                                
        self.createTable()     
        self.sequence_layout.addWidget(self.tableWidget)                        
        self.setLayout(self.sequence_layout)                                    
    
    def buttGoDef(self, i):
        self.send_sequence.emit(dataSequence[i])
        self.tableWidget.selectRow(i)
        
    def buttClearDef(self, i):
        try:
            for j in range(i, len(dataSequence)-1):
                self.buttClear[j] = self.buttClear[j+1]
                self.buttClearGroup.setId(self.buttClear[j+1], (j))
                self.buttGo[j] = self.buttGo[j+1]
                self.buttGoGroup.setId(self.buttGo[j+1], (j))
            dataSequence.pop(i)
            self.tableWidget.removeRow(i)  
            self.n -= 1
        except:
           print("error")
           
    def setAct(self, act):
        self.tableWidget.selectRow(act)        
        
    def simulation(self, sim):
        if sim == 0:
            for i in range(7):
                self.tableWidget.setColumnWidth(i, 59)
        if sim == 1:
            for i in range(7):
                self.tableWidget.setColumnWidth(i, 104)
        
    def addSequence(self, dataRet):
        data = []
        data.extend(dataRet)
        dataSequence.append(data)
        self.buttGo.append(self.n) 
        self.buttGo[self.n] = QPushButton("Go")
        self.buttClear.append(self.n) 
        self.buttClear[self.n] = QPushButton("Remove")
        
        self.n += 1
        self.tableWidget.setRowCount(self.n)
        for i in range(len(dataRet)):
            self.tableWidget.setItem(self.n-1,i, QTableWidgetItem(str(dataRet[i])))
        
        self.tableWidget.setCellWidget(self.n-1,i+1, self.buttGo[self.n-1])
        self.tableWidget.setCellWidget(self.n-1,i+2, self.buttClear[self.n-1])
        self.tableWidget.setRowHeight(self.n-1, 20)
        self.tableWidget.selectRow(self.n-1)
        self.buttGoGroup.addButton(self.buttGo[self.n-1], self.n-1)
        self.buttClearGroup.addButton(self.buttClear[self.n-1], self.n-1)
        
    def createTable(self):
       
        self.tableWidget = QTableWidget()
        self.tableWidget.setRowCount(0)
        self.tableWidget.setColumnCount(7)
        label = ['x [mm]', 'y [mm]', 'z [mm]', 'α [°]', 'stop [s]', ' ', ' ']
        self.tableWidget.setHorizontalHeaderLabels(label)
        self.tableWidget.itemChanged.connect(self.on_click)
        
    def on_click(self):
        for currentQTableWidgetItem in self.tableWidget.selectedItems():
            dataSequence[currentQTableWidgetItem.row()][currentQTableWidgetItem.column()] = float(currentQTableWidgetItem.text())
