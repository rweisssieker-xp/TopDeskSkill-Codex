# Installation Notes

Use this file when installing or updating the skill in a Codex skills directory.

## Local Development Location

Current development path:

```text
C:\tmp\topdeskskill\topdesk-expert
```

## Auto-Discovery Location

For Codex auto-discovery on this machine, copy the `topdesk-expert` folder to:

```text
C:\Users\weiss\.codex\skills\topdesk-expert
```

Before copying, check whether a skill already exists there and preserve user changes.

## Validation

Run:

```bash
python C:\Users\weiss\.codex\skills\.system\skill-creator\scripts\quick_validate.py C:\Users\weiss\.codex\skills\topdesk-expert
```

Also test scripts:

```bash
python -m py_compile C:\Users\weiss\.codex\skills\topdesk-expert\scripts\parse_odata_metadata.py
python -m py_compile C:\Users\weiss\.codex\skills\topdesk-expert\scripts\profile_topdesk_export.py
```

## Update Rule

When updating an installed copy:

- Do not delete unrelated local additions.
- Compare `SKILL.md`, `agents/openai.yaml`, `references/`, and `scripts/`.
- Re-run quick validation after copy.
