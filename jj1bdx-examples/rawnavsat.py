#!/usr/bin/env python3

import signal
import socket
import sys
from pyubx2 import UBXReader, UBX_PROTOCOL

def signal_handler(signal, frame):
    print('Terminated by CTRL/C')
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as stream:
  stream.connect(("clock-raspi.priv.k2r.org", 50012))
  ubr = UBXReader(stream, protfilter=UBX_PROTOCOL)
  for raw, msg in ubr:
    sys.stdout.buffer.write(raw)
    sys.stdout.flush()
