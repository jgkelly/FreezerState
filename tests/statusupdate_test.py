import pytest

import datetime
#from datetime import datetime
from freezerstate.statusupdate import StatusUpdate

@pytest.fixture
def statusobj():
    obj = StatusUpdate(True, '8:00,9:30,21:00,26:99')
    return obj

def test_update_initialization(statusobj):
    assert len(statusobj.notification_times) == 3

def test_should_notify_should_be_false_if_time_not_in_list(statusobj):
    test_time = datetime.time(10,30)
    result = statusobj.should_notify(test_time)

    assert result is False

def test_should_notify_should_be_true_if_time_is_in_list(statusobj):
    test_time = datetime.time(9, 30, 0)
    result = statusobj.should_notify(test_time)

    assert result is True

def test_should_notify_should_be_true_if_now_is_in_list(statusobj):
    test_time = datetime.datetime.now()
    result = statusobj.should_notify(test_time)

    assert result is False

