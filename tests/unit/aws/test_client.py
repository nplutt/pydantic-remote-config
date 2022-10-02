from unittest.mock import MagicMock, patch

import pytest

from pydantic_remote_config.aws.client import (
    fetch_boto3_client,
    load_current_region_name,
)


PACKAGE = "pydantic_remote_config.aws.client"


@pytest.fixture(autouse=True)
def clear_caches():
    fetch_boto3_client.cache_clear()
    load_current_region_name.cache_clear()


def test_fetch_boto3_client():
    boto3_mock = MagicMock(client=MagicMock(return_value="client"))
    config_mock = MagicMock(Config=MagicMock(return_value="config"))

    with patch.dict(
        "sys.modules",
        {"boto3": boto3_mock, "botocore.config": config_mock},
        clear=True,
    ):
        assert fetch_boto3_client("ssm", "us-west-2") == "client"
        config_mock.Config.assert_called_once_with(
            region_name="us-west-2",
            signature_version="v4",
            retries={"max_attempts": 10, "mode": "standard"},
        )
        boto3_mock.client.assert_called_once_with("ssm", config="config")


@patch.dict("sys.modules", {}, clear=True)
def test_fetch_boto3_client_raises():
    with pytest.raises(ImportError):
        fetch_boto3_client("ssm", "us-west-2")


def test_load_current_region_name():
    session_mock = MagicMock(region_name="region")
    boto3_mock = MagicMock(
        session=MagicMock(Session=MagicMock(return_value=session_mock)),
    )

    with patch.dict("sys.modules", {"boto3": boto3_mock}, clear=True):
        assert load_current_region_name() == "region"


@patch.dict("sys.modules", {}, clear=True)
def test_load_current_region_name_raises():
    with pytest.raises(ImportError):
        load_current_region_name()
