# Global status notification times

import freezerstate.config
import time
import datetime

class StatusUpdate:
    def __init__(self, test_enabled=None, test_times=None):
        self.module = '[StatusUpdate]'
        self.notification_times = []
        notify_times = freezerstate.CONFIG.STATUS_CHECK_TIMES if test_enabled is None else test_times

        self.load_times(notify_times)

    def should_notify(self, time_value):
        test_time = time_value

        if (type(time_value) == datetime.datetime):
            # time(hour = time_value.hour, minute = time_value.minute)
            test_time = time_value.time()

        test_text = test_time.strftime('%H:%M')

        for x in self.notification_times:
            if x.tm_hour == time_value.hour and x.tm_min == time_value.minute:
                return True
        return False

    def load_times(self, times):
        if times is None:
            return

        time_list = times.split(',')
        if len(time_list) == 0:
            return

        for x in time_list:
            try:
                note_time = time.strptime(x, '%H:%M')
                self.notification_times.append(note_time)
            except ValueError as ve:
                print(f'Time value: {x} is not a valid time - Ignoring')
