import freezerstate.updaters.homeassistant
import freezerstate.updaters.timedstatus


class Updaters():
    def __init__(self):
        self.updateRecipients = [
            freezerstate.updaters.timedstatus.TimedStatus(),
            freezerstate.updaters.homeassistant.Homeassistant(),
        ]

    def update(self, temperature, current_time):
        for x in self.updateRecipients:
            x.update(temperature, current_time)
