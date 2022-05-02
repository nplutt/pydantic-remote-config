from pydantic_remote_config.pydantic import RemoteSettings
from pydantic_remote_config.aws import StrSSMParam, IntSSMParam


class Settings(RemoteSettings):
    env: str
    barz: str

    ssm_param_1: str = StrSSMParam('/{{env}}/hello/world')
    ssm_param_2: int = IntSSMParam('/{{env}}/hello/world')

    class Config:
        env_file = ".env"
        base_path = "/app_name"
        aws_config = {
            'region': 'us-west-2'
        }


settings = Settings()
print(settings.dict())
