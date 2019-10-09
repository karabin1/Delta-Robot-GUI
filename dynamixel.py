from   dynamixel_sdk     import *                     # Uses Dynamixel SDK library

def getPoseInit():
    for i in range(len(dxl_id)):            
        dxl_present_position[i], dxl_comm_result, dxl_error = packetHandler.read2ByteTxRx(portHandler, dxl_id[i], ADDR_PRESENT_POSITION)
        check_error(dxl_comm_result, dxl_error)
        presentPosAngle[i] = dxl_present_position[i] / 3.41333333 - 150
    return presentPosAngle

def check_error(comm_result, error):
    if comm_result != COMM_SUCCESS: print("%s" % packetHandler.getTxRxResult(comm_result))
    elif error != 0:                print("%s" % packetHandler.getRxPacketError(error))

def run_dynamixel(dxl_moving_speed_all, dxl_goal_angle):
    errorTresch = 0
    
    for i in range(len(dxl_id)):
        dxl_goal_position[i] = int((dxl_goal_angle[i] + 150) * 3.41333333) 
        dxl_present_position[i], dxl_comm_result, dxl_error = packetHandler.read2ByteTxRx(portHandler, dxl_id[i], ADDR_PRESENT_POSITION)
        check_error(dxl_comm_result, dxl_error)
        abs_position[i] = abs(dxl_goal_position[i] - dxl_present_position[i])
    
    max_abs = max(abs_position)  

    while True:
        for i in range(len(dxl_id)):               
        # Write moving speed
            dxl_moving_speed[i] = int (dxl_moving_speed_all / ((max_abs+0.0001)/(abs_position[i]+0.0001))) 
            #print(dxl_moving_speed)
            dxl_comm_result, dxl_error = packetHandler.write2ByteTxRx(portHandler, dxl_id[i], ADDR_MOVING_SPEED, dxl_moving_speed[i])
            check_error(dxl_comm_result, dxl_error)
        # Write goal position
            dxl_comm_result, dxl_error = packetHandler.write2ByteTxRx(portHandler, dxl_id[i], ADDR_GOAL_POSITION, dxl_goal_position[i])
            check_error(dxl_comm_result, dxl_error)
                
        for i in range(len(dxl_id)):            
        # Read present position
            dxl_present_position[i], dxl_comm_result, dxl_error = packetHandler.read2ByteTxRx(portHandler, dxl_id[i], ADDR_PRESENT_POSITION)
            check_error(dxl_comm_result, dxl_error)
            #print("[ID:%03d] GoalPos:%03d  PresPos:%03d" % (dxl_id[i], dxl_goal_position[i], dxl_present_position[i]))
        
        for i in range(len(dxl_id)):   
            if not abs(dxl_goal_position[i] - dxl_present_position[i]) > DXL_MOVING_STATUS_THRESHOLD:
                end[i] = 1
            else:
                end[i] = 0
                errorTresch += 1
                
        if (end[0] == 1 and end[1] == 1 and end[2] == 1 or errorTresch > 5):
            break    
        
    for i in range(len(dxl_id)):            
        presentPosAngle[i] = dxl_present_position[i] / 3.41333333 - 150
            
    return presentPosAngle
    
def torque(state):
    for i in range(len(dxl_id)):                
    # Enable Dynamixel Torque
        dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(portHandler, dxl_id[i], ADDR_TORQUE_ENABLE, state)
        check_error(dxl_comm_result, dxl_error)
        if (dxl_comm_result == COMM_SUCCESS and dxl_error == 0):
            print("Dynamixel has been successfully connected")
        else:
            a = 10/0

def init():
    global portHandler
    # Open port
    try:
        portHandler = PortHandler('/dev/ttyACM0')
        portHandler.openPort()
        print("Succeeded to open the port")
    except:
        try:
            portHandler = PortHandler('/dev/ttyACM1')
            portHandler.openPort()
            print("Succeeded to open the port")
        except:
            try:
                portHandler = PortHandler('/dev/ttyACM2')
                portHandler.openPort()
                print("Succeeded to open the port")
            except:
                try:
                    portHandler = PortHandler('/dev/ttyACM3')
                    portHandler.openPort()
                    print("Succeeded to open the port")
                except: 
                    try:
                        portHandler = PortHandler('/dev/ttyACM4')
                        portHandler.openPort()
                        print("Succeeded to open the port")
                    except:
                        pass
                        print("Failed to open the port")
                        quit()
    
    # Set port baudrate
    if portHandler.setBaudRate(BAUDRATE):
        print("Succeeded to change the baudrate")
    else:
        print("Failed to change the baudrate")
        quit()
 
def close():
    torque(0)
    portHandler.closePort()
    
# Control table address
ADDR_TORQUE_ENABLE          = 24                # Control table address is different in Dynamixel model
ADDR_MOVING_SPEED           = 32
ADDR_GOAL_POSITION          = 30
ADDR_PRESENT_POSITION       = 36

# Default setting
BAUDRATE                    = 1000000           # Dynamixel default baudrate : 57600
#DEVICENAME                  = '/dev/ttyACM0'    # Check which port is being used on your controller
DXL_MOVING_STATUS_THRESHOLD = 4                 # Dynamixel moving status threshold

dxl_id                      = [1, 2, 3, 4]
dxl_moving_speed            = [0, 0, 0, 0]
dxl_present_position        = [0, 0, 0, 0]
dxl_goal_position           = [0, 0, 0, 0]
abs_position                = [0, 0, 0, 0]
end                         = [0, 0, 0, 0]
presentPosAngle             = [0, 0, 0, 0]

#portHandler                 = PortHandler(DEVICENAME)   # Initialize PortHandler instance. Set the port path. Get methods and members of PortHandlerLinux or PortHandlerWindows
packetHandler               = PacketHandler(1)          # Initialize PacketHandler instance. Set the protocol version. Get methods and members of Protocol1PacketHandler or Protocol2PacketHandler