#!/usr/bin/env python3
import os
from urllib.request import Request, urlopen
from xml.etree import ElementTree as ET

README_PATH = "README.md"
START_MARKER = "<!-- BLOG-POSTS:START -->"
END_MARKER = "<!-- BLOG-POSTS:END -->"
FEED_URL = os.getenv("BLOG_FEED_URL", "https://meese.rs/feed.xml")
MAX_POSTS = int(os.getenv("BLOG_MAX_POSTS", "5"))


def fetch_posts(url: str) -> list[tuple[str, str]]:
    req = Request(url, headers={"User-Agent": "blog-posts-updater"})
    with urlopen(req, timeout=10) as resp:
        root = ET.fromstring(resp.read())
    # ponytail: RSS 2.0 only (what @astrojs/rss emits); add Atom branch if the feed format changes.
    items = root.findall("./channel/item")[:MAX_POSTS]
    posts = []
    for item in items:
        title = (item.findtext("title") or "").strip()
        link = (item.findtext("link") or "").strip()
        if title and link:
            posts.append((title, link))
    return posts


def replace_block(content: str, replacement: str) -> str:
    start = content.find(START_MARKER)
    end = content.find(END_MARKER)
    if start == -1 or end == -1 or end < start:
        raise ValueError("Blog post markers not found or misordered.")

    start_end = start + len(START_MARKER)
    return f"{content[:start_end]}\n{replacement}\n{content[end:]}"


def main() -> int:
    try:
        posts = fetch_posts(FEED_URL)
    except Exception as exc:
        print(f"Failed to fetch blog feed: {exc}")
        return 0

    markdown = (
        "\n".join(f"- [{title}]({link})" for title, link in posts)
        if posts
        else "- _No posts yet._"
    )

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
