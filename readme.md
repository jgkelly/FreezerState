# FreezerState
Raspberry Pi freezer temperature monitor and notifier.

This project started after losing one too many freezer's full of food due to either a door not completely closed (it's an upright freezer, and the wife refuses to get a chest freezer), or a power outage.

The idea is to have a Raspberry Pi Zero sitting on some sort of battery back-up, monitoring the internal temperature within the freezer, and providing the following "services":

* Some sort of notification (probably a text message) if the freezer temperature rises over a certain value
* A web interface that will let me view the current temperature within the freezer.
* _Nice to have_: Blinking LED visually signalling the temperature is too warm.
* _Nice to have_: REST interface allowing external applications to query current temperature values.
* _Nice to have_: Running in a Docker container.


## Requirements

This project was written under Python 3.8 or greater. It was developed under Python 3.8.2. The application will fail if you attempt to run it in any version of Python less than 3.8.

### Required Packages

* flask
* matplotlib
* humanize

## Usage

Currently, you will need to run this in the same folder as freezerstate.py:

```
sudo python3 freezerstate.py
```

## Configuration

Configuration values for your environment and preferences are available in the config.ini file located in the root of this repository.

### Temperature Section

The Temperature section contains the minimum and maximum alerting values, and whether the value should trigger an alert when reached.

- `max_temperature` and `alert_on_max` control the maximum temperature (in degrees Celsius), and whether or not an alert is to be sent when the value specified in `max_temperature` is reached, or is greater.
- `min_temperature` and `alert_on_min` control the minimum temperature (in degrees Celsius), and whether or not an alert is to be sent when the value specified in `min_temperature` is reached or is lower.

### Config Section

This section contains the global configuration values

- `locaton` - String description of the temperature being monitored. This will be included in the alert notifications. Example: "Pool", "Freezer", "Air Conditioner". Default is None
- `temperature_units` - Units the measurements are to be displayed in. Accepted values are: "celsius" and "farenheit". Default is `celsius`.
- `sample_frequency` - Time (in seconds) between each temperature sample. Default is 1
- `alert_frequency` - Minimum time (in seconds) to wait between notifications. Default is 30

### Slack Section

This section contains the configuration values needed to send an alert to a configured slack Webhook URL.

- `slack_enabled`: Set to `True` to enable notifications via Slack.
- `slack_webhook_url`: Set this value to the URL you have configured to a Slack webhook application. Slack has a good article on setting up a Webhook [here](https://api.slack.com/messaging/webhooks).

### Homeassistant Section

This section contains the configuration values needed to enable status reporting to Homeassistant via the [Homeassistant REST API](https://developers.home-assistant.io/docs/api/rest/).

- `homeassistant_enabled`: (boolean) Set to `True` to enable status updates to Homeassistant.
- `homeassistant_url`: (string) Set this value to the URL configured to accept temperature update values. 
- `homeassistant_token` : (string) This value should contain the long-lived access token generated under your Homeassistant profile. See the [Homeassistant REST API Documentation](https://developers.home-assistant.io/docs/api/rest/) for details on setting up a long-lived access token.

The `location` config value will be used to name the sensor identifiers published to Homeassistant. For example: if `location` is set to "freezer", the current temperature will be published to the `sensor.freezer_temperature` entity.

The following sensor values are published to Homeassistant:

| Sensor Name | Description                            |
|-------------|----------------------------------------|
| temperature | Temperature value observed from device |
| uptime      | Total time the device has been active  |
