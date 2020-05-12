# Global level notifier

import freezerstate.config
import freezerstate.notifiers.slack
import freezerstate.notifiers.email
from datetime import datetime, timedelta

class Notifier:
    def __init__(self, test_enabled = None):
        self.module = '[Notifier]'
        self.location = freezerstate.CONFIG.LOCATION if test_enabled is None else 'Test Fixture'
        self.min_temperature = freezerstate.CONFIG.MIN_TEMPERATURE if test_enabled is None else -10
        self.max_temperature = freezerstate.CONFIG.MAX_TEMPERATURE if test_enabled is None else 55
        self.units = freezerstate.CONFIG.TEMPERATURE_UNITS if test_enabled is None else 'celsius'
        self.notifiers = [freezerstate.notifiers.slack.SlackSender(test_enabled, None if test_enabled is None else 'https://hooks.slack.com/services/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'),
                          freezerstate.notifiers.email.EmailSender(test_enabled, None if test_enabled is None else 'mail.google.com')]
        self.unit_conversion = ({
            'celsius': ('C'),
            'farenheit': ('F')
        })
        self.alert_frequency = freezerstate.CONFIG.ALERT_FREQUENCY if test_enabled is None else 30
        self.last_alert = datetime.min

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

        for x in self.notifiers:
            if x.enabled is True:
                x.notify(message)

        return True

    def get_notify_text(self, temperature):
        unitvalue = self.unit_conversion[self.units.lower()]
        measurement = self.to_farenheit(temperature) if self.units == 'farenheit' else temperature
        max_temp = self.to_farenheit(self.max_temperature) if self.units == 'farenheit' else self.max_temperature
        min_temp = self.to_farenheit(self.min_temperature) if self.units == 'farenheit' else self.min_temperature
        readingLocation = 'Temperature' if self.location is None else f'{self.location} temperature'
        alert_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        if temperature >= self.max_temperature:
            result = f'🌡🔥 {readingLocation} is above {max_temp}°{unitvalue} at {measurement}°{unitvalue}. Time: {alert_time}'
        else:
            result = f'🌡❄ {readingLocation} is below {min_temp}°{unitvalue} at {measurement}°{unitvalue}. Time: {alert_time}'

        return result

    def to_farenheit(self, celsius):
        farenheit = round((celsius * 1.8) + 32.0, 1)
        return farenheit