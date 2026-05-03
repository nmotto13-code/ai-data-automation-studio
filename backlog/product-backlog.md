Product Backlog
Backlog items are user/feature-level. Each maps to a thread (subagent) and a sprint phase. M0 = Sprint 1-3 (demo), M1 = Sprint 4-6 (MVP GA).
ID	Title	Phase	Pri	Owner	Description
P-001	Sign in and land in workspace	M0	P0	T2 Backend, T6 Frontend	User signs in, workspace and Default project auto-created on first signup, /me returns user/workspace context.
P-002	Upload CSV/XLSX/JSON to object storage	M0	P0	T2 Backend, T6 Frontend, T7 Storage	Drag/drop or browse upload, presigned URL, direct-to-blob, file_asset record created.
P-003	Profile uploaded data	M0	P0	T3 Data Engine, T6 Frontend	Generate DataProfile; display summary cards, column profile table, issues panel per UX 8.
P-004	AI suggests cleanup plan as schema-conformant steps	M0	P0	T5 AI Assistant, T2 Backend	Given a DataProfile, AI returns ordered list of step JSON validating against workflow-definition-schema-v0.1.json. Every step has ai.generated, ai.confidence, ai.explanation.
P-005	Three-pane Flow Builder with linear step list	M0	P0	T6 Frontend, T1 Schema	Left: step list with reorder/disable/duplicate/delete. Center: data preview. Right: step config + AI assistant.
P-006	Step-level before/after preview	M0	P0	T3 Data Engine, T6 Frontend, T2 Backend	On step selection or param commit, preview endpoint runs the step on sampled data and returns before/after rows + changed-cell map.
P-007	Apply MVP transform set (9 step types)	M0	P0	T3 Data Engine	Implement: rename_columns, cast_types, filter_rows, fill_nulls, find_replace, split_column, merge_columns, calculated_column, remove_duplicates.
P-008	Apply MVP validation set (7 rule types)	M0	P0	T3 Data Engine	Implement: validate_required, validate_type, validate_range, validate_accepted_values, validate_regex, validate_unique, validate_reference_match. Tag failures non-destructively.
P-009	Run workflow asynchronously with 9-state machine	M0	P0	T4 Runtime, T2 Backend, T3 Data Engine	POST /runs publishes execute_workflow command. Worker claims, walks steps, emits events. Backend reduces events into Postgres run state.
P-010	Generate four output artifacts	M0	P0	T3 Data Engine	On run completion produce clean_file (CSV/XLSX), exception_report (XLSX multi-sheet + CSV companion), run_summary (JSON+MD), documentation (MD).
P-011	Run detail page with timeline and download	M0	P0	T6 Frontend, T2 Backend	Display 9-state status header, step timeline with duration/row counts, artifacts panel, AI failure explanation when applicable.
P-012	Save workflow and rerun on new file	M0	P0	T2 Backend, T6 Frontend	Publish draft -> immutable workflow_version. Saved workflow detail page has 'Rerun on new file' drop zone.
P-013	Cancel queued or running workflows	M0	P1	T4 Runtime, T2 Backend	POST /runs/:id/cancel sets cancel intent; worker checks Redis flag between steps and emits cancelled event.
P-014	Plain-language failure explanations	M1	P1	T5 AI Assistant, T6 Frontend	POST /ai/explain-failure: given run_id, return cause + suggested fix as a draft step or schema alias.
P-015	Audit event skeleton on every state change	M0	P1	T7 Storage/Security, T2 Backend	Append-only audit_event row per state-changing action: workflow create/edit/publish/archive, run create/cancel/retry, file upload/delete, AI suggestion accept/reject, member invite.
P-016	Run history (workspace-wide)	M1	P1	T6 Frontend, T2 Backend	GET /runs returns paginated workspace runs with state, workflow, started_at, duration, row counts.
P-017	Empty / loading / error states for all MVP screens	M1	P1	T6 Frontend	Per UX 16 defaults: every MVP screen ships with empty, loading, error states; error messages follow what-cause-action contract.
P-018	Accessibility pass (WCAG 2.1 AA floor)	M1	P1	T6 Frontend	Keyboard navigation across builder, modals, drawers, DataGrid; screen-reader labels; focus management; reduced-motion respect.
P-019	Auto-generated workflow documentation artifact	M1	P2	T3 Data Engine, T5 AI Assistant	documentation.md generated from workflow definition + step logs. Engine emits structured facts; AI service composes prose.
P-020	Settings: profile, workspace, members, API keys (read-only)	M1	P2	T6 Frontend, T2 Backend	Four sub-pages per UX 6. Members: invite, three-role assign. API keys: list + generate, no edit/delete in MVP.

Per-item acceptance criteria, dependencies, and risks
P-001 - Sign in and land in workspace
Field	Detail
Acceptance criteria	User completes login; /me returns workspace_id, role; Default project visible in /flows.
Dependencies	T7 auth provider decision
Risks	Auth provider open question (PRD 16) blocks endpoint shape

P-002 - Upload CSV/XLSX/JSON to object storage
Field	Detail
Acceptance criteria	Files <100MB upload; metadata persists; 10-row preview shown pre-finalize; sheet selector for XLSX.
Dependencies	Storage abstraction, Postgres schema
Risks	XLSX parsing slow; unsupported encodings

P-003 - Profile uploaded data
Field	Detail
Acceptance criteria	Profile completes <10s for files <100MB; UX 8 panels render; profile cached on file_asset.
Dependencies	P-002, queue worker
Risks	Mixed-format date detection accuracy; large XLSX memory

P-004 - AI suggests cleanup plan as schema-conformant steps
Field	Detail
Acceptance criteria	AI output passes JSON Schema validation 100%; non-conforming output is rejected, never persisted; suggestions visible in UI within 15s of profile completion.
Dependencies	P-003, Schema v0.1.1
Risks	LLM produces invalid JSON; provider TBD blocks integration

P-005 - Three-pane Flow Builder with linear step list
Field	Detail
Acceptance criteria	Builder renders MVP step types; drag-reorder works; keyboard shortcuts (J/K/Enter/D) supported; autosave 800ms debounce.
Dependencies	P-002, P-003, P-004
Risks	Three-pane layout under 1024px; bundle size

P-006 - Step-level before/after preview
Field	Detail
Acceptance criteria	Preview returns <5s for <=1000 rows; changed cells highlighted (color + icon); destructive steps require confirmation modal.
Dependencies	P-005
Risks	Heavy steps tie up API workers; mitigate w/ row cap + timeout

P-007 - Apply MVP transform set (9 step types)
Field	Detail
Acceptance criteria	Each step type implemented with Pydantic params model; idempotent; covered by golden-file tests.
Dependencies	P-005, expression DSL parser
Risks	calculated_column DSL scope creep

P-008 - Apply MVP validation set (7 rule types)
Field	Detail
Acceptance criteria	All 7 rules tag rows via __validation_failures column; on_error routing honored; max_failures circuit breaker triggers awaiting_approval.
Dependencies	P-007
Risks	Reference table lifecycle; needs T1+T2 alignment

P-009 - Run workflow asynchronously with 9-state machine
Field	Detail
Acceptance criteria	Run transitions through created -> queued -> running -> succeeded|warning|failed; cancel works; SSE delivers state changes <2s.
Dependencies	P-007, P-008, Service Bus, run envelope contract
Risks	Worker pod restart mid-run; idempotency

P-010 - Generate four output artifacts
Field	Detail
Acceptance criteria	All four artifacts written to blob; references stored in artifact table; signed URLs <1 hour TTL.
Dependencies	P-009
Risks	Exception report sheet size cap (100K rows)

P-011 - Run detail page with timeline and download
Field	Detail
Acceptance criteria	Run page reflects all 9 states; logs drawer reveals technical detail on demand; downloads work via signed URL.
Dependencies	P-009, P-010
Risks	SSE flakiness on slow networks

P-012 - Save workflow and rerun on new file
Field	Detail
Acceptance criteria	Run record references frozen workflow_version_id; rerun starts when columns match; mismatch shows plain-language block message.
Dependencies	P-009
Risks	Schema-mismatch UX must not feel like a wall

P-013 - Cancel queued or running workflows
Field	Detail
Acceptance criteria	Cancel works during queued/profiling/running states; partial artifacts retained; UI reflects cancelled state.
Dependencies	P-009
Risks	Cancel between steps only; long single steps not cancellable

P-014 - Plain-language failure explanations
Field	Detail
Acceptance criteria	Failure drawer shows what happened, likely cause, one concrete action; fix is created as new draft version, never edits the failed run.
Dependencies	P-011
Risks	AI hallucination on causes; must ground on actual error context

P-015 - Audit event skeleton on every state change
Field	Detail
Acceptance criteria	Every action above produces exactly one audit row; admin GET /audit-events returns workspace-scoped list.
Dependencies	Postgres schema
Risks	Audit volume; needs index on (workspace_id, created_at)

P-016 - Run history (workspace-wide)
Field	Detail
Acceptance criteria	Sortable, filterable by state and workflow; links to run detail; paginated >50 results.
Dependencies	P-009
Risks	Pagination/filter perf if runs grow

P-017 - Empty / loading / error states for all MVP screens
Field	Detail
Acceptance criteria	All 10 MVP screens pass UX-team review; no raw stack traces visible; per-pane error boundaries in builder.
Dependencies	P-005, P-011, P-012
Risks	Scope creep into illustrations

P-018 - Accessibility pass (WCAG 2.1 AA floor)
Field	Detail
Acceptance criteria	Pass keyboard-only walkthrough of golden user flow; AI accent purple verified at 4.5:1; live regions on run status.
Dependencies	P-005, P-011
Risks	DataGrid virtualization with NVDA/VoiceOver

P-019 - Auto-generated workflow documentation artifact
Field	Detail
Acceptance criteria	Each run produces documentation artifact describing inputs, steps, validations, outputs; downloadable.
Dependencies	P-009, P-010
Risks	AI generates inaccurate prose; must constrain to engine facts

P-020 - Settings: profile, workspace, members, API keys (read-only)
Field	Detail
Acceptance criteria	Owner can invite Editor or Viewer; new member receives invite; basic profile rename works.
Dependencies	P-001, P-015
Risks	Email delivery dependency
