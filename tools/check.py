#!/usr/bin/env python3
"""Checks the plugin's manifests and skills.

- every manifest has the same name, version and description as
  .claude-plugin/plugin.json;
- each skill's SKILL.md has a name equal to its folder and a description of
  at most 1024 characters (Agent Skills);
- every relative link in the Markdown files resolves, including #anchors;
- links into another skill show that skill's name in the link text, so a
  skill installed on its own still says where the file lives.

With --schemas, also validates plugin.json and .antigravity-plugin/plugin.json
against their published JSON schemas (needs the jsonschema package and
network access).

Run from the repository root: python3 tools/check.py [--schemas]
"""

import glob
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
errors = []


def load(path):
    with open(os.path.join(ROOT, path), encoding="utf-8") as f:
        return json.load(f)


def check_manifests():
    src = load(".claude-plugin/plugin.json")
    want = {k: src[k] for k in ("name", "version", "description")}

    def same(where, got):
        for k, v in want.items():
            if k in got and got[k] != v:
                errors.append(f"{where}: {k} is {got[k]!r}, expected {v!r}")
            elif k not in got and k != "description":
                errors.append(f"{where}: {k} missing")

    same("plugin.json", load("plugin.json"))
    same(".antigravity-plugin/plugin.json", load(".antigravity-plugin/plugin.json"))
    for path in (".claude-plugin/marketplace.json", ".github/plugin/marketplace.json"):
        m = load(path)
        same(f"{path} plugins[0]", m["plugins"][0])
        meta = m.get("metadata", {})
        if meta.get("version") not in (None, want["version"]):
            errors.append(f"{path}: metadata.version is {meta['version']!r}, expected {want['version']!r}")
    codex = load(".agents/plugins/marketplace.json")["plugins"][0]
    if codex["name"] != want["name"]:
        errors.append(f".agents/plugins/marketplace.json plugins[0]: name is {codex['name']!r}")
    for key in ("policy", "category"):
        if key not in codex:
            errors.append(f".agents/plugins/marketplace.json plugins[0]: {key} missing (Codex requires it)")


def check_skills():
    for skill_md in sorted(glob.glob(os.path.join(ROOT, "skills", "*", "SKILL.md"))):
        folder = os.path.basename(os.path.dirname(skill_md))
        text = open(skill_md, encoding="utf-8").read()
        m = re.match(r"^---\n(.*?)\n---\n", text, re.S)
        if not m:
            errors.append(f"skills/{folder}/SKILL.md: no frontmatter")
            continue
        fm = dict(re.findall(r"^(\w+): (.*)$", m.group(1), re.M))
        if fm.get("name") != folder:
            errors.append(f"skills/{folder}/SKILL.md: name {fm.get('name')!r} differs from the folder")
        desc = fm.get("description", "")
        if not desc or len(desc) > 1024:
            errors.append(f"skills/{folder}/SKILL.md: description is {len(desc)} characters (1-1024)")


def slug(heading):
    h = re.sub(r"[^\w\- ]", "", heading.strip().lower())
    return h.replace(" ", "-")


def check_links():
    link = re.compile(r"\[([^\]]+)\]\(([^)\s]+)\)")
    for md in glob.glob(os.path.join(ROOT, "**", "*.md"), recursive=True):
        rel = os.path.relpath(md, ROOT)
        if rel.startswith((".git", "node_modules")):
            continue
        own_skill = rel.split(os.sep)[1] if rel.startswith("skills" + os.sep) else None
        for text, target in link.findall(open(md, encoding="utf-8").read()):
            if re.match(r"^[a-z]+:", target):
                continue
            path, _, anchor = target.partition("#")
            dest = os.path.normpath(os.path.join(os.path.dirname(md), path)) if path else md
            if not os.path.exists(dest):
                errors.append(f"{rel}: broken link {target}")
                continue
            if anchor:
                heads = re.findall(r"^#+\s+(.*)$", open(dest, encoding="utf-8").read(), re.M)
                if anchor not in [slug(h) for h in heads]:
                    errors.append(f"{rel}: missing anchor {target}")
            dest_rel = os.path.relpath(dest, ROOT)
            if own_skill and dest_rel.startswith("skills" + os.sep):
                other = dest_rel.split(os.sep)[1]
                if other != own_skill and f"{other}/" not in text:
                    errors.append(f"{rel}: link to {target} should name the skill ({other}/...) in its text")


def check_schemas():
    import urllib.request
    import jsonschema

    for path in ("plugin.json", ".antigravity-plugin/plugin.json"):
        doc = load(path)
        with urllib.request.urlopen(doc["$schema"]) as r:
            schema = json.load(r)
        try:
            jsonschema.validate(doc, schema)
        except jsonschema.ValidationError as e:
            errors.append(f"{path}: {e.message}")


check_manifests()
check_skills()
check_links()
if "--schemas" in sys.argv:
    check_schemas()

for e in errors:
    print(f"error: {e}")
print("ok" if not errors else f"{len(errors)} error(s)")
sys.exit(1 if errors else 0)
