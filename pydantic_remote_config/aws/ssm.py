from typing import Any, Dict

from botocore.exceptions import ClientError

from pydantic_remote_config.aws.client import (
    fetch_boto3_client,
    load_current_region_name,
)
from pydantic_remote_config.enum.VendorName import VendorName
from pydantic_remote_config.exceptions import AWSError
from pydantic_remote_config.pydantic import RemoteSetting


class SSMParam(RemoteSetting):
    def fetch(self, base_settings: Dict[str, Any]) -> None:
        self.render_path(base_settings)

        if self.config and "region" in self.config:
            region = self.config["region"]
        else:
            region = load_current_region_name()

        client = fetch_boto3_client("ssm", region)

        try:
            param = client.get_parameter(
                Name=self.path,
                WithDecryption=True,
            )
        except ClientError as e:
            raise AWSError(
                f"Failed to fetch the {self.path} SSM parameter value.",
                e,
            ) from None

        self.set_value(param["Parameter"]["Value"])

    @property
    def vendor_name(self) -> VendorName:
        return VendorName.AWS
