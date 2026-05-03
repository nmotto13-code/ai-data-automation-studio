# Developer Setup

## Prerequisites
- Python 3.12+
- Node.js 20+ and pnpm
- uv (Python package manager): `pip install uv`

## Running the engine tests
```bash
cd packages/engine
uv pip install -e ".[test]"
pytest
```

## Running the API tests
```bash
# From repo root — installs both packages in the uv workspace
uv sync
cd apps/api
pytest
```

## Running the smoke tests
```bash
# From repo root
uv pip install -e packages/engine
pytest tests/
```

## Running the full stack locally (no Docker required)
```bash
# Terminal 1 — API
cd apps/api
uv pip install -e .
uvicorn adas_api.main:app --reload --port 8000

# Terminal 2 — Web
cd apps/web
pnpm install
pnpm dev
```

## Running with Docker Compose
```bash
cp .env.example .env
docker compose up
```

## Running the linter
```bash
# Python
ruff check apps/ packages/
# TypeScript
cd apps/web && pnpm lint
```
