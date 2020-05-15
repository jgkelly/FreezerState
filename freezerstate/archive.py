import freezerstate.config
from datetime import datetime


class Archiver:
    def __init__(self):
        self.module = '[Archiver]'
        self.archivers = [freezerstate.archivers.MssqlArchiver()]

    # content expected to be in dictionary:
    #    content = {
    #        'Temperature': <current temperature in celsius>
    #        'Alert' : alarm_types or None
    #    }
    def update(self, content):

        # TODO: Complete this method

        updateRecord = content
        updateRecord['time'] = datetime.now()
        updateRecord['location'] = freezerstate.CONFIG.LOCATION

        self.update_all(updateRecord)

        return True

    def update_all(self, updateRecord):
        for x in self.archivers:
            if (x.enabled is True):
                x.update(updateRecord)
