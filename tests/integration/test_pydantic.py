from unittest.mock import MagicMock, patch

from pydantic import SecretStr

from pydantic_remote_config import RemoteSettings
from pydantic_remote_config.aws import SecretsManager, SSMParam


class TestClass(RemoteSettings):
    env: str

    ssm_param_1: str = SSMParam("/{env}/param_1")
    ssm_param_2: int = SSMParam("/foo/param_2")
    ssm_param_3: dict = SSMParam("/foo/param_3")
    ssm_param_4: SecretStr = SSMParam("/foo/param_4", "secret")

    secret_1: str = SecretsManager("/{env}/secret_1")
    secret_2: int = SecretsManager("/foo/secret_2")
    secret_3: dict = SecretsManager("/foo/secret_3", "key")
    secret_4: SecretStr = SecretsManager("/foo/secret_4")


def mock_get_parameter(Name, WithDecryption):
    values = {
        "/foo/param_1": "param 1",
        "/foo/param_2": 123456,
        "/foo/param_3": '{"foo": "bar"}',
        "/foo/param_4": '{"secret": "super"}',
    }
    return {"Parameter": {"Value": values.get(Name)}}


def mock_get_secret_value(SecretId):
    values = {
        "/foo/secret_1": "secret 1",
        "/foo/secret_2": 987654,
        "/foo/secret_3": '{"key": {"hello": "world"}}',
        "/foo/secret_4": "super secret",
    }
    return {"SecretString": values.get(SecretId)}


@patch("pydantic_remote_config.aws.ssm.fetch_boto3_client")
@patch("pydantic_remote_config.aws.secrets_manager.fetch_boto3_client")
@patch.dict("os.environ", {"env": "foo"}, clear=True)
def test_remote_settings_model(
    secrets_manager_boto3_client_patch,
    ssm_boto3_client_patch,
):
    mock_ssm_client = MagicMock(get_parameter=MagicMock(side_effect=mock_get_parameter))
    ssm_boto3_client_patch.return_value = mock_ssm_client
    mock_secrets_manager_client = MagicMock(
        get_secret_value=MagicMock(side_effect=mock_get_secret_value),
    )
    secrets_manager_boto3_client_patch.return_value = mock_secrets_manager_client

    settings = TestClass()
    assert settings.dict() == {
        "env": "foo",
        "secret_1": "secret 1",
        "secret_2": 987654,
        "secret_3": {"hello": "world"},
        "secret_4": SecretStr("super secret"),
        "ssm_param_1": "param 1",
        "ssm_param_2": 123456,
        "ssm_param_3": {"foo": "bar"},
        "ssm_param_4": SecretStr("super"),
    }
