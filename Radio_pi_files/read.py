import serial
# ******************************UNCLASSIFIED******************************
#  Northrop Grumman System
#  Arduino Code for Sensor within Edge of Space Project.
#  by Tim Kan M61636
# ******************************UNCLASSIFIED******************************
arduino_port = '/dev/ttyACM0' #CHANGE the port name to what needed
baud = 9600 #i leave this
fileName = "datalogger.csv" #name of the file you are going to write to
sample = 1000             #CHANGE how big you want your sample size to be
print_label = False
  #you don't need to touch the rest
ser = serial.Serial(arduino_port,baud)
print("Attempting to connecting to Arduino with Port:  " + arduino_port)

file = open(fileName, "a")
print("creating a file")

x = 0

while x <= sample:
    if print_label:
        if x == 0:
            print('printing coloumn')
        else:
            print("line " + str(x) + ": writting. . .")
    getData=str(ser.readline())
    data=getData[0:][:-2]
    print(data)

    file = open(fileName, "a")

    file.write(data + "\n")
    x = x+1
print("data collection complete")
file.close()