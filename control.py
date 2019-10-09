from PyQt5           import QtCore
from PyQt5.QtWidgets import QWidget, QPushButton, QTabWidget, QVBoxLayout, QDial, QRadioButton, QInputDialog
from PyQt5.QtWidgets import QHBoxLayout, QGridLayout, QLabel, QButtonGroup, QFormLayout, QDoubleSpinBox
from PyQt5.QtGui     import QIcon
from PyQt5.QtCore    import QSize

class controll_class(QWidget):
    dataControl = QtCore.pyqtSignal(list, float, int)                           
    
    def __init__(self, parent):                                                 
        super(QWidget, self).__init__(parent)
        parent.send_control_init.connect(self.controlInit)                      
        
        self.setMaximumSize(195, 240)                                           
        self.control_layoutV = QVBoxLayout(self)                                
        self.controlLayout()                                                    
        self.setLayout(self.control_layoutV)                                    
            
    def controlLayout(self):                                                    
        self.control_tabs = QTabWidget() 
        
        self.tab_contr1 = QWidget()                                             
        self.tab_contr2 = QWidget()                                             
        self.tab_contr3 = QWidget()                                             
        
        
        tab_contr1_layout = QFormLayout()
        tab_contr2_layout = QGridLayout()
        tab_contr3_layout = QFormLayout()
        check_axis_layout = QHBoxLayout()
    
        
        self.list1   = ["x", "y", "z", "α", "v"]                                
        self.change1 = 3                                                        
        self.spin1   = []                                                       
        
        for i in range(len(self.list1)):
            self.spin1.append(i)                                                
            self.spin1[i] = QDoubleSpinBox()                                    
            self.spin1[i].setRange    (-9999,9999)                              
            self.spin1[i].setDecimals (1)                                       
            if    i < self.change1: 
                self.spin1[i].setSuffix(' mm')                                  
            elif i == self.change1:
                self.spin1[i].setSuffix(' °')                                   
                self.spin1[i].setRange (-151, 151)                              
            else:                
                self.spin1[i].setSuffix(' %')                                   
                self.spin1[i].setValue (10)                                     
                self.spin1[i].setRange (0, 100) 
                self.spin1[2].setRange (-9999, -1)                              
                                 
            tab_contr1_layout.addRow(self.list1[i] + ":", self.spin1[i])        
                
        butt_save = QPushButton("Write")                                        
        butt_save.clicked.connect(self.click_butt_save)                         
        tab_contr1_layout.addRow(butt_save)                                     
    
        
        self.spin2_step = QDoubleSpinBox()                                      
        self.spin2_step.setRange     (0,5)                                      
        self.spin2_step.setDecimals  (1  )  
        self.spin2_step.setSingleStep(0.1)
        self.spin2_step.setValue     (1.0)
        self.spin2_step.setSuffix    (' mm')
        tab_contr2_layout.addWidget(QLabel("Step:"), 0, 0)                      
        tab_contr2_layout.addWidget(self.spin2_step, 0, 1, 1, 2)                
        
        self.label2 = ["x", "y", "z", "α"]                                      
        self.butt2  = []                                                        
        self.button2_Group = QButtonGroup()                                     
        self.button2_Group.buttonClicked[int].connect(self.click_butt_xyz)      
        
        for i in range(int(len(self.label2)*2)):                                
            self.butt2.append(i)                                                
            if(i%2): self.butt2[i] = QPushButton("+" + self.label2[int(i/2)])   
            else:    self.butt2[i] = QPushButton("-" + self.label2[int(i/2)])   
            self.butt2[i].setMaximumWidth (50)                                  
            self.butt2[i].setMinimumHeight(25)                                  
            self.button2_Group.addButton(self.butt2[i], i+1)                    
        
        for i in range(len(self.label2)):                                       
            tab_contr2_layout.addWidget(QLabel(self.label2[i] + ":"), i+1, 0)
            tab_contr2_layout.addWidget(self.butt2[i*2],              i+1, 1)
            tab_contr2_layout.addWidget(self.butt2[i*2+1],            i+1, 2)
        
        
        self.spin3_step = QDoubleSpinBox()                                      
        self.spin3_step.setDecimals  (1)                                        
        self.spin3_step.setRange     (0,2)
        self.spin3_step.setSingleStep(0.1)
        self.spin3_step.setValue     (1.0)
        self.spin3_step.setSuffix    (' mm')
        
        self.radioLabel = ["x:", "y:", "z:", "α"]                               
        self.radio = []                                                         
        
        for i in range(len(self.radioLabel)):                                   
            self.radio.append(i)
            self.radio[i] = QRadioButton(self.radioLabel[i])
            check_axis_layout.addWidget(self.radio[i])
            
        self.radio[0].setChecked(True)                                          
        
        self.spin_dial = QDoubleSpinBox()                                       
        self.spin_dial.setRange    (-9999,9999)                                 
        self.dial = QDial() 
        self.dial.setMinimumSize   (120,120)                                    
        self.dial.setValue         (0)                                          
        self.dial.setWrapping      (True)                                       
        self.dial.setNotchesVisible(True)                                       
        self.dial.valueChanged.connect(self.dail_loop)                          
        self.dial.valueChanged.connect(self.spin_dial.setValue)                 
        
        tab_contr3_layout.addRow(QLabel("Step:"),self.spin3_step)               
        tab_contr3_layout.addRow(check_axis_layout)                
        tab_contr3_layout.addRow(self.dial)
        
        self.tab_contr1.setLayout(tab_contr1_layout)                                      
        self.tab_contr2.setLayout(tab_contr2_layout)                       
        self.tab_contr3.setLayout(tab_contr3_layout)                            
        
        self.control_tabs.addTab(self.tab_contr1,"Tab 1")                            
        self.control_tabs.addTab(self.tab_contr2,"Tab 2")                     
        self.control_tabs.addTab(self.tab_contr3,"Tab 3")
        
        self.button_home = QPushButton("Home")
        self.button_home.setMinimumHeight(20)
        self.button_home.clicked.connect(self.click_butt_home)
        self.button_home.setStyleSheet('color: black; background-color: yellow;') 
        
        self.button_home_set = QPushButton("")
        self.button_home_set.setMinimumHeight(20)
        self.button_home_set.setIcon(QIcon('settings_icon.png'))
        self.button_home_set.setIconSize(QSize(16,16))
        self.button_home_set.clicked.connect(self.click_butt_home_set)
        
        self.buttol_layout = QHBoxLayout(self)
        self.buttol_layout.addWidget(self.button_home) 
        self.buttol_layout.addWidget(self.button_home_set) 
        self.control_layoutV.addWidget(self.control_tabs)                       
        self.control_layoutV.addLayout(self.buttol_layout)
        
        self.daialValue1 = 0                                                    
        self.daialValue2 = 0                                                    
        self.home_x      = 0
        self.home_y      = 0
        self.home_z      = -100
        self.control_tabs.currentChanged.connect(self.Tabs_number)
        self.click_butt_home()

    def controlInit(self, dataInit, angle):
        self.spin1[0].setValue(dataInit[0])                                     
        self.spin1[1].setValue(dataInit[1])
        self.spin1[2].setValue(dataInit[2])
        self.spin1[3].setValue(angle)
        
    def Tabs_number(self):                                                      
        if self.control_tabs.currentIndex() == 2:
            self.button_home.hide()
            self.button_home_set.hide()
        else:
            self.button_home.show()
            self.button_home_set.show()
       
    def click_butt_home(self):                                                  
        self.spin1[0].setValue(self.home_x)                                     
        self.spin1[1].setValue(self.home_y)
        self.spin1[2].setValue(self.home_z)
        self.spin1[3].setValue(0)
        self.dataEmit()        

    def click_butt_home_set(self):                                              
        x, okPressed = QInputDialog.getDouble(self, "Home","cooordinate X:", self.home_x, -1000, 0, 2)
        if okPressed:
            self.home_x = x  
        y, okPressed = QInputDialog.getDouble(self, "Home","cooordinate Y:", self.home_y, -1000, 0, 2)
        if okPressed:
            self.home_y = y  
        z, okPressed = QInputDialog.getDouble(self, "Home","cooordinate Z:", self.home_z, -1000, 0, 2)
        if okPressed:
            self.home_z = z  

    def click_butt_save(self):                                                  
        self.dataEmit()                                                         
        
    def click_butt_xyz(self, i):                                                
        self.butt2[i-1].setAutoRepeat        (True)                             
        self.butt2[i-1].setAutoRepeatDelay   (70)                               
        self.butt2[i-1].setAutoRepeatInterval(70)                               
        if  (i == 1): self.spin1[i-1].setValue(self.spin1[i-1].value() - self.spin2_step.value())
        elif(i == 2): self.spin1[i-2].setValue(self.spin1[i-2].value() + self.spin2_step.value())
        elif(i == 3): self.spin1[i-2].setValue(self.spin1[i-2].value() - self.spin2_step.value())
        elif(i == 4): self.spin1[i-3].setValue(self.spin1[i-3].value() + self.spin2_step.value())
        elif(i == 5): self.spin1[i-3].setValue(self.spin1[i-3].value() - self.spin2_step.value())
        elif(i == 6): self.spin1[i-4].setValue(self.spin1[i-4].value() + self.spin2_step.value())
        elif(i == 7): self.spin1[i-4].setValue(self.spin1[i-4].value() - self.spin2_step.value())
        elif(i == 8): self.spin1[i-5].setValue(self.spin1[i-5].value() + self.spin2_step.value())
        
        self.dataEmit()                                                         
            
    def dail_loop(self):                                                        
        self.daialValue1 = self.spin_dial.value()  
        if self.daialValue1 > self.daialValue2:
            for i in range(len(self.radio)):
                if  (self.radio[i].isChecked()): self.spin1[i].setValue(self.spin1[i].value() + self.spin3_step.value())
        else:
            for i in range(len(self.radio)):
                if  (self.radio[i].isChecked()): self.spin1[i].setValue(self.spin1[i].value() - self.spin3_step.value())
  
        self.daialValue2 = self.daialValue1
        self.dataEmit()  
                                                               
    def dataEmit(self):
        dataSend = [self.spin1[0].value(),self.spin1[1].value(), self.spin1[2].value()]        
        self.dataControl.emit(dataSend, self.spin1[3].value(), self.spin1[4].value()) 