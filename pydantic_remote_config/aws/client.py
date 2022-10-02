from functools import lru_cache


@lru_cache()
def fetch_boto3_client(service_name: str, region_name: str):
    """
    Takes a service name & region and returns a boto3 client for
    the given service.
    """
    try:
        import boto3
        from botocore.config import Config
    except ImportError as e:
        raise ImportError(
            "boto3 is not installed run `pip install pydantic-remote-config[aws]",
        ) from e

    config = Config(
        region_name=region_name,
        signature_version="v4",
        retries={"max_attempts": 10, "mode": "standard"},
    )
    return boto3.client(service_name, config=config)


@lru_cache()
def load_current_region_name() -> str:
    """
    Uses boto3 to load the current region set in the aws cli config
    """
    try:
        import boto3
    except ImportError as e:
        raise ImportError(
            "boto3 is not installed run `pip install pydantic-remote-config[aws]",
        ) from e

    session = boto3.session.Session()
    return session.region_name
