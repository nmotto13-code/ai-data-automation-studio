import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_health(async_client: AsyncClient):
    response = await async_client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


@pytest.mark.asyncio
async def test_upload_csv_success(async_client: AsyncClient, sample_csv_bytes: bytes):
    response = await async_client.post(
        "/api/v1/files/",
        files={"file": ("test_data.csv", sample_csv_bytes, "text/csv")},
    )
    assert response.status_code == 201
    body = response.json()
    assert body["status"] == "profiled"
    assert body["profile"] is not None
    assert body["profile"]["row_count"] > 0


@pytest.mark.asyncio
async def test_upload_xlsx_success(async_client: AsyncClient, sample_xlsx_bytes: bytes):
    response = await async_client.post(
        "/api/v1/files/",
        files={
            "file": (
                "test_data.xlsx",
                sample_xlsx_bytes,
                "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            )
        },
    )
    assert response.status_code == 201
    body = response.json()
    assert body["status"] == "profiled"
    assert body["profile"] is not None


@pytest.mark.asyncio
async def test_upload_invalid_extension(async_client: AsyncClient):
    response = await async_client.post(
        "/api/v1/files/",
        files={"file": ("report.pdf", b"%PDF-1.4 fake content", "application/pdf")},
    )
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_upload_too_large(async_client: AsyncClient):
    # Create content slightly over 100 MB
    oversized_content = b"x" * (100 * 1024 * 1024 + 1)
    response = await async_client.post(
        "/api/v1/files/",
        files={"file": ("big_file.csv", oversized_content, "text/csv")},
    )
    assert response.status_code == 413


@pytest.mark.asyncio
async def test_get_file_by_id(async_client: AsyncClient, sample_csv_bytes: bytes):
    # Upload first
    upload_response = await async_client.post(
        "/api/v1/files/",
        files={"file": ("test_data.csv", sample_csv_bytes, "text/csv")},
    )
    assert upload_response.status_code == 201
    file_id = upload_response.json()["id"]

    # Retrieve by ID
    get_response = await async_client.get(f"/api/v1/files/{file_id}")
    assert get_response.status_code == 200
    body = get_response.json()
    assert body["id"] == file_id
    assert body["profile"] is not None


@pytest.mark.asyncio
async def test_get_file_not_found(async_client: AsyncClient):
    response = await async_client.get("/api/v1/files/nonexistent-uuid")
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_list_files(async_client: AsyncClient, sample_csv_bytes: bytes, sample_xlsx_bytes: bytes):
    # Upload two files
    await async_client.post(
        "/api/v1/files/",
        files={"file": ("first.csv", sample_csv_bytes, "text/csv")},
    )
    await async_client.post(
        "/api/v1/files/",
        files={
            "file": (
                "second.xlsx",
                sample_xlsx_bytes,
                "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            )
        },
    )

    # List all files
    list_response = await async_client.get("/api/v1/files/")
    assert list_response.status_code == 200
    items = list_response.json()
    assert len(items) == 2
