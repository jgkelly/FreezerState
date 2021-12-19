import freezerstate.notifiers.slack


class Notifiers():
    def __init__(self):
        self.notifyRecipients = [
            freezerstate.notifiers.slack.SlackSender(),
        ]

    def notify(self, message):
        for x in self.notifyRecipients:
            x.notify(message=message)
