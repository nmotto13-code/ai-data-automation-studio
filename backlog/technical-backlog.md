Technical Backlog
Implementation tasks per workstream. Sized S (<=1 week), M (1-3 weeks), L (3-6 weeks). Ordered by dependency.
Backend (T2)
ID	Task	Size	Maps to
B-01	FastAPI scaffold + Pydantic v2 + Alembic + Dockerfile + CI	S	Foundations
B-02	Migration 0001: workspace, app_user, workspace_member, audit_event	S	P-001, P-015
B-03	Auth provider integration + session + GET /me	M	P-001
B-04	Tenancy middleware + role enforcement utility	S	All endpoints
B-05	Storage adapter interface; Azure Blob + local-fs impl	M	P-002
B-06	Migration 0002: file_asset	S	P-002
B-07	POST /files/upload-url, POST /files/:id/finalize, list/get/delete	M	P-002
B-08	Queue adapter interface; Service Bus impl	M	P-009
B-09	JSON Schema validator wired to workflow-definition-schema-v0.1.json	S	P-004
B-10	Migration 0003: project, workflow, workflow_version	S	P-005, P-012
B-11	Project CRUD + auto-create Default project on workspace creation	S	P-001
B-12	Workflow + version CRUD; draft/publish lifecycle; validation on every write	L	P-005, P-012
B-13	Step preview service + endpoint with row cap and timeout	M	P-006
B-14	Migration 0004: run, run_step_log, artifact	S	P-009
B-15	POST /runs, internal worker endpoints, run state machine, SSE event stream	L	P-009
B-16	Artifact download presigned URL endpoint	S	P-010
B-17	Migration 0005: ai_suggestion	S	P-004
B-18	AI service: profile suggestions + transform plan + suggestion lifecycle endpoints + guardrail validator	L	P-004
B-19	AI service: explain failure	M	P-014
B-20	Run cancel + retry endpoints	S	P-013
B-21	Audit writes wired across all state-changing services	M	P-015
B-22	Admin endpoints: list members, invite	S	P-020
B-23	Rate limiting middleware (per workspace; tighter on /ai/* and POST /runs)	S	Hardening
B-24	Integration tests: tenancy isolation, JSON Schema conformance, run state transitions, AI guardrail rejection	M	QA
B-25	Observability: structured logs, request IDs, per-run trace correlation, basic metrics	M	T7

Frontend (T6)
ID	Task	Size	Maps to
F-01	Next.js 14+ app router + TypeScript strict + shadcn/ui + Tailwind tokens	S	Foundations
F-02	Generate TS types from workflow-definition-schema-v0.1.json	S	Schema contract
F-03	MSW mock server seeded from schema fixtures	S	Unblocks UX work
F-04	Auth + login + /home shell with sidebar/topbar	M	P-001
F-05	Upload modal: dropzone, sheet selector, 10-row preview	M	P-002
F-06	AI Data Profile screen: summary cards, column profile table, issues panel, AI recommendations panel	L	P-003, P-004
F-07	Three-pane Flow Builder scaffold: step list, preview pane, config pane, AI assistant tab	L	P-005
F-08	Step config forms keyed by step type (start with rename_columns, filter_rows, validate_required)	M	P-005, P-007
F-09	Before/After Preview component (DataGrid pair w/ changed-cell map)	M	P-006
F-10	Run trigger + Run Detail page (status header, timeline, artifacts panel)	L	P-011
F-11	SSE useRunStatus hook with 2s polling fallback	S	P-011
F-12	Saved Workflow Detail with rerun-on-new-file drop zone	M	P-012
F-13	Schema mismatch dialog (MVP: block run, name missing columns)	S	P-012
F-14	AI Failure Drawer	M	P-014
F-15	Settings sub-pages: profile, workspace, members, API keys	M	P-020
F-16	Empty/loading/error states across all MVP screens	M	P-017
F-17	Accessibility audit + keyboard shortcuts + live regions	M	P-018
F-18	Bundle splitting: lazy-load step config modules + AI panel	S	Perf

Data Engine (T3)
ID	Task	Size	Maps to
D-01	Engine package skeleton (adas-engine) with run_workflow entry point	S	Foundations
D-02	Dataset envelope, step registry, workflow JSON loader/validator	M	Engine M1
D-03	fsspec I/O adapter (Azure Blob + local)	S	Portability
D-04	CSV reader with probe + ingest phases	M	P-002
D-05	XLSX reader + Parquet cache writer	M	P-002
D-06	JSON reader (records + ndjson + nested)	S	P-002
D-07	Run state machine + event emission	M	P-009
D-08	Implement rename_columns, cast_types (golden-file tests)	M	P-007
D-09	profile_data step: full DataProfile output	L	P-003
D-10	Sensitive-field detection (regex catalog + column heuristics)	S	P-003
D-11	Implement filter_rows, fill_nulls, find_replace, remove_duplicates	M	P-007
D-12	Expression DSL (Lark grammar -> AST -> Polars expression)	L	P-007
D-13	Implement calculated_column, split_column, merge_columns, standardize_dates	M	P-007
D-14	Validation tagging model + 7 validate_* steps	L	P-008
D-15	Exception report writer (XLSX multi-sheet + CSV companion)	M	P-010
D-16	on_error routing + max_failures circuit breaker	M	P-008
D-17	Run summary writer (JSON + Markdown)	S	P-010
D-18	DuckDB integration via Arrow	M	Joins
D-19	Implement join_datasets, lookup_reference, validate_reference_match, union_files	M	P-007, P-008
D-20	Output writers for clean files (CSV/XLSX/JSON)	S	P-010
D-21	Documentation artifact emitter (structured facts)	S	P-019
D-22	Determinism guarantees + memory instrumentation	M	Hardening
D-23	Performance benchmark suite + CI gate	M	QA
D-24	Property-based tests for transforms	M	QA

AI Engine (T5)
ID	Task	Size	Maps to
A-01	LLM provider integration (decision: Azure OpenAI vs OpenAI direct - see Open Questions)	M	Foundations
A-02	Prompt: profile -> step suggestions, constrained to JSON Schema	L	P-004
A-03	Constrained generation strategy + retry-on-invalid-schema	M	P-004
A-04	Confidence + explanation field population logic	M	P-004
A-05	Risk classification: destructive flag + risk_level computation	M	Schema 16
A-06	Server-side AI guardrail validator (schema + policy)	M	P-004
A-07	Prompt: user intent -> single step (transform plan)	M	P-004
A-08	Prompt: failure context -> plain-language explanation + draft fix	L	P-014
A-09	Prompt: workflow definition + run logs -> documentation prose	M	P-019
A-10	Cost telemetry per request (tokens in/out, model, run_id)	S	Ops
A-11	AI provenance preservation across workflow versions	S	Schema 14
A-12	Prompt eval harness with golden inputs/outputs	M	QA

Infrastructure (T7 + T4)
ID	Task	Size	Maps to
I-01	Provision dev Azure subscription, RG, VNet, subnets, private DNS	M	Foundations
I-02	Log Analytics workspace + Application Insights (dev)	S	Observability
I-03	Key Vault (dev) RBAC mode + soft delete	S	Secrets
I-04	Azure Container Registry + GitHub Actions OIDC federation	S	CI/CD
I-05	Postgres Flexible Server (Burstable B2s) + private endpoint	M	Metadata
I-06	Azure Blob Storage account + containers + lifecycle policies + private endpoint	M	Files
I-07	Service Bus namespace + topics + subscriptions with filters	M	Queue
I-08	Redis Basic C0	S	Cache
I-09	Container Apps Environment (control plane: frontend + backend)	M	Compute
I-10	Container Apps Environment (workers, separate)	M	Compute
I-11	Managed identities + Key Vault role assignments	S	Security
I-12	KEDA scalers: HTTP for API/UI, Service Bus depth for workers	M	Scaling
I-13	Provider interfaces: Storage, Secrets, Queue, Telemetry (shared lib)	M	Portability
I-14	Run envelope schema + SAS-issuance helper	M	Data plane isolation
I-15	OTel SDK in backend + workers, exporting to App Insights	M	Observability
I-16	CI guardrail: fail build if worker imports backend DB modules	S	Boundary enforcement
I-17	Diagnostic settings on every resource -> Log Analytics	S	Observability
I-18	MVP alert rules (API 5xx, worker DLQ, Postgres CPU, Blob throttling, run failure rate, KV access)	M	Ops
I-19	Runbooks: stuck run, DLQ triage, Postgres failover, secret rotation	M	Ops
I-20	Staging environment as scaled-down clone of dev	M	Pre-prod
I-21	Prod environment skeleton (not public until launch)	M	Pre-launch

Testing (T8)
ID	Task	Size	Maps to
Q-01	Acceptance test plan for FR-001 through FR-010	M	PRD coverage
Q-02	Golden-file fixtures: input file + expected workflow JSON + expected outputs	M	Engine M1
Q-03	JSON Schema conformance test harness	S	Schema enforcement
Q-04	Tenancy isolation integration tests	M	Security floor
Q-05	Run state machine transition tests	M	P-009
Q-06	AI guardrail rejection tests (invalid schema, destructive without flag)	M	P-004
Q-07	Exception report validation: routing rules vs failure rules	M	P-008, P-010
Q-08	End-to-end golden user flow Playwright test	L	MVP gate
Q-09	Performance regression suite (engine benchmarks)	M	Engine M5
Q-10	Accessibility audit (axe + keyboard walkthrough)	M	P-018
