
import threading
import sys
import time
import csv
import os
import random
import pytz
from datetime import datetime

path = os.getcwd()
path = os.path.dirname(path)
sys.path.insert(0, path)

print(path)

from Communications import DataSend
from SensorTesting import MultiplexorWithSensors
from SensorTesting import GPS as GPSHold

Gps = GPSHold.GPSUnit("/dev/ttyS0")
Sensors = MultiplexorWithSensors.Multiplexor()
Radio = DataSend.Radio(True)

Radio.getQueue()
Radio.addQueue(1,"FOCUK YOU")


        
def get_sensor_data():
    try:
        temperature = Sensors.avgTemp()
        pressure = Sensors.readPres()
        humidity = Sensors.getHumid()
        gps_coords = Gps.getLocation()
        gravity = Sensors.getGravity()
        acceleration = Sensors.getAccel()
        orientation = Sensors.getOrientation()
        
        GPSTime = Gps.getExactTime()
        
        #This is all to convert to UTC to PST because of GPS
        Faketz = pytz.utc
        Realtz = pytz.timezone("America/Los_Angeles")
        
        TrueTime = datetime(GPSTime[0],GPSTime[1],GPSTime[2], hour = GPSTime[3], minute = GPSTime[4], second = GPSTime[5])
        FakeTime = Faketz.localize(TrueTime)
        RealTime = FakeTime.astimezone(Realtz)
        
        timestamp = RealTime.strftime("%Y-%m-%d %H:%M:%S")
        
        return timestamp, temperature, pressure, humidity, gps_coords, gravity, acceleration, orientation
    except Exception as e:
        print(f"Error reading sensor data: {e}")
        return (None,e)



"""
Thread 1
"""
def RadioControlSend():
    print("Radio control thread initialized")
    move = True
    while move:
        input("Press enter to send test packet.")
        Radio.send()
        print("Packet sent.")




"""
Thread 2
"""
def WeatherLog():
    
    # Directory to store data files
    data_dir = "Log"
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)

    # File rotation parameters
    max_file_size = 5 * 1024 * 1024  # 5 MB
    file_prefix = "weather_data"
    file_extension = ".csv"
    
    # Get the current data file path
    def get_current_file_path():
        timestamp = get_sensor_data()[0]
        return os.path.join(data_dir, f"{file_prefix}_{timestamp}{file_extension}")

    # Function to write data to file with error correction
    def write_data_to_file(file_path, data):
        try:
            with open(file_path, mode='a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(data)
        except IOError as e:
            print(f"File I/O error: {e}")

    # Function to rotate files based on size
    def rotate_file(file_path):
        if os.path.exists(file_path) and os.path.getsize(file_path) >= max_file_size:
            return get_current_file_path()
        return file_path

    # Initialize the first file and write headers
    global current_file_path
    current_file_path = get_current_file_path()
    with open(current_file_path, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Timestamp", "Temperature (C)", "Pressure (hPa)", "Humidity (%)", "(Latitude, Longitude, Altitude (m))","Gravity Vector (m/s^2 , xyz)","Acceleration w/o-grav. Vector (m/s^2 , xyz)","Orientation (Euler angles, xyz)"])

    # Function to log data with rotation and error correction
    def log_data():
        global current_file_path
        data = get_sensor_data()
        print(data)
        if data[0] == None:
            write_data_to_file(current_file_path, [f"ERROR: {data[1]}"])
            current_file_path = rotate_file(current_file_path)
        else:
            write_data_to_file(current_file_path, data)
            current_file_path = rotate_file(current_file_path)
            
    while True:
        log_data()
        time.sleep(1)

thread1 = threading.Thread(target=RadioControlSend)
#thread1.start()

thread2 = threading.Thread(target=WeatherLog)
thread2.start()
"""
thread3 = threading.Thread(target=)
thread4 = threading.Thread(target=)"""

