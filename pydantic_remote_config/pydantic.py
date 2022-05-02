from pydantic import BaseSettings
from pydantic.env_settings import env_file_sentinel
from pydantic.fields import ModelField
from pydantic.typing import StrPath
from typing import Any, Dict, Optional
from jinja2 import Template


class RemoteSetting(object):
    def __init__(self, path: str):
        self.path = path
        self.value: Optional[str] = None

    def render_path(self, base_settings: Dict[str, Any]) -> None:
        self.path = Template(self.path).render(**base_settings)

    def fetch(self, base_settings: Dict[str, Any]) -> None:
        raise NotImplementedError


class RemoteSettings(BaseSettings):

    def __init__(
        __pydantic_self__,
        _env_file: Optional[StrPath] = env_file_sentinel,
        _env_file_encoding: Optional[str] = None,
        _env_nested_delimiter: Optional[str] = None,
        _secrets_dir: Optional[StrPath] = None,
        **values: Any,
    ) -> None:
        base_settings = __pydantic_self__._build_values(
            values,
            _env_file=_env_file,
            _env_file_encoding=_env_file_encoding,
            _env_nested_delimiter=_env_nested_delimiter,
            _secrets_dir=_secrets_dir,
        )
        base_settings = __pydantic_self__._build_remote_values(base_settings)
        super().__init__(**base_settings)

    def _build_remote_values(
        __pydantic_self__,
        base_settings: Dict[str, Any],
    ) -> Dict[str, Any]:
        remote_settings = {}

        for k, v in __pydantic_self__.__fields__.items():
            if issubclass(v.default.__class__, RemoteSetting):
                v.default.fetch(base_settings)
                remote_settings[k] = v.default.value

        return {**base_settings, **remote_settings}

    class Config(BaseSettings.Config):
        base_path = None
        aws_config = {
            'region': 'us-west-2',
        }

        @classmethod
        def prepare_field(cls, field: ModelField) -> None:
            BaseSettings.Config.prepare_field(field)
            pass
