import asyncio
import tempfile
from pathlib import Path
import boto3
from botocore.exceptions import ClientError
from adas_api.storage.base import StorageAdapter


class S3StorageAdapter(StorageAdapter):
    """S3-compatible storage adapter. Works with AWS S3, Cloudflare R2, Backblaze B2."""

    def __init__(
        self,
        bucket: str,
        access_key: str,
        secret_key: str,
        endpoint_url: str | None = None,
        region: str = "auto",
    ):
        self.bucket = bucket
        self._client = boto3.client(
            "s3",
            endpoint_url=endpoint_url,
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_key,
            region_name=region,
        )

    async def save(self, workspace_id: str, file_id: str, filename: str, content: bytes) -> str:
        blob_path = f"{workspace_id}/{file_id}_{filename}"
        await asyncio.to_thread(
            self._client.put_object,
            Bucket=self.bucket,
            Key=blob_path,
            Body=content,
        )
        return blob_path

    def get_local_path(self, blob_path: str) -> Path:
        """Download from S3 to a temp file and return the path. Sync — called from sync profiler context."""
        tmp = tempfile.NamedTemporaryFile(delete=False, suffix=Path(blob_path).suffix)
        self._client.download_fileobj(self.bucket, blob_path, tmp)
        tmp.flush()
        tmp.close()
        return Path(tmp.name)

    async def delete(self, blob_path: str) -> None:
        try:
            await asyncio.to_thread(
                self._client.delete_object,
                Bucket=self.bucket,
                Key=blob_path,
            )
        except ClientError:
            pass
