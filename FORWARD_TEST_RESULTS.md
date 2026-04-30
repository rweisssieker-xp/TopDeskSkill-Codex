# Forward-Test Results

Date: 2026-04-30

## Method

The forward-test prompt pack in `FORWARD_TEST_PROMPTS.md` was reviewed against the current skill inventory. Automated execution of the prompts requires fresh agent runs, so this file records readiness checks and expected validation criteria.

## Readiness Summary

| Area | Status | Evidence |
| --- | --- | --- |
| Skill inventory | Ready | 26 skills validated by `validate_all_skills.ps1` |
| Prompt coverage | Ready | Forward prompts exist for core and focused skills |
| Script support | Ready | Python scripts compile during validation |
| Template support | Ready | DAX, Power Query, SQL, test, runbook, proposal, and story templates exist |
| Tenant-specific tests | Blocked pending artifacts | Requires real TOPdesk metadata, exports, API samples, or PBIX docs |

## Recommended Manual Forward-Test Procedure

1. Start a fresh Codex thread.
2. Invoke one prompt from `FORWARD_TEST_PROMPTS.md`.
3. Check whether the expected skill triggers.
4. Verify output includes concrete artifacts, assumptions, validation steps, and source-of-truth boundaries.
5. Record pass/fail and improvement notes below.

## Result Template

| Skill | Prompt | Pass/Fail | Notes | Follow-up |
| --- | --- | --- | --- | --- |
| `topdesk-powerbi` | SLA dashboard spec | Not run | Requires fresh agent invocation | Run manually |
| `topdesk-odata` | Metadata mapping | Not run | Requires sample metadata for full test | Run with tenant/sample artifact |
| `topdesk-ai` | Ticket classification | Not run | Can run generically; real accuracy needs labeled data | Run manually |
| `topdesk-schema` | Incident schema | Not run | Can run generically | Run manually |
| `topdesk-handbook` | Operator/Power BI handbook | Not run | Can run generically | Run manually |
