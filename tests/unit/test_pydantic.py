import pytest

from pydantic_remote_config.config import AWSConfig
from pydantic_remote_config.pydantic import RemoteSetting


@pytest.fixture
def remote_setting():
    yield RemoteSetting("/foo/bar")


def test_set_config(remote_setting):
    assert remote_setting.config is None
    remote_setting.set_config(AWSConfig(region="us-east-1"))
    assert remote_setting.config == {"region": "us-east-1"}


@pytest.mark.parametrize(
    ("value", "expected"),
    (
        # Loads json
        ('{"foo": "bar"}', {"foo": "bar"}),
        # Handles string
        ("hello", "hello"),
        # Handles number
        (1, 1),
        # Handles None
        (None, None),
    ),
)
def test_set_value(remote_setting, value, expected):
    remote_setting.set_value(value)

    assert remote_setting._value == expected
    assert remote_setting.loaded is True


@pytest.mark.parametrize(
    ("path", "base_settings", "expected"),
    (
        # Templates string
        ("/foo/{env}/bar", {"env": "dev"}, "/foo/dev/bar"),
        # Handles missing template args
        ("/foo/{env}/bar", {}, "/foo/{env}/bar"),
        # Does nothing to non template string
        ("/foo/dev/bar", {}, "/foo/dev/bar"),
    ),
)
def test_render_path(remote_setting, path, base_settings, expected):
    remote_setting.path = path
    remote_setting.render_path(base_settings)
    assert remote_setting.path == expected


def test_fetch_raises(remote_setting):
    with pytest.raises(NotImplementedError):
        remote_setting.fetch({})


def test_vendor_name_raises(remote_setting):
    with pytest.raises(NotImplementedError):
        remote_setting.vendor_name


@pytest.mark.parametrize(
    ("value", "key", "expected"),
    (
        # Returns value if key is None
        ("foo", None, "foo"),
        # Handles None as value
        (None, "key", None),
        # Returns keyed value if key and value are set
        ({"foo": "bar"}, "foo", "bar"),
    ),
)
def test_value(remote_setting, value, key, expected):
    remote_setting._value = value
    remote_setting.key = key

    assert remote_setting.value == expected
