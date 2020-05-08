import configparser
import os

config = configparser.ConfigParser()

class Config():
    def __init__(self, config_file = 'config.ini'):
        self.config_file = config_file

    def Open(self):
        with open(self.config_file) as file:
            lines = file.readlines()
            print("Successfully got to this line!")

        if os.path.isfile(self.config_file):
            try:
                self.config = config.read_file(self.config_file)
                return True
            except Exception as e:
                return False
        else:
            return False


# import itertools
# from collections import OrderedDict
# from operator import itemgetter

# import os
# import codecs
# import freezerstate
# import errno

# config = configparser.ConfigParser()

# _CONFIG_DEFINITIONS = OrderedDict({
#     #keyname, type, section, default
#     'HIGH_TEMP': (int, 'Alert', -15),    # Maximum Temperature (in Celsius) 
#     'HIGH_ALARM': (bool, 'Alert', True), 
#     'LOW_TEMP': (int, 'Alert', -99),     # Minimum Temperature (in Celsius)
#     'LOW_ALARM': (bool, 'Alert', False),
#     'SMTP_ENABLED': (bool, "Email", False),
#     'NOTIFICATION_EMAIL_ADDRESS': (str, 'Email', None), 
#     'SMTP_SERVER': (str, 'Email', None),
#     'SMTP_USERNAME': (str, 'Email', None),
#     'SMTP_PASSWORD': (str, 'Email', None),
#     'SMTP_PORT': (int, 'Email', 485),
#     'SLACK_ENABLED': (bool, "Slack", False), 
#     'SLACK_WEBHOOK_URL': (str, 'Slack', None)
# })

# class Config(object):
#     def __init__(self, config_file):
#         self._config_file = config_file
        
#     def config_vals(self, update=False):
#         if update is False:
#             if (os.path.isfile):
#                 self.config = config.read_file(codecs.open(self._config_file, 'r', 'utf8'))
#                 count = sum(1 for line in open(self._config_file))
#             else:
#                 count = 0
#             self.newconfig = 10
#             if count == 0:
#                 CONFIG_VERSION = 0
#             #else:
    