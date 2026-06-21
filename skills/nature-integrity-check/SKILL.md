---
name: nature-integrity-check
description: "Pre-submission and post-revision integrity verification for top-tier journal manuscripts (Nature, Science, Cell, PNAS, ACS, Wiley families). Runs 5-phase protocol: citation integrity (calls nature-citation upstream), data & statistical claims cross-check, figure integrity, research integrity statements (auto-generates Data Availability, Code Availability, CRediT with 14 roles, Competing Interests, Ethics approval templates), and originality signals. Produces structured PASS/FAIL/WARNING report with CRITICAL/MAJOR/MINOR classification. Two modes: pre-review (before reviewer simulation, fix up to 3x on FAIL) and final-check (IRON RULE: zero CRITICAL to proceed to export). Trigger keywords: 完整性检查, integrity check, 投稿前检查, pre-submission check, 检查完整性, verify integrity, 投稿前验证."
metadata:
  version: "1.0"
  last_updated: "2026-05-20"
  status: active
  parent_skill: nature-paper-hub
  related_skills:
    - nature-citation
    - nature-reviewer-sim
    - nature-paper-hub
---

# nature-integrity-check — Nature Manuscript Integrity Verification

Performs end-to-end integrity verification of a Nature-series manuscript before peer review and before export. Catches citation errors, data inconsistencies, missing required statements, figure problems, and originality signals. Calls `nature-citation` for reference verification, then extends into data, figure, and research integrity checks specific to Nature portfolio journals.

**Core principle: Zero tolerance for CRITICAL issues at final-check.** Every fabricated reference, unsupported claim, missing mandatory statement, or data inconsistency must be found and corrected before submission.

---

## Trigger Keywords

| Language | Phrases |
|----------|---------|
| Chinese | 完整性检查、投稿前检查、检查完整性、投稿前验证、完整性验证、帮我检查论文完整性 |
| English | integrity check, pre-submission check, verify integrity, integrity verification, check manuscript integrity, pre-submission verification |

### Non-Trigger Scenarios

| Scenario | Use Instead |
|----------|-------------|
| Finding new citations for claims | `nature-citation` |
| Full reviewer simulation | `nature-reviewer-sim` |
| Writing or revising manuscript sections | `nature-paper-hub` Stages 2–5 |

---

## Two Operating Modes

### Mode 1: `pre-review` (Stage 6 — Before Reviewer Simulation)

**Goal:** Catch integrity issues before `nature-reviewer-sim` runs.

- Run all 5 phases with pre-review sampling rates (see Phase details below)
- Issues found → produce correction list → fix → re-verify corrected items
- Up to **3 fix-and-recheck cycles** before escalating to user
- **Must achieve zero CRITICAL issues to proceed to `nature-reviewer-sim`**
- MAJOR and MINOR issues may proceed with user acknowledgement

**Invoke:** say `完整性检查` / `integrity check` / `pre-review check`

---

### Mode 2: `final-check` (Stage 9 — Before Export)

**Goal:** Final gate before manuscript export. No CRITICAL issues allowed.

- Run all 5 phases at final-check sampling rates (higher coverage)
- Phase 1 runs **fresh** — does not rely on pre-review results
- Phase 4 checks that all auto-generated statement templates were actually filled in
- **⚠️ IRON RULE: Zero CRITICAL issues required to proceed to export**
- MAJOR issues require user acknowledgement and decision to proceed
- MINOR issues noted but do not block export

**Invoke:** say `最终检查` / `final integrity check` / `final-check`

---

## 5-Phase Verification Protocol

### Phase 1 — Citation Integrity

**Calls `nature-citation` upstream for reference verification.**

#### 1a. Reference Existence Verification
For every reference in the manuscript:
1. Invoke `nature-citation` Mode 2 (verify existing reference list)
2. Confirm each reference:
   - **VERIFIED**: Real publication found with matching bibliographic details
   - **NOT_FOUND**: No match after 3 search attempts → CRITICAL issue (suspected fabrication)
   - **MISMATCH**: Found similar but different publication → CRITICAL issue (suspected hallucinated mashup)

⚠️ Known Citation Hallucination Patterns to actively detect:

| Type | Code | Description | Detection |
|------|------|-------------|-----------|
| Total Fabrication | TF | Entire paper doesn't exist | Title + author search returns nothing |
| Plausible Author/Conference | PAC | Real scholars attributed to papers they never wrote | Verify author's actual publication list |
| Incomplete Hallucination | IH | Missing DOI, vague pages, no volume | Flag any reference lacking DOI + volume + pages |
| Partial Hallucination | PH | Mashup of real elements from different sources | Cross-verify ALL metadata fields against ONE source |
| Subtle Hallucination | SH | Minor distortions (wrong year, swapped venue) | Compare each field individually against publisher page |

#### 1b. Bibliographic Accuracy (for VERIFIED references)
- Author names and count (co-authors omitted?)
- Publication year (published version, not preprint)
- Journal name correct and properly abbreviated (Nature style)
- Volume, issue, page numbers accurate
- DOI resolves to the correct paper
- Not retracted (check RetractionWatch)

#### 1c. Ghost Citation Check
- Every reference list entry → cited in body text? (orphan reference = MINOR)
- Every in-text citation → appears in reference list? (dangling citation = MAJOR)

#### 1d. Nature Citation Format
- Numbered style (order of appearance)
- ≤6 authors then "et al."
- Journal names abbreviated (Nature portfolio abbreviations)
- Pages with en-dash (–) not hyphen (-)
- DOI included

**Sampling Rate:**
- pre-review: 100% of references (Phase 1 is always complete)
- final-check: 100% fresh verification (independent of pre-review results)

---

### Phase 2 — Data & Statistical Claims Cross-Check

#### 2a. Statistical Data Accuracy
For all numerical claims citing a source:
1. Identify the specific passage in the cited source supporting the claim
2. Compare: exact numbers match? Date ranges accurate? Population descriptions faithful?
3. Flag discrepancies

| Verdict | Severity | Definition |
|---------|----------|------------|
| VERIFIED | None | Claim matches source exactly or within rounding tolerance |
| MINOR_DISTORTION | MINOR | Paraphrases source but meaning preserved |
| MAJOR_DISTORTION | MAJOR | Oversimplifies, exaggerates, or misrepresents |
| UNVERIFIABLE | MAJOR | Source doesn't contain the claimed information |
| UNVERIFIABLE_ACCESS | MINOR | Source exists but full text not accessible |

#### 2b. Internal Consistency Check
- Same data point consistent across different paragraphs/sections?
- Calculations correct (percentages, ratios, totals add up)?
- Tables consistent with body text descriptions?
- Abstract statistics match Results section statistics?
- n values consistent between Methods, Results, and Figure legends?

#### 2c. Statistical Reporting Completeness (Quick Scan)
- Effect sizes present for all statistical tests? (HIGH severity if missing — APA 7.0 mandatory)
- Confidence intervals reported for key estimates?
- Exact *p*-values reported (not just *p* < .05)?
- Error bars defined in figure legends (mean ± s.d., n = X)?

**Sampling Rate:**
- pre-review: 30% of quantitative claims (minimum 10 claims)
- final-check: 100% of quantitative claims

---

### Phase 3 — Figure Integrity

#### 3a. Figure-Text Consistency
- All figures cited in order in body text (Fig. 1a before Fig. 2)?
- Every figure cited in text has a corresponding figure file / description?
- Figure count ≤ journal limit (from `${CLAUDE_PLUGIN_ROOT}/templates/journal-specs.json`)?

#### 3b. Figure Legend Completeness
Each figure legend must include:
- [ ] Scale bars defined for all microscopy images
- [ ] Error bars defined: "Data are mean ± s.d." or "mean ± s.e.m." with n value
- [ ] Statistical significance indicators explained (*, **, ***, exact *p*-values preferred)
- [ ] Sample sizes (*n* = X) stated
- [ ] Abbreviations defined at first use in legend
- [ ] Panel labels (a, b, c...) present and match figure

#### 3c. Extended Data / Supplementary
- Extended data figures ≤ 10 items (for journals that allow it)?
- Supplementary figures properly referenced in main text?
- Methods section: does it comply with journal rules (no figures in Methods for Nature Synthesis)?

**Sampling Rate:** 100% of figures in both modes.

---

### Phase 4 — Research Integrity Statements

#### 4a. Required Statement Presence Check

Check that ALL required statements are present (not placeholder templates):

| Statement | Required For | Pass Condition |
|-----------|-------------|---------------|
| **Data Availability** | All manuscripts | Present + specific repository/URL or "available upon reasonable request" with reason |
| **Code Availability** | Computational work | Present + repository URL or reason for restriction |
| **CRediT Author Contributions** | All manuscripts | All authors assigned roles from the 14 CRediT taxonomy |
| **Competing Interests** | All manuscripts | Present (even if "The authors declare no competing interests") |
| **Ethics Approval** | Human/animal studies | IRB number + approval statement present |
| **Acknowledgements** | All manuscripts | Funding sources with grant numbers |

#### 4b. Statement Quality Check
- Data Availability: is it specific (repository + accession number) or generic ("available upon request")?
  - ⚠️ Generic "available upon request" without reason → MINOR (some journals accept; flag for attention)
  - Missing entirely → MAJOR
- CRediT contributions: are all contributing authors assigned ≥1 role?

#### 4c. Auto-Generated Statement Templates

When any required statement is missing or placeholder, auto-generate a paste-ready template:

---

**📋 DATA AVAILABILITY STATEMENT TEMPLATE:**
```
The data that support the findings of this study are available [in the following 
repository: <REPOSITORY NAME> under accession code <CODE>] / [from the corresponding 
author upon reasonable request]. [Source data are provided as a Source Data file.]
```
*→ User must fill in: repository name and accession code, or reason for restricted access.*

---

**📋 CODE AVAILABILITY TEMPLATE:**
```
The code used in this study is available [at <REPOSITORY URL> (ref. <CITATION>)] / 
[from the corresponding author upon reasonable request]. [Custom code has been 
deposited at <URL>.]
```
*→ User must fill in: repository URL, or reason for restriction.*

---

**📋 CRediT AUTHOR CONTRIBUTIONS TEMPLATE:**
```
[Author A]: Conceptualization, Methodology, [add roles]. 
[Author B]: Investigation, Formal analysis, [add roles]. 
[Author C]: Writing – original draft, [add roles].
[Author D]: Writing – review & editing, Supervision, [add roles].
[Corresponding author]: Conceptualization, Funding acquisition, Supervision, 
Writing – review & editing.
```

**The 14 CRediT Roles (user must assign — do NOT fabricate):**
1. Conceptualization — Ideas; formulation of overarching research goals
2. Data curation — Management of research data, annotation, scrubbing
3. Formal analysis — Application of statistical / mathematical techniques
4. Funding acquisition — Acquisition of financial support
5. Investigation — Conducting experiments / data collection
6. Methodology — Development of methods and models
7. Project administration — Management and coordination
8. Resources — Provision of study materials, reagents, instruments
9. Software — Programming, software development
10. Supervision — Oversight of the research activity
11. Validation — Verification of outputs / experiments
12. Visualization — Data presentation, figures, tables
13. Writing – original draft — Preparation of initial draft
14. Writing – review & editing — Reviewing and revising the manuscript

⚠️ **IRON RULE: CRediT roles must be filled by the user.** The agent provides the template and role definitions but NEVER fabricates author contributions. Present the template and wait for user input.

---

**📋 COMPETING INTERESTS STATEMENT TEMPLATE:**
```
[Option A — No conflicts:]
The authors declare no competing interests.

[Option B — Conflicts present:]
[Author A] declares [specific relationship, e.g., "is a paid consultant for 
Company X"]. [Author B] holds a patent related to this work [patent number]. 
The remaining authors declare no competing interests.
```
*→ User must confirm which option applies and fill in any specific conflicts.*

---

**📋 ETHICS APPROVAL STATEMENT TEMPLATE:**
```
[For human studies:]
All experiments were performed in accordance with relevant guidelines and 
regulations. The study was approved by [INSTITUTION] Institutional Review Board 
(approval number: [IRB NUMBER]). Informed consent was obtained from all 
participants [or: Informed consent was waived by the IRB because...].

[For animal studies:]
All animal experiments were conducted in accordance with [INSTITUTION] Animal 
Care and Use Committee guidelines (protocol number: [IACUC NUMBER]) and complied 
with [ARRIVE guidelines / relevant national regulations].
```
*→ User must fill in: institution name, approval number, consent details.*

---

**Sampling Rate:** 100% of statements in both modes (statements are either present or not).

---

### Phase 5 — Originality Signals

#### 5a. Self-Citation Ratio Check
1. Count total references in manuscript
2. Count references authored by the manuscript's author(s)
3. Calculate self-citation ratio

| Self-Citation Ratio | Status | Action |
|--------------------|--------|--------|
| ≤ 20% | ✅ Normal | No action |
| 21–30% | ⚠️ Elevated | Flag for attention; note in report |
| > 30% | 🔴 **Flag** | **MAJOR** warning — reviewers will notice; user should review and trim |

#### 5b. Uncited Claims Check (Spot Sampling)
For a sample of key claims in Introduction and Discussion:
- Does each factual/quantitative claim have a citation?
- Are broad assertions ("it is well established that...") supported?

| Issue | Severity |
|-------|----------|
| Key quantitative claim without citation | MAJOR |
| Broad assertion without supporting reference | MINOR |
| Multiple consecutive uncited claims in Introduction | MAJOR |

#### 5c. Originality Spot-Check
Sample characteristic sentences (8–12 words, unique content) and search for exact/near matches:

| Grade | Definition | Severity |
|-------|-----------|---------|
| ORIGINAL | No matches | None |
| COMMON_KNOWLEDGE | Same fact in multiple sources, standard phrasing | None |
| PARAPHRASE | Semantically similar but clearly different wording, with citation | None |
| CLOSE_MATCH | Highly similar wording, few words substituted | MINOR |
| VERBATIM | 20+ consecutive identical words without quotation marks | CRITICAL |

**Sampling Rate:**
- pre-review: ≥ 30% of paragraphs, prioritizing Introduction and Discussion
- final-check: ≥ 50% of paragraphs; newly added/revised paragraphs 100%

---

## Output Format

```markdown
# Integrity Check Report
**Manuscript:** [Title]
**Target Journal:** [Journal]
**Check Mode:** [pre-review / final-check]
**Date:** [Date]

---

## ⚖️ OVERALL VERDICT: [PASS ✅ / PASS WITH NOTES ⚠️ / FAIL ❌]

| CRITICAL issues | MAJOR issues | MINOR issues |
|----------------|-------------|-------------|
| X              | X           | X           |

**Proceed to:** [nature-reviewer-sim (pre-review PASS) / Export (final-check PASS) / Fix required (FAIL)]

---

## Verification Summary

| Phase | Category | Total Checked | Passed | Issues Found |
|-------|----------|--------------|--------|-------------|
| 1 | Reference Existence | X | X | X |
| 1 | Bibliographic Accuracy | X | X | X |
| 1 | Ghost Citations | X | X | X orphan / X dangling |
| 1 | Nature Citation Format | X | X | X |
| 2 | Statistical Claims | X (X% sampled) | X | X |
| 2 | Internal Consistency | — | Pass/Fail | X inconsistencies |
| 2 | Statistical Reporting | — | Pass/Fail | X missing elements |
| 3 | Figure-Text Consistency | X | X | X |
| 3 | Figure Legend Completeness | X | X | X |
| 4 | Required Statements | 6 | X | X missing/placeholder |
| 4 | Statement Quality | X | X | X |
| 5 | Self-Citation Ratio | — | X% | [Flag if >30%] |
| 5 | Uncited Claims | X (sampled) | X | X |
| 5 | Originality Spot-Check | X (X% sampled) | X | X |

---

## Issue List (Sorted by Severity)

### 🔴 CRITICAL (Must Fix — blocks proceed)
| # | Phase | Location | Issue Description | Correct Information / Fix Required |
|---|-------|----------|------------------|----------------------------------|
| 1 | P1 | §References | [e.g., "Reference #14 not found after 3 searches — suspected fabrication"] | [Search and replace with real citation] |

### 🟡 MAJOR (Must Fix before submission — blocks final-check PASS)
| # | Phase | Location | Issue Description | Fix Required |
|---|-------|----------|------------------|-------------|
| 1 | P2 | §Results ¶3 | [e.g., "Effect size not reported for t-test on p. X"] | [Add Cohen's d with 95% CI] |

### 🔵 MINOR (Recommended Fix — does not block)
| # | Phase | Location | Issue Description | Suggestion |
|---|-------|----------|------------------|-----------|
| 1 | P1 | §References | [e.g., "Reference #7 missing DOI"] | [Add DOI: 10.xxxx/xxxxx] |

---

## Auto-Generated Statement Templates

[Include only for statements that are missing or need updating]

### Data Availability Statement
[Template text — see Phase 4 templates]
⚠️ *User must fill in: [specific items needed]*

### Code Availability Statement
[Template text — if applicable]

### CRediT Author Contributions
[Template with role definitions]
⚠️ *IRON RULE: User must assign roles — do not fabricate*

### Competing Interests
[Template text]

### Ethics Approval
[Template text — if applicable]

---

## Phase 5 Originality Summary

**Self-Citation Ratio:** X / Y = Z% [✅ Normal / ⚠️ Elevated / 🔴 Flag >30%]

**Originality Spot-Check:**
| Grade | Paragraphs | Proportion |
|-------|-----------|-----------|
| ORIGINAL | X | X% |
| COMMON_KNOWLEDGE | X | X% |
| PARAPHRASE | X | X% |
| CLOSE_MATCH | X | X% |
| VERBATIM | X | X% |

---

## ⚠️ Disclaimer

> This integrity check uses web search for reference verification and originality heuristics. It is not a substitute for professional plagiarism detection tools (Turnitin / iThenticate). Reference verification coverage is limited to publicly searchable literature. Originality check sampling rate: [X]%. Recommend using professional tools for final duplicate checking before formal submission.

---

## Correction Tracking (FAIL mode)

**Round [X] of 3:**
Items corrected: [list]
Items still requiring fix: [list]
[If round 3 reached without PASS → escalate to user with unresolved items list]
```

---

## Verdict Criteria

| Verdict | Condition | Proceed To |
|---------|-----------|-----------|
| **PASS ✅** | Zero CRITICAL + zero MAJOR + zero MAJOR_DISTORTION + zero UNVERIFIABLE | Next stage |
| **PASS WITH NOTES ⚠️** | Zero CRITICAL + zero MAJOR + has MINOR only | Next stage with notes attached |
| **FAIL ❌** | Any CRITICAL, or any MAJOR | Block; produce correction list; re-verify after fixes |

### IRON RULE for final-check Mode
**Zero CRITICAL issues required.** No exceptions. If CRITICAL issues remain after 3 fix cycles → user must resolve manually before export is permitted.

---

## IRON RULES

1. **ZERO CRITICAL IN FINAL-CHECK**: Final-check mode MUST produce zero CRITICAL issues before proceeding to export. This rule cannot be overridden by the user.

2. **NEVER FABRICATE AVAILABILITY STATEMENTS**: The agent provides templates and reminds users what to fill in. It never generates specific repository URLs, accession codes, IRB numbers, or claims of data availability that the user has not provided.

3. **CRediT FILLED BY USER**: Author contribution roles must be assigned by the user. The agent provides the 14-role taxonomy and templates but does not assign roles to authors.

4. **NO GRAY ZONE**: Every reference must have an explicit verdict: VERIFIED, NOT_FOUND, or MISMATCH. "Difficult to verify" is not a verdict — classify as NOT_FOUND.

5. **FRESH VERIFICATION IN FINAL-CHECK**: Phase 1 in final-check mode re-verifies ALL references from scratch, independent of pre-review results. Pre-review verification may have had sampling gaps.

6. **CORRECTION CYCLE LIMIT**: Maximum 3 fix-and-recheck cycles in pre-review mode. After 3 rounds with remaining issues → escalate to user with explicit unresolved items list.

---

## Integration

### Upstream: nature-citation
- Phase 1 calls `nature-citation` Mode 2 for reference existence and accuracy verification
- `nature-citation` handles the actual CrossRef lookups, DOI verification, and retraction checks
- `nature-integrity-check` receives results and escalates to CRITICAL/MAJOR/MINOR classification

### Downstream: Passes to nature-reviewer-sim (pre-review PASS)
- After pre-review PASS → manuscript proceeds to `nature-reviewer-sim` full mode
- Pass the integrity report summary to reviewer-sim so EIC agent is aware of any MINOR issues

### Downstream: Passes to Export (final-check PASS)
- After final-check PASS → manuscript proceeds to nature-paper-hub Stage 10 export
- Attach the final integrity report as part of the submission package documentation

### Pipeline Position

```
nature-paper-hub Stages 0–5 (draft + figures + citations)
    → nature-integrity-check [pre-review mode]    ← Stage 6
          ↓ PASS
    → nature-reviewer-sim [full mode]             ← Stage 7
          ↓ revision complete
    → nature-paper-hub Stage 8 (Pre-Submission Audit + cover letter)
    → nature-integrity-check [final-check mode]   ← Stage 9
          ↓ PASS (zero CRITICAL)
    → nature-paper-hub Stage 10 (export)
```

---

## Version Info

| Item | Value |
|------|-------|
| Version | 1.0 |
| Created | 2026-05-20 |
| Parent Skill | nature-paper-hub v1.0.0 |
| Based On | integrity_verification_agent (academic-pipeline) |
| Role | Pre-submission and final integrity gate for Nature manuscripts |
