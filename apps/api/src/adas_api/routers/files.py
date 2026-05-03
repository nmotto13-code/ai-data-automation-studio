import uuid

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from adas_api.config import settings
from adas_api.db.session import get_db
from adas_api.db.models.file_asset import FileAsset
from adas_api.schemas.file_asset import FileAssetListItem, FileAssetResponse
from adas_api.schemas.profile import DataProfileResponse, ColumnProfileResponse
from adas_api.storage import get_storage_adapter
from adas_api.storage.base import StorageAdapter
from adas_api.services.profile_service import run_profile

router = APIRouter(prefix="/files", tags=["files"])

ALLOWED_EXTENSIONS = {"csv", "xlsx"}


def _get_storage() -> StorageAdapter:
    return get_storage_adapter()


def _build_response(asset: FileAsset) -> FileAssetResponse:
    profile = None
    if asset.schema_snapshot:
        snap = asset.schema_snapshot
        profile = DataProfileResponse(
            row_count=snap["row_count"],
            column_count=snap["column_count"],
            duplicate_row_count=snap["duplicate_row_count"],
            profiled_at=snap["profiled_at"],
            columns=[ColumnProfileResponse(**col) for col in snap["columns"]],
        )
    return FileAssetResponse(
        id=str(asset.id),
        original_filename=asset.original_filename,
        format=asset.format,
        size_bytes=asset.size_bytes,
        status=asset.status,
        profile=profile,
        error_message=asset.error_message,
        created_at=asset.created_at,
    )


@router.post("/", response_model=FileAssetResponse, status_code=status.HTTP_201_CREATED)
async def upload_file(
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_db),
    storage: StorageAdapter = Depends(_get_storage),
):
    ext = (file.filename or "").rsplit(".", 1)[-1].lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(status_code=422, detail=f"Unsupported file type '.{ext}'. Allowed: csv, xlsx")

    content = await file.read()
    if len(content) > settings.max_upload_size_bytes:
        raise HTTPException(status_code=413, detail="File exceeds 100 MB limit")

    file_id = str(uuid.uuid4())
    blob_path = await storage.save(settings.stub_workspace_id, file_id, file.filename or "upload", content)

    asset = FileAsset(
        id=file_id,
        workspace_id=settings.stub_workspace_id,
        original_filename=file.filename or "upload",
        blob_path=blob_path,
        size_bytes=len(content),
        format=ext,
        status="uploaded",
    )
    db.add(asset)
    await db.commit()
    await db.refresh(asset)

    asset = await run_profile(asset, db, storage)
    return _build_response(asset)


@router.get("/", response_model=list[FileAssetListItem])
async def list_files(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(FileAsset).order_by(FileAsset.created_at.desc()))
    assets = result.scalars().all()
    return [FileAssetListItem.model_validate(a) for a in assets]


@router.get("/{file_id}", response_model=FileAssetResponse)
async def get_file(file_id: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(FileAsset).where(FileAsset.id == file_id))
    asset = result.scalar_one_or_none()
    if asset is None:
        raise HTTPException(status_code=404, detail="File not found")
    return _build_response(asset)
