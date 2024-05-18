
import threading
import sys
import time
import os

path = os.getcwd()
sys.path.insert(0, path)

print(path)

from Communications import DataSend

Radio = DataSend.Radio()

def RadioReceive():
    print("Radio control thread initialized")
    move = True
    while move:
        print("Acting radio...")
        success = Radio.receive
        print(success)


thread1 = threading.Thread(target=RadioReceive)
thread1.start()

"""
thread2 = threading.Thread(target=)
thread3 = threading.Thread(target=)
thread4 = threading.Thread(target=)"""

