import json
from typing import TYPE_CHECKING, Any, Dict, Optional

from pydantic import BaseSettings
from pydantic.env_settings import env_file_sentinel
from pydantic.fields import ModelField
from pydantic.typing import StrPath

from pydantic_remote_config.enum.VendorName import VendorName


if TYPE_CHECKING:
    Base = Any
else:
    Base = object


class RemoteSetting(Base):
    def __init__(self, path: str, key: str = None):
        self.path: str = path
        self.key: Optional[str] = key
        self.config: Optional[dict] = None
        self._value: Optional[Any] = None
        self.loaded: bool = False

    def set_config(self, config: dict) -> None:
        self.config = config

    def set_value(self, value: Any) -> None:
        try:
            value = json.loads(value)
        except (ValueError, TypeError):
            value = value

        self.loaded = True
        self._value = value

    def render_path(self, base_settings: Dict[str, Any]) -> None:
        try:
            self.path = self.path.format(**base_settings)
        except KeyError:
            pass

    def fetch(
        self,
        base_settings: Dict[str, Any],
    ) -> None:
        raise NotImplementedError

    @property
    def vendor_name(self) -> VendorName:
        raise NotImplementedError

    @property
    def value(self) -> Any:
        if self.key is not None and self._value is not None:
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

            if field.default.vendor_name == VendorName.AWS:
                field.default.set_config(cls.aws_config)
            elif field.default.vendor_name == VendorName.HASHICORP:
                field.default.set_config(cls.hashicorp_config)
