#!/usr/bin/env python3
"""check-skills.py — health check for every skill folder in this repo.

Usage: python3 check-skills.py [--strict] [--quiet] [--stale-days N]
  --strict      also exit non-zero on warnings
  --quiet       only print skills that have problems
  --stale-days  warn when metadata.last-reviewed is older than N days (default 180)

Errors (exit 1):
  - SKILL.md missing frontmatter, or `name` / `description` missing
  - `name` not equal to the folder name, or not lowercase-hyphen, or > 64 chars
  - `description` longer than 1024 chars
  - relative link in SKILL.md pointing at a file inside the skill that does not exist
  - bundled .py script with a syntax error, bundled .sh script failing `bash -n`
  - skill folder missing from .skill-lock.json, or lock entry with no folder
Warnings:
  - SKILL.md longer than 500 lines
  - ../ link to a file outside the skill (upstream shared file) that is missing
  - no vault note <name>.md, or the note's `source:` does not point at the skill
  - metadata.last-reviewed older than --stale-days

Standard library only, so it runs anywhere Python 3.8+ does.
"""
import argparse
import datetime as dt
import json
import re
import shutil
import subprocess
import sys
import warnings
from pathlib import Path

warnings.simplefilter("ignore", SyntaxWarning)  # bad escapes etc. in bundled scripts

REPO = Path(__file__).resolve().parent
NAME_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
LINK_RE = re.compile(r"(?<!!)\[[^\]]*\]\(([^)\s]+)(?:\s+\"[^\"]*\")?\)")
FENCE_RE = re.compile(r"^(```|~~~)")


def parse_frontmatter(text):
    """Return (dict, body_start_line) or (None, 0). Handles the subset of YAML
    used by SKILL.md: top-level scalars (plain, quoted, | and > blocks) plus one
    level of nested mapping (e.g. metadata:)."""
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return None, 0
    try:
        end = next(i for i in range(1, len(lines)) if lines[i].strip() == "---")
    except StopIteration:
        return None, 0
    try:
        import yaml  # use the real parser when it is installed
        data = yaml.safe_load("\n".join(lines[1:end])) or {}
        return (data if isinstance(data, dict) else None), end + 1
    except ImportError:
        pass

    data, i, block = {}, 1, lines[1:end]
    i = 0
    while i < len(block):
        line = block[i]
        m = re.match(r"^([A-Za-z0-9_-]+):\s*(.*)$", line)
        if not m:
            i += 1
            continue
        key, val = m.group(1), m.group(2).strip()
        i += 1
        if val in ("|", ">", "|-", ">-", "|+", ">+", ""):
            sub = []
            while i < len(block) and (block[i].startswith((" ", "\t")) or not block[i].strip()):
                sub.append(block[i])
                i += 1
            if val == "" and any(re.match(r"^\s+[A-Za-z0-9_-]+:", s) for s in sub):
                nested = {}
                for s in sub:
                    nm = re.match(r"^\s+([A-Za-z0-9_-]+):\s*(.*)$", s)
                    if nm:
                        nested[nm.group(1)] = _unquote(nm.group(2).strip())
                data[key] = nested
            else:
                parts = [s.strip() for s in sub]
                data[key] = ("\n" if val.startswith("|") else " ").join(p for p in parts if p).strip()
        else:
            # plain multi-line scalars: continuation lines are indented
            while i < len(block) and block[i].startswith((" ", "\t")) and block[i].strip():
                val += " " + block[i].strip()
                i += 1
            data[key] = _unquote(val)
    return data, end + 1


def _unquote(v):
    if len(v) >= 2 and v[0] == v[-1] and v[0] in "\"'":
        return v[1:-1]
    return v


def links_outside_code(text):
    in_fence = False
    for line in text.splitlines():
        if FENCE_RE.match(line.strip()):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        line = re.sub(r"`[^`]*`", "", line)
        yield from LINK_RE.findall(line)


def check_skill(d, lock_names, stale_days):
    errors, warns = [], []
    skill_md = d / "SKILL.md"
    text = skill_md.read_text(encoding="utf-8", errors="replace")
    fm, _ = parse_frontmatter(text)

    if fm is None:
        errors.append("SKILL.md has no valid --- frontmatter block")
        fm = {}
    name = str(fm.get("name") or "").strip()
    desc = str(fm.get("description") or "").strip()
    if not name:
        errors.append("frontmatter `name` missing")
    elif name != d.name:
        errors.append(f"`name: {name}` does not match folder `{d.name}`")
    elif not NAME_RE.match(name) or len(name) > 64:
        errors.append(f"`name: {name}` must be lowercase-hyphen and <= 64 chars")
    if not desc:
        errors.append("frontmatter `description` missing or empty")
    elif len(desc) > 1024:
        errors.append(f"`description` is {len(desc)} chars (max 1024)")

    n_lines = text.count("\n") + 1
    if n_lines > 500:
        warns.append(f"SKILL.md is {n_lines} lines (recommended <= 500)")

    for target in links_outside_code(text):
        if re.match(r"^[a-z][a-z0-9+.-]*:", target) or target.startswith(("#", "/")):
            continue  # URL, mailto:, anchor, absolute path
        path = target.split("#", 1)[0].split("?", 1)[0]
        if not path or ("/" not in path and "." not in path):
            continue  # placeholder like (url)
        if (d / path).exists():
            continue
        if path.startswith("../"):
            # e.g. ../shared/x.md: lives in the upstream repo, not installed by `npx skills`
            warns.append(f"link outside the skill folder is missing (upstream file not installed): {target}")
        else:
            errors.append(f"broken link in SKILL.md: {target}")

    for py in sorted(d.rglob("*.py")):
        try:
            compile(py.read_bytes(), str(py), "exec")
        except SyntaxError as e:
            errors.append(f"syntax error: {py.relative_to(d)}:{e.lineno}: {e.msg}")
        except ValueError as e:
            errors.append(f"cannot compile {py.relative_to(d)}: {e}")
    if shutil.which("bash"):
        for sh in sorted(d.rglob("*.sh")):
            r = subprocess.run(["bash", "-n", str(sh)], capture_output=True, text=True)
            if r.returncode:
                msg = (r.stderr.strip().splitlines() or ["bash -n failed"])[0]
                errors.append(f"shell syntax: {sh.relative_to(d)}: {msg}")

    if lock_names is not None and d.name not in lock_names:
        errors.append("not listed in .skill-lock.json")

    note = REPO / f"{d.name}.md"
    if not note.exists():
        warns.append(f"no vault note {d.name}.md")
    else:
        nfm, _ = parse_frontmatter(note.read_text(encoding="utf-8", errors="replace"))
        src = str((nfm or {}).get("source") or "")
        if src and src != f"{d.name}/SKILL.md":
            warns.append(f"vault note source is `{src}`, expected `{d.name}/SKILL.md`")

    meta = fm.get("metadata") if isinstance(fm.get("metadata"), dict) else {}
    reviewed = meta.get("last-reviewed") or fm.get("last-reviewed")
    if reviewed:
        try:
            day = reviewed if isinstance(reviewed, dt.date) else dt.date.fromisoformat(str(reviewed)[:10])
            age = (dt.date.today() - day).days
            if age > stale_days:
                warns.append(f"last-reviewed {day} is {age} days old")
        except ValueError:
            warns.append(f"unparseable last-reviewed: {reviewed}")

    return errors, warns


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--strict", action="store_true")
    ap.add_argument("--quiet", action="store_true")
    ap.add_argument("--stale-days", type=int, default=180)
    args = ap.parse_args()

    skills = sorted(p.parent for p in REPO.glob("*/SKILL.md"))
    lock_path = REPO / ".skill-lock.json"
    lock_names = None
    global_errors = []
    if lock_path.exists():
        try:
            lock_names = set(json.loads(lock_path.read_text())["skills"])
        except (ValueError, KeyError) as e:
            global_errors.append(f".skill-lock.json unreadable: {e}")
        else:
            folder_names = {d.name for d in skills}
            for missing in sorted(lock_names - folder_names):
                global_errors.append(f".skill-lock.json lists `{missing}` but the folder is missing")

    n_err = n_warn = n_bad = 0
    for d in skills:
        errors, warns = check_skill(d, lock_names, args.stale_days)
        n_err += len(errors)
        n_warn += len(warns)
        if errors or warns:
            n_bad += 1
        if errors or warns or not args.quiet:
            mark = "FAIL" if errors else ("WARN" if warns else " ok ")
            print(f"[{mark}] {d.name}")
            for e in errors:
                print(f"         error: {e}")
            for w in warns:
                print(f"         warn:  {w}")

    for e in global_errors:
        print(f"[FAIL] repo: {e}")
    n_err += len(global_errors)

    print(f"\n{len(skills)} skills checked: {n_err} errors, {n_warn} warnings "
          f"({len(skills) - n_bad} clean)")
    if n_err or (args.strict and n_warn):
        sys.exit(1)


if __name__ == "__main__":
    main()
