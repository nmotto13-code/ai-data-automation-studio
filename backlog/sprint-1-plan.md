Sprint 1 Plan
Sprint 1 is two weeks. Goal: smallest useful vertical slice that proves the contract chain (UI -> Backend -> Schema -> Engine) works end-to-end. We do NOT try to ship every step type or every screen.
Sprint goal
A user can sign in with mock auth, upload a CSV, see a real data profile, and get a workflow with two AI-suggested steps (rename_columns + cast_types) - viewable in the builder, but no run yet.
Why this slice
This slice exercises the full contract chain (frontend types from JSON Schema, backend writes to Postgres, schema validation on every write, engine produces a real DataProfile, AI returns valid step JSON) without the complexity of execution. Run/artifacts/save/rerun all wait for Sprint 2-3.
Deliverables
•	Schema v0.1.1 reconciled (doc + JSON enums aligned, destructive flag specified).
•	Monorepo scaffolded with apps/web (Next.js), apps/api (FastAPI), packages/engine (Python), packages/schema (canonical JSON + generated types).
•	Dev Azure environment provisioned (Postgres, Blob, Key Vault, Container Apps, App Insights).
•	Mock auth: email-only stub login. Real auth provider deferred to Sprint 2 once decision lands.
•	CSV upload to Blob via presigned URL; file_asset row in Postgres.
•	Profile worker that reads CSV, produces DataProfile JSON, writes to file_asset.schema_snapshot.
•	Frontend: /login (mock), /home, upload modal, AI Data Profile screen rendering real DataProfile.
•	AI service: profile -> 2 step types (rename_columns, cast_types) returned as schema-valid JSON.
•	Workflow draft creation on upload finalize; draft visible in 3-pane Flow Builder shell (no execution).
•	CI: schema conformance test + tenancy unit test.
Tasks by workstream
Schema (T1):
•	Reconcile schema doc + JSON file: enum step.type, add destructive flag, lock output_ref chain rules.
•	Publish v0.1.1 to packages/schema with 3 example workflow fixtures.
•	Generate TS types via json-schema-to-typescript and publish in packages/schema.
Backend (T2):
•	FastAPI scaffold (B-01).
•	Migration 0001-0002: workspace, app_user, workspace_member, audit_event, file_asset (B-02, B-06).
•	Mock auth + /me + tenancy middleware (B-03 stub, B-04).
•	Storage adapter interface + Azure Blob impl (B-05).
•	Upload endpoints: presigned URL + finalize (B-07).
•	Queue adapter interface + Service Bus impl (B-08, profile command only).
•	JSON Schema validator wired in (B-09).
•	Migration 0003 + workflow draft creation on finalize (B-10, B-12 minimal).
Frontend (T6):
•	Next.js scaffold + Tailwind + shadcn (F-01).
•	Generate TS types from schema (F-02).
•	MSW mock server with schema fixtures (F-03).
•	/login (mock) + /home shell (F-04).
•	Upload modal w/ dropzone + 10-row preview (F-05).
•	AI Data Profile screen rendering real profile (F-06 v1: summary cards + column profile table only; issues panel + AI panel scaffold).
•	Flow Builder shell with empty step list (F-07 scaffold only).
Data Engine (T3):
•	adas-engine package skeleton w/ run_workflow entry point (D-01).
•	Dataset envelope + step registry (D-02).
•	fsspec I/O adapter for Azure Blob (D-03).
•	CSV reader with probe + ingest (D-04).
•	profile_data step: minimum viable DataProfile (rows, columns, types, nulls, duplicates, samples) (D-09 v1).
•	Profile worker entry point that consumes Service Bus message + writes profile back.
AI Engine (T5):
•	LLM provider integration (interim: OpenAI direct with API key in Key Vault; revisit Azure OpenAI in Sprint 2) (A-01).
•	Prompt: DataProfile -> rename_columns + cast_types steps only (A-02 v1).
•	JSON Schema validation on AI output + retry-on-invalid (A-03, A-06).
•	Confidence + explanation populated for each step (A-04).
Infrastructure (T7 + T4):
•	Provision dev environment: VNet, Postgres, Blob, Key Vault, Service Bus, Container Apps, ACR, Log Analytics (I-01 through I-10).
•	Provider interfaces (I-13).
•	Run envelope + SAS helper (I-14).
•	OTel exporter wired (I-15).
•	CI guardrail: workers cannot import backend DB modules (I-16).
Testing (T8):
•	Acceptance test for FR-002 (upload), FR-003 (profile), FR-004 (AI suggestion) (Q-01 partial).
•	JSON Schema conformance test harness (Q-03).
•	Tenancy isolation tests for workspace + file_asset (Q-04 partial).
Acceptance criteria for Sprint 1
•	CSV file <10MB uploads end-to-end and DataProfile renders in UI within 15 seconds.
•	AI suggestions return at least one valid rename_columns or cast_types step that passes JSON Schema validation.
•	100% of AI outputs that fail validation are rejected and never persisted.
•	CI pipeline green: schema conformance + tenancy tests + lint + type check.
•	Workers do not import backend.db.* (CI-enforced).
•	Dev environment runs with all secrets in Key Vault, no env-file leaks.
Dependencies
•	LLM provider decision required by start of Sprint 1 day 3, or AI work blocks.
•	Azure subscription provisioned before Sprint 1 day 1.
•	Schema v0.1.1 must land in packages/schema by Sprint 1 day 3 or frontend + backend type generation blocks.
Risks
•	Azure provisioning delay (mitigation: backend + frontend devs use local Postgres + Azurite + Service Bus emulator until I-01 to I-10 complete).
•	AI returns invalid schema repeatedly (mitigation: constrained generation + retry; if still failing, ship with rule-based fallback for Sprint 1 demo).
•	Three-pane Flow Builder under-1024px collapse (mitigation: ship as scaffold only in Sprint 1; require >=1024px).
Stop conditions
Halt sprint and re-plan if any of the following occur:
•	AI cannot reliably produce schema-valid output after 3 days of constrained-generation work. Re-plan to defer AI suggestions to Sprint 2 and ship rule-based suggestions for Sprint 1 demo.
•	Schema reconciliation reveals a fundamental contract conflict that requires a new minor version (v0.2). Pause downstream work, resolve schema, restart frontend/backend type generation.
•	Azure region availability blocks Container Apps + Azure OpenAI co-location. Re-plan region in Decision Log.
•	Worker -> backend.db boundary violation discovered in code review. Halt and refactor before any further worker work.
