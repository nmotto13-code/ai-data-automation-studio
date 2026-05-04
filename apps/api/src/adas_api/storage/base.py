from abc import ABC, abstractmethod
from pathlib import Path


class StorageAdapter(ABC):
    @abstractmethod
    async def save(self, workspace_id: str, file_id: str, filename: str, content: bytes) -> str:
        """Save file bytes and return the blob_path string."""

    @abstractmethod
    def get_local_path(self, blob_path: str) -> Path:
        """Return an absolute local filesystem path the engine can read directly."""

    @abstractmethod
    async def delete(self, blob_path: str) -> None:
        """Delete the file at blob_path."""
