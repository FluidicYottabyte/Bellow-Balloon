""" 
    temperature - The sensor temperature in degrees Celsius.
    acceleration - This is a 3-tuple of X, Y, Z axis accelerometer values in meters per second squared.
    magnetic - This is a 3-tuple of X, Y, Z axis magnetometer values in microteslas.
    gyro - This is a 3-tuple of X, Y, Z axis gyroscope values in degrees per second.
    euler - This is a 3-tuple of orientation Euler angle values.
    quaternion - This is a 4-tuple of orientation quaternion values.
    linear_acceleration - This is a 3-tuple of X, Y, Z linear acceleration values (i.e. without effect of gravity) in meters per second squared.
    gravity - This is a 3-tuple of X, Y, Z gravity acceleration values (i.e. without the effect of linear acceleration) in meters per second squared.
 """

#sudo pip3 install adafruit-circuitpython-bno055
import board
import busio
import adafruit_bno055

class IMU:
    def __init__(self, i2c):
        self.sensor = adafruit_bno055.BNO055_I2C(i2c)

    def Orientation(self):
        return(self.sensor.euler)
    
    