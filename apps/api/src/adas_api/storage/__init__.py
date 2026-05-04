from adas_api.config import settings
from adas_api.storage.base import StorageAdapter
from adas_api.storage.local import LocalStorageAdapter


def get_storage_adapter() -> StorageAdapter:
    """Return the configured storage adapter based on environment."""
    if settings.s3_bucket and settings.s3_access_key and settings.s3_secret_key:
        from adas_api.storage.s3 import S3StorageAdapter
        return S3StorageAdapter(
            bucket=settings.s3_bucket,
            access_key=settings.s3_access_key,
            secret_key=settings.s3_secret_key,
            endpoint_url=settings.s3_endpoint_url or None,
            region=settings.s3_region,
        )
    return LocalStorageAdapter()
