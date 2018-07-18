#!/usr/bin/env python
import time
import serial
import re
from pythonosc import osc_message_builder
from pythonosc import udp_client

serialport = '/dev/tty.usbmodem1422' # mac
#serialport = '/dev/ttyACM0' # Linux
ip = '192.168.240.39' # IP address of dmx servers
port = 9000 # port of dmx servers

ser = serial.Serial(
 port = serialPort, 
 baudrate = 115200,
 parity=serial.PARITY_NONE,
 stopbits=serial.STOPBITS_ONE,
 bytesize=serial.EIGHTBITS,
 timeout=1
)
counter=0

client = udp_client.SimpleUDPClient(ip, port)

r = 0
g = 0
b = 0

while 1:
 x=str(ser.readline()) # read data from microbit
 '''The way the microbit formats the data over serial
 can be kind of messy. The next few calls to string replace
 are to clear up extra spaces, newlines, etc.'''
 x=x.replace(" ", "")
 x=x.replace("'", "")
 x=x.replace("b", "")
 x=x.replace("\\r\\n", "")
 '''With the microbit program included in this example the data
 (after cleaning it up) looks like:
 light1:#,#,#
 with the numbers obviously being actual integers.
 Next we will split up this string to access the 3 numbers
 before we send them to the dmx server via OSC.''' 
 if "light1" in x:
   data = x.split(":")
   colors = data[1]
   colors = colors.split(",")
   r = int(colors[0])
   g = int(colors[1])
   b = int(colors[2])
   print(r, g, b)
   client.send_message("/light1", [r, g, b])

 