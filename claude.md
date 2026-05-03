# AI Data Automation Studio

## Source of Truth

Read these files before making changes:

- docs/mvp-consolidated-plan.md
- docs/prd.md
- docs/workflow-definition-schema.md
- docs/ux-ui-spec.md
- docs/workflow-definition-schema-v0.1.json
- backlog/sprint-1-plan.md
- decisions/decision-log.md

## MVP Focus

The MVP is uploaded-file AI data automation.

The golden workflow is:
Upload file → profile data → suggest transformations → approve workflow steps → run workflow → output clean file + exception report.

## Rules

- Do not create a new product vision.
- Do not expand into generic RPA.
- Do not build broad connectors first.
- Do not build BYOC first.
- Do not bypass the workflow schema.
- Every transformation must be inspectable.
- AI suggests; deterministic services execute.
- Separate MVP, V1, V2, and Enterprise Later.