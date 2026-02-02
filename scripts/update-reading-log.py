#!/usr/bin/env python3
import os
from urllib.request import Request, urlopen

README_PATH = "README.md"
START_MARKER = "<!-- READING-LOG:START -->"
END_MARKER = "<!-- READING-LOG:END -->"


def fetch_markdown(url: str) -> str:
    req = Request(url, headers={"User-Agent": "reading-log-updater"})
    with urlopen(req, timeout=10) as resp:
        body = resp.read().decode("utf-8")
    return body.strip()


def replace_block(content: str, replacement: str) -> str:
    start = content.find(START_MARKER)
    end = content.find(END_MARKER)
    if start == -1 or end == -1 or end < start:
        raise ValueError("Reading log markers not found or misordered.")

    start_end = start + len(START_MARKER)
    before = content[:start_end]
    after = content[end:]
    return f"{before}\n{replacement}\n{after}"


def main() -> int:
    url = os.getenv("READING_LOG_MARKDOWN_URL")
    if not url:
        print("READING_LOG_MARKDOWN_URL is not set. Skipping update.")
        return 0

    try:
        markdown = fetch_markdown(url)
    except Exception as exc:
        print(f"Failed to fetch reading log: {exc}")
        return 0
    if not markdown:
        markdown = "- _No items yet._"

    with open(README_PATH, "r", encoding="utf-8") as handle:
        original = handle.read()

    updated = replace_block(original, markdown)
    if updated == original:
        print("README already up to date.")
        return 0

    with open(README_PATH, "w", encoding="utf-8") as handle:
        handle.write(updated)

    print("README updated.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
