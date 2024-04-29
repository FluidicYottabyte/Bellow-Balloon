
import threading
import sys
sys.path.insert(0, '/home/Quincy/Bellow-Balloon')
from Communications import DataSend

Radio = DataSend.Radio()

Radio.getQueue()

"""
thread1 = threading.Thread(target=)
thread2 = threading.Thread(target=)
thread3 = threading.Thread(target=)
thread4 = threading.Thread(target=)"""

