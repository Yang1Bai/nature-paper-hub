# Quick Start — a 10-minute end-to-end walkthrough

This shows the most common path: turning your data + notes into a submission-ready
manuscript for a target journal. It works **out of the box** — no API keys needed.
(Optional: set `LITREVIEW_API` to plug in your own literature library; see README.)

The example uses an electrocatalysis paper aimed at *Nature Materials*, but the same
flow applies to any of the 19 supported journals.

---

## 0. Start & pick a journal

```
你: 选刊
```

The hub lists all 19 journals with word/figure/reference limits. Pick one:

```
你: Nature Materials, Article
```

→ Loads limits from `templates/journal-specs.json` (3,000 words body, 6 figures, 50 refs,
Methods after references) and the journal's special rules.

## 1. Define the work & gather literature

```
你: 文献综述
你: 研究内容：用高熵合金做碱性析氧(OER)电催化剂；创新点：自驱动实验室闭环优化组分；
    关键结果：过电位 198 mV @ 10 mA/cm²，1000 h 稳定
```

→ Searches the local index (`data/papers-index.json`) + CrossRef + web for template
papers and gaps; proposes a positioning angle and 3–5 style-anchor papers.

## 2. Outline → 3. Draft section by section

```
你: 写大纲
你: 写introduction
你: 写results
```

→ Generates a journal-tailored outline, then drafts each section in Nature style.
After **every** section it runs a built-in self-critique (likely reviewer concerns + fixes).

## 4. Figures from your data

```
你: 图表规划
# then, from your CSV:
python3 scripts/auto_figure.py --input oer_data.csv --type auto --width single --palette colorblind
```

→ Auto-detects chart type, applies Nature rcParams (Arial, 300 dpi, colorblind-safe),
exports PDF + PNG.

## 5. Citations

```
你: 检查引用
你: 帮我格式化引用   # paste a messy reference list
```

→ Verifies each DOI via CrossRef, checks retractions, reformats to Nature numbered
style, and emits a `.bib` block.

## 6–9. Integrity → mock review → audit → final check

```
你: 完整性检查      # Stage 6  (pre-review: citations/data/figures/statements)
你: 模拟审稿        # Stage 7  (7 specialist agents + Editorial Decision Letter)
你: 投稿检查        # Stage 8  (checklist + auto cover letter)
你: 最终检查        # Stage 9  (final gate: zero CRITICAL required)
```

## 10. Export

```
你: 导出
你: Overleaf        # or: Word
```

→ Fills `templates/nature-latex.tex` → `main.tex` + `references.bib`, or runs
`scripts/export_docx.py` for a formatted `.docx`. (`scripts/export_pptx.py` makes a deck.)

## 11. After reviews come back

```
你: 写回复信        # paste reviewer comments
```

→ Triages every comment (🔴/🟡/🟢), drafts point-by-point responses tied to manuscript
changes, and a revision cover letter.

---

### Tips
- You can jump to any stage by its keyword at any time (see "Quick Commands" in `SKILL.md`).
- All manuscript output is in English; you can talk to the agent in Chinese.
- Reviewer simulation (Stage 7) can be triggered at any point, not just in sequence.
