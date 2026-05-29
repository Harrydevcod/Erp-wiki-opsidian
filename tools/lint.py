#!/usr/bin/env python3
"""Lightweight vault lint: frontmatter, orphans, broken links, index coverage, un-ingested sources."""
import os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WIKILINK = re.compile(r"\[\[([^\]|#]+)")
OPERATING = {"CLAUDE", "AGENTS", "log", "index", "Bem-vindo"}

md_files = {}          # title (stem) -> relpath
for dp, _, files in os.walk(ROOT):
    if any(seg in dp for seg in (os.sep + ".git", os.sep + ".obsidian")):
        continue
    for f in files:
        if f.endswith(".md"):
            rel = os.path.relpath(os.path.join(dp, f), ROOT)
            md_files[f[:-3]] = rel

# Collect link targets + frontmatter presence
links_to = {}          # title -> set of titles it references
no_frontmatter = []
all_text = {}
for title, rel in md_files.items():
    with open(os.path.join(ROOT, rel), encoding="utf-8") as fh:
        txt = fh.read()
    all_text[title] = txt
    if not txt.lstrip().startswith("---"):
        no_frontmatter.append(rel)
    links_to[title] = set(m.group(1).strip() for m in WIKILINK.finditer(txt))

referenced = set()
for s in links_to.values():
    referenced |= s

# Orphans: wiki pages nobody links to (exclude operating files + root module entry pages which are entry points)
orphans = []
for title, rel in sorted(md_files.items()):
    if title in OPERATING:
        continue
    if title not in referenced:
        orphans.append(rel)

# Broken links: [[X]] where no X.md exists
broken = {}
for title, targets in links_to.items():
    for t in targets:
        if t not in md_files and t not in OPERATING:
            broken.setdefault(t, []).append(title)

# Index coverage: wiki/ pages whose title not mentioned in index.md
idx = all_text.get("index", "")
idx_links = set(m.group(1).strip() for m in WIKILINK.finditer(idx))
uncovered = []
for title, rel in sorted(md_files.items()):
    if rel.startswith("wiki" + os.sep) and title not in idx_links:
        uncovered.append(rel)

# Un-ingested raw inbox
inbox = os.path.join(ROOT, "raw", "inbox")
inbox_files = []
if os.path.isdir(inbox):
    inbox_files = [f for f in os.listdir(inbox) if not f.startswith(".")]

def show(label, items, limit=40):
    print(f"\n## {label} ({len(items)})")
    for i in items[:limit]:
        print(f"  - {i}")
    if len(items) > limit:
        print(f"  ... +{len(items)-limit} more")

print(f"Total .md files: {len(md_files)}")
show("Pages WITHOUT frontmatter", no_frontmatter)
show("ORPHAN pages (no inbound wikilink)", orphans)
print(f"\n## BROKEN wikilinks ({len(broken)})")
for t, srcs in sorted(broken.items()):
    print(f"  - [[{t}]] <- {', '.join(sorted(srcs)[:4])}")
show("wiki/ pages NOT in index.md", uncovered)
show("Un-ingested raw/inbox files", inbox_files)
