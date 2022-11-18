from inputs import get_gamepad
import math
import rclpy
import rclpy.node
from rclpy.parameter import Parameter



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
class MinimalParam(rclpy.node.Node):
    
    def __init__(self):
        super().__init__('digit_qp')
        self.timer = self.create_timer(0.001, self.timer_callback)
        self.declare_parameter("SWBCP.des_ori")
        self.ti = 0.0
        self.roll  = 0.0
        self.pitch = 0.0
        self.yaw = 0.0
        self.a = 0.0
        self.b = 0.0
        self.c = 0.0
        self.d = 0.0
        
    def timer_callback(self):
        events = get_gamepad()
        for event in events:
            # print(event.code, event.state)
            if(event.code == 'ABS_RZ'):
                self.ti = event.state
                self.ti = round(100 - self.ti*100/255, 2)
                
            elif(event.code == 'ABS_X'):
                self.roll  = event.state
                self.roll  = -scaling(self.roll, 0, 255, 15)
                self.roll  = deg2rad(self.roll)
            
            elif(event.code == 'ABS_Y'):
                self.pitch = event.state
                self.pitch = -scaling(self.pitch, 0, 255, 15)
                self.pitch = deg2rad(self.pitch)
        
            elif(event.code == 'ABS_Z'): #error 3
                self.yaw = event.state
                self.yaw = -scaling(self.yaw, 0, 255, 15)
                self.yaw = deg2rad(self.yaw)
        
        print('w = ', self.a,'x = ', self.b,'y = ', self.c, 'z = ', self.d)        
        self.a, self.b, self.c, self.d = quaternion(self.yaw, self.pitch, self.roll)
        param_ori = Parameter('SWBCP.des_ori', Parameter.Type.DOUBLE_ARRAY, [self.a, self.b, self.c, self.d])
        self.set_parameters([param_ori])

def main():
    rclpy.init()
    node = MinimalParam()
    rclpy.spin(node)

if __name__ == '__main__':
    main()
    
    
    # SWBCP.des_ori