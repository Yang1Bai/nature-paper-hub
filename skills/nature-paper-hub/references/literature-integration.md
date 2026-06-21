# Literature search, RAG & CrossRef integration

_Part of the `nature-paper-hub` skill — loaded on demand; do not duplicate into SKILL.md._

## Integration: Literature Search (two-tier)

### Tier 1 — Static papers index (available to ALL users)
The plugin includes `${CLAUDE_PLUGIN_ROOT}/data/papers-index.json`: 485 cleaned, de-duplicated papers (titles, plus
journal/year/DOI where available) covering the Nature portfolio, Science/Sci. Adv., JACS, Angew. Chem., Adv. Mater.,
npj Computational Materials, and more. Regenerate any time with `python3 ${CLAUDE_PLUGIN_ROOT}/scripts/clean_papers_index.py`.

Load and search it locally:
```python
import json
with open(f"{PLUGIN_ROOT}/data/papers-index.json") as f:  # PLUGIN_ROOT = $CLAUDE_PLUGIN_ROOT
    index = json.load(f)['papers']
# Simple keyword match across title / abstract / journal:
q = query.lower()
results = [p for p in index
           if q in (p.get('title','') + ' ' + p.get('abstract','') + ' ' + p.get('journal','')).lower()]
```
Use for: finding relevant papers to cite, checking what's published, writing style reference.

### Tier 2 — Optional personal literature API (opt-in, off by default)
This tier is **disabled unless** the user sets the `LITREVIEW_API` environment variable to a base
URL that accepts a `?q=<query>` parameter and returns paper records. There is **no hardcoded
endpoint** — never call a specific private host.

- If `LITREVIEW_API` **is set**: `web_fetch(f"{LITREVIEW_API}?q=<URL-encoded query>")`, then merge with Tier 1.
- If `LITREVIEW_API` **is unset** (the default for all users): skip this tier entirely. The full
  pipeline works using Tier 1 + CrossRef + `web_search`.

Always query Tier 1 first.

### RAG-enhanced writing (use when drafting any section):
Before drafting Introduction, Results, or Discussion:

1. Gather style-anchor papers for the topic:
   - Tier 1: keyword-search the local `${CLAUDE_PLUGIN_ROOT}/data/papers-index.json`.
   - Tier 2 (only if `LITREVIEW_API` is set): `web_fetch(f"{LITREVIEW_API}?q=<topic>")`.
   - Always supplement with `web_search("site:nature.com <topic> <year>")`.
2. **Filter returned results — only use high-impact journal papers as style anchors:**
   Priority tier (use for style): Nature, Nature [sub-journals], Science, Cell, JACS, Angew. Chem., Adv. Mater., ACS Nano
   Skip for style (still valid as citations): Electrochimica Acta, JES, Surf. Coat. Technol., J. Alloys Compd., and other engineering/applied journals
   If the returned results are mostly lower-tier journals, supplement with:
   ```
   web_search("site:nature.com <topic> <year>")
   ```
3. From the **filtered** papers, note:
   - How they open the Introduction (first sentence patterns)
   - How Results subsections are titled (use action phrases, not nouns)
   - How Discussion compares with prior work
   - Sentence structures used to present quantitative data
4. Use these as **style anchors** when drafting — mirror the register,
   hedging language, and argumentation patterns of real Nature papers
   in the same field (not generic academic writing).
5. When quoting style patterns, attribute: "[modelled on: Author et al., Journal, Year]"

### CrossRef metadata enrichment:
For any paper found in the index, via the optional personal API, or cited by the user:
```
web_fetch("https://api.crossref.org/works/<DOI>")
```
This returns: full author list, exact title, volume/pages, citation count, funder info.
Use citation count as a proxy for impact when recommending references.
