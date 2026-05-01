---
name: topdesk-python
description: Advanced Python automation for TOPdesk data, APIs, OData, reporting, migration, testing, and delivery tooling. Use for writing, reviewing, hardening, testing, or packaging Python scripts that parse TOPdesk OData metadata, profile CSV/Excel exports, call TOPdesk REST APIs, generate field catalogs, create data-quality findings, build Power BI/reporting artifacts, run migration checks, or provide CLI utilities.
---

# TOPdesk Python

Use this skill for production-grade Python in TOPdesk projects.

## Workflow

1. Identify whether the task is API/OData, export profiling, transformation, validation, artifact generation, or packaging.
2. Prefer standard-library implementations unless the repo already uses a dependency or the task clearly requires one.
3. Build CLIs with `argparse`, deterministic output paths, explicit encodings, and nonzero exit codes on failure.
4. Use structured parsers for JSON, CSV, XML, and ZIP files. Avoid ad hoc parsing when a standard module exists.
5. Keep secrets out of code. Read credentials from environment variables or explicit runtime parameters.
6. Separate pure transformation functions from I/O so behavior is testable.
7. Run `scripts/validate_topdesk_python.py` against generated scripts when practical.

## References

Load only what is needed:

- `references/python-patterns.md` for CLI architecture, file safety, testing, API clients, and packaging.
- `references/topdesk-python-recipes.md` for TOPdesk OData/API, CSV profiling, metadata parsing, and report generation recipes.

## Assets

Use `assets/topdesk_cli_template.py` as the starting point for new Python CLIs.

