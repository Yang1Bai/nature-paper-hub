# 🧬 Nature Paper Hub

<p align="center">
  <b>全流程 Nature 系列期刊论文写作 AI Agent</b><br>
  <b>Full-pipeline AI Agent for Nature-series Journal Writing</b>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Nature_Journals-9_supported-blue?style=flat-square" />
  <img src="https://img.shields.io/badge/OpenClaw-compatible-green?style=flat-square" />
  <img src="https://img.shields.io/badge/Claude_Code-plugin-purple?style=flat-square" />
  <img src="https://img.shields.io/badge/Codex-compatible-orange?style=flat-square" />
  <img src="https://img.shields.io/badge/License-MIT-lightgrey?style=flat-square" />
</p>

---

## 简介 | Introduction

**中文：** `nature-paper-hub` 是一套面向 Nature 系列期刊投稿的全流程 AI 写作 agent，覆盖从选刊、文献调研、论文起草、图表生成、引用核验、投稿前检查，到审稿意见回复的完整链路。支持 OpenClaw、Claude Code、Codex 三种平台安装，输出格式支持 LaTeX（Overleaf）和 Word（.docx）。

**English:** `nature-paper-hub` is a full-pipeline AI writing agent for Nature-series journal submissions. It covers journal selection, literature review, manuscript drafting, figure generation, citation verification, pre-submission audit, and reviewer response. Compatible with OpenClaw, Claude Code, and Codex. Outputs LaTeX (Overleaf-ready) or Word (.docx).

---

## 功能一览 | Features

| Skill | 功能 | Function |
|-------|------|----------|
| 🏠 `nature-paper-hub` | 主入口，8阶段全流程路由 | Main hub, 8-stage full pipeline |
| 📊 `nature-figure` | Nature 风格 matplotlib/R 科研图 | Publication-quality figure generation |
| 📖 `nature-reader` | 论文双语精读 + 图文注释 | Bilingual paper reader with figure grounding |
| 📚 `nature-citation` | 引用检索、核验、多格式导出 | Citation retrieval, verification & export |
| 🎞️ `nature-paper2ppt` | 论文转中文 PPT | Paper to Chinese presentation |

---

## 支持的 Nature 子刊 | Supported Journals

| 期刊 | IF | 接收率 |
|------|----|--------|
| Nature | 63.7 | ~8% |
| Nature Materials | 37.2 | ~9% |
| Nature Chemistry | 19.2 | ~9% |
| Nature Energy | 60.9 | ~8% |
| Nature Catalysis | 37.8 | ~8% |
| Nature Sustainability | 25.1 | ~10% |
| Nature Communications | 15.7 | ~20% |
| Nature Methods | 32.1 | ~8-10% |
| Nature Computational Science | 12.0 | ~12% |

---

## 安装 | Installation

### 方式一：OpenClaw

```bash
# 克隆仓库
git clone https://github.com/Yang1Bai/nature-paper-hub.git

# 复制到 OpenClaw workspace skills 目录
cp -R nature-paper-hub ~/.openclaw/workspace/skills/

# 重启 OpenClaw 后，对话中直接说"选刊"或"写论文"即可激活
```

### 方式二：Claude Code

```bash
# 通过插件市场安装（推荐）
/plugin marketplace add https://github.com/Yang1Bai/nature-paper-hub
/plugin install nature-paper-hub
/reload-plugins
```

或手动安装子 skill：
```bash
mkdir -p ~/.claude/agents
cp nature-paper-hub/skills/nature-figure/SKILL.md ~/.claude/agents/nature-figure.md
cp nature-paper-hub/skills/nature-reader/SKILL.md ~/.claude/agents/nature-reader.md
cp nature-paper-hub/skills/nature-citation/SKILL.md ~/.claude/agents/nature-citation.md
cp nature-paper-hub/skills/nature-paper2ppt/SKILL.md ~/.claude/agents/nature-paper2ppt.md
```

### 方式三：Codex

```bash
mkdir -p ~/.codex/skills

# 安装所有 skills
for d in nature-paper-hub/skills/nature-*; do
  cp -R "$d" ~/.codex/skills/
done

# 重启 Codex 后生效
```

### 方式四：安装 Python 依赖

```bash
cd nature-paper-hub
pip install -r scripts/requirements.txt
```

---

## 快速上手 | Quick Start

### OpenClaw / Telegram
在对话中说：
```
选刊               → 选择目标 Nature 子刊
写大纲             → 生成论文结构
写摘要             → 起草 Abstract
图表规划           → 规划论文图表
检查引用           → 核验参考文献
导出               → 导出 LaTeX 或 Word
写回复信           → 生成审稿意见回复
```

### Claude Code
```
Use nature-figure to generate a matplotlib figure for my OER data.
Use nature-reader to create a bilingual reader for this paper: <PDF path>
Use nature-citation to find and export citations for oxygen evolution catalysis.
```

### Codex
```
Use the nature-writing skill to draft the Results section for my Nature Materials paper.
Use nature-paper2ppt to convert this paper into a Chinese presentation.
```

---

## 全流程说明 | Full Pipeline

```
Stage 0: Journal Selection    → 选期刊，加载字数/图数/引用限制
Stage 1: Literature Review    → 调 LitReview API + 网络文献搜索
Stage 2: Outline Planning     → 按子刊定制论文结构
Stage 3: Section Writing      → 逐节起草（Abstract/Intro/Results/Discussion/Methods）
Stage 4: Figure Planning      → 图表叙事规划 + matplotlib/R 代码生成
Stage 5: Citation Check       → 引用核验 + 多格式导出
Stage 6: Pre-submission Audit → 完整投稿 checklist
Stage 7: Export               → LaTeX (Overleaf) 或 Word (.docx)
Stage 8: Rebuttal             → 逐条审稿意见回复框架
```

---

## 文件结构 | Repository Structure

```
nature-paper-hub/
├── README.md                        # 本文件（中英双语）
├── SKILL.md                         # 主 skill（OpenClaw 入口）
├── skills/
│   ├── nature-figure/
│   │   └── SKILL.md                 # 科研绘图
│   ├── nature-reader/
│   │   └── SKILL.md                 # 双语论文阅读器
│   ├── nature-citation/
│   │   └── SKILL.md                 # 引用管理与导出
│   └── nature-paper2ppt/
│       └── SKILL.md                 # 论文转 PPT
├── templates/
│   ├── journal-specs.json           # 9个子刊规格数据
│   └── nature-latex.tex             # Overleaf LaTeX 模板
└── scripts/
    ├── export_docx.py               # Word 导出脚本
    ├── export_pptx.py               # PPT 导出脚本
    └── requirements.txt             # Python 依赖
```

---

## 与同类项目对比 | Comparison

| 功能 | nature-paper-hub | Yuan1z0825/nature-skills | Boom5426/Nature-Paper-Skills |
|------|:---:|:---:|:---:|
| 9个子刊精确规格 | ✅ | ❌ | ✅ |
| 全流程单入口路由 | ✅ | ❌ | ✅ |
| LaTeX / Overleaf 模板 | ✅ | ❌ | ❌ |
| Word 导出 | ✅ | ❌ | ❌ |
| matplotlib 科研绘图 | ✅ | ✅ | ❌ |
| **CSV/Excel → 自动生图** | ✅ | ❌ | ❌ |
| 双语论文阅读器 | ✅ | ✅ | ❌ |
| 论文转 PPT | ✅ | ✅ | ❌ |
| 引用多格式导出 | ✅ | ✅ | ❌ |
| **CrossRef API 实时核验** | ✅ | ❌ | ❌ |
| **RetractionWatch 撤稿检查** | ✅ | ❌ | ❌ |
| **LitReview RAG 风格锚定** | ✅ | ❌ | ❌ |
| 个人文献库集成 | ✅ | ❌ | ❌ |
| Claude Code 插件 | ✅ | ✅ | ✅ |
| Codex 兼容 | ✅ | ✅ | ✅ |
| OpenClaw 兼容 | ✅ | ❌ | ❌ |

---

## 致谢 | Acknowledgements

部分设计灵感来源于：
- [Yuan1z0825/nature-skills](https://github.com/Yuan1z0825/nature-skills) — SJTU 袁一哲团队
- [Boom5426/Nature-Paper-Skills](https://github.com/Boom5426/Nature-Paper-Skills)
- [Nature Portfolio Author Guidelines](https://www.nature.com/authors)

---

## 许可证 | License

MIT License — 自由使用、修改和分发。  
MIT License — Free to use, modify, and distribute.

---

## 贡献 | Contributing

欢迎提 Issue 和 PR！请在 Issue 中描述：  
Welcome Issues and PRs! Please describe:
1. 期刊 / Journal targeted
2. 功能缺口 / Feature gap
3. 建议实现方式 / Suggested implementation
