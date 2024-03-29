import freezerstate.config
import requests


class SlackSender():

    def __init__(self, test_enabled=None, test_slack_server=None):
        self.module = '[SLACK]'
        self.enabled = freezerstate.CONFIG.SLACK_ENABLED if test_enabled is None else test_enabled
        self.webhook_url = freezerstate.CONFIG.SLACK_WEBHOOK_URL if test_slack_server is None else test_slack_server

    def notify(self, message):
        payload = {
            "text": message
        }

        return self.notify_extended(payload)

    def notify_extended(self, payload):
        if (self.enabled is False):
            print(f'{self.module} - Slack Sender is disabled')
            return False

        try:
            requests.post(self.webhook_url, json=payload, verify=True)
        except Exception as e:
            print(f'{self.module} - Slack notify failed: {e}')
            return False
        return True
