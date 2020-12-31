#!/usr/bin/python3

import subprocess
import re

connRegex = re.compile("\|client connected '.*'\(id:(\d+)\) from \d+\.\d+\.\d+\.\d+:\d+$")
discRegex = re.compile("\|client disconnected '.*'\(id:(\d+)\) from \d+\.\d+\.\d+\.\d+:\d+$")

proc = subprocess.Popen(['docker','logs', 'ts', '-f'],stdout=subprocess.PIPE)
while True:
  line = proc.stdout.readline().decode('utf-8')
  if not line:
    break
  match = connRegex.search(line)
  if match:
      print(match.group(1))