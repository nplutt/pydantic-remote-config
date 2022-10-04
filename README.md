# pydantic-remote-config

Library that extends [pydantic's BaseSettings model](https://pydantic-docs.helpmanual.io/usage/settings/)
and integrates with various remote sources to fetch application secrets & configuration.
Supported remote sources include:
* [AWS Secrets Manager](https://docs.aws.amazon.com/secretsmanager/latest/userguide/intro.html)
* [AWS SSM Parameter Store](https://docs.aws.amazon.com/systems-manager/latest/userguide/systems-manager-parameter-store.html)

## Installation
For AWS services support:
```bash
$ pip install pydantic-remote-config[aws]
```

## Usage

### Simple Example
```python
from pydantic_remote_config.aws import SecretsManager, SSMParam
from pydantic_remote_config import RemoteSettings

class Settings(RemoteSettings):
    param_1: str = SSMParam("/foo/bar/param")
    param_2: int = SSMParam("/foo/bar/num_param")
    secret: str = SecretsManager("test-secret")

settings = Settings()
print(settings)
#> Settings(param_1="remote param", param_2=101, secret="super secret code")
```

### Templating strings

Strings can be templated using attributes that have been defined in the class and have
corresponding environment variables set. This is useful in cases where a value is
stored under a different path depending on the environment.

In this example if the environment variable `ENV` is set to `dev`, the
`/app-name/dev/db_password` value will be retrieved.

```python
from pydantic_remote_config.aws import SSMParam
from pydantic_remote_config import RemoteSettings


class Settings(RemoteSettings):
    env: str

    db_password: str = SSMParam("/app-name/{env}/db_password")
```



### Accessing Nested Values

Key value pairs can be accessed by specifying the `key` arg. The example below
illustrates an example where only the database password is retrieved from a json
object.

SSM Param value for `/app-name/database_info`:
```json
{
  "host": "foo.rds.aws.com",
  "port": 5432,
  "username": "db_user",
  "password": "super-secret-password"
}
```

Remote config implementation:
```python
from pydantic_remote_config.aws import SSMParam
from pydantic_remote_config import RemoteSettings


class Settings(RemoteSettings):
    db_password: str = SSMParam("/app-name/database_info", key="password")
```

### Class Configuration

Each remote source or class of sources has its own configuration class that
can be set.

#### AWS

The AWS config class supports specifying an aws region to fetch configuration
from. Note that this will override the default aws region configured on the
machine or boto3.

```python
from pydantic_remote_config.aws import SecretsManager, SSMParam
from pydantic_remote_config import RemoteSettings
from pydantic_remote_config.config import AWSConfig


class Settings(RemoteSettings):
    env: str
    param: str = SSMParam("/foo/bar")
    secret: dict = SecretsManager("test-secret")

    class Config:
        aws = AWSConfig(region='us-west-2')
```

### MyPy Support
This library works with mypy!

## Roadmap
This library aims to be the one stop shop for python applications that need
to fetch configuration from remote sources regardless of source. Services
that are supported or on the roadmap are listed below.
- [x] AWS Secrets Manager
- [x] AWS SSM Parameter Store
- [ ] Hashicorp Vault
- [ ] Hashicorp Consul
- [ ] Azure Key Vault

If you'd like to add a service to our roadmap, please open an issue and we'll
be happy to get it added.

## Contributing
WIP

### Development Dependencies
* `asdf` for managing multiple python version
* `pre-commit` for formatting & linting code before commits
* `poetry` managing dependencies & publishing the package

### Installing Development Dependencies
