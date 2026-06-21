# nature-paper-hub (hub skill)

The router for the `nature-paper-hub` plugin. It drives the full 12-stage submission
pipeline (journal selection → drafting → figures → citations → integrity → reviewer
simulation → audit → export → rebuttal) and delegates to the specialist skills
(`nature-figure`, `nature-citation`, `nature-integrity-check`, `nature-reviewer-sim`,
`nature-reader`, `nature-paper2ppt`).

Detailed rules load on demand from `references/` (next to this file):

- `writing-rules.md` — per-section writing rules + self-critique
- `outlines.md` — manuscript outline templates
- `audit-and-cover-letter.md` — pre-submission checklist + cover letter
- `rebuttal.md` — reviewer rebuttal workflow
- `literature-integration.md` — literature search / RAG / CrossRef
- `journal-special-rules.md` — journal-specific rules

Shared resources live at the plugin root and are referenced via `${CLAUDE_PLUGIN_ROOT}`
(`scripts/`, `templates/`, `data/`).

**Trigger:** say `选刊` / `choose journal`, or any stage keyword listed in `SKILL.md`.
