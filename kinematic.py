import math                 as maths
from   mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot    as plt
import numpy                as np


def forward(theta, dataConstruct):
    f, rf, re, e = float(dataConstruct[1]), float(dataConstruct[2]), float(dataConstruct[3]), float(dataConstruct[4])
    theta1, theta2, theta3 = maths.radians(theta[0]), maths.radians(theta[1]), maths.radians(theta[2])
    t = f-e
    
    # Calculate position of leg1's joint.  x1 is implicitly zero - along the axis
    y1 = -(t + rf*maths.cos(theta1))
    z1 = -rf*maths.sin(theta1)

    # Calculate leg2's joint position
    y2 = (t + rf*maths.cos(theta2))*maths.sin(maths.pi/6)
    x2 = y2*maths.tan(maths.pi/3)
    z2 = -rf*maths.sin(theta2)

    # Calculate leg3's joint position
    y3 = (t + rf*maths.cos(theta3))*maths.sin(maths.pi/6)
    x3 = -y3*maths.tan(maths.pi/3)
    z3 = -rf*maths.sin(theta3)

    # From the three positions in space, determine if there is a valid
    # location for the effector
    dnm = (y2-y1)*x3-(y3-y1)*x2

    w1 = y1*y1 + z1*z1
    w2 = x2*x2 + y2*y2 + z2*z2
    w3 = x3*x3 + y3*y3 + z3*z3

    # x = (a1*z + b1)/dnm
    a1 = (z2-z1)*(y3-y1)-(z3-z1)*(y2-y1)
    b1 = -((w2-w1)*(y3-y1)-(w3-w1)*(y2-y1))/2.0

    # y = (a2*z + b2)/dnm;
    a2 = -(z2-z1)*x3+(z3-z1)*x2
    b2 = ((w2-w1)*x3 - (w3-w1)*x2)/2.0

    # a*z^2 + b*z + c = 0
    a = a1*a1 + a2*a2 + dnm*dnm
    b = 2*(a1*b1 + a2*(b2-y1*dnm) - z1*dnm*dnm)
    c = (b2-y1*dnm)*(b2-y1*dnm) + b1*b1 + dnm*dnm*(z1*z1 - re*re)
 
    # discriminant
    d = b*b - 4.0*a*c
    if d < 0:
        return None # non-existing point

    z0 = -0.5*(b+maths.sqrt(d))/a
    x0 = (a1*z0 + b1)/dnm
    y0 = (a2*z0 + b2)/dnm
    xyz = [x0,y0,z0]
    
    return (xyz)
    
# Helper functions, calculates angle theta1 (for YZ-pane)
def angle_yz(x0, y0, z0, f, rf, re, e, theta=None):
    y1 = -f
    y0 -= e
    a = (x0*x0 + y0*y0 + z0*z0 + rf*rf - re*re - y1*y1)/(2*z0)
    b = (y1-y0)/z0
    d = -(a + b*y1)*(a + b*y1) + rf*(b*b*rf + rf)
    if d < 0:
        return [1,0] # non-existing povar.  return error, theta
    yj = (y1 - a*b - maths.sqrt(d))/(b*b + 1)
    zj = a + b*yj
    theta = 180.0*maths.atan(-zj/(y1-yj))/maths.pi
    if yj>y1:
        theta += 180.0
    
    return [0,theta] # return error, theta

def inverse(xyz, dataConstruct):
    f, rf, re, e = float(dataConstruct[1]), float(dataConstruct[2]), float(dataConstruct[3]), float(dataConstruct[4])

    x0,y0,z0 = xyz[0], xyz[1], xyz[2]
    theta1, theta2, theta3 = 0, 0, 0
    
    status = angle_yz(x0,y0,z0, f, rf, re, e)

    cos120 = maths.cos(2.0*maths.pi/3.0)
    sin120 = maths.sin(2.0*maths.pi/3.0)
    
    if status[0] == 0:
        theta1 = status[1]
        status = angle_yz(x0*cos120 + y0*sin120, y0*cos120-x0*sin120, z0, f, rf, re, e, theta2)
    if status[0] == 0:
        theta2 = status[1] 
        status = angle_yz(x0*cos120 - y0*sin120, y0*cos120+x0*sin120, z0, f, rf, re, e, theta3)
    theta3 = status[1]
    theta  = [theta1,theta2,theta3]
    
    return [status[0], theta]
    

def workspace(construct):
    
    dataConstruct = [0, construct[0], construct[1], construct[2], construct[3], construct[4]]

    step     = 10
    minServo = -1
    maxServo = 100
    
    points = []
    for t1 in range(minServo, maxServo, step):
        for t2 in range(minServo, maxServo, step):
            for t3 in range(minServo, maxServo, step):
                servos = (t1, t2, t3)
                xyz = forward(servos, dataConstruct)
                if xyz != None:
                    points.append(xyz)
                    status, there_and_back = inverse(xyz, construct)
                    there_and_back2 = there_and_back[0], there_and_back[1], there_and_back[2]
                    err = map(lambda a,b: abs(a-b), servos, there_and_back2)
                    if max(err) > 0.0000000000001:
                        a=0

    fig = plt.figure(figsize=(6.5,3.8), num='Workspace')
    ax = fig.add_subplot(1,1,1, projection='3d')
    ax.set_zlim3d(-construct[4]*1.1,0)
    ax.set_xlabel('$X$')
    ax.set_ylabel('$Y$')
    ax.set_zlabel('$Z$')
    
    surf = ax.scatter(xs=[x for x,y,z in points] ,ys=[y for x,y,z in points],zs=[z for x,y,z in points])
    plt.show()
    