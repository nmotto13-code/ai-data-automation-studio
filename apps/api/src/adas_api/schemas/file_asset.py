from datetime import datetime

from pydantic import BaseModel

from adas_api.schemas.profile import DataProfileResponse


class FileAssetResponse(BaseModel):
    id: str
    original_filename: str
    format: str
    size_bytes: int
    status: str
    profile: DataProfileResponse | None = None
    error_message: str | None = None
    created_at: datetime

    model_config = {"from_attributes": True}


class FileAssetListItem(BaseModel):
    id: str
    original_filename: str
    format: str
    size_bytes: int
    status: str
    created_at: datetime

    model_config = {"from_attributes": True}
