from unittest.mock import MagicMock, patch

import pytest
from botocore.exceptions import ClientError

from pydantic_remote_config.aws.secrets_manager import SecretsManager
from pydantic_remote_config.enum.VendorName import VendorName
from pydantic_remote_config.exceptions import AWSError


PACKAGE = "pydantic_remote_config.aws.secrets_manager"


@pytest.mark.parametrize(
    ("config", "expected_region"),
    (
        # Uses current region when region not in config
        ({}, "current-region"),
        # Uses config region when present in config
        ({"region": "config-region"}, "config-region"),
    ),
)
@patch(f"{PACKAGE}.load_current_region_name", return_value="current-region")
@patch(f"{PACKAGE}.fetch_boto3_client")
def test_fetch_uses_config_region(
    fetch_boto3_client_patch,
    load_current_region_name_patch,
    config,
    expected_region,
):
    mock_client = MagicMock(
        get_secret_value=MagicMock(return_value={"SecretString": "secret"}),
    )
    fetch_boto3_client_patch.return_value = mock_client

    sm = SecretsManager("foo")
    sm.config = config

    assert sm.fetch({}) is None
    fetch_boto3_client_patch.assert_called_once_with(
        "secretsmanager",
        expected_region,
    )
    mock_client.get_secret_value.assert_called_once_with(SecretId="foo")

    assert sm.value == "secret"


@patch(f"{PACKAGE}.load_current_region_name", return_value="current-region")
@patch(f"{PACKAGE}.fetch_boto3_client")
def test_fetch_handles_exception(
    fetch_boto3_client_patch,
    load_current_region_name_patch,
):
    mock_client = MagicMock(
        get_secret_value=MagicMock(side_effect=ClientError({}, "bar")),
    )
    fetch_boto3_client_patch.return_value = mock_client

    with pytest.raises(AWSError):
        sm = SecretsManager("foo")
        sm.fetch({})


def test_vendor_name_property():
    sm = SecretsManager("foo")
    assert sm.vendor_name == VendorName.AWS
