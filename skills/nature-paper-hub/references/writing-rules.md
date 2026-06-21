# Section-by-section writing rules

_Part of the `nature-paper-hub` skill — loaded on demand; do not duplicate into SKILL.md._

### Abstract Writing Rules (Nature Portfolio):
- Single paragraph, no citations, no undefined abbreviations
- Sentence 1–2: Broad context (why does this matter globally?)
- Sentence 3–4: Specific problem or gap
- Sentence 5–6: Your approach/method (brief)
- Sentence 7–8: Key quantitative results
- Sentence 9–10: Significance and outlook
- Target: exactly 150 words (or journal limit)
- Tense: Present for known facts; Past for what you did; Present for conclusions

**📊 After drafting abstract — always run word count check:**
```
Current word count: [X] / [journal limit]
Status: [✅ within limit | ⚠️ X words over — suggest cuts below]
```
If over limit, suggest specific cuts: remove adjectives, merge sentences, cut background context.

### Introduction Writing Rules:
- 4–6 paragraphs, ~800 words total
- Each paragraph has a clear topic sentence
- Citations must be accurate — verify with web_search if uncertain
- Final paragraph: explicitly state what this paper reports
- Avoid: "In this paper, we..." (use "Here we show/report/demonstrate...")
- Avoid: excessive self-citation

### Results Writing Rules:
- Lead each subsection with the key finding (topic sentence = result)
- Present data before interpretation
- Every figure/table must be cited in order (Fig. 1a, Fig. 1b, Fig. 2...)
- Use past tense for observations; present tense for general truths
- Quantify everything: "increased by 3.2-fold" not "significantly increased"
- Error bars: always state what they represent (mean ± s.d., n = X)

### Discussion Writing Rules:
- Do NOT restate Results — interpret and contextualize them
- Compare explicitly with the best prior work (with citations)
- Address limitations honestly (reviewers will ask if you don't)
- End with 1 sentence of broader impact

### Methods Writing Rules:
- Enough detail for independent reproduction
- Include all instrument models, software versions, parameters
- For computational work: functional, basis set, k-points, cutoff energy, software version
- Statistical methods: which test, software, significance threshold (p < 0.05)
- Ethics/IRB statements if applicable

### 🔍 Post-Section Self-Critique (run after drafting EVERY section)
After delivering each drafted section, immediately evaluate it from a Nature reviewer's perspective:

```
📋 Self-critique — [Section Name]:
✅ Strengths:
  - [what works well]
⚠️ Weaknesses / likely reviewer concerns:
  - [specific issue 1: e.g., "Claim in ¶2 lacks quantitative support"]
  - [specific issue 2: e.g., "Mechanism not distinguished from alternative explanations"]
  - [specific issue 3: e.g., "'Significantly' used without p-value"]
💡 Suggested improvements:
  - [concrete fix for each weakness]
```

Do NOT skip this step. If the user wants to proceed anyway, acknowledge the risks.
