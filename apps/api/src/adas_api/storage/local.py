import aiofiles
from pathlib import Path

from adas_api.config import settings
from adas_api.storage.base import StorageAdapter


class LocalStorageAdapter(StorageAdapter):
    def __init__(self, root: str | None = None):
        self.root = Path(root or settings.storage_root)

    async def save(self, workspace_id: str, file_id: str, filename: str, content: bytes) -> str:
        dir_path = self.root / workspace_id
        dir_path.mkdir(parents=True, exist_ok=True)
        blob_path = f"{workspace_id}/{file_id}_{filename}"
        abs_path = self.root / workspace_id / f"{file_id}_{filename}"
        async with aiofiles.open(abs_path, "wb") as f:
            await f.write(content)
        return blob_path

    def get_local_path(self, blob_path: str) -> Path:
        return (self.root / blob_path).resolve()

    async def delete(self, blob_path: str) -> None:
        path = self.root / blob_path
        if path.exists():
            path.unlink()
