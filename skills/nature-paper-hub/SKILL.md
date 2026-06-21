---
name: nature-paper-hub
description: Full-pipeline assistant for submitting to 19 top journals — the Nature portfolio (12) plus Science, Cell, PNAS, JACS, ACS Nano, Angewandte Chemie and Advanced Materials. Covers journal selection, literature review, manuscript drafting, figure generation, citation verification, integrity checking, pre-submission reviewer simulation, submission audit, cover letter, export (LaTeX/Word/PPTX) and reviewer rebuttal. Trigger when the user wants to write, revise, format, review, or submit a research paper to any top-tier journal (Nature / Science / Cell / PNAS / ACS / Wiley families), or needs help with any part of the academic writing and submission process.
version: 1.2.0
author: Yang1Bai
tags:
  - academic-writing
  - nature-journal
  - science-journal
  - cell-press
  - acs-journals
  - scientific-writing
  - research-paper
  - latex
  - claude-code
  - codex
  - openclaw
---

# Nature Paper Hub

## Description
Full-pipeline top-journal writing assistant (Nature / Science / Cell / PNAS / ACS / Wiley families, 19 journals). Trigger when the user wants to:
- Write, draft, or outline a Nature-series research paper
- Select a target journal for submission (19 supported)
- Revise any section of a manuscript
- Plan or improve figures
- Check citations or generate reference lists
- Prepare a submission checklist or rebuttal letter
- Export manuscript as LaTeX (Overleaf) or Word

Multi-language: interact in Chinese or English; all manuscript output is in English.

## Skill Location & Resources
This skill is the hub of the `nature-paper-hub` Claude Code plugin. Shared resources live at the
plugin root and are referenced with `${CLAUDE_PLUGIN_ROOT}`:
- `${CLAUDE_PLUGIN_ROOT}/scripts/` — figure / Word / PPTX generators
- `${CLAUDE_PLUGIN_ROOT}/templates/` — `journal-specs.json` (word/figure/reference limits) + `nature-latex.tex`
- `${CLAUDE_PLUGIN_ROOT}/data/` — local literature index (`papers-index.json`)

Detailed rules for this skill live alongside it in `references/` (relative to this skill, loaded on demand):
writing rules, outlines, audit + cover letter, rebuttal, literature integration, and journal-special rules.

---

## STAGE 0 — Journal Selection

**Always run this stage first unless the user has already specified a journal.**

Present this menu and ask the user to choose:

```
📋 请选择目标期刊 / Select target journal:

1.  Nature (IF 63.7)                       — 顶级综合科学
2.  Nature Materials (IF 37.2)             — 材料科学
3.  Nature Chemistry (IF 19.2)             — 化学
4.  Nature Energy (IF 60.9)                — 能源
5.  Nature Catalysis (IF 37.8)             — 催化
6.  Nature Sustainability (IF 25.1)        — 可持续发展
7.  Nature Communications (IF 15.7)        — 全科学，开放获取，最灵活
8.  Nature Methods (IF 32.1)               — 方法学
9.  Nature Computational Science (IF 12.0) — 计算科学
10. Nature Chemical Engineering (IF 13.0)  — 化学工程
11. Nature Machine Intelligence (IF 23.9)  — 机器学习/AI/机器人
12. Nature Synthesis (IF 20.0)             — 合成化学与材料合成
13. Science (IF 44.7)                      — 顶级综合科学（Article / Report）
14. Cell (IF 45.5)                         — 生命科学（Article / Short Article）
15. PNAS (IF 11.1)                         — 综合科学（Research Article）
16. JACS (IF 14.4)                         — 化学（Article / Letter）
17. ACS Nano (IF 15.8)                     — 纳米科学（Article / Letter）
18. Angewandte Chemie (IF 16.1)            — 化学（Research Article / Communication）
19. Advanced Materials (IF 27.4)           — 材料科学（Research Article / Communication）
20. 其他 / Other — 请告诉我期刊名
```

After selection, load the corresponding entry from `templates/journal-specs.json` and display:
- Word limits (body, abstract, Methods)
- Figure/table limit
- Reference limit
- Methods location (within text vs. after references)
- Acceptance rate and IF

Then ask: **"您的论文类型是 Article 还是 Letter？"**

### ⚠️ Journal-specific special rules

Several journals have special formatting rules (e.g. Nature Synthesis: figures only, no schemes; Nature Chemical Engineering: "Online Methods" after Discussion; Nature Machine Intelligence: reproducibility-weighted). **Before proceeding, read `references/journal-special-rules.md`** and load the rules for the selected journal.

---

## STAGE 1 — Concept & Literature Review

### 1a. Concept Definition
Ask the user:
1. **Research topic in one sentence** (用一句话描述研究内容)
2. **Core innovation** — what makes this new? (核心创新点是什么？)
3. **Key result** — what did you find/achieve? (最重要的结果/发现)
4. **Target scope** — does it fit the selected journal's scope?

### 1b. Literature Search
Search for related papers in this order: (1) the local Tier-1 index `${CLAUDE_PLUGIN_ROOT}/data/papers-index.json`; (2) a personal literature API **only if** the `LITREVIEW_API` environment variable is set (a base URL that accepts `?q=<query>`); (3) `web_search`. Never call a hardcoded private host.
Also use web_search with queries like:
- `site:nature.com "<topic>" filetype:pdf`
- `arxiv.org "<topic>" Nature-style`

Search for 3–5 open-access papers from the target journal as structural templates:
```
Search query: site:nature.com/[journal-shortname] "<topic keyword>" open access
```
For each found paper, extract:
- Paper structure (section titles used)
- Abstract style
- Figure count and types

Present the user with: key gap in literature, positioning suggestion, and 3–5 recommended template papers.

### 1c. Novelty Check
Ask: "Has anyone published very similar work in the past 2 years?" 
Run a targeted web search. Report findings honestly — if there's overlap, suggest how to differentiate.

---

## STAGE 2 — Outline & Structure Planning

Based on the journal selected and paper type, generate a tailored outline.

### Outline templates

**Read `references/outlines.md`** for the full journal-tailored outline (Article / Letter, section-by-section structure, and Nature Communications variant). Generate a tailored outline from it, then ask the user to review and modify before proceeding.

---

## STAGE 3 — Section-by-Section Writing

Work through each section one at a time. Ask for the user's raw data/notes for each section, then draft in Nature style.

**Read `references/writing-rules.md` before drafting.** It holds the per-section rules (Abstract / Introduction / Results / Discussion / Methods), the word-count checks, and the mandatory post-section self-critique. Apply them to every section you draft, one section at a time.

---

## STAGE 4 — Figure Planning

Ask user: how many figures do you have data for? (Must be ≤ journal limit)

For each figure, guide:
```
Figure X: [What story does this figure tell?]
  Panel (a): [Data type] — [Message]
  Panel (b): [Data type] — [Message]
  Panel (c): [Data type] — [Message]

Design rules:
- Each figure tells ONE clear story
- Panel a = overview/schematic; subsequent panels = evidence
- Resolution: 300 DPI min (600 DPI for line art)
- Font: Arial or Helvetica, ≥7pt in final printed size
- Color: accessible palette (avoid red-green for colorblind readers)
- Scale bars: always include for microscopy images
- Statistical indicators: *, **, *** for significance; exact p-values preferred
```

Suggest figure order: schematic → characterization → mechanism → performance → application

---

## STAGE 5 — Citation Verification

For each reference cited in the manuscript:
1. Verify it exists using web_search: `"[author] [year] [journal] [abbreviated title]"`
2. Check if it's been retracted: search `"[paper title] retraction"`
3. Verify it supports the claim being made (use Scite-style thinking: supporting vs. contrasting)
4. Format in Nature numbered style:
   ```
   1. LastName, A., LastName, B. & LastName, C. Title of paper. Journal Vol, pages (Year).
   ```

Flag any:
- References older than 10 years (unless seminal)
- References that don't directly support the claim
- Missing DOIs

### 📋 Bulk Reference Formatting (quick mode)
If user pastes a list of references in any format (Google Scholar export, DOI list, messy copy-paste):
1. Parse each entry — extract authors, year, title, journal, volume, pages, DOI
2. For any missing fields, look up via CrossRef: `web_fetch("https://api.crossref.org/works/<DOI>")`
3. Re-format ALL entries into Nature numbered style in one batch
4. Also output a `.bib` BibTeX block for the entire list
5. Flag any entries that could not be verified

Trigger phrase: "帮我格式化引用" / "format my references" / "整理参考文献"

---

## STAGE 6 — Pre-Review Integrity Check

Before simulating peer review, run `nature-integrity-check` in `pre-review` mode to catch citation errors, data inconsistencies, and missing required statements.

**Invoke:** say `完整性检查` / `integrity check`

⚠️ Must achieve zero CRITICAL issues before proceeding to Stage 7 reviewer simulation.

---

## STAGE 7 — Pre-Submission Reviewer Simulation

Invoke `nature-reviewer-sim` for full 7-agent simulation calibrated to your target journal.

**Modes:** full (7 agents, recommended) | quick (EIC only, ~15 min) | re-review (post-revision)

**Invoke:** say `模拟审稿` / `reviewer simulation`

---

## STAGE 8 — Pre-Submission Audit

Run through this checklist before export:

**Read `references/audit-and-cover-letter.md`** for the full pre-submission checklist (formatting / content / science / journal-specific) and the cover-letter template. Run the checklist, then auto-generate the cover letter (tone calibrated to journal prestige).

---

## STAGE 9 — Final Integrity Check

⚠️ IRON RULE: Must achieve zero CRITICAL issues before export.

Run `nature-integrity-check` in `final-check` mode.

**Invoke:** say `最终检查` / `final integrity check`

---

## STAGE 10 — Export

Ask user: **"导出格式？Overleaf (LaTeX) 还是 Word (.docx)？"**

### Option A: LaTeX / Overleaf
1. Load template from `templates/nature-latex.tex`
2. Fill in all sections with the drafted content
3. Generate `main.tex` and `references.bib` (BibTeX format)
4. Save to user-specified path (default: `~/Downloads/nature-paper-[journal]-[date]/`)
5. Instructions: "Upload main.tex + references.bib + figure files to Overleaf as a new project"

### Option B: Word (.docx)
1. Run `python3 ${CLAUDE_PLUGIN_ROOT}/scripts/export_docx.py`
2. Script takes the drafted sections and generates a properly formatted .docx
3. Styles: Heading 1 for sections, 11pt Times New Roman body, double-spaced
4. Save to `~/Downloads/nature-paper-[journal]-[date].docx`

---

## STAGE 11 — Rebuttal Response

When the user receives reviewer comments:

**Read `references/rebuttal.md`** for the full three-step workflow: (1) triage every comment (🔴/🟡/🟢) and confirm strategy, (2) point-by-point responses tied to manuscript changes, (3) revision cover letter.

---

## Integration: Literature Search & RAG

Two-tier literature search: **Tier 1** = the local `${CLAUDE_PLUGIN_ROOT}/data/papers-index.json` (works for everyone); **Tier 2** = an optional personal API, used **only if** the `LITREVIEW_API` env var is set. **Read `references/literature-integration.md`** for the full search, RAG style-anchoring, and CrossRef metadata-enrichment workflow.

---

## Language & Interaction

- Interact with user in Chinese (or whichever language they use)
- All manuscript drafts, templates, and exports are in English
- When asking for input about experiments/data, accept Chinese descriptions and translate to academic English
- When uncertain about a translation of a scientific term, provide both Chinese and English and ask for confirmation

---

## Quick Commands

The user can say any of these to jump to a specific stage:
- "选刊" / "choose journal" → Stage 0
- "文献综述" / "literature review" → Stage 1
- "写大纲" / "outline" → Stage 2
- "写[某章节]" / "write [section]" → Stage 3
- "图表规划" / "figure plan" → Stage 4
- "检查引用" / "check citations" → Stage 5
- "格式化引用" / "format references" → Stage 5 bulk mode
- "投稿检查" / "submission check" → Stage 8
- "写cover letter" / "cover letter" → Stage 8 cover letter
- "导出" / "export" → Stage 10 (Export)
- "写回复信" / "rebuttal" → Stage 11
- "审稿意见分类" / "triage reviewers" → Stage 11 triage only
- "从头开始" / "start new paper" → Stage 0
- "完整性检查" / "integrity check" → Stage 6 (pre-review integrity check)
- "投稿前检查" / "pre-submission check" → Stage 6
- "模拟审稿" / "reviewer simulation" → Stage 7 (reviewer sim)
- "审稿模拟" / "simulate peer review" → Stage 7 (reviewer sim)
- "投稿前审稿" / "pre-submission review" → Stage 7 (reviewer sim)
- "快速审稿" / "quick review" → Stage 7 quick mode
- "验证审稿" / "re-review" → Stage 7 re-review mode
- "最终检查" / "final integrity check" → Stage 9
- "final-check" / "最终完整性检查" → Stage 9
