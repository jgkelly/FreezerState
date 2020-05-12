# Global level notifier

import freezerstate.config
import freezerstate.notifiers.slack
import freezerstate.notifiers.email

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

    def update(self, temperature):

        if temperature < self.max_temperature and temperature > self.min_temperature:
            return False

        message = self.get_notify_text(temperature)

        for x in self.notifiers:
            print(f'Notifier: {x.module} - Enabled: {x.enabled}')

            if x.enabled is True:
                x.notify(message)

        return True

    def get_notify_text(self, temperature):
        unitvalue = self.unit_conversion[self.units]
        measurement = to_farenheit(temperature) if self.units == 'farenheit' else temperature
        readingLocation = 'Temperature' if self.location is None else f'{self.location} temperature'

        if temperature >= self.max_temperature:
            result = f'🌡🔥 {readingLocation} is above {self.max_temperature}°{unitvalue} at {measurement}°{unitvalue}'
        else:
            result = f'🌡❄ {readingLocation} is below {self.min_temperature}°{unitvalue} at {measurement}°{unitvalue}'

        return result

    def to_farenheit(self, celsius):
        farenheit = round((celsius * 1.8) + 32.0, 1)
        return farenheit
