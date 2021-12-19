import freezerstate.updaters.homeassistant
import freezerstate.updaters.timedstatus


class Updaters():
    def __init__(self):
        self.updateRecipients = [
            freezerstate.updaters.updaters.timedstatus,
            freezerstate.updaters.updaters.homeassistant,
        ]

    def update(self, temperature, current_time):
        for x in self.updateRecipients:
            if x.enabled is True:
                x.update(temperature, current_time)
