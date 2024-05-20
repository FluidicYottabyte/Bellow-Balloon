
import threading
import sys
import time
import os


import signal

default_handler = None



path = os.getcwd()
path = os.path.dirname(path)
sys.path.insert(0, path)

print(path)

from Communications import DataSend

Radio = DataSend.Radio()



def RadioReceive():
    print("Radio control thread initialized")
    move = True
    while move:
        print("Acting radio...")
        success = Radio.receive()
        print(success)


thread1 = threading.Thread(target=RadioReceive)
thread1.start()

def handler(num, frame):    
    # Do something that cannot throw here (important)
    thread1.join()

    return default_handler(num, frame) 

if __name__ == "__main__":
    default_handler = signal.getsignal(signal.SIGINT)

    # Assign the new handler
    signal.signal(signal.SIGINT, handler)

"""
thread2 = threading.Thread(target=)
thread3 = threading.Thread(target=)
thread4 = threading.Thread(target=)"""

