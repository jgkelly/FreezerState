#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of freezerstate.

import threading
import freezerstate.config

DATA_DIR = None
ARGS = None
DEVICE_FOLDER = "/sys/bus/w1/devices/"
DEVICE_SUFFIX = "/w1_slave"
CONFIG = None
CONFIG_FILE = None

def initialize(config_file):
    global CONFIG, CONFIG_FILE, DEVICE_FOLDER, DEVICE_SUFFIX, DATA_DIR, ARGS

    cfg = freezerstate.config.Config(config_file)
    CONFIG = cfg.read();

    assert CONFIG is not None
    return True
