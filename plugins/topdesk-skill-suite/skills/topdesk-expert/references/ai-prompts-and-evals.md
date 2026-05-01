# AI/KI Prompts and Evaluation for TOPdesk

Use this file for prompt templates, structured JSON outputs, RAG architecture, feedback loops, and evaluation datasets.

## Prompt Rules

- Ask for structured JSON when output feeds an app or automation.
- Include allowed category/status/group values rather than letting the model invent them.
- Include "unknown" or "requires_human_review" as valid outputs.
- Require evidence from ticket text or retrieved knowledge.
- Keep public reply drafts separate from internal analysis.

## Classification Prompt Template

```text
You classify TOPdesk incidents. Return only valid JSON.

Allowed categories:
{{categories}}

Allowed operator groups:
{{operator_groups}}

Ticket:
- Brief description: {{brief_description}}
- Request text: {{request_text}}
- Caller branch: {{branch}}
- Source channel: {{source_channel}}
- Linked asset/service: {{asset_or_service}}

Return:
{
  "category_id": string|null,
  "subcategory_id": string|null,
  "assignment_group_id": string|null,
  "priority_hint": "low"|"normal"|"high"|"critical"|"unknown",
  "confidence": number,
  "reason": string,
  "requires_human_review": boolean,
  "sensitive_flags": string[]
}
```

## Response Draft Prompt Template

```text
Draft a customer-visible reply for a TOPdesk incident.

Rules:
- Do not claim the issue is resolved unless the ticket status or operator notes say so.
- Do not include internal notes.
- Cite the knowledge article IDs used.
- If evidence is insufficient, ask one concise clarification question.

Ticket summary:
{{safe_ticket_summary}}

Relevant knowledge:
{{retrieved_knowledge_snippets}}

Return JSON:
{
  "draft_reply": string,
  "knowledge_ids": string[],
  "needs_operator_review": true,
  "risk_flags": string[]
}
```

## Summary Prompt Template

```text
Summarize this TOPdesk incident for operator handoff.

Separate:
1. Customer-visible facts
2. Internal-only notes
3. Timeline
4. Current blocker
5. Recommended next action

Incident actions:
{{actions}}
```

## RAG Architecture

Index sources:

- Published knowledge articles.
- Approved standard solutions.
- Service catalog descriptions.
- Public/manual troubleshooting docs.
- Historical incidents only when privacy and retention rules allow it.

Chunk metadata:

- `source_type`
- `source_id`
- `chunk_id`
- `title`
- `language`
- `visibility`
- `branch_id`
- `category_id`
- `last_modified_at`

Retrieval rules:

- Apply permissions before retrieval.
- Filter by language, branch, visibility, and category when available.
- Return citations and source links.
- Exclude outdated or archived articles unless explicitly requested.

## Evaluation Dataset Format

```json
{
  "case_id": "INC-001",
  "input": {
    "brief_description": "Laptop screen broken",
    "request_text": "My screen cracked after travel.",
    "branch": "Berlin",
    "source_channel": "ssp"
  },
  "expected": {
    "category_id": "workplace.hardware.laptop",
    "assignment_group_id": "hardware-support",
    "requires_human_review": false
  },
  "sensitive_flags": [],
  "notes": "Use for classification regression."
}
```

Metrics:

- Classification top-1 accuracy.
- Classification top-3 accuracy.
- Assignment-group accuracy.
- Precision/recall for sensitive flags.
- Reply hallucination rate.
- Citation coverage.
- Operator acceptance rate.
- Mean edit distance for response drafts.

## Feedback Loop

Capture:

- Suggested value.
- Operator final value.
- Accepted/rejected/edited.
- Override reason.
- Time to decision.
- Confidence score.
- Model/prompt version.

Use feedback to:

- Tune thresholds.
- Improve category descriptions.
- Identify missing knowledge articles.
- Detect drift by branch, language, source channel, or category.
