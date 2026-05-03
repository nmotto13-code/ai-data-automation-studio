import io
import pytest
import pytest_asyncio
import openpyxl
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from adas_api.main import app
from adas_api.db.base import Base
from adas_api.db.session import get_db
from adas_api.storage.local import LocalStorageAdapter
from adas_api.routers.files import _get_storage


@pytest.fixture
def sample_csv_bytes() -> bytes:
    csv_content = "id,name,value\n1,Alice,10.5\n2,Bob,20.0\n3,Charlie,30.0\n"
    return csv_content.encode("utf-8")


@pytest.fixture
def sample_xlsx_bytes() -> bytes:
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.append(["id", "name", "score"])
    ws.append([1, "Alice", 95.5])
    ws.append([2, "Bob", None])
    ws.append([3, "Charlie", 78.0])
    buf = io.BytesIO()
    wb.save(buf)
    buf.seek(0)
    return buf.read()


@pytest_asyncio.fixture
async def async_client(tmp_path):
    # In-memory SQLite test database
    test_engine = create_async_engine("sqlite+aiosqlite:///:memory:", echo=False)
    TestSessionLocal = async_sessionmaker(test_engine, expire_on_commit=False)

    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async def override_get_db():
        async with TestSessionLocal() as session:
            yield session

    test_storage = LocalStorageAdapter(root=str(tmp_path / "storage"))

    def override_get_storage():
        return test_storage

    app.dependency_overrides[get_db] = override_get_db
    app.dependency_overrides[_get_storage] = override_get_storage

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        yield client

    app.dependency_overrides.clear()
    await test_engine.dispose()
