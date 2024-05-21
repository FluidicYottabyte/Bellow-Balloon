
import threading
import sys
import time
import os

path = os.getcwd()
path = os.path.dirname(path)
sys.path.insert(0, path)

print(path)

from Communications import DataSend

Radio = DataSend.Radio(True)

Radio.getQueue()
Radio.addQueue(1,"ABCDEFGHIJKLMNOPQRSTUVWXYZ")

def RadioControlSend():
    print("Radio control thread initialized")
    move = True
    while move:
        Radio.send()

thread1 = threading.Thread(target=RadioControlSend)
thread1.start()

"""
thread2 = threading.Thread(target=)
thread3 = threading.Thread(target=)
thread4 = threading.Thread(target=)"""

