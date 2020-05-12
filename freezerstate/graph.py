#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of freezerstate.

import freezerstate.config

class TemperatureGraph:

    def __init__(self):
        self.x = []
        self.y = []
        self.max_data_points = freezerstate.CONFIG.GRAPH_DATA_POINTS


    def plot(self, x, y):
        if (self.x.count > self.max_data_points):
            self.x.pop(0)
            self.y.pop(0)

        self.x.append(x)
        self.y.append(y)

        print(f'-- X Count: {self.x.count} - Y Count: {self.y.count}')

    def last_time(self):
        return self.x[-1]

    def last_temp(self):
        return self.y[-1]