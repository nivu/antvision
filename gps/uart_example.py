#!/usr/bin/python3

import time
import serial
import pynmea2
import datetime
import pandas
import datetime
import csv


print("UART Demonstration Program")
print("NVIDIA Jetson Nano Developer Kit")

date_now = datetime.datetime.now()
file_name = "GPS_log_" + date_now.strftime("%d%m%Y_%H%H%S")

file = open(file_name, "a", newline="")

header =["date", "lon" , "lat", "time"]

with file:
     writer = csv.writer(file)
     writer.writerow(header)

serial_port = serial.Serial(
    port="/dev/ttyTHS1",
    baudrate=9600,
    bytesize=serial.EIGHTBITS,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
)
# Wait a second to let the port initialize
time.sleep(1)

try:
    # Send a simple header
    serial_port.write("UART Demonstration Program\r\n".encode())
    serial_port.write("NVIDIA Jetson Nano Developer Kit\r\n".encode())

    while True:
        if serial_port.inWaiting() > 0:
            data = serial_port.readline()
            serial_port.write(data)
            #print(data)
            data = data.decode("utf-8")
            if data[0:6] == "$GPRMC":
                #print("mc found")
                newmsg=pynmea2.parse(data)
                lat=newmsg.latitude
                lng=newmsg.longitude
                time = newmsg.timestamp
                gps = "Latitude=" + str(lat) + " and Longitude=" + str(lng)
                #print(gps)
                print(newmsg.timestamp)
                #t1 = datetime.datetime.strptime(str(newmsg.timestamp), "%H:%M:%S")
                #date_now = datetime.datetime.now()
                #print("timediff", date_now - t1)
                data = [date_now, str(lng), str(lat), str(time)]
                file = open(file_name, "a", newline="")
                with file:
                  writer = csv.writer(file)
                  writer.writerow(data)
                file.close()
     
            if data == "\r".encode():
                # For Windows boxen on the other end
                serial_port.write("\n".encode())


except KeyboardInterrupt:
    print("Exiting Program")

except Exception as exception_error:
    print("Error occurred. Exiting Program")
    print("Error: " + str(exception_error))

finally:
    serial_port.close()
    pass
