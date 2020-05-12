import pytest
from freezerstate.notifiers.email import EmailSender

@pytest.fixture
def sender():
    obj = EmailSender(True, 'smtp.email.com')
    return obj

def test_email_notify_should_return_false_if_disabled(sender):
    sender.enabled = False
    result = sender.notify('message', 'jgkelly1022@gmail.com', 'test', 'test', 900)

    assert result is False

def test_email_notify_should_return_true_if_enabled(sender):
    result = sender.notify('message', 'jgkelly1022@gmail.com', 'test', 'test', 900)

    assert result is True
