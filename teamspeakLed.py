#!/usr/bin/python3

import subprocess
import re
import serial
import time


connected = list()

def makeUsersList():
    users = {}
    file = open("ts_names.txt", "r")
    for line in file:
        values = line.split()
        if len(values) >= 2 and values[0] != '#':
            ledValue = None
            # Get the LED value and convert it to a byte
            if values[1] != 'x':
                ledValue = bytes(values[1], 'ascii')
            users[values[0]] = ledValue
    return users

def updateLed():
  ser.write(b'-')
  print(connected)
  for id in connected:
    #if known
    if id in users:
      # if the user is not hidden
      if users[id]:
        ser.write(users[id])
    # write magenta for unknown users
    else:
      ser.write(b'm')


ser = serial.Serial('/dev/ttyACM0')
ser.close()
ser.open()
# Wait and clear
time.sleep(3)
ser.write(b'-')

users = makeUsersList()

connRegex = re.compile("\|client connected '.*'\(id:(\d+)\) from \d+\.\d+\.\d+\.\d+:\d+$")
discRegex = re.compile("\|client disconnected '.*'\(id:(\d+)\) reason '.*'$")

proc = subprocess.Popen(['docker', 'logs', 'ts', '--follow', '--tail', '15'],stdout=subprocess.PIPE)

while True:
  line = proc.stdout.readline().decode('utf-8')
  if not line:
    break
  connMatch = connRegex.search(line)
  if connMatch:
    new_id = connMatch.group(1)
    connected.append(new_id)
    updateLed()


  discMatch = discRegex.search(line)
  if discMatch:
    new_id = discMatch.group(1)
    if (new_id in connected):
      connected.remove(new_id)
    updateLed()
