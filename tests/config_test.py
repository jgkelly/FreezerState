import pytest
from freezerstate.config import Config

@pytest.fixture
def config():
    obj = Config()
    return obj

def test_config(config):
    assert True