#!/usr/bin/env python3
from __future__ import annotations

import json
import re
from pathlib import Path
from urllib.request import urlopen

from bs4 import BeautifulSoup
from markdownify import markdownify as md


PAGES = [
    ("get-started/install", "https://docs.langchain.com/oss/python/langchain/install"),
    ("get-started/quickstart", "https://docs.langchain.com/oss/python/langchain/quickstart"),
    ("get-started/changelog", "https://docs.langchain.com/oss/python/releases/changelog"),
    ("get-started/philosophy", "https://docs.langchain.com/oss/python/langchain/philosophy"),
    ("core-components/agents", "https://docs.langchain.com/oss/python/langchain/agents"),
    ("core-components/models", "https://docs.langchain.com/oss/python/langchain/models"),
    ("core-components/messages", "https://docs.langchain.com/oss/python/langchain/messages"),
    ("core-components/tools", "https://docs.langchain.com/oss/python/langchain/tools"),
    ("core-components/short-term-memory", "https://docs.langchain.com/oss/python/langchain/short-term-memory"),
    ("core-components/overview", "https://docs.langchain.com/oss/python/langchain/overview"),
    ("core-components/structured-output", "https://docs.langchain.com/oss/python/langchain/structured-output"),
    ("middleware/overview", "https://docs.langchain.com/oss/python/langchain/middleware/overview"),
    ("middleware/prebuilt-middleware", "https://docs.langchain.com/oss/python/langchain/middleware/built-in"),
    ("middleware/custom-middleware", "https://docs.langchain.com/oss/python/langchain/middleware/custom"),
    ("frontend/overview", "https://docs.langchain.com/oss/python/langchain/frontend/overview"),
    ("frontend/markdown-messages", "https://docs.langchain.com/oss/python/langchain/frontend/markdown-messages"),
    ("frontend/tool-calling", "https://docs.langchain.com/oss/python/langchain/frontend/tool-calling"),
    ("frontend/human-in-the-loop", "https://docs.langchain.com/oss/python/langchain/frontend/human-in-the-loop"),
    ("frontend/branching-chat", "https://docs.langchain.com/oss/python/langchain/frontend/branching-chat"),
    ("frontend/reasoning-tokens", "https://docs.langchain.com/oss/python/langchain/frontend/reasoning-tokens"),
    ("frontend/structured-output", "https://docs.langchain.com/oss/python/langchain/frontend/structured-output"),
    ("frontend/message-queues", "https://docs.langchain.com/oss/python/langchain/frontend/message-queues"),
    ("frontend/join-rejoin-streams", "https://docs.langchain.com/oss/python/langchain/frontend/join-rejoin"),
    ("frontend/time-travel", "https://docs.langchain.com/oss/python/langchain/frontend/time-travel"),
    ("frontend/generative-ui", "https://docs.langchain.com/oss/python/langchain/frontend/generative-ui"),
    ("advanced-usage/guardrails", "https://docs.langchain.com/oss/python/langchain/guardrails"),
    ("advanced-usage/runtime", "https://docs.langchain.com/oss/python/langchain/runtime"),
    ("advanced-usage/context-engineering", "https://docs.langchain.com/oss/python/langchain/context-engineering"),
    ("advanced-usage/mcp", "https://docs.langchain.com/oss/python/langchain/mcp"),
    ("advanced-usage/human-in-the-loop", "https://docs.langchain.com/oss/python/langchain/human-in-the-loop"),
    ("advanced-usage/multi-agent", "https://docs.langchain.com/oss/python/langchain/multi-agent"),
    ("advanced-usage/retrieval", "https://docs.langchain.com/oss/python/langchain/retrieval"),
    ("advanced-usage/long-term-memory", "https://docs.langchain.com/oss/python/langchain/long-term-memory"),
]


def clean_markdown(text: str) -> str:
    text = text.replace("\u200b", "")
    text = re.sub(r"\n{3,}", "\n\n", text)
    text = re.sub(r"\nCopy\n", "\n", text)
    return text.strip() + "\n"


def extract_page(url: str) -> str:
    html = urlopen(url).read().decode("utf-8", "ignore")
    soup = BeautifulSoup(html, "html.parser")
    content = soup.select_one("div.mdx-content")
    if content is None:
        raise RuntimeError(f"content not found for {url}")
    return clean_markdown(md(str(content), heading_style="ATX"))


def main() -> None:
    root = Path(__file__).resolve().parents[1]
    out_dir = root / "langchain-python-source"
    out_dir.mkdir(parents=True, exist_ok=True)

    manifest = []
    for slug, url in PAGES:
        target = out_dir / f"{slug}.md"
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(extract_page(url), encoding="utf-8")
        manifest.append({"slug": slug, "url": url, "path": str(target.relative_to(root))})

    (out_dir / "manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
