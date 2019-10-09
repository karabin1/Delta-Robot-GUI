from PyQt5            import QtCore, QtWidgets
from PyQt5.QtWidgets  import QWidget, QPushButton, QHBoxLayout, QLabel, QComboBox, QFormLayout, QDoubleSpinBox, QMessageBox
from newDataConstruct import newData_class
from kinematic        import workspace

class construct_class(QWidget):
    global  j, dataList
    j, dataList = [], [[],[],[],[],[],[]]
    send_construct = QtCore.pyqtSignal(int, list)
    
    def __init__(self, parent):                                                
        super(QWidget, self).__init__(parent)
  
        self.setMaximumSize(195, 240)
        self.construct_layoutH = QHBoxLayout(self)                             
        self.dataLayout()                                                       
        self.setLayout(self.construct_layoutH)                                 
        
        parent.send_construct_save.connect(self.construct_return)    

    def construct_return(self, l, dataListRet):                               
        for k in range(len(dataListRet)):                                     
            for i in range(len(dataListRet[0])):
                dataList[k].append(dataListRet[k][i])
        
        for i in range(len(dataListRet[0])):
            self.listName.addItem(dataListRet[0][i])   
        
        for i in range(len(dataListRet)-1):
            self.spin[i].setValue(float(dataList[i+1][l])) 
        self.listName.setCurrentIndex(l)                                    
        
    def dataLayout(self):                                                    
        data_layout = QFormLayout()                                            
    
        self.listName  = QComboBox()                                           
        self.listName.currentIndexChanged.connect(self.select_data_list)      
        data_layout.addRow(QLabel("Name:"), self.listName)                      
        
        butt_newData    = QPushButton("Add new data")                          
        butt_removeData = QPushButton("Remove actual data")                      
        butt_workspace  = QPushButton("Workspace")                              
        butt_newData.clicked.connect   (self.click_butt_newData)                
        butt_removeData.clicked.connect(self.click_butt_removeData)
        butt_workspace.clicked.connect (self.click_butt_worspace)
        
        self.list = ["f", "rf", "re", "e", "b"]
        self.spin = [] 
        
        for i in range(len(self.list)):
            self.spin.append(i)                                                
            self.spin[i] = QDoubleSpinBox()                                  
            self.spin[i].setReadOnly (True)                                     
            self.spin[i].setButtonSymbols(QtWidgets.QAbstractSpinBox.NoButtons)
            self.spin[i].setStyleSheet('color: black; background-color: white;')
            self.spin[i].setRange   (-9999,9999)                                
            self.spin[i].setDecimals(1)                                        
            self.spin[i].setSuffix  (' mm')                                    
            data_layout.addRow(QLabel(self.list[i] + ":"), self.spin[i])        
        data_layout.addRow(butt_workspace)
        data_layout.addRow(butt_newData)
        data_layout.addRow(butt_removeData)
        
        self.construct_layoutH.addLayout(data_layout)    

    def click_butt_newData(self):                                               
        self.new_data_window = newData_class()                                  
        self.new_data_window.send_data.connect(self.new_data_return)            
        self.new_data_window.show()                                             
        
        
    def click_butt_removeData(self):                                            
        if len(dataList[1]) < 2:
            QMessageBox.about(self, "Warning", "Add new data first and delete old data later")
            self.click_butt_newData()
            
        else:              
            for i in range(len(dataList)):      
                dataList[i].pop(j)                                              
            for i in range(len(dataList)-1): 
                self.spin[i].setValue(float(dataList[i+1][j-1]))
            self.listName.removeItem(j)
            self.listName.setCurrentIndex(j-1)

    def click_butt_worspace(self): 
        global j
        for i in range(len(dataList)-1): 
            self.spin[i].setValue(float(dataList[i+1][j]))                      
        
        dataworkspace = self.spin[0].value(), self.spin[1].value(), self.spin[2].value(), self.spin[3].value(), self.spin[4].value()
        workspace(dataworkspace)

    def new_data_return(self, dataListRet):                                     
        for i in range(len(dataList)): 
            dataList[i].append(dataListRet[i])
        
        self.listName.addItem(dataListRet[0])                                   
        self.listName.setCurrentIndex(len(dataList[0]))
        
    def select_data_list(self, k):                                              
        global j
        j = k
        for i in range(len(dataList)-1): 
            self.spin[i].setValue(float(dataList[i+1][j]))                      
        self.send_construct.emit(k, dataList)
