# Reviewer rebuttal workflow

_Part of the `nature-paper-hub` skill — loaded on demand; do not duplicate into SKILL.md._

### Step 1: Triage — classify ALL comments before writing any response

First, parse and classify every comment:

```
📊 Reviewer Comment Triage:

Reviewer 1:
  Comment 1: [summary] → 🔴 Major | Needs new experiment
  Comment 2: [summary] → 🟡 Major | Needs clarification/additional analysis  
  Comment 3: [summary] → 🟢 Minor | Text revision only
  Comment 4: [summary] → ✅ Valid concern | ❌ Disagree — evidence-based

Reviewer 2:
  ...

📋 Revision Strategy:
  New experiments needed: [list]
  New analyses needed: [list]
  Text-only revisions: [list]
  Planned disagreements: [list with justification]
  Estimated revision effort: [X weeks]
```

Present this triage to the user and confirm strategy before writing responses.

### Step 2: Write point-by-point responses

For each comment (after triage confirmed):
```
**Reviewer X, Comment Y:** [🔴/🟡/🟢]
[Quote the comment exactly]

**Response:**
We thank the reviewer for this [insightful/constructive] comment.
[Acknowledge validity of concern.]
[Explain what you did: new experiment / clarification / revision]
[If adding data]: "We have added [X] to the revised manuscript (Fig. X / Line X)."
[If disagreeing]: "We respectfully disagree because [evidence-based reason with citation]."

**Manuscript change:**
[Quote revised text with line numbers, or state "no change required"]
```

### Step 3: Generate revision cover letter
After all responses:
- Summary of major changes (numbered)
- List of new figures/data added
- Statement of how each reviewer's concerns were addressed
- Tone: confident but respectful
