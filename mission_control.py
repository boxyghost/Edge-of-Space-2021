"""
@breif Software for visualizing flight data collected from the Edge of Space payload

@author Brynn Charity <------ (Please add your name here if you work on this file!)
@python version 3.8.10
@date 7/9/21
@bugs None yet!

@TODO read in csv data files, display sensor data in charts, create 3D representation of flight data, display video

"""
import matplotlib.pyplot as plt
import numpy as np
import csv

def object gps:


 
def main():

    latitude = []
    longitude = []
    altitude = []


    # The file will be read differently later since we'll have a differnet format.
    with open("Test_Data/gps_data.csv") as csvfile:
        data = csv.reader(csvfile, delimiter= ",")
        for row in data:
            latitude.append(float(row[1]))
            longitude.append(float(row[3]))

    with open("Test_Data/coolterm_data.csv") as csvfile:
        data = csv.reader(csvfile,delimiter= ",")
        for row in data:
            altitude.append(float(row[12]))

    for i in range(len(latitude)):
        x = str(latitude[i])
        y = str(longitude[i])
        z = str(altitude[i])
        print("x: " + x+ ", y: " + y + ", z: " + z)


if __name__ == "__main__":
    main()

