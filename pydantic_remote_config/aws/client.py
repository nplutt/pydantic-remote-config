from typing import Optional


CLIENT_CACHE = {}


def fetch_boto3_client(service_name: str, region_name: Optional[str] = None):
    """
    Takes a service name & region and returns a boto3 client for
    the given service.
    """
    cache_key = f"{region_name}-{service_name}"

    if CLIENT_CACHE.get(cache_key):
        return CLIENT_CACHE[cache_key]

    try:
        import boto3
        from botocore.config import Config
    except ImportError as e:
        raise ImportError(
            'boto3 is not installed run `pip install pydantic-remote-config[aws]',
        ) from e

    config = Config(
        region_name=region_name,
        signature_version="v4",
        retries={"max_attempts": 10, "mode": "standard"},
    )
    client = boto3.client(service_name, config=config)

    CLIENT_CACHE[cache_key] = client

    return client


def _load_current_region_name() -> str:
    """
    Uses boto3 to load the current region set in the aws cli config
    """
    try:
        import boto3
    except ImportError as e:
        raise ImportError(
            'boto3 is not installed run `pip install pydantic-remote-config[aws]',
        ) from e

    session = boto3.session.Session()
    return session.region_name
