from pydantic_remote_config.pydantic import RemoteSetting
from typing import Dict, Any
from pydantic_remote_config.aws.client import fetch_boto3_client, load_current_region_name
from pydantic_remote_config.enum.service_name_enum import ServiceName
from botocore.exceptions import ClientError
from pydantic_remote_config.aws.exceptions import AWSError


class SecretsManager(RemoteSetting):
    def fetch(self, base_settings: Dict[str, Any]) -> None:
        self.render_path(base_settings)

        region = self.config.get('region', load_current_region_name())
        client = fetch_boto3_client('secretsmanager', region)

        try:
            param = client.get_secret_value(SecretId=self.path)
        except ClientError as e:
            raise AWSError(
                f'Failed to fetch the {self.path} SecretsManager value.', e,
            ) from None

        self.set_value(param['SecretString'])

    @property
    def service_name(self) -> ServiceName:
        return ServiceName.AWS