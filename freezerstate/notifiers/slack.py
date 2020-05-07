import freezerstate.config

class SlackSender():
    
    def __init__(self, test_enabled = None, test_slack_server = None):
        self.module = '[SLACK]'
        self.enabled = freezerstate.config.SLACK_ENABLED if test_enabled is None else test_enabled
        self.webhook_url = freezerstate.config.SLACK_WEBHOOK_URL if test_slack_server is None else test_slack_server

    def notify(self, message):
        if (self.enabled is True):
            # TODO: Complete this code
            print(f'--- {module} - Sending {message} to {webhook_url}')
        return