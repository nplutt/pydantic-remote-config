from pydantic import SecretStr

from pydantic_remote_config import RemoteSettings
from pydantic_remote_config.aws import SecretsManager, SSMParam
from pydantic_remote_config.config import AWSConfig


class Settings(RemoteSettings):
    env: str

    random: str = SSMParam("/foo/{env}/random")
    secret_param: SecretStr = SSMParam("/bar/{env}/secret")
    secret_map: dict = SecretsManager("test-secret")
    secrets_value: str = SecretsManager("test-secret", key="foo")

    class Config:
        aws = AWSConfig(region="us-west-2")


settings = Settings()
print(settings.dict())
