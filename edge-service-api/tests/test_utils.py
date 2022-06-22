import pytest
from utils.utils import strtobool


def test_str_bool():
    tru = ('y', 'yes', 't', 'true', 'on', '1')
    fal = ('n', 'no', 'f', 'false', 'off', '0')

    for s in tru:
        assert True is strtobool(s)

    for s in fal:
        assert False is strtobool(s)

    with pytest.raises(ValueError):
        strtobool("qwerqwer")
