#!/usr/bin/env python3
"""Import K-Dense scientific-agents profiles as native SKILL.md folders.

Upstream (K-Dense-AI/scientific-agents) ships ~500 expert-thinking AGENTS.md
profiles plus a catalog.json. The skills CLI and build-vault.py only discover
folders that contain a SKILL.md, so this script converts every profile into a
first-class skill under skills/<slug>/SKILL.md, keeps the original profile body
verbatim, and records source provenance in the frontmatter `metadata:` block.
It also writes a `scientific-agents` dispatcher skill that indexes the catalog.

Every generated SKILL.md carries `scientific-agents-profile: true`; build-vault.py
uses that flag to file these skills under the Scientific Expert Profiles domain
without listing 500 names in CATEGORIES.

The catalog records each profile path relative to the repo root, but checkouts
store them under scientific-agents/, so the importer tries the catalog path
first and the nested layout second.

These folders have no .skill-lock.json entry, so `npx skills update` leaves
them alone; re-run this script against a newer checkout to refresh them.

Usage:
  git clone https://github.com/K-Dense-AI/scientific-agents.git /tmp/sa
  git -C /tmp/sa checkout 896ed6ed1e1a6686572db06ca59fd1c1b0055ca7
  python3 .skill-vault/import-scientific-agents.py /tmp/sa [--prune]
  python3 .skill-vault/build-vault.py --prune

  --prune            delete previously imported profile folders whose slug is no
                     longer in the catalog (only folders this script generated)
  --allow-unpinned   import from a checkout at a commit other than PINNED_COMMIT
                     (then update PINNED_COMMIT so the pin stays truthful)
"""
from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
import textwrap
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]          # script lives in .skill-vault/
SKILLS_DIR = ROOT / "skills"                        # the skills CLI's flat store
SOURCE_REPO = "K-Dense-AI/scientific-agents"
SOURCE_URL = "https://github.com/K-Dense-AI/scientific-agents"
PINNED_COMMIT = "896ed6ed1e1a6686572db06ca59fd1c1b0055ca7"
DISPATCHER = "scientific-agents"
FLAG = "scientific-agents-profile: true"
SLUG_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")


def folded(text: str, *, width: int = 88, indent: str = "  ") -> str:
    lines = []
    for paragraph in text.splitlines() or [""]:
        if not paragraph.strip():
            lines.append(indent.rstrip())
            continue
        lines.extend(textwrap.wrap(paragraph, width=width, initial_indent=indent,
                                   subsequent_indent=indent))
    return "\n".join(lines)


def q(value) -> str:
    """YAML-safe scalar: JSON strings are valid YAML double-quoted scalars."""
    return json.dumps(str(value), ensure_ascii=False)


def source_commit(source: Path) -> str:
    try:
        return subprocess.check_output(
            ["git", "-C", str(source), "rev-parse", "HEAD"],
            text=True,
            stderr=subprocess.DEVNULL,
        ).strip()
    except (OSError, subprocess.CalledProcessError):
        return "unknown"


def compact_description(agent: dict) -> str:
    work_mode = " ".join(agent.get("work_mode", "").split())
    summary = " ".join(agent.get("summary", "").split())
    if len(summary) > 320:
        summary = summary[:320].rsplit(" ", 1)[0].rstrip(" .;,") + "..."
    desc = f"Expert-thinking profile for {agent['profession']}"
    if work_mode:
        if len(work_mode) > 140:
            work_mode = work_mode[:140].rsplit(" ", 1)[0].rstrip(" /,;") + "..."
        desc += f" ({work_mode})"
    if summary:
        desc += f": {summary}"
    return desc


def catalog_profile_path(agent: dict) -> Path:
    profile_path = Path(agent.get("path") or f"{agent['slug']}/AGENTS.md")
    if profile_path.is_absolute() or ".." in profile_path.parts:
        raise ValueError(f"Unsafe catalog path for {agent['slug']}: {profile_path}")
    return profile_path


def resolve_profile_path(source: Path, agent: dict) -> Path:
    catalog_path = catalog_profile_path(agent)
    candidates = [
        source / catalog_path,
        source / "scientific-agents" / catalog_path,
    ]
    for candidate in candidates:
        if candidate.is_file():
            return candidate
    tried = ", ".join(str(candidate) for candidate in candidates)
    raise FileNotFoundError(f"{catalog_path} for {agent['slug']} (tried: {tried})")


def render_skill(agent: dict, profile_body: str, commit: str) -> str:
    slug = agent["slug"]
    profession = agent["profession"]
    upstream_path = catalog_profile_path(agent).as_posix()
    desc = compact_description(agent)
    summary = " ".join(agent.get("summary", "").split())
    work_mode = " ".join(agent.get("work_mode", "").split())

    frontmatter = [
        "---",
        f"name: {slug}",
        "description: >",
        folded(desc),
        "metadata:",
        f"  short-description: {q(profession + ' expert profile')}",
        f"  source-repo: {SOURCE_REPO}",
        f"  source-url: {SOURCE_URL}",
        f"  source-commit: {commit}",
        f"  source-path: {q(upstream_path)}",
        f"  upstream-created: {q(agent.get('created', ''))}",
        f"  upstream-updated: {q(agent.get('updated', ''))}",
        f"  source-count: {q(agent.get('source_count', ''))}",
        f"  {FLAG}",
        "---",
        "",
    ]

    intro = [
        f"# {profession} Expert Profile",
        "",
        f"Imported from [{SOURCE_REPO}]({SOURCE_URL}) at commit `{commit}`.",
        "",
        "Use this skill when the task benefits from a senior domain practitioner's",
        "operating model: how they frame problems, select methods, stress-test",
        "claims, watch for artifacts, and report uncertainty.",
        "",
        "This profile should be combined with project instructions, local protocols,",
        "tool-specific skills, and current primary sources. For medical, clinical,",
        "regulatory, or safety-critical work, treat it as research support rather",
        "than individualized professional advice.",
        "",
        "## Catalog Metadata",
        "",
        f"- Profession: {profession}",
        f"- Work mode: {work_mode or 'unspecified'}",
        f"- Upstream path: `{upstream_path}`",
        f"- Upstream source count: {agent.get('source_count', 'unknown')}",
    ]
    if summary:
        intro.append(f"- Catalog summary: {summary}")
    intro += ["", "## Imported Profile", "", profile_body.rstrip(), ""]
    return "\n".join(frontmatter + intro)


def render_dispatcher(agents: list[dict], commit: str) -> str:
    examples = [
        "bioinformatician",
        "single-cell-biologist",
        "clinical-epidemiologist",
        "computational-chemist",
        "materials-scientist",
        "astrophysicist",
        "statistician",
        "machine-learning-researcher",
    ]
    examples = [slug for slug in examples if any(a["slug"] == slug for a in agents)]
    catalog_lines = [
        f"- `{a['slug']}` - {a['profession']}: {' '.join(a.get('summary', '').split())}"
        for a in agents[:60]
    ]
    if len(agents) > 60:
        catalog_lines.append(f"- ... {len(agents) - 60} more profiles in references/catalog.json")

    return "\n".join([
        "---",
        f"name: {DISPATCHER}",
        "description: >",
        folded(
            "Dispatcher for the K-Dense scientific-agents collection. Use when you need "
            "to choose among imported scientific and engineering expert profiles, such "
            "as bioinformatician, clinical epidemiologist, materials scientist, "
            "astrophysicist, or machine-learning researcher."
        ),
        "metadata:",
        f"  short-description: {q('K-Dense scientific-agents profile dispatcher')}",
        f"  source-repo: {SOURCE_REPO}",
        f"  source-url: {SOURCE_URL}",
        f"  source-commit: {commit}",
        "  source-path: catalog.json",
        f"  {FLAG}",
        "---",
        "",
        "# Scientific Agents Profile Dispatcher",
        "",
        f"This skill indexes {len(agents)} expert-thinking profiles imported from "
        f"[{SOURCE_REPO}]({SOURCE_URL}) at commit `{commit}`.",
        "",
        "Use it when the user asks for a scientific discipline perspective but no",
        "specific profile has been selected yet. Pick the closest imported profile,",
        "then read that profile's `SKILL.md` before acting.",
        "",
        "## Selection Rules",
        "",
        "- Prefer the narrowest relevant profile over a broad one.",
        "- Search `references/catalog.json` (profession, work_mode, summary) when the",
        "  preview below does not list a good fit; each profile lives at `../<slug>/SKILL.md`.",
        "- Combine profession profiles with tool skills already in this vault.",
        "- For clinical, regulatory, safety, legal, or financial topics, verify current",
        "  primary sources and keep advice scoped to research support.",
        "- If several profiles fit, say which ones you are combining and why.",
        "",
        "## Useful Starting Profiles",
        "",
        *(f"- [{slug}](../{slug}/SKILL.md)" for slug in examples),
        "",
        "## Catalog Preview",
        "",
        *catalog_lines,
        "",
        "The complete upstream catalog is stored at `references/catalog.json`.",
        "",
    ])


def rewrite_readme(text: str) -> str:
    """Point upstream README links at the imported skills.

    README.md lands in skills/scientific-agents/references/, where the upstream
    links `scientific-agents/<slug>/AGENTS.md` would be dead; the imported
    profile is skills/<slug>/SKILL.md, i.e. ../../<slug>/SKILL.md from there.
    """
    return re.sub(r"\]\((?:\./)?scientific-agents/([a-z0-9-]+)/(?:AGENTS|CLAUDE)\.md\)",
                  r"](../../\1/SKILL.md)", text)


def is_imported(skill_dir: Path) -> bool:
    md = skill_dir / "SKILL.md"
    if not md.is_file():
        return False
    head = md.read_text(encoding="utf-8", errors="replace").split("\n---", 1)[0]
    return FLAG in head


def load_agents(source: Path) -> list[dict]:
    catalog_path = source / "catalog.json"
    with catalog_path.open(encoding="utf-8") as f:
        data = json.load(f)
    agents = data["agents"]
    seen = set()
    for agent in agents:
        slug = agent["slug"]
        if not SLUG_RE.match(slug) or len(slug) > 64 or slug == DISPATCHER:
            raise ValueError(f"Unusable slug in catalog: {slug!r}")
        if slug in seen:
            raise ValueError(f"Duplicate slug in catalog: {slug}")
        seen.add(slug)
        resolve_profile_path(source, agent)
    return agents


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n", 1)[0])
    parser.add_argument("source", type=Path, help="Local checkout of K-Dense-AI/scientific-agents")
    parser.add_argument("--dest", type=Path, default=SKILLS_DIR,
                        help="Skills directory (default: skills/ next to .skill-vault/)")
    parser.add_argument("--prune", action="store_true",
                        help="Remove imported profiles that are no longer in the catalog")
    parser.add_argument("--allow-unpinned", action="store_true",
                        help=f"Allow a checkout that is not at {PINNED_COMMIT[:10]}")
    args = parser.parse_args()

    source = args.source.resolve()
    dest = args.dest.resolve()
    commit = source_commit(source)
    if commit != PINNED_COMMIT and not args.allow_unpinned:
        sys.exit(f"Checkout is at {commit}, not the pinned {PINNED_COMMIT}. "
                 f"Check out the pin, or pass --allow-unpinned and update PINNED_COMMIT.")
    agents = load_agents(source)

    # never overwrite a skill this script did not generate (e.g. one from `npx skills add`)
    targets = [a["slug"] for a in agents] + [DISPATCHER]
    clashes = [s for s in targets if (dest / s).exists() and not is_imported(dest / s)]
    if clashes:
        sys.exit(f"Refusing to overwrite existing non-imported skills: {', '.join(clashes)}")

    for agent in agents:
        slug = agent["slug"]
        profile_path = resolve_profile_path(source, agent)
        skill_dir = dest / slug
        skill_dir.mkdir(parents=True, exist_ok=True)
        skill_text = render_skill(agent, profile_path.read_text(encoding="utf-8"), commit)
        (skill_dir / "SKILL.md").write_text(skill_text, encoding="utf-8")

    dispatcher_dir = dest / DISPATCHER
    references_dir = dispatcher_dir / "references"
    references_dir.mkdir(parents=True, exist_ok=True)
    (dispatcher_dir / "SKILL.md").write_text(render_dispatcher(agents, commit), encoding="utf-8")
    shutil.copy2(source / "catalog.json", references_dir / "catalog.json")
    readme = (source / "README.md").read_text(encoding="utf-8")
    (references_dir / "README.md").write_text(rewrite_readme(readme), encoding="utf-8")
    shutil.copy2(source / "LICENSE.md", references_dir / "LICENSE.md")

    pruned = []
    if args.prune:
        keep = set(targets)
        for d in sorted(dest.iterdir()):
            if d.is_dir() and d.name not in keep and is_imported(d):
                shutil.rmtree(d)
                pruned.append(d.name)

    print(f"Imported {len(agents)} profiles plus dispatcher into {dest}")
    print(f"Source commit: {commit}")
    if pruned:
        print(f"Pruned {len(pruned)} profile(s) no longer in the catalog: {', '.join(pruned)}")


if __name__ == "__main__":
    main()
