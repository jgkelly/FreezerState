import freezerstate.config
import requests

class SlackSender():
    
    def __init__(self, test_enabled = None, test_slack_server = None):
        self.module = '[SLACK]'
        self.enabled = freezerstate.config.SLACK_ENABLED if test_enabled is None else test_enabled
        self.webhook_url = freezerstate.config.SLACK_WEBHOOK_URL if test_slack_server is None else test_slack_server

    def notify(self, message):
        if (self.enabled is True):
            print(f'--- {self.module} - Sending {message} to {self.webhook_url}')

            payload = {
                "text": message
            }

            try:
                requests.post(self.webhook_url, json=payload, verify=True)
            except Exception as e:
                print(f'{self.module} - Slack notify failed: {e}')
                return False
            return True
        else:
            print(f'{self.module} - Slack Sender is disabled')
            return False
