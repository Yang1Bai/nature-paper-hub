# 🧬 Top Journal Paper Hub

<p align="center">
  <img src="https://img.shields.io/badge/Journals-19_supported-blue?style=flat-square" />
  <img src="https://img.shields.io/badge/Nature_Series-12_journals-brightgreen?style=flat-square" />
  <img src="https://img.shields.io/badge/Science%2FCell%2FPNAS%2FACS%2FWiley-7_journals-orange?style=flat-square" />
  <img src="https://img.shields.io/badge/OpenClaw-compatible-green?style=flat-square" />
  <img src="https://img.shields.io/badge/Claude_Code-plugin-purple?style=flat-square" />
  <img src="https://img.shields.io/badge/Codex-compatible-orange?style=flat-square" />
  <img src="https://img.shields.io/badge/License-MIT-lightgrey?style=flat-square" />
</p>

<p align="center">
  <a href="#chinese">中文版</a> · <a href="#english">English</a>
</p>

---

<h2 id="chinese">🇨🇳 中文版</h2>

### 简介

`top-journal-paper-hub` 是一套面向顶级期刊投稿的全流程 AI 写作 agent，覆盖从**选刊、文献调研、论文起草、图表生成、引用核验、投稿前模拟审稿、投稿前检查，到审稿意见回复**的完整链路。

支持 **OpenClaw、Claude Code、Codex** 三种平台，输出格式支持 **LaTeX（Overleaf）和 Word（.docx）**，并内置 CSV/Excel 自动生图、CrossRef 实时引用核验、个人文献库 RAG 写作风格锚定。

**v1.1.0 新增：** 7 个 Science / Cell / ACS / Wiley 顶刊 + 投稿前模拟审稿技能 + 期刊规格自动维护 CI。

---

### 功能一览

| Skill | 功能说明 |
|-------|----------|
| 🏠 `nature-paper-hub` | 主入口，9 阶段全流程对话路由（含模拟审稿） |
| 🔬 `nature-reviewer-sim` | 投稿前模拟审稿：3 位审稿人视角 + 编辑综合意见 |
| 📊 `nature-figure` | CSV/Excel → 顶刊风格 matplotlib/R 图，自动识别图表类型 |
| 📖 `nature-reader` | PDF/DOI/arXiv → 双语精读 Markdown，含图表解读与引用建议 |
| 📚 `nature-citation` | CrossRef 实时核验 + RetractionWatch 撤稿检查 + BibTeX/RIS/ENW/Zotero 导出 |
| 🎞️ `nature-paper2ppt` | 论文 → 中文/双语 PPTX，含演讲者备注 |

---

### 支持期刊（19 个）

#### Nature 系列（12 个）

| 期刊 | 影响因子 | 接收率 | 正文字数 | 图数 | 引用 |
|------|---------|--------|---------|------|------|
| Nature | 63.7 | ~8% | 3,000 | 6 | 30 |
| Nature Energy | 60.9 | ~8% | 3,000 | 6 | 50 |
| Nature Materials | 37.2 | ~9% | 3,000 | 6 | 50 |
| Nature Catalysis | 37.8 | ~8% | 3,000 | 6 | 50 |
| Nature Methods | 32.1 | ~8-10% | 3,000 | 6 | 50 |
| Nature Machine Intelligence | 23.9 | ~8% | 3,500 | 6 | 50 |
| Nature Synthesis | 20.0 | ~8% | 3,000 | 6‡ | 50 |
| Nature Chemistry | 19.2 | ~9% | 3,000 | 6 | 50 |
| Nature Communications | 15.7 | ~20% | 5,000† | 10 | 60 |
| Nature Chemical Engineering | 13.0 | ~8% | 3,500 | 6+10ED | 50 |
| Nature Computational Science | 12.0 | ~12% | 5,000 | 8 | 60 |
| Nature Sustainability | 25.1 | ~10% | 4,000 | 8 | 60 |

† Nature Communications 字数含 Methods 章节
‡ Nature Synthesis 不接受 Scheme，只接受 Figure；Methods 中不可含图表

#### 其他顶刊（7 个）

| 期刊 | 影响因子 | 接收率 | 文章类型 | 正文字数 | 图数 |
|------|---------|--------|---------|---------|------|
| Science | 44.7 | ~7% | Article / Report | 4,500 / 2,500 | 6 / 4 |
| Cell | 45.5 | ~8% | Article / Short Article | 8,000 / 4,000 | 8 / 4 |
| PNAS | 11.1 | ~18% | Research Article | 6,000 | 6 |
| JACS | 14.4 | ~11% | Article / Letter | ~6,000 / 4pp | 8 / 4 |
| ACS Nano | 15.8 | ~10% | Article / Letter | 10,000 / 4,000 | 10 / 5 |
| Angewandte Chemie | 16.1 | ~10% | Research Article / Communication | 5,000 / 2,500 | 8 / 4 |
| Advanced Materials | 27.4 | ~9% | Research Article / Communication | 5,000 / 2,500 | 8 / 4 |

---

### 安装

#### 方式一：OpenClaw

```bash
git clone https://github.com/Yang1Bai/nature-paper-hub.git
cp -R nature-paper-hub ~/.openclaw/workspace/skills/
# 重启 OpenClaw，对话中说"选刊"即可激活
```

#### 方式二：Claude Code

```bash
git clone https://github.com/Yang1Bai/nature-paper-hub.git

# 安装为用户级 subagents（全局可用）
mkdir -p ~/.claude/agents
cp nature-paper-hub/SKILL.md ~/.claude/agents/nature-paper-hub.md
cp nature-paper-hub/skills/nature-reviewer-sim/SKILL.md ~/.claude/agents/nature-reviewer-sim.md
cp nature-paper-hub/skills/nature-figure/SKILL.md ~/.claude/agents/nature-figure.md
cp nature-paper-hub/skills/nature-reader/SKILL.md ~/.claude/agents/nature-reader.md
cp nature-paper-hub/skills/nature-citation/SKILL.md ~/.claude/agents/nature-citation.md
cp nature-paper-hub/skills/nature-paper2ppt/SKILL.md ~/.claude/agents/nature-paper2ppt.md
```

或安装为项目级 subagents（仅当前项目）：
```bash
mkdir -p .claude/agents
cp nature-paper-hub/skills/*/SKILL.md .claude/agents/
cp nature-paper-hub/SKILL.md .claude/agents/
```

#### 方式三：Codex

```bash
git clone https://github.com/Yang1Bai/nature-paper-hub.git
mkdir -p ~/.codex/skills
for d in nature-paper-hub/skills/nature-*; do
  cp -R "$d" ~/.codex/skills/
done
```

#### 安装 Python 依赖

```bash
pip install -r nature-paper-hub/scripts/requirements.txt
```

---

### 快速上手

#### OpenClaw / Telegram
在对话中输入以下关键词直接跳转对应阶段：

```
选刊 / choose journal  → 选择目标期刊（19个可选），显示字数/图数/引用限制
文献综述 / literature  → 调用个人文献库 + 网络搜索
写大纲 / outline       → 按期刊生成定制化论文结构
写摘要 / abstract      → 起草符合期刊风格的 Abstract
图表规划 / figure plan → 规划每张图的叙事逻辑
模拟审稿 / reviewer simulation → 投稿前3位审稿人视角模拟评审
检查引用 / citations   → CrossRef 实时核验 + 撤稿检查
导出 / export          → 选择 LaTeX（Overleaf）或 Word
写回复信 / rebuttal    → 逐条审稿意见生成回复框架
```

#### Claude Code
```
Use nature-paper-hub to start writing a paper for Nature Materials
Use nature-reviewer-sim to simulate peer review of my manuscript
Use nature-figure to generate a matplotlib figure from my data.csv
Use nature-reader to create a bilingual reader for this paper: ~/Downloads/paper.pdf
Use nature-citation to verify my reference list and export as BibTeX
Use nature-paper2ppt to convert this paper into a Chinese presentation
```

---

### 全流程说明

```
阶段 PRE: 模拟审稿（可在任意阶段触发）
           → 3位审稿人视角（领域专家 / 方法论 / 影响力）+ 编辑综合意见

阶段 0: 选刊           → 19个顶刊可选，加载对应字数/图数/引用限制
阶段 1: 文献调研       → LitReview 个人库 + CrossRef + 网络搜索
阶段 2: 结构规划       → 按期刊类型定制论文大纲
阶段 3: 逐节起草       → Abstract / Introduction / Results / Discussion / Methods
阶段 4: 图表生成       → CSV/Excel 自动出图 + matplotlib/R 代码 + 图例文字
阶段 5: 引用核验       → CrossRef API + RetractionWatch + 多格式导出
阶段 6: 投稿前检查     → 字数/图数/格式/内容完整 checklist
阶段 7: 导出           → LaTeX (Overleaf) / Word (.docx) / PPTX
阶段 8: 审稿回复       → 逐条回复框架 + 修改说明 + 封面信
```

---

### 文件结构

```
nature-paper-hub/
├── README.md                              # 本文件（中英双语）
├── SKILL.md                               # 主 skill（OpenClaw 入口，v1.1.0）
├── .github/
│   └── workflows/
│       └── journal-spec-check.yml         # 每周自动检查期刊规格 URL 健康状态
├── skills/
│   ├── nature-reviewer-sim/SKILL.md       # 🆕 投稿前模拟审稿（3审稿人+编辑）
│   ├── nature-figure/SKILL.md             # 科研绘图（自动识别 + matplotlib/R）
│   ├── nature-reader/SKILL.md             # 双语论文精读器
│   ├── nature-citation/SKILL.md           # CrossRef 引用核验 + 多格式导出
│   └── nature-paper2ppt/SKILL.md          # 论文转 PPT
├── templates/
│   ├── journal-specs.json                 # 19个期刊规格数据 🆕
│   └── nature-latex.tex                   # Overleaf LaTeX 模板
└── scripts/
    ├── auto_figure.py                     # CSV/Excel → 顶刊图（540行）
    ├── export_docx.py                     # Word 导出
    ├── export_pptx.py                     # PPT 导出
    └── requirements.txt                   # Python 依赖
```

---

### 与同类项目对比

| 功能 | **top-journal-paper-hub** | Yuan1z0825/nature-skills | Boom5426/Nature-Paper-Skills |
|------|:---:|:---:|:---:|
| 期刊覆盖（Nature / Science / Cell / ACS / Wiley） | ✅ **19个** | ❌ Nature only | ✅ Nature only |
| 全流程单入口路由 | ✅ | ❌ | ✅ |
| 投稿前模拟审稿（3审稿人视角） | ✅ | ❌ | ❌ |
| LaTeX / Overleaf 模板 | ✅ | ❌ | ❌ |
| Word 导出（.docx） | ✅ | ❌ | ❌ |
| matplotlib/R 科研绘图代码 | ✅ | ✅ | ❌ |
| CSV/Excel → 自动生图 | ✅ | ❌ | ❌ |
| 双语论文精读器 | ✅ | ✅ | ❌ |
| 论文转 PPT（PPTX） | ✅ | ✅ | ❌ |
| CrossRef 实时引用核验 | ✅ | ❌ | ❌ |
| RetractionWatch 撤稿检查 | ✅ | ❌ | ❌ |
| 期刊规格自动维护 CI | ✅ | ❌ | ❌ |
| OpenClaw / Telegram 兼容 | ✅ | ❌ | ❌ |
| Claude Code 插件 | ✅ | ✅ | ✅ |
| Codex 兼容 | ✅ | ✅ | ✅ |

---

### 更新日志

**v1.1.0（2025-05）**
- 新增 7 个期刊：Science、Cell、PNAS、JACS、ACS Nano、Angewandte Chemie、Advanced Materials
- 新增 `nature-reviewer-sim` 投稿前模拟审稿技能
- 新增 GitHub Actions 每周期刊规格 URL 健康检查
- 期刊总数：9 → 19

**v1.0.0**
- 首发：12 个 Nature 系列期刊，5 个核心技能

---

### 用户反馈 💬

如果你用过这个工具写过论文，欢迎在 **[留言板](https://github.com/Yang1Bai/nature-paper-hub/discussions/1)** 分享体验。

---

### 致谢

设计灵感部分来源于：
- [Yuan1z0825/nature-skills](https://github.com/Yuan1z0825/nature-skills)（上海交通大学袁一哲团队）
- [Boom5426/Nature-Paper-Skills](https://github.com/Boom5426/Nature-Paper-Skills)
- [Nature Portfolio Author Guidelines](https://www.nature.com/authors)

---

### 许可证

MIT License — 自由使用、修改和分发，保留原始署名即可。

---

### 贡献指南

欢迎提 Issue 和 PR！请说明：
1. 目标期刊或功能
2. 功能缺口或 bug 描述
3. 建议实现方式

---
---

<h2 id="english">🇬🇧 English</h2>

### Introduction

`top-journal-paper-hub` is a full-pipeline AI writing agent for top-journal submissions. It covers every stage from **journal selection, literature review, manuscript drafting, figure generation, citation verification, pre-submission mock review, and reviewer response**.

Compatible with **OpenClaw, Claude Code, and Codex**. Outputs **LaTeX (Overleaf-ready) and Word (.docx)**. Features automatic figure generation from CSV/Excel, CrossRef real-time citation verification, and RAG-enhanced writing grounded in your personal literature library.

**v1.1.0:** Added 7 Science/Cell/ACS/Wiley journals + pre-submission reviewer simulation skill + automated journal spec CI.

---

### Features

| Skill | Description |
|-------|-------------|
| 🏠 `nature-paper-hub` | Main hub with 9-stage conversational pipeline (incl. reviewer sim) |
| 🔬 `nature-reviewer-sim` | Pre-submission mock review: 3 reviewer personas + Editor summary |
| 📊 `nature-figure` | CSV/Excel → publication-quality matplotlib/R figures |
| 📖 `nature-reader` | PDF/DOI/arXiv → bilingual annotated Markdown with figure grounding |
| 📚 `nature-citation` | CrossRef verification + RetractionWatch + BibTeX/RIS/ENW/Zotero export |
| 🎞️ `nature-paper2ppt` | Paper → Chinese/bilingual PPTX with presenter notes |

---

### Supported Journals (19)

#### Nature Series (12)

| Journal | IF | Accept | Words | Figs | Refs |
|---------|:---:|:---:|:---:|:---:|:---:|
| Nature | 63.7 | ~8% | 3,000 | 6 | 30 |
| Nature Energy | 60.9 | ~8% | 3,000 | 6 | 50 |
| Nature Materials | 37.2 | ~9% | 3,000 | 6 | 50 |
| Nature Catalysis | 37.8 | ~8% | 3,000 | 6 | 50 |
| Nature Methods | 32.1 | ~8-10% | 3,000 | 6 | 50 |
| Nature Machine Intelligence | 23.9 | ~8% | 3,500 | 6 | 50 |
| Nature Synthesis | 20.0 | ~8% | 3,000 | 6‡ | 50 |
| Nature Chemistry | 19.2 | ~9% | 3,000 | 6 | 50 |
| Nature Communications | 15.7 | ~20% | 5,000† | 10 | 60 |
| Nature Chemical Engineering | 13.0 | ~8% | 3,500 | 6+10ED | 50 |
| Nature Computational Science | 12.0 | ~12% | 5,000 | 8 | 60 |
| Nature Sustainability | 25.1 | ~10% | 4,000 | 8 | 60 |

† Nature Communications word count includes Methods
‡ Nature Synthesis: figures only (no Schemes); Methods cannot contain figures or tables

#### Other Top Journals (7)

| Journal | IF | Accept | Article Types | Words | Figs |
|---------|:---:|:---:|:---:|:---:|:---:|
| Science | 44.7 | ~7% | Article / Report | 4,500 / 2,500 | 6 / 4 |
| Cell | 45.5 | ~8% | Article / Short Article | 8,000 / 4,000 | 8 / 4 |
| PNAS | 11.1 | ~18% | Research Article | 6,000 | 6 |
| JACS | 14.4 | ~11% | Article / Letter | ~6,000 / 4pp | 8 / 4 |
| ACS Nano | 15.8 | ~10% | Article / Letter | 10,000 / 4,000 | 10 / 5 |
| Angewandte Chemie | 16.1 | ~10% | Research Article / Communication | 5,000 / 2,500 | 8 / 4 |
| Advanced Materials | 27.4 | ~9% | Research Article / Communication | 5,000 / 2,500 | 8 / 4 |

---

### Installation

#### Option 1: OpenClaw

```bash
git clone https://github.com/Yang1Bai/nature-paper-hub.git
cp -R nature-paper-hub ~/.openclaw/workspace/skills/
# Restart OpenClaw. Say "选刊" or "choose journal" to activate.
```

#### Option 2: Claude Code

```bash
git clone https://github.com/Yang1Bai/nature-paper-hub.git

mkdir -p ~/.claude/agents
cp nature-paper-hub/SKILL.md ~/.claude/agents/nature-paper-hub.md
cp nature-paper-hub/skills/nature-reviewer-sim/SKILL.md ~/.claude/agents/nature-reviewer-sim.md
cp nature-paper-hub/skills/nature-figure/SKILL.md ~/.claude/agents/nature-figure.md
cp nature-paper-hub/skills/nature-reader/SKILL.md ~/.claude/agents/nature-reader.md
cp nature-paper-hub/skills/nature-citation/SKILL.md ~/.claude/agents/nature-citation.md
cp nature-paper-hub/skills/nature-paper2ppt/SKILL.md ~/.claude/agents/nature-paper2ppt.md
```

#### Option 3: Codex

```bash
git clone https://github.com/Yang1Bai/nature-paper-hub.git
mkdir -p ~/.codex/skills
for d in nature-paper-hub/skills/nature-*; do
  cp -R "$d" ~/.codex/skills/
done
```

#### Python dependencies

```bash
pip install -r nature-paper-hub/scripts/requirements.txt
```

---

### Quick Start

#### OpenClaw / Telegram

```
选刊 / choose journal          → Select from 19 journals; see word/figure/ref limits
文献综述 / literature          → Personal library + CrossRef + web search
写大纲 / outline               → Journal-specific manuscript structure
写摘要 / abstract              → Draft journal-style Abstract
模拟审稿 / reviewer simulation → Pre-submission mock peer review (3 personas)
检查引用 / citations           → CrossRef verify + retraction check
导出 / export                  → LaTeX (Overleaf) or Word
写回复信 / rebuttal            → Point-by-point reviewer response framework
```

#### Claude Code

```
Use nature-paper-hub to start writing a paper for Advanced Materials
Use nature-reviewer-sim to simulate peer review of my manuscript
Use nature-figure to generate a matplotlib figure from my data.csv
Use nature-citation to verify my reference list and export as BibTeX
```

---

### Full Pipeline

```
Stage PRE: Reviewer Simulation (can trigger at any point)
           → 3 reviewer personas (Domain Expert / Methodologist / Impact Judge) + Editor summary

Stage 0: Journal Selection    → Choose from 19 journals; load word/figure/ref limits
Stage 1: Literature Review    → Personal library + CrossRef + web search
Stage 2: Outline Planning     → Journal-tailored manuscript structure
Stage 3: Section Drafting     → Abstract / Intro / Results / Discussion / Methods
Stage 4: Figure Generation    → Auto-plot from CSV/Excel + matplotlib/R code + legend text
Stage 5: Citation Check       → CrossRef API + RetractionWatch + multi-format export
Stage 6: Pre-submission Audit → Word count / figure count / format / content checklist
Stage 7: Export               → LaTeX (Overleaf) / Word (.docx) / PPTX
Stage 8: Reviewer Response    → Point-by-point reply + change summary + cover letter
```

---

### Repository Structure

```
nature-paper-hub/
├── README.md                              # This file (bilingual CN/EN)
├── SKILL.md                               # Main skill (OpenClaw entry point, v1.1.0)
├── .github/
│   └── workflows/
│       └── journal-spec-check.yml         # Weekly journal spec URL health check CI
├── skills/
│   ├── nature-reviewer-sim/SKILL.md       # 🆕 Pre-submission mock review (3 personas)
│   ├── nature-figure/SKILL.md             # Figure generation (auto-detect + matplotlib/R)
│   ├── nature-reader/SKILL.md             # Bilingual paper reader
│   ├── nature-citation/SKILL.md           # CrossRef citation verification + multi-format
│   └── nature-paper2ppt/SKILL.md          # Paper to presentation
├── templates/
│   ├── journal-specs.json                 # 19-journal specs database 🆕
│   └── nature-latex.tex                   # Overleaf-ready LaTeX template
└── scripts/
    ├── auto_figure.py                     # CSV/Excel → publication figure (540 lines)
    ├── export_docx.py                     # Word export
    ├── export_pptx.py                     # PPTX export
    └── requirements.txt                   # Python dependencies
```

---

### Comparison

| Feature | **top-journal-paper-hub** | Yuan1z0825/nature-skills | Boom5426/Nature-Paper-Skills |
|---------|:---:|:---:|:---:|
| Journal coverage (Nature / Science / Cell / ACS / Wiley) | ✅ **19** | ❌ Nature only | ✅ Nature only |
| Single-entry full-pipeline routing | ✅ | ❌ | ✅ |
| Pre-submission mock review (3 reviewer personas) | ✅ | ❌ | ❌ |
| LaTeX / Overleaf template | ✅ | ❌ | ❌ |
| Word export (.docx) | ✅ | ❌ | ❌ |
| matplotlib/R figure code generation | ✅ | ✅ | ❌ |
| CSV/Excel → auto figure | ✅ | ❌ | ❌ |
| Bilingual paper reader | ✅ | ✅ | ❌ |
| Paper to PPTX | ✅ | ✅ | ❌ |
| CrossRef real-time citation verification | ✅ | ❌ | ❌ |
| RetractionWatch retraction check | ✅ | ❌ | ❌ |
| Automated journal spec CI | ✅ | ❌ | ❌ |
| OpenClaw / Telegram compatible | ✅ | ❌ | ❌ |
| Claude Code plugin | ✅ | ✅ | ✅ |
| Codex compatible | ✅ | ✅ | ✅ |

---

### Changelog

**v1.1.0 (2025-05)**
- Added 7 journals: Science, Cell, PNAS, JACS, ACS Nano, Angewandte Chemie, Advanced Materials
- New skill: `nature-reviewer-sim` — pre-submission 3-persona mock peer review
- GitHub Actions: weekly journal spec URL health check with auto-issue on failure
- Journal count: 9 → 19

**v1.0.0**
- Initial release: 12 Nature-series journals, 5 core skills

---

### User Feedback 💬

If you have used this tool in your research, please share your experience on the **[feedback board](https://github.com/Yang1Bai/nature-paper-hub/discussions/1)**.

---

### Acknowledgements

Inspired in part by:
- [Yuan1z0825/nature-skills](https://github.com/Yuan1z0825/nature-skills) — Yuan Yizhe, Shanghai Jiao Tong University
- [Boom5426/Nature-Paper-Skills](https://github.com/Boom5426/Nature-Paper-Skills)
- [Nature Portfolio Author Guidelines](https://www.nature.com/authors)

---

### License

MIT License — free to use, modify, and distribute with attribution.

---

### Contributing

Issues and PRs welcome. Please include:
1. Target journal or feature
2. Feature gap or bug description
3. Suggested implementation approach
