import serial
from time import strftime, gmtime
import time
import subprocess
# ******************************UNCLASSIFIED******************************
#  Northrop Grumman System
#  Arduino Code for Sensor within Edge of Space Project.
#  by Tim Kan M61636 and Deshawn Brown J57507
# ******************************UNCLASSIFIED******************************


time_stamp = strftime('%Y-%m-%d-%H_%M_%S', gmtime())
arduino_port0 = '/dev/ttyACM0' # Port for the first Teensy
baud = 9600 #i leave this
fileName = "/home/pi/Edge-of-Space-2021/datalogger_ACM0_" + time_stamp + ".csv" #name of the file you are going to write to

print_label = False
#you don't need to touch the rest
result = None
while result is None:
    try:
        result = serial.Serial(arduino_port0, baud)
    except:
        pass
    

ser_0 = serial.Serial(arduino_port0, baud)
print("Attempting to connect to Arduino with Port:  " + arduino_port0)

with open(fileName, "a") as file_0:
    # Print headers
    file_0.write("TimeStamp,TVOC,eCO2,H2,Ethanol,Temperature,Pressure,Altitude,Humidity,X_Ori,Y_Ori,Z_Ori")

while True:

    getData=str(ser_0.readline())
    data=getData[0:][:-2]
    print(data)
    
    with open(fileName, "a") as file_0:
        time_stamp = strftime('%Y-%m-%d-%H_%M_%S', gmtime())
        file_0.write(time_stamp + "," + data + "\n")
        
