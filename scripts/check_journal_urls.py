"""Check author guides; distinguish broken URLs from unverified bot blocks."""
import json
import os
import time
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


def classify(status):
    if 200 <= status < 300:
        return "ok"
    if status in (401, 403, 429):
        return "unverified"
    return "failed"


def check(url):
    for attempt in range(3):
        try:
            with urlopen(Request(url, headers={"User-Agent": "Mozilla/5.0 (journal-spec-check)"}), timeout=20) as response:
                status = response.status
        except HTTPError as exc:
            status = exc.code
        except (URLError, TimeoutError, OSError):
            status = 0
        if status not in (0, 429) and status < 500:
            break
        if attempt < 2:
            time.sleep(attempt + 1)
    return status, classify(status)


def main():
    specs = json.loads(Path("templates/journal-specs.json").read_text(encoding="utf-8"))
    urls = sorted({j["url"] for j in specs["journals"].values() if j.get("url")})
    if not urls:
        raise ValueError("No journal URLs found")
    report = ["# Journal author guide URL check", "", "403/401/429 are unverified, not proof that a page exists.", "",
              "| Status | HTTP | URL |", "|---|---|---|"]
    failures = 0
    for url in urls:
        status, outcome = check(url)
        report.append(f"| {outcome} | {status or 'network error'} | {url} |")
        print(f"{outcome}: {status} {url}", flush=True)
        if outcome == "failed":
            failures += 1
            print(f"::error::Journal URL failed: {status} {url}")
        elif outcome == "unverified":
            print(f"::warning::Publisher blocked automated verification: {status} {url}")
    text = "\n".join(report) + "\n"
    Path("journal-url-report.md").write_text(text, encoding="utf-8")
    if os.environ.get("GITHUB_STEP_SUMMARY"):
        with open(os.environ["GITHUB_STEP_SUMMARY"], "a", encoding="utf-8") as stream:
            stream.write(text)
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
