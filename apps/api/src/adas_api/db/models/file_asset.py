import uuid
from datetime import datetime
from typing import Optional

from sqlalchemy import JSON, String, func
from sqlalchemy.orm import Mapped, mapped_column

from adas_api.db.base import Base


class FileAsset(Base):
    __tablename__ = "file_asset"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    workspace_id: Mapped[str] = mapped_column(String, nullable=False)
    original_filename: Mapped[str] = mapped_column(String, nullable=False)
    blob_path: Mapped[str] = mapped_column(String, nullable=False)
    size_bytes: Mapped[int]
    format: Mapped[str] = mapped_column(String, nullable=False)  # "csv" | "xlsx"
    status: Mapped[str] = mapped_column(String, nullable=False, default="uploaded")
    schema_snapshot: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)
    error_message: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(server_default=func.now(), onupdate=func.now())
