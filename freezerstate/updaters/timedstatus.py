import freezerstate.config
import freezerstate.statusupdate
import freezerstate.notifiers.notifiers
import humanize
from datetime import datetime


class TimedStatus():
    def __init__(self):
        self.module = '[TimedStatus]'
        self.alert_frequency = freezerstate.CONFIG.ALERT_FREQUENCY
        self.notifiers = freezerstate.notifiers.notifiers.Notifiers()
        self.last_notify = datetime.min
        self.status_update_times = freezerstate.statusupdate.StatusUpdate()

    def update(self, temperature, current_time):
        if self.status_update_times.should_notify(current_time):
            self.send_status_update(temperature, current_time)

        return False

    def send_status_update(self, temperature, current_time):
        difference = current_time - self.last_notify
        if (difference.total_seconds() <= 60):
            print(
                f'--- It has been {difference.total_seconds()} seconds since last status update. Skipping status update')
            return False

        timestring = current_time.strftime(
            freezerstate.CONFIG.DATE_TIME_STAMP_FORMAT)
        uptime_diff = current_time - freezerstate.START_TIME
        uptime = uptime_diff.total_seconds()
        uptime_readable = humanize.time.precisedelta(uptime)

        message = f'*{self.location}* status update.\n🌡 {freezerstate.CONVERSION.TemperatureString(temperature, True)}\n⏰ {timestring}\n💻 Uptime: {uptime_readable}'
        print(f'--- {current_time}: Sending uptime notification')
        self.last_notify = current_time
        self.notifiers.notify(message)
