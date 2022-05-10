from pydantic import BaseSettings
from pydantic.env_settings import env_file_sentinel
from pydantic.fields import ModelField
from pydantic.typing import StrPath
from typing import Any, Dict, Optional, TYPE_CHECKING
from jinja2 import Template
from pydantic_remote_config.enum.service_name_enum import ServiceName
import json

if TYPE_CHECKING:
    Base = Any
else:
    Base = object


class RemoteSetting(Base):
    def __init__(self, path: str, key: str = None):
        self.path = path
        self.key = key
        self.config = None
        self._value = None
        self.loaded = False

    def set_config(self, config: dict) -> None:
        self.config = config

    def set_value(self, value: Any) -> None:
        try:
            value = json.loads(value)
        except ValueError:
            value = value

        self.loaded = True
        self._value = value

    def render_path(self, base_settings: Dict[str, Any]) -> None:
        self.path = Template(self.path).render(**base_settings)

    def fetch(
        self,
        base_settings: Dict[str, Any],
    ) -> None:
        raise NotImplementedError

    @property
    def service_name(self) -> ServiceName:
        raise NotImplementedError

    @property
    def value(self) -> Any:
        if self.key is not None:
            return self._value[self.key]

        return self._value


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
        aws_config = None
        hashicorp_config = None

        @classmethod
        def prepare_field(cls, field: ModelField) -> None:
            BaseSettings.Config.prepare_field(field)

            if not issubclass(field.default.__class__, RemoteSetting):
                return None

            if field.default.service_name == ServiceName.AWS:
                field.default.set_config(cls.aws_config)
