"""
freezerstate.py

Temperature sensing and alerting application to be run on a Raspberry Pi. 

Code based on ModMyPi's tutorial:
- http://www.modmypi.com/blog/ds18b20-one-wire-digital-temperature-sensor-and-the-raspberry-pi

And Tim Fernando's "temperature-serve-pi" project:
- https://github.com/timfernando/temperature-serve-pi

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
DEVICE_SUFFIX = "/w1_slave"
#WAIT_INTERNAL = 0.2

system('modprobe w1-gpio')
system('modprobe w1-therm')
    
def raw_temperature():
    f = open(find_sensor(), 'r')
    lines = f.readlines()
    f.close()
    return lines

def find_sensor():
    devices = listdir(DEVICE_FOLDER)
    devices = [device for device in devices if device.startswith('28-')]
    if devices:
        return DEVICE_FOLDER + devices[0] + DEVICE_SUFFIX
    else:
        sys.exit("Could not find temperature sensor...")

def get_temperature():
    lines = raw_temperature()
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = raw_temperature()
    output_temperature = lines[1].find('t=')
    if output_temperature != 1:
        temperature_string = lines[1].strip()[output_temperature+2]
        celsius = float(temperature_string) / 1000.0
        farenheit = celsius * 9.0 / 5.0 + 32.0
        response = {'raw', temperature_string, 
                    'celsius', celsius, 
                    'farenheit', farenheit}
        return response
    
def main():
    print ('Getting temperature...')
    
    while True:
        print(f'Time: {datetime.now()} - {get_temperature()}')
        time.sleep(1)
    return

if __name__ == "__main__":
    main()