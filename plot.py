import math
from PyQt5.QtWidgets import QSizePolicy
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
        
class Plot(FigureCanvas):
        
    def __init__(self, parent=None):

        parent.send_plotConst.connect(self.get_construct)        
        parent.send_plotXYZtheta.connect(self.xyz_tetha)
        
        fig = Figure(figsize=(20, 15), dpi=80)
        #self.axes = fig.add_subplot(111)
    
        FigureCanvas.__init__(self, fig)
        self.setParent(parent)
 
        FigureCanvas.setSizePolicy(self,
                QSizePolicy.Expanding,
                QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)
        
        self.ax = self.figure.gca(projection='3d')
        #self.plot()

    def xyz_tetha(self, xyz, theta):
        self.x = float(xyz[0])
        self.y = float(xyz[1])
        self.z = float(xyz[2])
        self.theta1 = float(theta[0])
        self.theta2 = float(theta[1])
        self.theta3 = float(theta[2])
        self.plot()
         
    def get_construct(self, constructData):
        self.f  = float(constructData[1])
        self.rf = float(constructData[2])
        self.e  = float(constructData[4])
        self.b  = float(constructData[5])  
        
    def plot(self):
        self.ax.clear()
                
        f_x = -(math.sin(60.0 * math.pi / 180.0) * self.f)   # obrót podstawy dla osi x        
        f_y = -(math.cos(60.0 * math.pi / 180.0) * self.f)   # obrót podstawy dla osi y

        e_x = -(math.sin(60.0 * math.pi / 180.0) * self.e)   # obrót podstawy dla osi x        
        e_y = -(math.cos(60.0 * math.pi / 180.0) * self.e)   # obrót podstawy dla osi y
        
        radian1 = self.theta1 * math.pi / 180                #
        r1_x =   math.cos(radian1) * self.rf                 #
        r1_z = -(math.sin(radian1) * self.rf)                #
        
        radian2 = self.theta2 * math.pi / 180
        r2_xy =  math.cos(radian2) * self.rf
        r2_x = -(math.cos(30 * math.pi / 180) * r2_xy)
        r2_y = -(math.cos(60 * math.pi / 180) * r2_xy)
        r2_z = -(math.sin(radian2) * self.rf)
        
        radian3 = self.theta3 * math.pi / 180
        r3_xy =  math.cos(radian3) * self.rf
        r3_x =  (math.cos(30 * math.pi / 180) * r3_xy)
        r3_y = -(math.cos(60 * math.pi / 180) * r3_xy)
        r3_z = -(math.sin(radian3) * self.rf)

        tbx = [      0, -f_x,  f_x,       0]
        tby = [-self.f, -f_y, -f_y, -self.f]
        tbz = [      0,    0,    0,       0]      

        dbx = [         self.x, self.x - e_x, self.x + e_x,          self.x]
        dby = [self.y - self.e, self.y - e_y, self.y - e_y, self.y - self.e]
        dbz = [         self.z,       self.z,       self.z,          self.z]   
        
        r1x = [     0,                 0,          self.x]
        r1y = [-self.f, -(r1_x + self.f), self.y - self.e]
        r1z = [     0,              r1_z,          self.z]  

        r2x = [-f_x, -r2_x - f_x, self.x - e_x]
        r2y = [-f_y, -r2_y - f_y, self.y - e_y]
        r2z = [     0,      r2_z,       self.z]  

        r3x = [ f_x, -r3_x + f_x, self.x + e_x]
        r3y = [-f_y, -r3_y - f_y, self.y - e_y] 
        r3z = [      0,     r3_z,       self.z]  

        efx = [self.x, self.x]
        efy = [self.y, self.y]
        efz = [self.z, self.z - 20] 

        scale = 3        
        groundx = [self.f*scale, self.f*scale, -self.f*scale, -self.f*scale, self.f*scale]
        groundy = [-self.f*scale, self.f*scale, self.f*scale, -self.f*scale, -self.f*scale]
        groundz = [-self.b, -self.b, -self.b, -self.b, -self.b] 
        
        tbase = [] 
        tbase.append(list(zip(tbx, tby, tbz))) 
        poly3dCollection = Poly3DCollection(tbase, facecolors='b', linewidths=1, alpha=0.5)
        self.ax.add_collection3d(poly3dCollection)   

        dbase = [] 
        dbase.append(list(zip(dbx, dby, dbz))) 
        poly3dCollection = Poly3DCollection(dbase, facecolors='b', linewidths=1, alpha=0.5)
        self.ax.add_collection3d(poly3dCollection)  
        
        self.ax.plot3D(groundx, groundy, groundz, 'gray')
        
        self.ax.plot3D(tbx, tby, tbz, 'blue')
        self.ax.plot3D(dbx, dby, dbz, 'blue')
        self.ax.plot3D(r1x, r1y, r1z, 'red')
        self.ax.plot3D(r2x, r2y, r2z, 'red')
        self.ax.plot3D(r3x, r3y, r3z, 'red')
        self.ax.plot3D(efx, efy, efz, 'red')        
       
        self.ax.scatter(tbx, tby, tbz, c='r', marker='o')
        self.ax.scatter(dbx, dby, dbz, c='r', marker='o')
        self.ax.scatter(r1x, r1y, r1z, c='r', marker='o')
        self.ax.scatter(r2x, r2y, r2z, c='r', marker='o')
        self.ax.scatter(r3x, r3y, r3z, c='r', marker='o')
        self.ax.scatter(efx, efy, efz, c='r', marker='o') 
        
        self.ax.set_xlim3d(-self.f*scale,self.f*scale)
        self.ax.set_ylim3d(-self.f*scale,self.f*scale)
        self.ax.set_zlim3d(-self.b,0)
        
        self.ax.set_xlabel('$X$')
        self.ax.set_ylabel('$Y$')
        self.ax.set_zlabel('$Z$')

        self.draw()
