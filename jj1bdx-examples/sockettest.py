#!/usr/bin/env python3

import signal
import socket
import sys
import azarashi
import pprint

def signal_handler(signal, frame):
    print('Terminated by CTRL/C')
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

def print_handler(report):
    report_params = report.get_params()
    timestamp = report_params.get('timestamp')
    print(timestamp.isoformat())
    print("---")
    print(report)
    print(" ")

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as stream:
  stream.connect(("127.0.0.1", 50012))
  with stream.makefile('rb') as source:
    azarashi.decode_stream(
      source,
      msg_type='ublox',
      callback=print_handler,
      unique=True,
      ignore_dcx=False,
    )
