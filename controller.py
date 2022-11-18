from inputs import get_gamepad
from rclpy.parameter import Parameter
import math
ti = 0
roll = 0
pitch = 0
yaw = 0

def quaternion(yaw, pitch, roll):
    c1 = math.cos(yaw/2)
    s1 = math.sin(yaw/2)
    c2 = math.cos(pitch/2)
    s2 = math.sin(pitch/2)
    c3 = math.cos(roll/2)
    s3 = math.sin(roll/2)
    c1c2 = c1*c2
    s1s2 = s1*s2
    w = round(c1c2*c3 - s1s2*s3, 2)
    x = round(c1c2*s3 + s1s2*c3, 2)
    y = round(s1*c2*c3 + c1*s2*s3, 2)
    z = round(c1*s2*c3 - s1*c2*s3, 2)
    return w, x, y, z
    
def scaling(val, lbi, ubi, ebf):
    val = (val/((ubi-lbi)*0.5) - 1)*ebf
    return round(val,2)

def deg2rad(val):
    return round(val*math.pi/180, 2)

while(1):
    events = get_gamepad()
    for event in events:
        # print(event.code, event.state)
        if(event.code == 'ABS_RZ'):
            ti = event.state
            ti = round(100 - ti*100/255, 2)
            
        elif(event.code == 'ABS_X'):
            roll = event.state
            roll = -scaling(roll, 0, 255, 15)
            roll = deg2rad(roll)
        
        elif(event.code == 'ABS_Y'):
            pitch = event.state
            pitch = -scaling(pitch, 0, 255, 15)
            pitch = deg2rad(pitch)
    
        elif(event.code == 'ABS_Z'): #error 3
            yaw = event.state
            yaw = -scaling(yaw, 0, 255, 15)
            yaw = deg2rad(yaw)
            
    a, b, c, d = quaternion(yaw, pitch, roll)
    # print(roll, pitch, yaw)
    # print('Throttle Input = ', ti,'Roll Input = ', roll,'Pitch Input = ', pitch, 'Yaw Input = ', yaw)
    print('w = ', a,'x = ', b,'y = ', c, 'z = ', d)
    
    # param_ori = Parameter('SWBCP.des_ori', Parameter.Type.DOUBLE_ARRAY [a, b, c, d])
    
    