from pydantic import SecretStr

from pydantic_remote_config.aws import SecretsManager, SSMParam
from pydantic_remote_config.pydantic import RemoteSettings


class Settings(RemoteSettings):
    env: str

    random: str = SSMParam("/foo/{{env}}/random")
    secret: SecretStr = SSMParam("/bar/{{env}}/secret")
    secrets_manager: str = SecretsManager("test-secret", "foo")

    class Config:
        env_file = ".env"
        aws_config = {"region": "us-west-2"}


settings = Settings()
print(settings.dict())
