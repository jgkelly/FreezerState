import pytest
import freezerstate.notifiers.slack

from freezerstate.notifiers.slack import SlackSender

@pytest.fixture
def sender():
    obj = SlackSender(True, 'https://jeffandjannakelly.slack.com/archives/G013MDE8TT3')
    return obj

def test_slack_notify_should_return_false_if_disabled(sender):
    sender.enabled = False
    result = sender.notify('message')

    assert result is False

def test_slack_notify_should_return_true_if_enabled(sender):
    result = sender.notify('message')

    assert result is True
