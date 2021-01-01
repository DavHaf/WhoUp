#!/usr/bin/python3

import subprocess
import re

connRegex = re.compile("\|client connected '.*'\(id:(\d+)\) from \d+\.\d+\.\d+\.\d+:\d+$")
discRegex = re.compile("\|client disconnected '.*'\(id:(\d+)\) reason 'reasonmsg=.*'$")

proc = subprocess.Popen(['docker', 'logs', 'ts', '-f'],stdout=subprocess.PIPE)

connected = list()
while True:
  line = proc.stdout.readline().decode('utf-8')
  if not line:
    break
  connMatch = connRegex.search(line)
  if connMatch:
    print('add')
    id = connMatch.group(1)
    print(id)
    connected.append(id)
    print(connected)

  discMatch = discRegex.search(line)
  if discMatch:
    print('delete')
    id = discMatch.group(1)
    print(id)
    if (id in connected):
      connected.remove(id)
    print(connected)
