FROM python:3.12-slim

WORKDIR /app

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv
ENV UV_SYSTEM_PYTHON=1

# Copy and install engine package first (better layer caching)
COPY packages/engine /app/packages/engine
RUN uv pip install --no-cache /app/packages/engine

# Copy and install API package
COPY apps/api/pyproject.toml /app/pyproject.toml
RUN uv pip install --no-cache -e .

# Copy application source
COPY apps/api/src /app/src
COPY apps/api/alembic /app/alembic
COPY apps/api/alembic.ini /app/alembic.ini

# Railway injects PORT env var
ENV PORT=8000

CMD alembic upgrade head && uvicorn adas_api.main:app --host 0.0.0.0 --port ${PORT}
