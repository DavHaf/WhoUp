#!/usr/bin/python3

import subprocess
import re
import serial
import time

# None means hidden
users = {
  '138' : None, # Admin
  '118' : None, # me
  '3'   : b'w', # Nick Martz
  '134'   : b'w', # Nick Martz
  '127' : b'p', # TJ
  '130' : b'p', # TJ
  '140' : b'p', # TJ
  '141' : b'p', # TJ
  '142' : b'p', # TJ
  '132' : b'g', # Troy
  '131' : b'b', # Nick Mac
  '139' : b'b', # Nick Mac
  '42' : b'b', # Nick Mac
  '133' : b'y', # Alex
  '135' : b'y', # Alex
  '112' : b'c'  # Mikey
}

connected = list()

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

connRegex = re.compile("\|client connected '.*'\(id:(\d+)\) from \d+\.\d+\.\d+\.\d+:\d+$")
discRegex = re.compile("\|client disconnected '.*'\(id:(\d+)\) reason '.*'$")

proc = subprocess.Popen(['docker', 'logs', 'ts', '-f'],stdout=subprocess.PIPE)

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
