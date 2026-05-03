from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    database_url: str = "sqlite+aiosqlite:///./dev.db"
    storage_root: str = "./storage"
    stub_workspace_id: str = "00000000-0000-0000-0000-000000000001"
    cors_origins: list[str] = ["http://localhost:3000"]
    max_upload_size_bytes: int = 100 * 1024 * 1024

    # S3-compatible storage (leave empty to use LocalStorageAdapter)
    s3_bucket: str = ""
    s3_access_key: str = ""
    s3_secret_key: str = ""
    s3_endpoint_url: str = ""   # Set for Cloudflare R2 / Backblaze; leave blank for AWS S3
    s3_region: str = "auto"

    @field_validator("database_url", mode="before")
    @classmethod
    def fix_postgres_scheme(cls, v: str) -> str:
        """Railway provides postgresql:// or postgres:// — SQLAlchemy async needs postgresql+asyncpg://"""
        if v.startswith("postgres://"):
            return v.replace("postgres://", "postgresql+asyncpg://", 1)
        if v.startswith("postgresql://"):
            return v.replace("postgresql://", "postgresql+asyncpg://", 1)
        return v


settings = Settings()
