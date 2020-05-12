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

import os
import sys
import time
import threading
from datetime import datetime
from os import listdir, system
from flask import Flask, jsonify, render_template

import freezerstate.config
import argparse

#from flask import Flask, jsonify
#from flask.ext.cors import CORS

#WAIT_INTERNAL = 0.2

system('modprobe w1-gpio')
system('modprobe w1-therm')

app = Flask(__name__)

@app.route("/")
def index():
    template_data = {
        'time': freezerstate.GRAPH.last_time(),
        'temperature': freezerstate.GRAPH.last_temp()
    }
    return render_template('index.html', **template_data)

def raw_temperature():
    f = open(find_sensor(), 'r')
    lines = f.readlines()
    f.close()
    return lines

def find_sensor():
    devices = listdir(freezerstate.DEVICE_FOLDER)
    devices = [device for device in devices if device.startswith('28-')]
    if devices:
        return freezerstate.DEVICE_FOLDER + devices[0] + freezerstate.DEVICE_SUFFIX
    else:
        sys.exit("Could not find temperature sensor...")

def get_temperature():
    lines = raw_temperature()

    while not lines and len(lines) < 2 and lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = raw_temperature()
    output_temperature = lines[1].split('t=')[1]
    if output_temperature != 1:
        celsius = round(float(output_temperature) / 1000.0, 1)
        return celsius

def main_thread(name):
    if hasattr(sys, 'frozen'):
        freezerstate.FULL_PATH = os.path.abspath(sys.executable)
    else:
        freezerstate.FULL_PATH = os.path.abspath(__file__)

    freezerstate.PROG_DIR = os.path.dirname(freezerstate.FULL_PATH)

    freezerstate.ARGS = sys.argv[1:]

    parser = argparse.ArgumentParser(description='Temperature monitor and alerter')
    parser.add_argument('--datadir', help='Alternate data directory')
    parser.add_argument('--config', help='Alternate path to config file')
    args = parser.parse_args()

    if args.datadir:
        freezerstate.DATA_DIR = args.datadir
    else:
        freezerstate.DATA_DIR = freezerstate.PROG_DIR

    if args.config:
        freezerstate.CONFIG_FILE = args.config
    else:
        freezerstate.CONFIG_FILE = os.path.join(freezerstate.DATA_DIR, 'config.ini')

    print (f'Loading configuration from: {freezerstate.CONFIG_FILE}')
    freezerstate.initialize(freezerstate.CONFIG_FILE)

    print ('Getting temperature...')

    while True:
        temperature = get_temperature()
        print(f'Time: {datetime.now()} - {temperature}°C')
        freezerstate.GRAPH.plot(datetime.now(), temperature)
        freezerstate.NOTIFY.update(temperature)
        time.sleep(freezerstate.CONFIG.SAMPLE_FREQUENCY)
    return

if __name__ == "__main__":
    x = threading.Thread(target=main_thread, args=(1,))
    x.start()
    app.run(host='0.0.0.0', port=80, debug=False)
