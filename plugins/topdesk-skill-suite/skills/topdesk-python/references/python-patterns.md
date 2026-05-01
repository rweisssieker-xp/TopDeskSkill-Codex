# Python Patterns

## CLI Shape

- Use `argparse` with explicit input and output parameters.
- Put logic in `main(argv: list[str] | None = None) -> int`.
- Use `if __name__ == "__main__": raise SystemExit(main())`.
- Use `pathlib.Path` for filesystem paths.
- Use `encoding="utf-8"` and `newline=""` for CSV output.

## File Safety

- Resolve input paths before reading.
- Create output parents explicitly.
- Avoid overwriting unrelated files. Prefer deterministic generated filenames or an explicit `--force`.
- Write structured outputs as JSON/CSV/Markdown depending on consumer needs.

## API/OData

- Use `urllib.request` or `requests` only if already available/allowed.
- Keep base URL, endpoint, credentials, timeout, and pagination configurable.
- Parse `$metadata` with `xml.etree.ElementTree`; preserve namespaces.
- Store raw response metadata for reconciliation when building reporting artifacts.

## Testing

- Keep parsing/transformation functions pure.
- Add small fixture-driven tests for CSV, JSON, and XML parsers.
- Use `python -m py_compile` as the minimal syntax gate.
- For CLIs, run a smoke command that writes to a temporary directory.

