#!/usr/bin/env python3

import signal
import socket
import sys
import azarashi
import serial
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

ser = serial.Serial('/dev/cu.usbserial-11330', 115200)
azarashi.decode_stream(ser, msg_type='ublox',
                       callback=print_handler, unique=True)
