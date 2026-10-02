#!/usr/bin/env python3

import signal
import socket
import sys
from pyubx2 import UBXReader, UBX_PROTOCOL
import azarashi
import datetime
import pprint

def signal_handler(signal, frame):
    print('Terminated by CTRL/C')
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as stream:
  stream.connect(("127.0.0.1", 50012))
  ubr = UBXReader(stream, protfilter=UBX_PROTOCOL)
  for raw, msg in ubr:
    if msg.identity == 'RXM-SFRBX' and msg.gnssId == 5 and msg.sigId == 1: 
      try:
        report = azarashi.decode(raw, msg_type='ublox')
        report_params = report.get_params()
        message_type = report_params.get('message_type')
        dcx_message_type = report_params.get('dcx_message_type')
        timestamp = report_params.get('timestamp')
        doprint = False
        if message_type == 'DCR':
          doprint = True
        if message_type == 'DCX' and dcx_message_type != 'Null Message':
          doprint = True
        if doprint:
          print(timestamp.isoformat())
          print(report)
          print("")
      except Exception as e:
        # do nothing
        test = 0
        #print(f'# [{type(e).__name__}] {e}', file=sys.stderr)
