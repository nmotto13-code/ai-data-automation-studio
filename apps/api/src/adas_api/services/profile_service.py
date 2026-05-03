import json
from pathlib import Path

from sqlalchemy.ext.asyncio import AsyncSession

from adas_api.db.models.file_asset import FileAsset
from adas_api.storage.base import StorageAdapter


async def run_profile(file_asset: FileAsset, db: AsyncSession, storage: StorageAdapter) -> FileAsset:
    """Synchronously profile the file and update the FileAsset row."""
    from adas_engine import profile_file
    from adas_engine.exceptions import FileTooLargeError, UnsupportedFormatError

    file_asset.status = "profiling"
    await db.commit()
    await db.refresh(file_asset)

    try:
        local_path: Path = storage.get_local_path(file_asset.blob_path)
        profile = profile_file(local_path, file_asset.format)
        file_asset.schema_snapshot = json.loads(profile.model_dump_json())
        file_asset.status = "profiled"
    except (FileTooLargeError, UnsupportedFormatError, Exception) as exc:
        file_asset.status = "error"
        file_asset.error_message = str(exc)

    await db.commit()
    await db.refresh(file_asset)
    return file_asset
