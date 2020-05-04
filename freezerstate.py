"""
freezerstate.py

Temperature sensing and alerting application to be run on a Raspberry Pi. 

Copyright (c) 2020, Jeff Kelly
Licensed under the MIT license scheme
"""

import sys
import time
from datetime import datetime
from os import listdir, system

#from flask import Flask, jsonify
#from flask.ext.cors import CORS

DEVICE_FOLDER = "/sys/bus/w1/devices/"
DEVICE_SUFFIX = "/W1_slave"
WAIT_INTERNAL = 0.2

system('modprobe w1-gpio')
system('modprobe w1-therm')
    
def main():
    
    return

if __name__ == "__main__":
    main()