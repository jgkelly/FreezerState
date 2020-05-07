import pytest
import freezerstate.notifiers.slack

from freezerstate.notifiers.slack import SlackSender

@pytest.fixture
def sender():
    obj = SlackSender(True, 'https://hooks.slack.com/services/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')
    return obj

def test_slack_notify_should_return_false_if_disabled(sender):
    sender.enabled = False
    result = sender.notify('message')

    assert result is False

def test_slack_notify_should_return_true_if_enabled(sender):
    result = sender.notify('This is a test message from the FreezerState unit tests.')

    assert result is True
