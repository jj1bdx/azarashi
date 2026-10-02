#!/usr/bin/env python3

import signal
import socket
import sys
from pyubx2 import UBXReader, UBX_PROTOCOL
from pyubx2.ubxhelpers import itow2utc
import curses

def signal_handler(signal, frame):
    print('Terminated by CTRL/C')
    curses.endwin()
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

stdscr = curses.initscr()
curses.curs_set(0)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as stream:
  stream.connect(("127.0.0.1", 50012))
  ubr = UBXReader(stream, protfilter=UBX_PROTOCOL)
  for raw, msg in ubr:
    if msg.identity == 'NAV-SAT':
      stdscr.clear()
      svIdList = []
      cnoList = []
      elevList = []
      azimList = []
      svUsedList = []
#      print(msg)
      utc = itow2utc(msg.iTOW)
      for i in range(msg.numSvs):
        gnssId = getattr(msg, f"gnssId_{i+1:02d}")
        if gnssId == 5: # QZSS
          svId = getattr(msg, f"svId_{i+1:02d}")
          svIdList.append(svId)
          cno = getattr(msg, f"cno_{i+1:02d}")
          cnoList.append(cno)
          elev = getattr(msg, f"elev_{i+1:02d}")
          elevList.append(elev)
          azim = getattr(msg, f"azim_{i+1:02d}")
          azimList.append(azim)
          svUsed = getattr(msg, f"svUsed_{i+1:02d}")
          svUsedList.append(svUsed)
      stdscr.addstr(0, 0, 'QZSS List at UTC: {0:02d}:{1:02d}:{2:02d}.{3:01d}'.format(utc.hour, utc.minute, utc.second, int(utc.microsecond/100000)))
      usedSats = 0
      for j in range(len(svIdList)):
        if svUsedList[j] == 1:
          beingUsed = "Y"
          usedSats = usedSats + 1
        else:
          beingUsed = "N"
        stdscr.addstr(j + 2, 0, '{}'.format(beingUsed))
        stdscr.addstr(j + 2, 2, 'svId={}'.format(svIdList[j]))
        stdscr.addstr(j + 2, 12, 'cno={}dB'.format(cnoList[j]))
        stdscr.addstr(j + 2, 22, 'elev={}'.format(elevList[j]))
        stdscr.addstr(j + 2, 32, 'azim={}'.format(azimList[j]))
      stdscr.addstr(1, 0, 'Satellites used: {}'.format(usedSats))
      stdscr.refresh()
