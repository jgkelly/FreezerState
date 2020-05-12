import pytest
from freezerstate.notify import Notifier

@pytest.fixture
def notifier():
    obj = Notifier(True)
    return obj

def test_update_should_not_notify_if_temperature_is_in_range(notifier):
    result = notifier.update(0)
    assert result is False

# def test_update_temperature_high(notifier):
#     result = notifier.update(90)

#     assert result is True

# def test_update_temperature_low(notifier):
#     result = notifier.update(-30)

#     assert result is True