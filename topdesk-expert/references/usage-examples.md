# Usage Examples

Use this file when the user asks what the skill can do, requests documentation, wants example prompts, or needs a standard output shape.

## Example Prompts

Feature and workflow:

- "Use `$topdesk-expert` to design an incident intake workflow for password reset requests."
- "Use `$topdesk-expert` to compare whether this request belongs in Incident Management or Change Management."
- "Use `$topdesk-expert` to define acceptance criteria for an SSP form."

Schema:

- "Use `$topdesk-expert` to design the database schema for incidents, actions, and SLA history."
- "Use `$topdesk-expert` to review these migrations against TOPdesk data concepts."
- "Use `$topdesk-expert` to create reporting views for incidents and assets."

OData/API:

- "Use `$topdesk-expert` to map this TOPdesk OData metadata to a local schema."
- "Use `$topdesk-expert` to design an idempotent incident sync from TOPdesk."
- "Use `$topdesk-expert` to build a field catalog from these API payloads."

Power BI:

- "Use `$topdesk-expert` to design a Power BI model for TOPdesk incident reporting."
- "Use `$topdesk-expert` to write DAX for SLA compliance, backlog, and reopen rate."
- "Use `$topdesk-expert` to define RLS by branch and operator group."

AI/KI:

- "Use `$topdesk-expert` to design AI ticket classification with operator feedback."
- "Use `$topdesk-expert` to create prompt templates for TOPdesk response suggestions."
- "Use `$topdesk-expert` to design a RAG knowledge assistant for the Self-Service Portal."

Security/testing:

- "Use `$topdesk-expert` to create a DSGVO checklist for AI-generated replies."
- "Use `$topdesk-expert` to write validation tests for a TOPdesk Power BI dashboard."
- "Use `$topdesk-expert` to create a release gate for schema, BI, and AI changes."

## Standard Output Shapes

Schema design output:

1. Assumptions and source of truth.
2. Entity list.
3. Relationships/cardinality.
4. Table fields and constraints.
5. Indexes.
6. Reporting views.
7. Migration and test notes.

Power BI output:

1. Data sources.
2. Fact/dimension model.
3. Relationships.
4. Measures.
5. Report pages.
6. RLS/security.
7. Refresh and validation.

AI/KI output:

1. Use case and risk level.
2. Input data.
3. Prompt/model/rules strategy.
4. Structured output.
5. Human review and confidence thresholds.
6. Audit and privacy controls.
7. Evaluation metrics.

Integration output:

1. Source and target systems.
2. Identity mapping.
3. Payload mapping.
4. Sync mode and idempotency.
5. Error handling.
6. Observability.
7. Tests and reconciliation.

## Good Skill Behavior

- Inspect provided artifacts before generalizing.
- State when exact TOPdesk tenant schema must be verified with OData `$metadata` or API samples.
- Prefer concrete tables, measures, prompts, or acceptance criteria over abstract advice.
- Keep security, audit, and privacy visible in every design that handles tickets, persons, attachments, or AI.
