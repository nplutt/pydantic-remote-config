from pydantic_remote_config.pydantic import RemoteSetting
from typing import Dict, Any


class SSMParam(RemoteSetting):
    def fetch(self, base_settings: Dict[str, Any]) -> None:
        self.render_path(base_settings)
        print(f'Fetching {self.path}...')
        self.value = 'fetched_value'


class DictSSMParam(SSMParam, dict):
    pass


class IntSSMParam(SSMParam, int):
    pass


class StrSSMParam(SSMParam, str):
    pass
