Decision Log Entries
Initial entries to seed docs/adr/. Each entry locks a decision; future change requires new ADR superseding it.
ADR-001 - MVP wedge: uploaded file workflows only
Field	Detail
Decision	MVP scope is restricted to manual upload of CSV/XLSX/JSON. Connectors (SharePoint, OneDrive, SQL, Power BI) are deferred to V2 / Phase 3.
Rationale	PRD Section 6.1 + 13. Avoid scope creep into generic iPaaS. File-first proves the AI suggestion + transparent step + run loop without integration complexity.
Consequences	No connector framework in MVP. UX shows only file upload sources. Sales messaging is file-centric initially.

ADR-002 - Workflow Definition Schema is the shared contract
Field	Detail
Decision	All threads (frontend, backend, AI, runtime, engine) read/write the same workflow definition. TS types and Python Pydantic models are generated from packages/schema.
Rationale	Schema doc Section 2 + Section 16. Prevents threads from inventing parallel formats. Enforces inspectability.
Consequences	Any change requires schema version bump and regeneration. AI output is validated against schema and rejected if non-conforming.

ADR-003 - Control plane / data plane separation from day one
Field	Detail
Decision	Workers receive a signed run envelope; never read Postgres or call backend.db.* directly. CI enforces this boundary.
Rationale	PROJECT_PLAN Infra Section 3. Required seam for hybrid agent and BYOC (Phase 5). Cheapest to enforce now.
Consequences	Slightly more event plumbing (Service Bus topics + reducer). Backend and worker code physically separated in apps/api and apps/worker.

ADR-004 - Service Bus + simple in-process worker, not Temporal in MVP
Field	Detail
Decision	MVP uses Azure Service Bus topics with KEDA-scaled Container Apps workers. Temporal evaluation moves to V2 when scheduled triggers and long durable workflows arrive.
Rationale	PROJECT_PLAN Infra Section 5. Service Bus + idempotent steps + Postgres run state is sufficient for upload-driven, sub-30-minute runs. Temporal is overhead without payoff at this stage.
Consequences	No automatic workflow-level retries; user reruns manually. Migration path preserved by keeping queue adapter interface and idempotent steps.

ADR-005 - Polars + DuckDB compute kernel; Parquet cache after ingest
Field	Detail
Decision	Engine uses Polars as primary kernel, DuckDB for joins/SQL. Every uploaded file is converted to Parquet after probe; subsequent steps read Parquet.
Rationale	PROJECT_PLAN Engine Section 4.3. Determinism, memory, performance, and portability all favor this. XLSX read cost is paid once.
Consequences	One extra blob write per upload. Final user artifacts remain CSV/XLSX/JSON; intermediate artifacts are Parquet.

ADR-006 - Expression DSL only - no eval, no exec, no user Python in MVP
Field	Detail
Decision	All user-supplied expressions (filter predicates, calculated columns) parsed by Lark grammar -> AST -> Polars expression. No code execution path from workflow JSON.
Rationale	PROJECT_PLAN Engine Section 6.1, Schema Section 16. Required for BYOC viability and security.
Consequences	Limited expressiveness in MVP (arithmetic, string concat, if/else, comparisons, is_null). No regex in DSL, no date arithmetic in MVP. Pro-code steps are Schema Section 17 future extension.

ADR-007 - AI proposes, deterministic backend executes
Field	Detail
Decision	AI generates schema-conformant step JSON only. The data engine executes approved steps with deterministic logic. AI never executes data transformations directly.
Rationale	PRD Section 10, Schema Section 16. Trust requirement; reproducibility requirement.
Consequences	AI service is a suggestion + explanation service, not a data processing service. AI failure modes (invalid JSON, hallucinated columns) are caught by guardrail validator before persistence.

ADR-008 - Linear step list builder in MVP, not node canvas
Field	Detail
Decision	Flow Builder is a 3-pane linear step list. Optional read-only canvas view deferred to V1.
Rationale	UX Spec Section 20 + Open Q1. Most MVP workflows are linear file cleanup. Canvas adds bundle weight, accessibility complexity, and provides little real value.
Consequences	Joins are represented as steps in the list, not visual branches. Canvas-as-edit-surface only with user research evidence.

ADR-009 - Azure-first cloud; Container Apps over AKS in MVP
Field	Detail
Decision	MVP deploys to a single Azure subscription, single region, using Container Apps for frontend, backend, and workers.
Rationale	PROJECT_PLAN Infra Section 2. KEDA built in, scale-to-zero workers, ~30% the operational cost of AKS at this stage.
Consequences	Migration to AKS later if GPU pools, sidecar networking, or replica ceilings demand. Workloads are containerized so migration is straightforward.

ADR-010 - Mock auth in Sprint 1; real auth provider decision deferred to Sprint 2
Field	Detail
Decision	Sprint 1 ships email-only stub auth to unblock the vertical slice. Real provider (Microsoft Entra External ID vs email/password vs both) decided before Sprint 2 starts.
Rationale	PRD Section 16 Q1 is unresolved. Blocking the vertical slice on this decision wastes a sprint.
Consequences	Mock auth is clearly labeled and CI-blocked from prod deployment. Settings/members UI built against real provider in Sprint 2-3.

ADR-011 - RBAC: three roles in MVP (Owner / Editor / Viewer)
Field	Detail
Decision	Workspace member roles in MVP are owner, admin, editor, viewer. Functionally only owner and editor differ; admin = owner alias, viewer = read-only.
Rationale	PROJECT_PLAN Backend Section 3. Sufficient for MVP. Per-resource ACLs and full RBAC are Phase 4.
Consequences	Cannot model viewer-on-one-workflow scenarios. Documented as known limitation.

ADR-012 - 100MB hard cap, 250MB stretch ceiling for MVP file size
Field	Detail
Decision	MVP rejects uploads above 100MB. Engine targets 250MB but does not guarantee. Streaming/out-of-core for >250MB is V1.
Rationale	PRD Section 16 Q2 + PROJECT_PLAN Engine Section 4.4. Keeps MVP in well-understood single-worker regime.
Consequences	Some real customer files will exceed and be blocked at upload with a clear message. Customer feedback drives the V1 raise.
