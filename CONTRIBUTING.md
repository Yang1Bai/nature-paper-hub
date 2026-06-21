# Contributing

This repository is a full-pipeline skill package for top-journal manuscript work. Contributions should improve the real writing, review, figure, citation, submission, or installation workflow.

## Good Contributions

- Fix install paths, packaging metadata, or cross-platform setup instructions.
- Improve existing skills with concrete routing rules, journal constraints, examples, or quality checks.
- Add focused helper scripts that are referenced by an owning skill.
- Add tests that catch broken paths, invalid JSON, stale README claims, or script syntax errors.
- Improve bilingual documentation when it reduces user friction.

## Out Of Scope

- Generic prompt collections that are not connected to the manuscript workflow.
- Large dependency-heavy tools without a clear owner skill.
- Orphan scripts, templates, or references that are not loaded by any skill.
- Claims about competing projects that are not checked against their current public repository state.

## Repository Conventions

- Keep skill directories self-contained under `skills/`.
- Keep shared runtime resources under the repository root: `scripts/`, `templates/`, and `data/`.
- If a skill needs root resources, document the `CLAUDE_PLUGIN_ROOT` requirement in user-facing install instructions.
- Update README sections in both Chinese and English when changing install, scope, workflow, or packaging behavior.
- Keep comparison tables dated and tied to specific commits when referencing other repositories.

## Validation

Before opening a pull request, run:

```bash
python -m unittest discover -s tests
python -m py_compile scripts/*.py
```

On Windows PowerShell, use:

```powershell
py -3 -m unittest discover -s tests
Get-ChildItem .\scripts -Filter *.py | ForEach-Object { py -3 -m py_compile $_.FullName }
```

Also check that README install snippets still copy full skill directories rather than only `SKILL.md`.
