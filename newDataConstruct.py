from PyQt5           import QtCore
from PyQt5.QtWidgets import QWidget, QPushButton, QHBoxLayout, QGroupBox, QLabel, QLineEdit, QFormLayout, QDoubleSpinBox, QMessageBox
from PyQt5.QtGui     import QPixmap
from PyQt5.QtCore    import Qt

class newData_class(QWidget):
    
    send_data = QtCore.pyqtSignal(list)                                         
    cancel_button = QtCore.pyqtSignal(bool)                                     
    
    global check_data_name                                                      
    check_data_name = []
    
    def __init__(self):                                                         
        super().__init__()
        flags = Qt.Window | Qt.WindowMaximizeButtonHint                         
        self.setWindowFlags(flags)
        
        self.setWindowTitle("New construct data")                                
        self.createGridLayout()                                                 
        self.createImage()                                                      
 
        self.windowLayout = QHBoxLayout()                                       
        self.windowLayout.addWidget(self.data_GroupBox)                         
        self.windowLayout.addWidget(self.image_label)                           
        self.setLayout(self.windowLayout)                                       
        
        self.setGeometry(0, 0, 200, 200)                                        
        
    def createGridLayout(self):
        self.data_GroupBox = QGroupBox('New construct data')     
        data_layout = QFormLayout()                                             
        
        self.name = QLineEdit()                                                 
               
        data_layout.addRow(QLabel("Name :"), self.name)                        
        data_layout.addRow(QLabel("Data :"))
        
        self.list = ["f", "rf", "re", "e", "b"]
        self.spin = [] 
        
        for i in range(len(self.list)):
            self.spin.append(i)                                                 
            self.spin[i] = QDoubleSpinBox()                                     
            self.spin[i].setRange   (-9999,9999)                                
            self.spin[i].setDecimals(1)                                         
            self.spin[i].setSuffix  (' mm')                                     
            data_layout.addRow(QLabel(self.list[i] + ":"), self.spin[i])
        
        butt_save   = QPushButton("Save")                                       
        butt_cancel = QPushButton("Cancel")                                     
        
        butt_save.clicked.connect  (self.click_butt_save)                       
        butt_cancel.clicked.connect(self.click_butt_cancel)                     
         
        data_layout.addRow(butt_save)
        data_layout.addRow(butt_cancel)
        
        self.data_GroupBox.setLayout(data_layout)                               
        
    def createImage(self):
        self.image_label = QLabel(self)                                         
        self.image_label.setContentsMargins(0, 0, 0, 0);                        
        self.pixmap = QPixmap("konstrukcja.png")                                
        self.pixmap = self.pixmap.scaled(450, 420)                              
        self.image_label.setPixmap(self.pixmap)                                 
        self.image_label.show()
    
    def click_butt_save(self):                                                  
        error = 0                                                               
        dataEmit = [self.name.text()]
        
        for i in range(len(self.list)):
            dataEmit.append(i)
            dataEmit[i+1] = self.spin[i].value()
            if (self.name.text() == "" or self.spin[i].value() == 0):
                if i == len(self.list):
                    QMessageBox.about(self, "Warning", "Complete all data")
                    error = 1
       
        for i in check_data_name:                                               
            if i == self.name.text():
                QMessageBox.about(self, "Warning", "The same name")  
                error = 1 
        if error == 0:
            check_data_name.append(self.name.text())                            
            self.send_data.emit(dataEmit)
            self.close()                                                        
        
    def click_butt_cancel(self):                                                
        self.cancel_button.emit(1)                                              
        self.close()       