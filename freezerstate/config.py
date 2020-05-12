from collections import OrderedDict

import configparser
import codecs
import os

config = configparser.ConfigParser()

_CONFIG_DEFINITIONS = OrderedDict({
    #keyname, type, section, default
    'LOCATION': (str, 'Config', None),
    'MAX_TEMPERATURE': (int, 'Temperature', -15),    # Maximum Temperature (in Celsius)
    'ALERT_ON_MAX': (bool, 'Temperature', True),
    'MIN_TEMPERATURE': (int, 'Temperature', -99),     # Minimum Temperature (in Celsius)
    'ALERT_ON_MIN': (bool, 'Temperature', False),
    'SAMPLE_FREQUENCY': (int, 'Temperature', 1),
    'TEMPERATURE_UNITS': (str, 'Temperature', 'celsius'),
    'SMTP_ENABLED': (bool, "Email", False),
    'NOTIFICATION_EMAIL_ADDRESS': (str, 'Email', None),
    'SMTP_SERVER': (str, 'Email', None),
    'SMTP_USERNAME': (str, 'Email', None),
    'SMTP_PASSWORD': (str, 'Email', None),
    'SMTP_PORT': (int, 'Email', 485),
    'SLACK_ENABLED': (bool, "Slack", False),
    'SLACK_WEBHOOK_URL': (str, 'Slack', None)
})

class Config():
    def __init__(self, config_file = 'config.ini'):
        self.config_file = config_file

    def read(self):
        self.config_vals()
        return self

    def config_vals(self):
        if os.path.isfile(self.config_file):
            self.config = config.read_file(codecs.open(self.config_file, 'r', 'utf8'))
            count = sum(1 for line in open(self.config_file))
        else:
            count = 0

        config_values = []
        for k,v in _CONFIG_DEFINITIONS.items():
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
                #make sure interpolation isn't being used, so we can just escape the % character
                if v[0] == str:
                    value = value.replace('%', '%%')
            except Exception as e:
                pass

            #just to ensure defaults are properly set...
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
                myval = {'status': True, 'value': config.getint(section, inikey)}
            elif definition_type == bool:
                myval = {'status': True, 'value': config.getboolean(section, inikey)}
        except Exception:
            if definition_type == str:
                try:
                    myval = {'status': True, 'value': config.get(section, inikey, raw=True)}
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
