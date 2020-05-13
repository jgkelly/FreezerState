#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of freezerstate.

import threading
import freezerstate.config
import freezerstate.notify
import freezerstate.graph
import freezerstate.conversion

DATA_DIR = None
ARGS = None
DEVICE_FOLDER = "/sys/bus/w1/devices/"
DEVICE_SUFFIX = "/w1_slave"
CONFIG = None
CONFIG_FILE = None
NOTIFY = None
GRAPH = None
CONVERSION = None
RANGE_MIN = -40
RANGE_MAX = 50

def initialize(config_file):
    global CONFIG, CONFIG_FILE, DEVICE_FOLDER, DEVICE_SUFFIX, DATA_DIR, ARGS, NOTIFY, GRAPH, CONVERSION, RANGE_MIN, RANGE_MAX

    cfg = freezerstate.config.Config(config_file)
    CONFIG = cfg.read();

    CONVERSION = freezerstate.conversion.Conversion()
    NOTIFY = freezerstate.notify.Notifier()
    GRAPH = freezerstate.graph.TemperatureGraph()

    RANGE_MIN = freezerstate.CONFIG.MIN_TEMPERATURE - 10
    RANGE_MAX = freezerstate.CONFIG_MAX_TEMPERATURE + 10

    assert CONFIG is not None
    return True