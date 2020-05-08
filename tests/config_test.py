import freezerstate.config

def test_config():
    config = freezerstate.config.Config()
    result = config.Open();

    print(f'{config.config}')

    assert result is True
    # TODO: Complete this test