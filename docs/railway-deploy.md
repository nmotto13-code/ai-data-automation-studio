# Railway Deployment Guide

## Prerequisites

- Railway account at [railway.app](https://railway.app) — free tier works for MVP validation
- GitHub repo with this code pushed to it
- For file storage: Cloudflare R2 account (free tier: 10 GB storage, zero egress fees) OR AWS S3

---

## Section 1 — Set up Cloudflare R2 (recommended for file storage)

1. Go to your Cloudflare dashboard → **R2** → **Create bucket**
   - Name it `adas-uploads` (or any name; you'll set it as `S3_BUCKET`)
2. Go to **R2** → **Manage R2 API tokens** → **Create API token**
   - Permission: **Object Read & Write** scoped to the bucket you just created
3. Copy and store these values:
   - **Account ID** (visible on the R2 overview page)
   - **Access Key ID**
   - **Secret Access Key**
4. Your R2 endpoint URL will be: `https://<ACCOUNT_ID>.r2.cloudflarestorage.com`

---

## Section 2 — Deploy to Railway

1. Push your code to GitHub (ensure `railway.toml` is committed at the repo root)
2. Go to [railway.app](https://railway.app) → **New Project** → **Deploy from GitHub repo**
3. Select your repository and authorize Railway
4. Railway detects `railway.toml` and creates two services: `api` and `web`
5. Add a Postgres database:
   - Click **+ New** → **Database** → **PostgreSQL**
   - Railway automatically injects `DATABASE_URL` into all services in the project

---

## Section 3 — Configure environment variables

Navigate to each service → **Variables** tab and set the following.

### `api` service

```
S3_BUCKET=adas-uploads
S3_ACCESS_KEY=<your R2 access key id>
S3_SECRET_KEY=<your R2 secret access key>
S3_ENDPOINT_URL=https://<your account id>.r2.cloudflarestorage.com
S3_REGION=auto
CORS_ORIGINS=["https://<your-web-service>.railway.app"]
```

### `web` service

```
NEXT_PUBLIC_API_URL=https://<your-api-service>.railway.app
```

Railway sets `PORT` and `DATABASE_URL` automatically — do not set these manually.

---

## Section 4 — Verify deployment

1. Open the `api` service logs — you should see `alembic upgrade head` succeed followed by uvicorn starting
2. Visit `https://<api>.railway.app/health` → should return `{"status": "ok"}`
3. Visit `https://<web>.railway.app` → should redirect to `/upload`
4. Upload a CSV file → data profile should render in the UI

---

## Section 5 — Custom domains (optional)

Railway → your service → **Settings** → **Networking** → **Custom Domain**

---

## Troubleshooting

| Symptom | Fix |
|---|---|
| `alembic upgrade head` fails on startup | Check `DATABASE_URL` is set and the Postgres service is running and healthy |
| File upload returns 500 error | Verify `S3_BUCKET`, `S3_ACCESS_KEY`, and `S3_SECRET_KEY` are all set; confirm the R2 API token has Object Write permission |
| CORS errors in browser | Ensure `CORS_ORIGINS` on the API service includes the exact web service URL with no trailing slash |
| Frontend shows blank page | Check `NEXT_PUBLIC_API_URL` on the web service points to the correct API service URL |
| `pnpm install --frozen-lockfile` fails in web build | Ensure `pnpm-lock.yaml` is committed to the repo |
