#!/usr/bin/env python3
"""
clean_papers_index.py — Clean and de-duplicate the static literature index.

The original data/papers-index.json was built from raw PDF text extraction and
contains patents, mid-sentence text fragments, OCR-garbled author strings, and
duplicate / citation-as-title entries. This script produces a cleaned index that
is safe to use for local keyword search.

Usage:
    python3 scripts/clean_papers_index.py \
        --input data/papers-index.json \
        --output data/papers-index.json \
        --backup data/papers-index.raw.json
It is idempotent and re-runnable. A backup of the raw file is written once.
"""
import argparse, json, re, os, sys
from pathlib import Path

WS = re.compile(r'\s+')
# Known venue abbreviations -> canonical journal name (for backfilling empty journal)
VENUES = [
    (r'\bNat\.?\s+Mater', 'Nature Materials'),
    (r'\bNat\.?\s+Chem\b', 'Nature Chemistry'),
    (r'\bNat\.?\s+Commun', 'Nature Communications'),
    (r'\bNat\.?\s+Energy', 'Nature Energy'),
    (r'\bNat\.?\s+Catal', 'Nature Catalysis'),
    (r'\bNat\.?\s+Synth', 'Nature Synthesis'),
    (r'\bNature\b', 'Nature'),
    (r'\bSci\.?\s+Adv', 'Science Advances'),
    (r'\bScience\b', 'Science'),
    (r'\bJ\.?\s*Am\.?\s*Chem\.?\s*Soc|JACS', 'Journal of the American Chemical Society'),
    (r'\bAngew\.?\s*Chem', 'Angewandte Chemie'),
    (r'\bAdv\.?\s+Mater', 'Advanced Materials'),
    (r'\bACS\s+Nano', 'ACS Nano'),
    (r'\bPNAS|Proc\.?\s*Natl', 'PNAS'),
    (r'\bnpj\s+Comput', 'npj Computational Materials'),
    (r'\bCell\b', 'Cell'),
]
DOI_RE = re.compile(r'10\.\d{4,9}/[-._;()/:A-Za-z0-9]+')
YEAR_RE = re.compile(r'(19|20)\d{2}')

def norm_ws(x):
    return WS.sub(' ', (x or '').strip())

def is_patent(title):
    t = title.lower()
    return bool(
        'patent application publication' in t
        or re.search(r'\(\s*1[0-9]\s*\)\s*united states', t)
        or re.search(r'\bus\s?\d{4}/?\s?\d{6,}', t)
        or t.startswith('in us ')
        or re.search(r'pub\.?\s*no\.?\s*:?\s*us', t)
    )

def is_fragment(title):
    # mid-sentence fragment: begins with a lowercase letter
    if not title:
        return True
    first = title.lstrip()[:1]
    if first.islower():
        return True
    # almost no letters / mostly symbols
    letters = sum(c.isalpha() for c in title)
    return letters < 8

def is_garbled_author(a):
    if not a:
        return False
    if re.search(r'[a-z][A-Z][a-z]', a):          # ReSeAR / AnceS camel-noise
        return True
    toks = a.split()
    if not toks:
        return False
    short = sum(1 for t in toks if len(t) <= 2)
    return short >= 3 or '|' in a

def backfill_journal(rec):
    if rec.get('journal', '').strip():
        return rec['journal'].strip()
    hay = (rec.get('title', '') + ' ' + rec.get('abstract', ''))
    for pat, name in VENUES:
        if re.search(pat, hay):
            return name
    return ''

def trim_citation_title(title):
    # "Author et al., Sci. Adv. 11, eadw7071 (2025)   4 July 202" -> up to (2025)
    m = re.match(r'^(.{10,}?\((?:19|20)\d{2}\))', title)
    return m.group(1) if m else title

def key_of(title):
    return re.sub(r'[^a-z0-9]', '', title.lower())[:120]

def completeness(rec):
    return sum(1 for k in ('journal', 'doi', 'year', 'authors', 'abstract') if rec.get(k, '').strip())

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--input', default='data/papers-index.json')
    ap.add_argument('--output', default='data/papers-index.json')
    ap.add_argument('--backup', default='data/papers-index.raw.json')
    args = ap.parse_args()

    data = json.load(open(args.input, encoding='utf-8'))
    papers = data['papers'] if isinstance(data, dict) and 'papers' in data else data
    n0 = len(papers)

    # one-time raw backup
    if args.backup and not Path(args.backup).exists():
        json.dump(data, open(args.backup, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)

    dropped = {'patent': 0, 'fragment': 0, 'duplicate': 0}
    fixed = {'authors_cleared': 0, 'title_trimmed': 0, 'journal_filled': 0, 'year_filled': 0, 'doi_filled': 0}
    seen = {}
    out = []

    for p in papers:
        title = norm_ws(p.get('title', ''))
        if is_patent(title):
            dropped['patent'] += 1
            continue
        # trim citation-as-title noise before fragment test
        tt = trim_citation_title(title)
        if tt != title:
            title = tt; fixed['title_trimmed'] += 1
        if is_fragment(title):
            dropped['fragment'] += 1
            continue

        rec = {
            'title': title,
            'authors': norm_ws(p.get('authors', '')),
            'journal': norm_ws(p.get('journal', '')),
            'year': norm_ws(str(p.get('year', ''))),
            'doi': norm_ws(p.get('doi', '')),
            'abstract': norm_ws(p.get('abstract', '')),
        }
        # if abstract just duplicates the title, drop the abstract noise
        if rec['abstract'] == rec['title']:
            rec['abstract'] = ''
        # clean garbled authors
        if is_garbled_author(rec['authors']):
            rec['authors'] = ''; fixed['authors_cleared'] += 1
        # backfill journal
        j = backfill_journal(rec)
        if j and not p.get('journal', '').strip():
            rec['journal'] = j; fixed['journal_filled'] += 1
        # backfill year (only plausible publication years)
        if not rec['year']:
            cands = [int(y) for y in re.findall(r'(?:19|20)\d{2}', rec['title'] + ' ' + rec['abstract'])]
            cands = [y for y in cands if 1990 <= y <= 2027]
            if cands:
                rec['year'] = str(max(cands)); fixed['year_filled'] += 1
        # backfill doi from text
        if not rec['doi']:
            m = DOI_RE.search(p.get('abstract', '') + ' ' + p.get('title', ''))
            if m:
                rec['doi'] = m.group(0); fixed['doi_filled'] += 1

        k = key_of(rec['title'])
        if k in seen:
            dropped['duplicate'] += 1
            # keep the more complete of the two
            if completeness(rec) > completeness(out[seen[k]]):
                out[seen[k]] = rec
            continue
        seen[k] = len(out)
        out.append(rec)

    out.sort(key=lambda r: (r.get('year') or '0', r['title']), reverse=True)
    result = {
        'description': (data.get('description') if isinstance(data, dict) else
                        'Curated literature index for top-journal writing style anchoring and citation lookup.'),
        'source': (data.get('source') if isinstance(data, dict) else 'mixed'),
        'cleaned': True,
        'total': len(out),
        'papers': out,
    }
    json.dump(result, open(args.output, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)

    print(f"papers in : {n0}")
    print(f"papers out: {len(out)}")
    print(f"dropped   : {dropped}  (total {sum(dropped.values())})")
    print(f"fixed     : {fixed}")
    empty_j = sum(1 for r in out if not r['journal'])
    empty_d = sum(1 for r in out if not r['doi'])
    print(f"remaining empty journal: {empty_j} ({100*empty_j//max(1,len(out))}%)  empty doi: {empty_d} ({100*empty_d//max(1,len(out))}%)")

if __name__ == '__main__':
    main()
