from picamera2 import Picamera2
import os

path = os.getcwd()
path = os.path.dirname(path)

picam2 = Picamera2()
file_name=input("enter a file name for your picture: ")
picam2.start_and_capture_file("/home/rebelford/Pictures/"+file_name+".jpg")