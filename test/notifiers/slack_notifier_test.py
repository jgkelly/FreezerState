import unittest
import freezerstate.notifiers.slack

from freezerstate.notifiers.slack import SlackSender

class Slack_Notifier_Tests(unittest.TestCase):
    
    def SetUp(self):    
        self.notifier = SlackSender(True, 'https://jeffandjannakelly.slack.com/archives/G013MDE8TT3')
        
    def should_return_false_if_disabled(self):
        self.notifier.enabled = False;
        result = self.notifier.notify('This is a test message - Disabled')
        
        assert result is False
        
    def should_return_true_if_enabled(self):
        result = self.notifier.notify('This is a test message - Enabled')
        
        assert result is True