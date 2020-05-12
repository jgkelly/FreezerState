# Global level notifier

import freezerstate.config
import freezerstate.notifiers.slack
import freezerstate.notifiers.email
from datetime import datetime, timedelta

class Notifier:
    def __init__(self):
        self.module = '[Notifier]'
        self.location = freezerstate.CONFIG.LOCATION
        self.min_temperature = freezerstate.CONFIG.MIN_TEMPERATURE
        self.max_temperature = freezerstate.CONFIG.MAX_TEMPERATURE
        self.units = freezerstate.CONFIG.TEMPERATURE_UNITS.lower()
        self.notifiers = [freezerstate.notifiers.slack.SlackSender(),
                          freezerstate.notifiers.email.EmailSender()]
        self.unit_conversion = ({
            'celsius': ('C'),
            'farenheit': ('F')
        })
        self.alert_frequency = freezerstate.CONFIG.ALERT_FREQUENCY
        self.last_alert = datetime.min
        self.last_temperature = None

    def update(self, temperature):

        if temperature < self.max_temperature and temperature > self.min_temperature:
            return False

        current_time = datetime.now()
        difference = current_time - self.last_alert
        if (difference.total_seconds() < self.alert_frequency):
            print(f'--- It has been {difference.total_seconds()} seconds since last alert. Frequency is {self.alert_frequency}. Skipping this alert')
            return False

        self.last_alert = current_time
        message = self.get_notify_text(temperature)

        self.last_temperature = temperature

        for x in self.notifiers:
            if x.enabled is True:
                x.notify(message)

        return True

    def get_notify_text(self, temperature):
        readingLocation = 'Temperature' if self.location is None else f'{self.location} temperature'
        alert_time = datetime.now().strftime('%x %X')
        level_change_description = self.change_description(temperature)

        if temperature >= self.max_temperature:
            result = f'🌡🔥{level_change_description} {readingLocation} is above {freezerstate.CONVERSION.TemperatureString(self.max_temperature, True)} at {freezerstate.CONVERSION.TemperatureString(temperature, True)}. Time: {alert_time}'
        else:
            result = f'🌡❄{level_change_description} {readingLocation} is below {freezerstate.CONVERSION.TemperatureString(self.min_temperature, True)} at {freezerstate.CONVERSION.TemperatureString(temperature, True)}. Time: {alert_time}'

        return result

    def change_description(self, temperature):
        if (self.last_temperature is None):
            return ' '

        if (temperature > self.last_temperature):
            return '↗'

        if (temperature < self.last_temperature):
            return '↘'

        return '➡'

    def to_farenheit(self, celsius):
        farenheit = round((celsius * 1.8) + 32.0, 1)
        return farenheit