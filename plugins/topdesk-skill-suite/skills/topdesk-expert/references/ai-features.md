# AI/KI Features for TOPdesk

Use this file for AI/KI, ML, LLM, copilot, chatbot, semantic search, prediction, classification, summarization, and automation features around TOPdesk or a custom Topdesk app.

For prompt templates, structured output schemas, RAG chunk metadata, evaluation dataset formats, and feedback-loop details, load `ai-prompts-and-evals.md`.

## Core Principle

Design AI/KI features as assistive and auditable by default. Keep humans in control for customer-visible communication, ticket closure, priority escalation, permission changes, data deletion, and any action with contractual/SLA impact unless the user explicitly designs a controlled automation with approval and rollback.

## Feature Catalog

### Ticket Classification

Predict category, subcategory, service, priority, impact, urgency, branch, and assignment group from incoming text and metadata.

Inputs:

- Brief description, request text, email subject/body, SSP form fields.
- Caller/person, branch, department, location.
- Asset or service selection.
- Historical incident categories and resolution outcomes.

Outputs:

- Suggested category/subcategory.
- Suggested operator group.
- Confidence score and top alternatives.
- Explanation using non-sensitive evidence.

Controls:

- Auto-apply only above a high confidence threshold and only for low-risk categories.
- Require operator confirmation for priority, security, HR, legal, VIP, or major-incident categories.
- Log accepted/overridden suggestions for retraining and quality reporting.

### Smart Routing

Route tickets to operator groups based on classification, workload, skills, branch, language, service, SLA risk, and historical resolution patterns.

Required data:

- Operator groups, active operators, category ownership.
- Historical assignment and reassignment history.
- SLA targets, breach risk, business calendar.
- Exclusion rules for sensitive tickets.

Acceptance criteria:

- Reduce reassignment rate.
- Do not increase SLA breaches.
- Provide a fallback group when confidence is low.
- Record why a route was suggested or applied.

### Response Suggestions

Generate draft replies for operators based on the ticket, known solutions, linked assets, previous actions, and knowledge articles.

Rules:

- Mark generated text as draft.
- Include cited knowledge items or source snippets when possible.
- Avoid inventing policy, dates, prices, contract details, or resolution status.
- Never send externally without operator confirmation unless an approved template and deterministic rule applies.

### Ticket Summaries

Summarize long incident/action histories for handoff, escalation, or closure.

Good summary fields:

- User problem.
- Environment/asset/service.
- Timeline of important actions.
- Current status and blocker.
- Next recommended action.
- Customer-visible vs internal-only notes separated.

Guardrail:

- Do not mix private operator notes into customer-facing summaries.

### Knowledge Article Suggestions

Detect repeated incidents and propose new or improved knowledge items.

Signals:

- High ticket volume for a category.
- Repeated resolution text.
- Frequent operator search terms.
- Incidents resolved by similar actions.
- Reopen rate after a known resolution.

Outputs:

- Draft title, summary, steps, affected service/assets, tags, visibility, owner, review date.
- Source ticket list for reviewer validation.

### Semantic Search

Search across knowledge items, incidents, changes, assets, and manuals by meaning rather than exact keyword match.

Implementation notes:

- Chunk long articles/actions by section or action entry.
- Store embeddings with source ID, source type, visibility, branch restriction, language, and last modified timestamp.
- Apply permissions before retrieval and again before displaying results.
- Return source links/citations, not only generated answers.

### Chatbot / Self-Service Assistant

Help end users create tickets, find knowledge items, check status, or complete guided service requests.

Required controls:

- Authenticate before showing personal tickets or branch-restricted data.
- Escalate to a human or create an incident when confidence is low.
- Keep a clear distinction between answering a question and performing an action.
- Use form-based confirmation before creating/updating a ticket.

### Duplicate Detection

Find similar open incidents or known major incidents during intake.

Signals:

- Similar description/request text.
- Same branch, service, asset, category, error code, or time window.
- Known major incident or outage link.

Outputs:

- Candidate duplicates with similarity score and reason.
- Link suggestion, not automatic merge, unless business rules allow it.

### Predictive Insights

Predict SLA breach risk, expected resolution time, major-incident candidates, backlog growth, or asset failure clusters.

Inputs:

- Incident age, priority, category, group, actions, reassignment count.
- SLA target and business calendar.
- Current queue load and historical resolution times.
- Asset/service/branch incident history.

Outputs:

- Risk score, top drivers, recommended mitigation.
- Power BI measures or model outputs for monitoring.

## Data Contracts

For each AI/KI feature, define:

| Area | Required definition |
| --- | --- |
| Input data | Tables/entities, fields, refresh frequency, retention |
| Output data | Suggested value, confidence, explanation, source references |
| Action mode | Suggest-only, require approval, or auto-apply |
| Audit | Who/what generated it, prompt/model/version, timestamp, accepted/overridden |
| Security | PII fields, branch/customer restrictions, operator-only notes |
| Evaluation | Accuracy, precision/recall, acceptance rate, time saved, SLA impact |

Recommended AI tables for a custom app:

- `ai_suggestions`: generic suggestion records for category, routing, reply, summary, duplicate, or SLA risk.
- `ai_suggestion_feedback`: accepted, rejected, edited, override reason, operator ID.
- `ai_prompt_runs`: prompt/model/version, input references, output references, token/cost metadata when applicable.
- `ai_embeddings`: source type, source ID, chunk ID, embedding vector reference, visibility, last indexed timestamp.
- `ai_evaluation_results`: test set, metric, score, model/prompt version, evaluation timestamp.

Do not store raw prompts containing unnecessary PII when a reference to the source ticket is enough.

## Prompt and Model Guidance

- Use deterministic rules for simple routing/classification when rules are transparent and reliable.
- Use supervised ML or LLM classification when categories are numerous, text-heavy, or inconsistent.
- Use retrieval-augmented generation for replies and knowledge answers. Do not answer from the model alone when policy or support accuracy matters.
- Include allowed output schema and confidence fields in prompts.
- Keep prompts tenant-specific only through retrieved context and configuration, not hard-coded secrets.
- Version prompts like application code.

Example structured output:

```json
{
  "suggestion_type": "incident_classification",
  "category": "Workplace > Hardware",
  "assignment_group": "Servicedesk Hardware",
  "confidence": 0.87,
  "alternatives": [
    {"category": "Workplace > Accessories", "confidence": 0.42}
  ],
  "reason": "The request mentions a broken laptop screen and asset tag.",
  "requires_human_review": true
}
```

## Safety and Privacy

- Apply TOPdesk/person/branch permissions before sending context to an AI service.
- Minimize PII: caller name, email, phone, address, medical/HR/legal details, and private notes need explicit handling.
- Redact secrets, passwords, tokens, and credentials from ticket text.
- Separate internal notes from public replies.
- Keep model outputs out of audit-sensitive fields unless reviewed.
- Provide a manual override path for every AI-applied value.
- Make generated content traceable to source records and model/prompt versions.

For broader DSGVO/GDPR, PII, audit, permission, and governance requirements, load `security-compliance.md`.

## Evaluation Checklist

Before release:

- Build a test set from historical tickets with accepted categories, assignment groups, and outcomes.
- Measure top-1 and top-3 classification accuracy.
- Measure routing reassignment rate before and after.
- Review false positives for sensitive categories.
- Test multilingual tickets if the tenant uses multiple languages.
- Test short/noisy tickets, email signatures, attachments missing, and incomplete caller data.
- Verify row-level and branch-level security in semantic search.
- Confirm model behavior when knowledge articles are outdated or contradictory.

Production monitoring:

- Suggestion volume.
- Acceptance and edit rate.
- Override reasons.
- Confidence distribution.
- SLA impact.
- Reassignment rate.
- Deflection rate for chatbot/self-service.
- User/operator satisfaction.
- Data drift by category, branch, language, and channel.

For release gates and regression checklists, load `testing-validation.md`.

## Implementation Pattern

1. Start with suggest-only mode.
2. Store suggestion, confidence, explanation, model/prompt version, and source references.
3. Let operators accept, edit, or reject.
4. Report quality in Power BI.
5. Tighten prompts/rules based on feedback.
6. Allow auto-apply only for low-risk, high-confidence cases with rollback and audit.
