from PyQt5.QtCore    import Qt
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QLabel, QDoubleSpinBox, QAbstractSpinBox
class dataResult_class(QWidget):
    
    def __init__(self, parent):                                                 
        super(QWidget, self).__init__(parent)
        
        parent.send_data_result.connect(self.get_data)                          
        
        self.dataResult_layoutH = QHBoxLayout(self)                             
        self.dataResultLayout()                                                 
        self.setLayout(self.dataResult_layoutH)                                 
        
    def dataResultLayout(self):                                                 
        self.list   = ["x:", "y:", "z:", "α:", "t1:", "t2:", "t3:"]             
        self.change = 3                                                         
        self.spin   = []                                                        
        self.label  = []                                                        
        
        for i in range(len(self.list)):
            self.spin.append(i)
            self.spin[i] = QDoubleSpinBox()
            self.spin[i].setReadOnly (True)                                     
            self.spin[i].setButtonSymbols(QAbstractSpinBox.NoButtons)           
            self.spin[i].setRange    (-999,999)                                 
            self.spin[i].setDecimals (1)                                        
            
            if i < self.change:
                self.spin[i].setStyleSheet('color: black; background-color: rgb(160, 251, 172);')   
                self.spin[i].setSuffix   (' mm')                                                    
            elif i == self.change:
                self.spin[i].setStyleSheet('color: black; background-color: rgb(243, 243, 104);')   
                self.spin[i].setSuffix   ('°')                                                      
            else:
                self.spin[i].setStyleSheet('color: black; background-color: rgb(255, 200, 134);')   
                self.spin[i].setSuffix   ('°')                                                      
                
            self.label.append(i)
            self.label[i] = QLabel(self.list[i])
            self.label[i].setAlignment(Qt.AlignRight | Qt.AlignVCenter)         
        
            self.dataResult_layoutH.addWidget(self.label[i])                    
            self.dataResult_layoutH.addWidget(self.spin[i])                     
     
    def get_data(self, xyz, alpha, theta):                                      
        data = [xyz[0], xyz[1], xyz[2], alpha, theta[0], theta[1], theta[2]]
        
        for i in range(len(self.list)):
            self.spin[i].setValue(data[i])