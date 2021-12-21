import freezerstate.config
import freezerstate.conversion
import requests
import humanize

class Homeassistant():
    def __init__(self, test_enabled = None, test_homeassistant_server=None, test_token = None):
        self.module = '[Homeassistant]'
        self.enabled = freezerstate.CONFIG.HOMEASSISTANT_ENABLED if test_enabled is None else test_enabled
        self.rest_url = freezerstate.CONFIG.HOMEASSISTANT_URL if test_homeassistant_server is None else test_homeassistant_server
        self.token = freezerstate.CONFIG.HOMEASSISTANT_TOKEN if test_enabled is None else 'token'
        self.device_name = freezerstate.CONFIG.LOCATION.lower() if test_enabled is None else 'testfreezer'
        self.converation = freezerstate.conversion.Conversion()

    def update(self, temperature, current_time):
        if (self.enabled is False):
            print(f'{self.module} - Homeassistant Sender is disabled')
            return False

        self.notify_temperature(temperature)
        return self.notify_uptime(current_time)

    def notify_temperature(self, temperature):
        payload = {
            "state": self.converation.UnitizedTemperature(temperature),
            "attributes": {
                "unit_of_measurement": self.converation.UnitString(),
            }
        }

        return self.notify_homeassistant_state('temperature', payload)

    def notify_uptime(self, current_time):
        uptime_diff = current_time - freezerstate.START_TIME
        uptime = uptime_diff.total_seconds()
        uptime_readable = humanize.time.precisedelta(uptime)

        payload = {
            "state": uptime_readable,
        }

        self.notify_homeassistant_state('uptime', payload)

    def notify_homeassistant_state(self, sensorName, payload):
            url = f'{self.rest_url}/api/states/sensor.{self.device_name}_{sensorName}'
            headers = {
                "Authorization": f"Bearer {self.token}",
                "content-type": "application/json",
            }

            try:
                print(f'Sending {sensorName} update to URL: {url} -- Payload: {payload}')
                requests.post(url, headers=headers, json=payload, verify=True)
            except Exception as e:
                print(f'{self.module} - Homeassistant update for sensor {sensorName} failed: {e}')
                return False
            return True
