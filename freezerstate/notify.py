# Global level notifier

import freezerstate.config
import freezerstate.statusupdate
import freezerstate.updaters.updaters
import freezerstate.notifiers.notifiers
from datetime import datetime, timedelta


class Notifier:
    def __init__(self):
        self.module = '[Notifier]'
        self.location = freezerstate.CONFIG.LOCATION
        self.min_temperature = freezerstate.CONFIG.MIN_TEMPERATURE
        self.max_temperature = freezerstate.CONFIG.MAX_TEMPERATURE
        self.notify_min = freezerstate.CONFIG.ALERT_ON_MIN
        self.notify_max = freezerstate.CONFIG.ALERT_ON_MAX
        self.notifiers = freezerstate.notifiers.notifiers.Notifiers()
        self.updaters = freezerstate.updaters.updaters.Updaters()
        self.alert_frequency = freezerstate.CONFIG.ALERT_FREQUENCY
        self.status_update_times = freezerstate.statusupdate.StatusUpdate()
        self.last_alert = datetime.min
        self.last_temperature = None

    def update(self, temperature):
        current_time = datetime.now()
        self.updaters.update(temperature, current_time)

        if temperature < self.max_temperature and temperature > self.min_temperature:
            return False

        if temperature >= self.max_temperature and self.notify_max is False:
            return False

        if temperature <= self.min_temperature and self.notify_min is False:
            return False

        difference = current_time - self.last_alert
        if (difference.total_seconds() < self.alert_frequency):
            print(
                f'--- It has been {difference.total_seconds()} seconds since last alert. Frequency is {self.alert_frequency}. Skipping this alert')
            return False

        self.last_alert = current_time
        message = self.get_notify_text(temperature)

        self.last_temperature = temperature
        self.notifiers.notify(message)

        return True

    def send_startup_message(self):
        timestring = freezerstate.START_TIME.strftime(
            freezerstate.CONFIG.DATE_TIME_STAMP_FORMAT)
        message = f'💻 *{self.location}* monitoring started at {timestring}'
        self.notifiers.notify(message)

    def reading_location(self):
        readingLocation = 'Temperature' if self.location is None else f'{self.location} temperature'
        return readingLocation

    def get_notify_text(self, temperature):
        readingLocation = self.reading_location()
        alert_time = datetime.now().strftime(freezerstate.CONFIG.DATE_TIME_STAMP_FORMAT)
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

