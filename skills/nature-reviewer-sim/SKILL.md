---
name: nature-reviewer-sim
description: "Pre-submission peer review simulation calibrated to top-tier journals (Nature, Science, Cell, PNAS, ACS, Wiley families). Deploys 7 specialist agents (field analyst, EIC, methodology reviewer, domain reviewer, perspective reviewer, devils advocate, editorial synthesizer) to simulate the full peer review process. Outputs structured reviewer reports, an Editorial Decision Letter, and a Revision Roadmap. Supports three modes: full (all 7 agents, default), quick (EIC only, ~15 min), and re-review (R&R traceability matrix for post-revision verification). Trigger keywords: 模拟审稿, reviewer simulation, pre-submission review, simulate peer review, 审稿模拟, 投稿前审稿, review my paper, 帮我审稿, 预审稿."
metadata:
  version: "1.0"
  last_updated: "2026-05-20"
  status: active
  parent_skill: nature-paper-hub
  related_skills:
    - nature-integrity-check
    - nature-citation
    - nature-paper-hub
---

# nature-reviewer-sim — Nature-Series Pre-Submission Peer Review Simulator

Simulates a complete Nature-journal peer review process before you submit. Automatically identifies the paper's field and target journal, configures 7 specialist reviewer agents, runs independent multi-perspective reviews, and produces an Editorial Decision Letter with a prioritized Revision Roadmap.

**Key difference from a generic reviewer:** Every reviewer is calibrated to the specific Nature-series journal's standards, loaded from `${CLAUDE_PLUGIN_ROOT}/templates/journal-specs.json`. Acceptance thresholds, scope judgments, and statistical standards all reflect the target journal's real expectations.

---

## Trigger Keywords

| Language | Phrases |
|----------|---------|
| Chinese | 模拟审稿、审稿模拟、投稿前审稿、帮我审稿、预审稿、模拟同行评审 |
| English | reviewer simulation, pre-submission review, simulate peer review, review my paper, peer review simulation, editorial review |

### Non-Trigger Scenarios

| Scenario | Use Instead |
|----------|-------------|
| Responding to actual reviewer comments | Stage 8 rebuttal in `nature-paper-hub` |
| Checking citations/references only | `nature-citation` |
| Checking integrity before review | `nature-integrity-check` |
| Writing or revising the manuscript | `nature-paper-hub` Stages 2–5 |

---

## Agent Team (7 Agents)

| # | Agent ID | Role | Phase | Nature-Specific Focus |
|---|----------|------|-------|-----------------------|
| 1 | `field_analyst` | Analyzes paper field; configures all 5 reviewer personas | Phase 0 | Identifies journal fit, scope, paper maturity |
| 2 | `eic_reviewer` | Editor-in-Chief — journal fit, novelty, significance, readership | Phase 1 | Loads journal-specs.json for exact scope/IF calibration |
| 3 | `methodology_reviewer` | Peer Reviewer 1 — research design, statistics, reproducibility | Phase 1 | Applies statistical_reporting_standards (see §Statistical Standards) |
| 4 | `domain_reviewer` | Peer Reviewer 2 — literature coverage, theory, field contribution | Phase 1 | Checks for missing seminal/recent Nature-portfolio citations |
| 5 | `perspective_reviewer` | Peer Reviewer 3 — cross-disciplinary connections, practical impact | Phase 1 | Flags societal/policy relevance gaps for broad-scope Nature journals |
| 6 | `devils_advocate` | Devil's Advocate — core argument challenges, logical fallacy detection | Phase 1 | Frame-lock detection; CRITICAL finding blocks Accept decision |
| 7 | `editorial_synthesizer` | Synthesizes all 5 reviews; produces Editorial Decision + Roadmap | Phase 2 | Consensus/divergence mapping; DA CRITICAL escalation |

### Agent Boundaries (Non-Overlap Rules)

| Agent | DOES | DOES NOT |
|-------|------|---------|
| `eic_reviewer` | Scope, novelty, overall significance, readership interest | Deep methodology, literature gaps |
| `methodology_reviewer` | Stats, design rigor, reproducibility, EQUATOR compliance | Scope judgment, literature breadth |
| `domain_reviewer` | Literature coverage, theoretical framework, citation completeness | Statistics, interdisciplinary angles |
| `perspective_reviewer` | Broader impact, policy implications, cross-disciplinary connections | Literature audit, statistical details |
| `devils_advocate` | Logical consistency, evidence gaps, strongest counter-arguments, cherry-picking | Stats design, literature coverage, practical impact |

---

## Operational Modes

| Mode | Trigger Phrase | Agents Active | Output | Time |
|------|---------------|---------------|--------|------|
| **`full`** | Default / "full review" / "完整审稿" | All 7 agents | 5 review reports + Editorial Decision + Revision Roadmap | ~45–60 min |
| **`quick`** | "quick review" / "快速审稿" / "15 min" | field_analyst + eic_reviewer | EIC assessment + top-10 issues list | ~15 min |
| **`re-review`** | "re-review" / "验证审稿" / "check revisions" / "R&R" | field_analyst + eic_reviewer + editorial_synthesizer | R&R Traceability Matrix + residual issues + new Decision | ~30 min |

### Mode Selection Logic

```
"Review this paper"                        → full
"Help me review my paper"                  → full
"快速看一下这篇论文"                          → quick
"15-minute check"                          → quick
"Did I address all reviewer comments?"     → re-review
"Verification review after revision"       → re-review
"Check if my revisions are sufficient"     → re-review
```

---

## Orchestration Workflow (3 Phases + Nature-Specific Hooks)

```
User: "模拟审稿" / "Review this paper"
       |
       [Input check: Does manuscript exist? Has nature-integrity-check been run?]
       ⚠️ If integrity check not run → remind user to run nature-integrity-check first
       |
=== PHASE 0: FIELD ANALYSIS & JOURNAL CALIBRATION ===
       |
       +→ [field_analyst]
          1. Read complete manuscript
          2. Identify: primary field, methodology type, paper maturity
          3. Load journal specs: read ${CLAUDE_PLUGIN_ROOT}/templates/journal-specs.json
             → Extract: scope, word limit, figure limit, ref limit, IF, acceptance rate
          4. Assess journal fit (1–5 scale)
          5. Configure 5 reviewer personas with specific:
             - Academic identity (institution, seniority, research focus)
             - Review preferences and known sensitivities
             - What they specifically look for in this journal
       |
       ** CHECKPOINT 1: Present Reviewer Configuration Card to user **
       ** User may adjust reviewer identities before proceeding **
       ** Show: journal specs loaded, reviewer personas, any scope concerns **
       |
=== PHASE 1: PARALLEL MULTI-PERSPECTIVE REVIEW ===
       |
       ⚠️ IRON RULE: All 5 reviewers work independently. No cross-referencing.
       |
       |→ [eic_reviewer]
       |  - Journal scope fit (using loaded journal-specs.json)
       |  - Novelty & significance for target journal tier
       |  - Readership interest
       |  - Data/Code Availability statement presence
       |  - CRediT author contributions presence
       |  - Competing interests declaration presence
       |  - EQUATOR reporting guideline compliance (if clinical/observational)
       |  → Output: EIC Review Report (400–600 words)
       |
       |→ [methodology_reviewer]
       |  - Research design rigor and appropriateness
       |  - Statistical reporting (apply §Statistical Standards below)
       |  - Reproducibility: methods detail, software versions, parameters
       |  - Data transparency: raw data, code, materials availability
       |  - Scan §Red Flags list (see §Statistical Standards)
       |  → Output: Methodology Review Report (600–900 words)
       |
       |→ [domain_reviewer]
       |  - Literature coverage completeness
       |  - Theoretical framework appropriateness
       |  - Missing key citations (especially recent Nature-portfolio papers)
       |  - Incremental vs. substantial contribution to field
       |  - Academic argument accuracy
       |  → Output: Domain Review Report (500–700 words)
       |
       |→ [perspective_reviewer]
       |  - Cross-disciplinary connections
       |  - Practical applications and policy implications
       |  - Broader societal/ethical implications
       |  - Challenges fundamental assumptions from outside the field
       |  → Output: Perspective Review Report (400–600 words)
       |
       +→ [devils_advocate]
          - Strongest counter-argument (200–300 words — most important part)
          - Cherry-picking / confirmation bias detection
          - Logic chain validation (premise → conclusion)
          - Overgeneralization check
          - Alternative explanations analysis
          - Missing stakeholder perspectives
          - "So what?" test
          - Frame-lock detection (unstated premises)
          → Output: Devil's Advocate Report (special format, see §Output Formats)
       |
       ** CHECKPOINT 2: All 5 reports complete. Present summary to user. **
       ** User may ask clarifying questions before Phase 2. **
       |
=== PHASE 2: EDITORIAL SYNTHESIS & DECISION ===
       |
       +→ [editorial_synthesizer]
          1. Read all 5 Phase 1 reports
          2. Map consensus (≥3 reviewers agree) vs. divergence (conflicting opinions)
          3. Arbitrate divergent opinions with reasoning
          4. Flag all DA CRITICAL findings in the Decision Letter
             ⚠️ IRON RULE: If DA CRITICAL findings present → Decision CANNOT be Accept
          5. Produce Editorial Decision Letter (Accept / Minor Revision / Major Revision / Reject)
          6. Produce Revision Roadmap (prioritized, ready for nature-paper-hub Stage 3 revision input)
       |
       ** CHECKPOINT 3: Editorial Decision delivered. **
       ** If Decision = Minor/Major Revision → offer Socratic Revision Coaching **
       ** User can say "just give me the roadmap" to skip coaching **
```

---

## Nature-Specific Calibration

### Journal Specs Loading

At Phase 0, `field_analyst` reads `${CLAUDE_PLUGIN_ROOT}/templates/journal-specs.json` and extracts for the target journal:

```json
{
  "journal": "Nature Catalysis",
  "scope": "...",
  "word_limit_body": 3000,
  "word_limit_abstract": 150,
  "figure_limit": 6,
  "reference_limit": 50,
  "acceptance_rate": "~5%",
  "impact_factor": 37.8,
  "methods_location": "after_references",
  "special_rules": [...]
}
```

All reviewer calibrations use these specs as the baseline.

### Mandatory Nature Compliance Checks (EIC Reviewer)

The EIC reviewer checks these Nature-specific requirements in **every** review:

| Check | Pass Condition | Severity if Missing |
|-------|---------------|-------------------|
| **Data Availability Statement** | Present and specific (not generic "available upon request") | MAJOR |
| **Code Availability Statement** | Present if computational work included | MAJOR |
| **CRediT Author Contributions** | All 14 CRediT roles considered, at least contributor roles filled | MAJOR |
| **Competing Interests Declaration** | Present (even if "none") | MAJOR |
| **EQUATOR Compliance** | CONSORT/ARRIVE/STROBE checklist attached if applicable | MAJOR |
| **Ethics Approval** | Present for human/animal studies | CRITICAL |
| **Funding/Acknowledgements** | Grant numbers included | MINOR |

---

## Statistical Reporting Standards

`methodology_reviewer` applies this complete checklist. Adapted from APA 7.0 + Nature portfolio requirements.

### Universal Reporting Requirements

| Category | Requirement | Red Flag if Missing |
|----------|-------------|-------------------|
| **Descriptive statistics** | *M*, *SD*, *N* (total and per group), range for all continuous variables | HIGH |
| **Effect sizes** | ALL statistical tests must report effect sizes (Cohen's *d*, η², *r*, OR, etc.) | HIGH — APA 7.0 mandatory |
| **Confidence intervals** | 95% CI for all effect sizes and key estimates; format: 95% CI [lower, upper] | MEDIUM |
| **Exact *p*-values** | Report as *p* = .032 (not *p* < .05); use *p* < .001 only when very small | LOW |
| **Statistical power** | A priori power analysis with target power ≥ .80, effect size source stated | MEDIUM |
| **Assumption testing** | Normality, homogeneity of variance, linearity, independence — all tested | MEDIUM |
| **Multiple comparisons** | Bonferroni/Holm/FDR correction when multiple tests performed | HIGH |
| **Missing data** | Amount, proportion, mechanism (MCAR/MAR/MNAR), handling method | MEDIUM |

### Effect Size Quick Reference

| Analysis | Effect Size Metric | Small / Medium / Large |
|----------|--------------------|----------------------|
| *t*-test | Cohen's *d* | 0.2 / 0.5 / 0.8 |
| ANOVA | partial η² | .01 / .06 / .14 |
| Correlation | *r* | .10 / .30 / .50 |
| Regression | *R*², *f*² | *f*²: .02 / .15 / .35 |
| Chi-square | Cramer's *V* | .10 / .30 / .50 |
| Odds ratio | OR | 1.5 / 2.5 / 4.3 |

### Statistical Red Flags (Trigger MAJOR or CRITICAL)

| Red Flag | Severity | Description |
|----------|----------|-------------|
| No effect sizes reported | HIGH | Conclusions rest solely on *p*-values — APA 7.0 violation |
| p-hacking indicators | HIGH | Multiple *p* near .05; selective reporting; flexible stopping rules |
| HARKing | HIGH | Hypotheses appear constructed post-hoc to match results |
| Uncorrected multiple comparisons | HIGH | 3+ group comparisons via multiple *t*-tests instead of ANOVA |
| No power analysis | MEDIUM | Sample size lacks a priori justification |
| Assumption violations untreated | HIGH | Violations reported but original analysis retained unchanged |
| *p* = .000 | LOW | Raw software output; must be *p* < .001 |
| df inconsistent with *N* | HIGH | Strong indicator of data reporting error |
| Causal language, correlational design | MEDIUM | Survey/observational studies claiming causation |
| SEM *N* < 200 without correction | MEDIUM | Small sample SEM without robust ML or bootstrapping |
| VIF > 10 unaddressed | HIGH | Severe multicollinearity ignored |
| p-values only near .05 cluster | HIGH | Distribution anomaly suggesting selective reporting |

### APA 7.0 Format Verification

- Statistics that cannot exceed 1.0 (no leading zero): *r*, *p*, η², *R*², *beta*, Cramer's *V*
- Statistics that can exceed 1.0 (with leading zero): *M*, *SD*, *B*, Cohen's *d*, *t*, *F*, χ²
- Italicize: *M*, *SD*, *N*, *n*, *t*, *F*, *p*, *r*, *R*, *d*, *B*, *beta*, χ²
- Do NOT italicize: df, SS, MS, OR, CI, VIF, AIC, BIC, CFI, RMSEA, ICC, ANOVA, SEM

---

## IRON RULES

1. **READ-ONLY CONSTRAINT**: Reviewers MUST NOT modify the manuscript. All output is separate review documents. If any reviewer agent attempts to edit the paper file → STOP and redirect to report generation only.

2. **REVIEWER INDEPENDENCE**: 5 reviewers work in Phase 1 without seeing each other's reports. No cross-referencing during independent review phases.

3. **NO FABRICATION**: `editorial_synthesizer` cannot invent critique not present in Phase 1 reports. Every synthesis point traces to a specific reviewer report.

4. **DA CRITICAL BLOCKS ACCEPT**: If `devils_advocate` raises any CRITICAL finding → Editorial Decision cannot be Accept or Minor Revision. Decision must be Major Revision or Reject, with DA findings prominently flagged.

5. **NO SYCOPHANCY**: Scores must be evidence-based. A paper with methodology gaps cannot score > 6/10 on rigor. Reviewer pushback does not automatically improve scores.

6. **SPECIFICITY REQUIRED**: Every criticism must state: what is wrong, where it appears (section/paragraph), and a concrete suggested fix. Vague feedback ("the methodology could be stronger") is not acceptable.

7. **JOURNAL CALIBRATION MANDATORY**: Reviews must reference loaded journal specs. A paper that passes for Nature Communications may not pass for Nature Materials — calibrate thresholds accordingly.

---

## Output Formats

### Full Mode Output

```markdown
# Peer Review Simulation Report
**Manuscript:** [Title]
**Target Journal:** [Journal Name] (IF: X.X, acceptance rate: ~X%)
**Review Date:** [Date]
**Mode:** Full Review

---

## Reviewer Configuration Card
[field_analyst output: 5 reviewer personas with identities and focus areas]

---

## EIC Review (Editor-in-Chief)
**Reviewer:** [Configured EIC persona]
**Recommendation:** [Accept / Minor Revision / Major Revision / Reject]

### Journal Fit Assessment
[Scope alignment, novelty for target journal tier]

### Strengths
[3–5 specific strengths]

### Required Changes
**CRITICAL:**
- [Issue: description | Location | Suggested fix]

**MAJOR:**
- [Issue: description | Location | Suggested fix]

**MINOR:**
- [Issue: description | Location]

### Nature Compliance Checklist
- Data Availability Statement: [✅ Present / ⚠️ Generic / ❌ Missing]
- Code Availability Statement: [✅ / ⚠️ / ❌ / N/A]
- CRediT Contributions: [✅ / ⚠️ / ❌]
- Competing Interests: [✅ / ⚠️ / ❌]
- EQUATOR Guideline: [✅ / N/A / ❌]
- Ethics Approval: [✅ / N/A / ❌]

---

## Methodology Review (Peer Reviewer 1)
**Reviewer:** [Configured methodology reviewer persona]
**Recommendation:** [Accept / Minor / Major / Reject]

### Statistical Reporting Assessment
[Score: X/100 | Level: Exemplary/Adequate/Needs Improvement/Inadequate/Unacceptable]

### Red Flags Detected
[List from §Statistical Red Flags, with severity]

### Reproducibility Assessment
[Methods detail, software versions, data/code availability]

### Required Changes
[CRITICAL / MAJOR / MINOR list]

---

## Domain Review (Peer Reviewer 2)
[Literature coverage, theory, field contribution]
[CRITICAL / MAJOR / MINOR list]

---

## Perspective Review (Peer Reviewer 3)
[Cross-disciplinary angles, broader impact]
[CRITICAL / MAJOR / MINOR list]

---

## Devil's Advocate Review
**Reviewer:** [Configured DA persona]

### Strongest Counter-Argument
[200–300 words: the best possible case AGAINST the paper's conclusions]

### Issue List

#### CRITICAL
| # | Dimension | Issue Description | Location |
|---|-----------|-------------------|----------|

#### MAJOR
| # | Dimension | Issue Description | Location |
|---|-----------|-------------------|----------|

#### MINOR
| # | Dimension | Issue Description | Location |
|---|-----------|-------------------|----------|

### Ignored Alternative Explanations
1. [Alternative A: why it might be more parsimonious than authors' explanation]
2. [Alternative B: ...]

### Missing Stakeholder Perspectives
- [Perspective 1]
- [Perspective 2]

### Unexamined Premise (if detected)
[Unstated assumption underlying the entire paper]

### Observations (Non-Defects)
- [Observation 1]

---

## Editorial Decision

### Summary of Reviewer Consensus
[What all/most reviewers agreed on]

### Points of Divergence
[Where reviewers disagreed + editorial arbitration]

### ⚠️ Devil's Advocate CRITICAL Issues
[Flagged prominently — these block an Accept decision]

### Editorial Decision: [Accept / Minor Revision / Major Revision / Reject]

**Decision Rationale:**
[Evidence-based reasoning citing specific reviewer reports]

---

## Revision Roadmap

Priority 1 — Must Address (CRITICAL):
- [ ] [Issue description] | Reviewer: [X] | Section: [Y]

Priority 2 — Should Address (MAJOR):
- [ ] [Issue description] | Reviewer: [X] | Section: [Y]

Priority 3 — Consider Addressing (MINOR):
- [ ] [Issue description] | Reviewer: [X] | Section: [Y]

**Estimated revision effort:** [X weeks | new experiments: Y/N | new analyses: Y/N]
```

---

### Quick Mode Output

```markdown
# Quick EIC Assessment
**Target Journal:** [Journal] | **Mode:** Quick (~15 min)

## Top Issues (EIC Perspective)
1. [Most critical issue]
2. [Second issue]
...10. [Tenth issue]

## Nature Compliance Gaps
[Quick checklist from EIC compliance check]

## Preliminary Recommendation
[Accept / Minor / Major / Reject] — based on EIC review only
*Note: Full simulation (full mode) recommended before actual submission.*
```

---

### Re-Review Mode Output (R&R Traceability Matrix)

```markdown
# Re-Review / Revision Verification Report
**Mode:** Re-Review | **Original Decision:** [Decision]

## R&R Traceability Matrix

| # | Original Concern | Reviewer | Claimed Fix (Author) | Verified? | Status |
|---|-----------------|----------|---------------------|-----------|--------|
| 1 | [issue] | R1 | [author's response] | ✅/⚠️/❌ | Resolved/Partial/Unresolved |
| 2 | ... | | | | |

## Residual Issues
[Issues from original review not adequately addressed]

## New Issues Introduced
[Problems created by the revision that weren't in the original paper]

## New Editorial Decision
[Accept / Minor Revision / Major Revision / Reject]
```

---

## Integration

### Pipeline Position

```
nature-paper-hub Stage 6 (Pre-Submission Audit)
    → nature-integrity-check (pre-review mode)   ← run first
    → nature-reviewer-sim (full mode)             ← this skill
    → nature-paper-hub Stage 3 (revisions)
    → nature-reviewer-sim (re-review mode)        ← verify revisions
    → nature-integrity-check (final-check mode)
    → nature-paper-hub Stage 7 (export)
```

### Upstream: nature-paper-hub → nature-reviewer-sim
- Input: completed manuscript (from Stage 2–5 drafting)
- Prerequisite: `nature-integrity-check` in `pre-review` mode must PASS before review simulation begins
- ⚠️ If integrity check not passed: remind user and decline to proceed until resolved

### Downstream: nature-reviewer-sim → nature-paper-hub Stage 8
- The Revision Roadmap format is directly compatible with Stage 8 rebuttal input
- Pass the entire Revision Roadmap to Stage 8 for point-by-point response drafting
- For re-review after revisions: use `re-review` mode

### Downstream: nature-reviewer-sim → nature-integrity-check (final)
- After re-review passes: trigger `nature-integrity-check` in `final-check` mode
- Only after final integrity check PASS → proceed to Stage 7 export

---

## Anti-Patterns

| # | Anti-Pattern | Why It Fails | Correct Behavior |
|---|-------------|-------------|-----------------|
| 1 | Fabricating review comments | Synthesizer invents critique not in any Phase 1 report | Every synthesis point traces to a specific reviewer report |
| 2 | Duplicate criticisms across reviewers | R1/R2/R3 raise identical points = fake diversity | Each reviewer has a distinct non-overlapping angle |
| 3 | Ignoring DA CRITICAL findings | Decision says Accept despite DA flagging critical issues | DA CRITICAL → Decision cannot be Accept (IRON RULE) |
| 4 | Rubber-stamp re-review | Re-review says "all addressed" without verification | Each concern independently verified against revised manuscript |
| 5 | Sycophantic score inflation | Giving 8/10 to mediocre work to avoid conflict | Scores evidence-based; methodology gaps cannot score > 6 on rigor |
| 6 | Editing the manuscript | Reviewer "helpfully" fixes the paper | READ-ONLY: produce reports, never modify the paper |
| 7 | Generic feedback | "The methodology could be stronger" | Every criticism: what's wrong + where it is + proposed fix |
| 8 | Skipping journal calibration | Reviewing against generic standards | Must load journal-specs.json and calibrate thresholds to target journal |

---

## Version Info

| Item | Value |
|------|-------|
| Version | 1.0 |
| Created | 2026-05-20 |
| Parent Skill | nature-paper-hub v1.0.0 |
| Based On | academic-paper-reviewer v1.7 |
| Role | Nature-series pre-submission peer review simulator |
