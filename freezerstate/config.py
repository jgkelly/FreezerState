from collections import OrderedDict

import configparser
import codecs
import os
import socket

config = configparser.ConfigParser()

_CONFIG_DEFINITIONS = OrderedDict({
    #keyname, type, section, default
    'LOCATION': (str, 'Config', None),
    'TEMPERATURE_UNITS': (str, 'Config', 'celsius'),
    # Number of seconds between temperature samples
    'SAMPLE_FREQUENCY': (int, 'Config', 1),
    # Number of seconds allowed between alert notifications
    'ALERT_FREQUENCY': (int, 'Config', 30),
    'GRAPH_DATA_POINTS': (int, 'Config', 14400),
    'DEVICE_ADDRESS': (str, 'Config', None),
    'STATUS_CHECK_TIMES': (str, 'Config', None),
    'DATE_TIME_STAMP_FORMAT': (str, 'Config', '%m/%d/%Y %X'),
    # -- Temperature Section --
    # Maximum Temperature (in Celsius)
    'MAX_TEMPERATURE': (int, 'Temperature', 40),
    'ALERT_ON_MAX': (bool, 'Temperature', True),
    # Minimum Temperature (in Celsius)
    'MIN_TEMPERATURE': (int, 'Temperature', -40),
    'ALERT_ON_MIN': (bool, 'Temperature', False),
    # -- Slack Section --
    'SLACK_ENABLED': (bool, 'Slack', False),
    'SLACK_WEBHOOK_URL': (str, 'Slack', None),
    # -- MSSQL Section --
    'MSSQL_ENABLED': (bool, 'MSSQL', False),
    'MSSQL_SERVER': (str, 'MSSQL', None),
    'MSSQL_DATABASE': (str, 'MSSQL', None),
    'MSSQL_SERVER_USERNAME': (str, 'MSSQL', None),
    'MSSQL_SERVER_PASSWORD': (str, 'MSSQL', None)
})


class Config():
    def __init__(self, config_file='config.ini'):
        self.config_file = config_file

    def read(self):
        self.config_vals()
        self.set_local_defaults()
        return self

    def set_local_defaults(self):
        if (self.DEVICE_ADDRESS is not None):
            return

        host_name = socket.gethostname()
        deviceAddress = host_name

    def config_vals(self):
        if os.path.isfile(self.config_file):
            self.config = config.read_file(
                codecs.open(self.config_file, 'r', 'utf8'))
            count = sum(1 for line in open(self.config_file))
        else:
            count = 0

        config_values = []
        for k, v in _CONFIG_DEFINITIONS.items():
            values = []
            values.append(k)
            for x in v:
                if x is None:
                    x = 'None'
                values.append(x)
            value = self.check_settings(values)

            try:
                if v[0] == str and any([value == "", value is None, len(value) == 0, value == 'None']):
                    value = v[2]
            except:
                value = v[2]

            try:
                if v[0] == bool:
                    value = self.argToBool(value)
            except:
                value = self.argToBool(v[2])
            try:

                if all([v[0] == int, str(value).isdigit()]):
                    value = int(value)
            except:
                value = v[2]

            setattr(self, k, value)

            try:
                # make sure interpolation isn't being used, so we can just escape the % character
                if v[0] == str:
                    value = value.replace('%', '%%')
            except Exception as e:
                pass

            # just to ensure defaults are properly set...
            if any([value is None, value == 'None']):
                value = v[0](v[2])

    def check_settings(self, key):
        keyname = key[0].upper()
        inikey = key[0].lower()
        definition_type = key[1]
        section = key[2]
        default = key[3]
        myval = self.check_config(definition_type, section, inikey, default)

        if myval['status'] is False:
            myval = {'value': definition_type(default)}

        return myval['value']

    def check_config(self, definition_type, section, inikey, default):
        try:
            if definition_type == str:
                myval = {'status': True, 'value': config.get(section, inikey)}
            elif definition_type == int:
                myval = {'status': True,
                         'value': config.getint(section, inikey)}
            elif definition_type == bool:
                myval = {'status': True,
                         'value': config.getboolean(section, inikey)}
        except Exception:
            if definition_type == str:
                try:
                    myval = {'status': True, 'value': config.get(
                        section, inikey, raw=True)}
                except (configparser.NoSectionError, configparser.NoOptionError):
                    myval = {'status': False, 'value': None}
            else:
                myval = {'status': False, 'value': None}
        return myval

    def argToBool(self, argument):
        _arg = argument.strip().lower() if isinstance(argument, str) else argument
        if _arg in (1, '1', 'on', 'true', True):
            return True
        elif _arg in (0, '0', 'off', 'false', False):
            return False
        return argument
