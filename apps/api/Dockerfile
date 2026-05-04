FROM python:3.12-slim

WORKDIR /app

COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv
ENV UV_SYSTEM_PYTHON=1

# Install engine package first (better layer caching)
COPY packages/engine /app/packages/engine
RUN uv pip install --no-cache /app/packages/engine

# Install API dependencies
COPY pyproject.toml /app/pyproject.toml
COPY src /app/src
RUN uv pip install --no-cache -e .
COPY alembic /app/alembic
COPY alembic.ini /app/alembic.ini

ENV PORT=8000

CMD alembic upgrade head && uvicorn adas_api.main:app --host 0.0.0.0 --port ${PORT}
