
import threading
import sys
import time
import csv
import os
import random
import pytz
from datetime import datetime
import subprocess

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



  
def get_sensor_data():
    
    global OnSystemTime
    
    try:
        
        #trying every value so logging functionality is upheld
        dataErrors = 0
        try:
            temperature = Sensors.avgTemp()
        except Exception as e:
            temperature = f"Error: {str(e)}"
            dataErrors +=1

        try:
            pressure = Sensors.readPres()
        except Exception as e:
            pressure = f"Error: {str(e)}"
            dataErrors +=1

        try:
            humidity = Sensors.getHumid()
        except Exception as e:
            humidity = f"Error: {str(e)}"
            dataErrors +=1

        try:
            gps_coords = Gps.getLocation()
        except Exception as e:
            gps_coords = f"Error: {str(e)}"
            dataErrors +=1

        try:
            gravity = Sensors.getGravity()
        except Exception as e:
            gravity = f"Error: {str(e)}"
            dataErrors +=1

        try:
            acceleration = Sensors.getAccel()
        except Exception as e:
            acceleration = f"Error: {str(e)}"
            dataErrors +=1

        try:
            orientation = Sensors.getOrientation()
        except Exception as e:
            orientation = f"Error: {str(e)}"
            dataErrors +=1

        print(f"Completed data collection with {dataErrors} error(s)")
            
            
            
        try:
            GPSTime = Gps.getExactTime()
            if OnSystemTime:
                OnSystemTime = False
                return(None," - TIME ERROR RESOLVED, SWITCHING BACK TO PRIMARY (GPS) TIME SYSTEM")
        except Exception as e:
            if not OnSystemTime:
                print("FATAL ERROR REGARDING TIME DATA - SWITCHING TO SECONDARY SYSTEM")
            
                OnSystemTime = True
            
                return (None,f" - TIME SYSTEM ERROR; GPS LIKELY LOST. SWITCHING TO SECONDARY TIME SYSTEM (PI-TIME) UNTIL RESOLVED: {e}")
            
            else:
                GPSTime = datetime.now()
        
        #This is all to convert to UTC to PST because of GPS
        Faketz = pytz.utc
        Realtz = pytz.timezone("America/Los_Angeles")
        
        timestamp = None
        
        if isinstance(GPSTime,datetime):
            timestamp = GPSTime.strftime("%Y-%m-%d %H:%M:%S")
        else:
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
    
    global OnSystemTime
    OnSystemTime = False
    
    
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


#Beginning of program
def run():
    
    try:
        
        #set the systems time to the current GPS time
        
        truetime = Gps.getExactTime()
        
        TrueTime = datetime(truetime[0],truetime[1],truetime[2], hour = truetime[3], minute = truetime[4], second = truetime[5])
        
        Faketz = pytz.utc
        Realtz = pytz.timezone("America/Los_Angeles")
        
        FakeTime = Faketz.localize(TrueTime)
        RealTime = FakeTime.astimezone(Realtz)
        
        print(f"Current system time is: {RealTime}")
        
        
        set_string = RealTime.strftime("%Y-%m-%d %H:%M:%S")


        sudodate = subprocess.Popen(["sudo", "date", "-s", set_string])
        sudodate.communicate()
                
        

        thread1 = threading.Thread(target=RadioControlSend)
        #thread1.start()

        thread2 = threading.Thread(target=WeatherLog)
        thread2.start()
        """
        thread3 = threading.Thread(target=)
        thread4 = threading.Thread(target=)"""

    finally:
        print("-END FLIGHT-")
    
if __name__ == '__main__':
  run()