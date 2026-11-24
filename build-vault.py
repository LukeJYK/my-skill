#!/usr/bin/env python3
"""Build the human-navigation layer for the skills vault.

Generates, for every skills/<skill>/ folder that contains a SKILL.md:
  - vault/notes/<domain>/<skill>.md  a wrapper note (safe to hand-edit; the
                          "Personal notes" section AND your frontmatter edits
                          to status / rating / aliases are preserved on re-run,
                          also when the skill moves to another domain)
  - vault/maps/<domain>.md  one map (MOC) note per domain, linking to wrappers
  - vault/index.md          master index linking to maps + every wrapper (A-Z)

All links are true relative paths, so they resolve in Obsidian (vault root =
repo root) and in any plain markdown renderer, GitHub's file view included.
The frontmatter `source:` stays vault-root relative (skills/<skill>/SKILL.md)
because vault/skills.base resolves it with link().

The original skills/<skill>/SKILL.md files are never touched, so the skills
CLI keeps managing them. Hand-authored files (vault/skills.base, README.md,
.obsidian/*) are also never touched. Re-run this script after adding/removing
skills.

Usage:  python3 build-vault.py [--prune] [--graph] [--force-aliases]
  --prune          delete generated notes not at the exact path this build writes
                   (removed skills, stale domain folders) and orphan map notes
  --graph          rewrite .obsidian/graph.json colors + filter (quit Obsidian first)
  --force-aliases  regenerate aliases on every wrapper (overwrites hand edits)
"""
import os
import re
import sys
from datetime import date

ROOT = os.path.dirname(os.path.abspath(__file__))
# skill folders live in ROOT/skills (the skills CLI's flat canonical store and
# must stay flat); everything this script writes lives under ROOT/vault.
SKILLS_DIR = os.path.join(ROOT, "skills")
VAULT_DIR = os.path.join(ROOT, "vault")
NOTES_DIR = os.path.join(VAULT_DIR, "notes")
MAPS_DIR = os.path.join(VAULT_DIR, "maps")


def note_path(skill, domain):
    return os.path.join(NOTES_DIR, domain, skill + ".md")


def find_existing_note(skill, domain):
    """The note at its expected path, else one stranded in another domain folder."""
    p = note_path(skill, domain)
    if os.path.isfile(p):
        return p
    if os.path.isdir(NOTES_DIR):
        for d in sorted(os.listdir(NOTES_DIR)):
            q = note_path(skill, d)
            if os.path.isfile(q):
                return q
    return None
TODAY = date.today().isoformat()
# one-time: regenerate aliases even if a wrapper already has an aliases key.
# Do NOT use after you have hand-curated aliases.
FORCE_ALIASES = "--force-aliases" in sys.argv
# delete generated wrapper notes whose skill folder no longer exists, and map
# notes whose domain is no longer in CATEGORIES (orphans).
PRUNE = "--prune" in sys.argv
# rewrite .obsidian/graph.json color groups + filter. QUIT Obsidian first, or it
# will overwrite the file from memory.
GRAPH = "--graph" in sys.argv

# graph color per domain (24-bit RGB ints = 0xRRGGBB), keyed by category key.
PALETTE = {
    "ml-ai": 0xBFEF45, "data-science-compute": 0xFABED4, "quantum-physics": 0x469990,
    "research-writing": 0xDCBEFF, "academic-pipelines": 0x9A6324,
    "literature-discovery": 0xFFFAC8, "documents-office": 0x800000,
    "cloud-devops": 0xAAFFC3, "software-engineering": 0xFF6B6B,
    "agent-workflow": 0x2EC4B6, "vault-meta": 0x808000, "reasoning-ideation": 0x000075,
}
# graph shows only generated notes (hides the ~870 untagged files inside skill folders)
GRAPH_SEARCH = "tag:#skill OR tag:#skill-map OR tag:#moc"
PERSONAL_MARKER = "%% ---8<--- personal notes below are preserved on re-run ---8<--- %%"

# acronyms too generic to be useful aliases (auto-extracted from descriptions)
STOP = {"API", "CLI", "ML", "AI", "QC", "DNA", "RNA", "GPU", "CPU", "PDF", "CSV",
        "JSON", "HTML", "REST", "SDK", "LLM", "GO", "3D", "2D", "ID", "OS", "UI",
        "NGS", "PCA", "URL", "HTTP", "IO", "OK", "FAIR", "METHODOLOGY"}

# Curated search terms that Obsidian's fuzzy quick-switcher would NOT match from
# the skill id itself. Extend freely; on rebuild these only apply to wrappers
# that don't yet have an `aliases:` key (or with --force-aliases).
SYNONYMS = {
    # software engineering
    "test-driven-development": ["TDD"], "spec-driven-development": ["SDD"],
    "ci-cd-and-automation": ["CI/CD", "GitHub Actions"], "documentation-and-adrs": ["ADR"],
    "git-workflow-and-versioning": ["branching", "semver"],
    "observability-and-instrumentation": ["logging", "tracing", "metrics"],
    "security-and-hardening": ["OWASP"], "performance-optimization": ["profiling"],
    # cloud / ML
    "aws-cdk-development": ["CDK"], "aws-serverless-eda": ["Lambda", "EventBridge"],
    "aws-agentic-ai": ["Bedrock", "AgentCore"], "hf-cli": ["huggingface"],
    "transformers": ["huggingface"], "optimize-for-gpu": ["CUDA"],
    "scikit-learn": ["sklearn"], "pytorch-lightning": ["PyTorch"],
    "stable-baselines3": ["SB3", "RL"], "umap-learn": ["UMAP"],
    # stats / science
    "statistical-power": ["sample size"], "uncertainty-and-units": ["pint"],
    "pybamm": ["battery"], "geopandas": ["GIS"],
    # writing / research
    "rebuttal-guidance": ["rebuttal", "response to reviewers"],
    "literature-review": ["systematic review"], "pyzotero": ["Zotero"],
    "consciousness-council": ["panel", "council"],
    # office
    "docx": ["Word"], "pptx": ["PowerPoint"], "xlsx": ["Excel"],
}

# ---------------------------------------------------------------------------
# Domain definition: ordered. key -> (title, scope, related_keys, [skills])
# ---------------------------------------------------------------------------
CATEGORIES = [
    ("ml-ai", "Machine Learning & AI",
     "General ML/DL frameworks, model interpretability, RL, graph learning, and scientific model hubs.",
     ["data-science-compute", "cloud-devops", "agent-workflow"],
     ["scikit-learn", "pytorch-lightning", "transformers", "shap", "stable-baselines3", "pufferlib",
      "torch-geometric", "umap-learn", "aeon", "timesfm-forecasting", "hugging-science"]),

    ("data-science-compute", "Data Science, Stats & Scientific Computing",
     "DataFrames, big-data tooling, statistics, optimization, simulation, geospatial, and plotting.",
     ["ml-ai", "quantum-physics", "research-writing"],
     ["polars", "dask", "vaex", "zarr-python", "networkx", "sympy", "matlab", "statsmodels",
      "statistical-analysis", "scikit-survival", "pymc", "pymoo", "simpy", "geomaster", "geopandas",
      "exploratory-data-analysis", "optimize-for-gpu", "usfiscaldata", "matplotlib", "seaborn",
      "statistical-power", "uncertainty-and-units"]),

    ("quantum-physics", "Quantum, Physics & Materials",
     "Quantum computing frameworks, open quantum systems, astronomy, fluid dynamics, materials science, and battery modeling.",
     ["data-science-compute", "ml-ai"],
     ["qiskit", "cirq", "pennylane", "qutip", "astropy", "fluidsim", "pymatgen", "pybamm"]),

    ("research-writing", "Scientific Writing, Figures & Publishing",
     "Manuscript writing, figures and schematics, posters/slides, reference management, and pre-submission review.",
     ["academic-pipelines", "literature-discovery", "documents-office", "reasoning-ideation"],
     ["scientific-writing", "scientific-visualization", "scientific-slides", "scientific-schematics",
      "scientific-critical-thinking", "citation-management", "peer-review", "research-grants",
      "venue-templates", "latex-posters", "pptx-posters", "paper-2-web", "markdown-mermaid-writing",
      "figure-designer", "scholar-evaluation", "tech-paper-template", "benchmark-paper-template",
      "intro-drafter", "pre-submission-reviewer", "pyzotero", "rebuttal-guidance"]),

    ("academic-pipelines", "Academic Paper & Nature Pipelines",
     "End-to-end multi-agent paper pipelines and the Nature-family writing/review/translation suite.",
     ["research-writing", "literature-discovery", "reasoning-ideation"],
     ["academic-paper", "academic-paper-reviewer", "academic-pipeline", "deep-research",
      "nature-academic-search", "nature-citation", "nature-data", "nature-figure", "nature-paper2ppt",
      "nature-polishing", "nature-reader", "nature-response", "nature-reviewer", "nature-writing"]),

    ("literature-discovery", "Literature Search & Knowledge Discovery",
     "Paper search across databases, web research, content extraction, and knowledge bases.",
     ["research-writing", "academic-pipelines", "documents-office"],
     ["paper-lookup", "pubmed-summariser", "lit-synthesizer", "research-lookup", "exa-search",
      "parallel-web", "bgpt-mcp", "bgpt-paper-search", "paperzilla", "open-notebook", "defuddle",
      "literature-review", "data-extractor", "claw-semantic-sim"]),

    ("documents-office", "Documents, Office & Media",
     "Office document toolkits (docx/pptx/pdf/xlsx), file-to-markdown conversion, and image/report generation.",
     ["research-writing", "literature-discovery"],
     ["docx", "pptx", "pdf", "xlsx", "markitdown", "liteparse", "infographics", "generate-image",
      "market-research-reports"]),

    ("cloud-devops", "Cloud, Infra & MLOps",
     "AWS architecture and operations, serverless GPU compute, the Hugging Face CLI, and Nextflow pipelines.",
     ["ml-ai", "software-engineering", "vault-meta"],
     ["aws-agentic-ai", "aws-cdk-development", "aws-cost-operations", "aws-mcp-setup",
      "aws-serverless-eda", "modal", "hf-cli", "nextflow"]),

    ("software-engineering", "Software Engineering Practices",
     "Spec-, test- and source-driven development, planning, code review, debugging, security, performance, CI/CD, and shipping.",
     ["cloud-devops", "agent-workflow", "vault-meta"],
     ["spec-driven-development", "test-driven-development", "source-driven-development",
      "constraint-driven-development", "doubt-driven-development", "planning-and-task-breakdown",
      "incremental-implementation", "api-and-interface-design", "frontend-ui-engineering",
      "browser-testing-with-devtools", "code-review-and-quality", "code-simplification",
      "debugging-and-error-recovery", "security-and-hardening", "performance-optimization",
      "observability-and-instrumentation", "ci-cd-and-automation", "git-workflow-and-versioning",
      "documentation-and-adrs", "deprecation-and-migration", "shipping-and-launch"]),

    ("agent-workflow", "Agents & Context Engineering",
     "Agent harnesses, context setup, skill discovery, and eliciting what the user actually wants.",
     ["software-engineering", "vault-meta", "reasoning-ideation"],
     ["context-engineering", "using-agent-skills", "pi-agent", "interview-me"]),

    ("vault-meta", "Vault, Skills & Workflow Meta",
     "Obsidian authoring, skill building/discovery, reproducibility, orchestration, and resource detection.",
     ["cloud-devops", "reasoning-ideation"],
     ["obsidian-markdown", "obsidian-bases", "obsidian-cli", "json-canvas", "skill-builder",
      "find-skills", "autoskill", "clawpathy-autoresearch", "repro-enforcer", "bio-orchestrator",
      "get-available-resources"]),

    ("reasoning-ideation", "Reasoning, Ideation & Decision",
     "Multi-perspective deliberation, brainstorming, hypothesis generation, idea evaluation, and scenario analysis.",
     ["research-writing", "academic-pipelines", "vault-meta"],
     ["consciousness-council", "what-if-oracle", "dhdna-profiler", "scientific-brainstorming",
      "hypothesis-generation", "idea-evaluator", "vibe-research-workflow", "hypogenic", "idea-refine"]),
]


# ---------------------------------------------------------------------------
def read_description(skill):
    path = os.path.join(SKILLS_DIR, skill, "SKILL.md")
    if not os.path.isfile(path):
        return None
    with open(path, "r", encoding="utf-8") as f:
        text = f.read()
    m = re.match(r"^---\s*\n(.*?)\n---\s*\n", text, re.DOTALL)
    if not m:
        return None
    fm = m.group(1)
    desc_lines, capturing = [], False
    for line in fm.splitlines():
        if not capturing:
            km = re.match(r"^description:\s*(.*)$", line)
            if km:
                capturing = True
                rest = km.group(1).strip()
                if rest and rest not in (">", "|", ">-", "|-"):
                    desc_lines.append(rest)
        else:
            if re.match(r"^[A-Za-z0-9_-]+:(\s|$)", line) or line.strip() == "---":
                break
            desc_lines.append(line.strip())
    desc = " ".join(p for p in desc_lines if p).strip().strip("'\"").strip()
    desc = " ".join(desc.split())
    return desc or None


def one_liner(desc, limit=185):
    if not desc:
        return "(no description)"
    parts = re.split(r"(?<=[.;])\s+", desc)
    out = ""
    for p in parts:
        out = (out + " " + p).strip() if out else p
        if len(out) >= 40:
            break
    out = " ".join(out.split()).rstrip(" .;,")
    if len(out) > limit:
        out = out[:limit].rsplit(" ", 1)[0].rstrip(" .;,") + "..."
    return out


def gen_aliases(skill, desc):
    """Curated synonyms + tool acronyms in parentheses in the FIRST sentence."""
    al = list(SYNONYMS.get(skill, []))
    first = re.split(r"(?<=[.;])\s+", desc or "", maxsplit=1)[0]
    for m in re.finditer(r"\(([^)]{1,40})\)", first):
        for tok in re.split(r"[,/]| or | and ", m.group(1)):
            tok = tok.strip()
            if (re.fullmatch(r"[A-Za-z][A-Za-z0-9.+-]{1,14}", tok)
                    and any(c.isupper() for c in tok)
                    and tok.upper() not in STOP
                    and tok.lower() != skill.lower()):
                al.append(tok)
    seen, out = set(), []
    for a in al:
        if a.lower() not in seen:
            seen.add(a.lower())
            out.append(a)
    return out[:5]


def discover_skills():
    found = set()
    for name in os.listdir(SKILLS_DIR):
        if name.startswith("."):
            continue
        p = os.path.join(SKILLS_DIR, name)
        if os.path.isdir(p) and os.path.isfile(os.path.join(p, "SKILL.md")):
            found.add(name)
    return found


def build_related(skills, full_desc):
    """Undirected related-graph mined from cross-references in descriptions."""
    patterns = {s: re.compile(r"(?<![\w-])" + re.escape(s) + r"(?![\w-])", re.IGNORECASE)
                for s in skills}
    edges = {s: set() for s in skills}
    for s in skills:
        d = full_desc.get(s) or ""
        if not d:
            continue
        for t in skills:
            if t == s:
                continue
            if patterns[t].search(d):
                edges[s].add(t)
                edges[t].add(s)  # symmetrize
    return edges


def parse_existing(skill, domain):
    """Read user-editable bits from an existing wrapper so re-runs preserve them.
    Also finds the note in an old domain folder after a recategorisation."""
    path = find_existing_note(skill, domain)
    if path is None:
        return None
    txt = open(path, encoding="utf-8").read()
    m = re.match(r"^---\s*\n(.*?)\n---\s*\n", txt, re.DOTALL)
    fm = m.group(1) if m else ""
    data = {}
    for key in ("created", "status", "rating"):
        km = re.search(rf"^{key}:\s*(.+)$", fm, re.MULTILINE)
        if km:
            data[key] = km.group(1).strip()
    # None => no aliases key at all (auto-generate); [] => user set it empty (respect)
    aliases = None
    block = re.search(r"^aliases:\s*\n((?:[ \t]*-[ \t].*\n?)+)", fm, re.MULTILINE)
    inline = re.search(r"^aliases:\s*\[(.*)\]\s*$", fm, re.MULTILINE)
    empty = re.search(r"^aliases:\s*(\[\s*\]|)\s*$", fm, re.MULTILINE)
    if block:
        aliases = []
        for line in block.group(1).splitlines():
            lm = re.match(r"[ \t]*-[ \t]+(.*)$", line)
            if lm:
                aliases.append(lm.group(1).strip().strip("'\""))
    elif inline:
        aliases = [a.strip().strip("'\"") for a in inline.group(1).split(",") if a.strip()]
    elif empty:
        aliases = []
    data["aliases"] = aliases
    idx = txt.find(PERSONAL_MARKER)
    data["personal"] = txt[idx:] if idx != -1 else None
    return data


def emit_alias_block(aliases):
    if not aliases:
        return []
    out = ["aliases:"]
    for a in aliases:
        out.append(f'  - "{a}"' if re.search(r'[:#\[\],&*?{}|<>=!%@`"/]', a) else f"  - {a}")
    return out


def update_graph():
    """Rewrite graph.json color groups + filter, preserving all other settings."""
    import json
    path = os.path.join(ROOT, ".obsidian", "graph.json")
    cfg = {}
    if os.path.isfile(path):
        try:
            cfg = json.load(open(path, encoding="utf-8"))
        except (OSError, ValueError):
            cfg = {}
    missing = [k for k, *_ in CATEGORIES if k not in PALETTE]
    if missing:
        print(f"WARNING: no graph color in PALETTE for: {missing}", file=sys.stderr)
    cfg["search"] = GRAPH_SEARCH
    cfg["showOrphans"] = False
    cfg["colorGroups"] = [
        {"query": f"tag:#domain/{key}", "color": {"a": 1, "rgb": PALETTE[key]}}
        for key, *_ in CATEGORIES if key in PALETTE
    ]
    with open(path, "w", encoding="utf-8") as f:
        json.dump(cfg, f, indent=2)
        f.write("\n")
    print(f"graph.json: wrote {len(cfg['colorGroups'])} color groups + filter "
          f"(if Obsidian was running, quit it and re-run with --graph)")


def prune(expected):
    """Delete generated notes that are not at the exact path this build wrote
    (removed skills, notes stranded in an old domain folder), then remove the
    emptied domain folders. Returns the list of removed paths."""
    removed = []
    expected = {os.path.normpath(p) for p in expected}
    for dirpath, _, files in os.walk(NOTES_DIR):
        for f in files:
            p = os.path.normpath(os.path.join(dirpath, f))
            if not f.endswith(".md") or p in expected:
                continue
            try:
                txt = open(p, encoding="utf-8").read()
            except OSError:
                continue
            # only delete files that are clearly generated wrappers
            if re.search(r"^source:\s*.+/SKILL\.md\s*$", txt, re.MULTILINE) or PERSONAL_MARKER in txt:
                os.remove(p)
                removed.append(os.path.relpath(p, VAULT_DIR))
    for d in sorted(os.listdir(NOTES_DIR)):
        dp = os.path.join(NOTES_DIR, d)
        if os.path.isdir(dp) and not os.listdir(dp):
            os.rmdir(dp)
    live_maps = {f"{k}.md" for k, *_ in CATEGORIES}
    for f in os.listdir(MAPS_DIR):
        if not f.endswith(".md") or f in live_maps:
            continue
        p = os.path.join(MAPS_DIR, f)
        try:
            txt = open(p, encoding="utf-8").read()
        except OSError:
            continue
        if re.search(r"^\s*-\s*skill-map\s*$", txt, re.MULTILINE):  # generated map
            os.remove(p)
            removed.append(f"maps/{f}")
    if removed:
        print(f"PRUNED {len(removed)} orphan note(s): {', '.join(sorted(removed))}",
              file=sys.stderr)
    return removed


def main():
    os.makedirs(MAPS_DIR, exist_ok=True)
    os.makedirs(NOTES_DIR, exist_ok=True)
    if GRAPH:
        update_graph()
    title_by_key = {k: t for k, t, _, _, _ in CATEGORIES}
    key_by_skill, assigned = {}, {}
    for key, title, scope, related, skills in CATEGORIES:
        for s in skills:
            if s in assigned:
                print(f"WARNING: {s} in both {assigned[s]} and {key}", file=sys.stderr)
            assigned[s] = key
            key_by_skill[s] = key

    on_disk = discover_skills()
    unsorted = sorted(on_disk - set(assigned))
    if unsorted:
        print(f"WARNING: not categorized: {unsorted}", file=sys.stderr)
    for s in unsorted:
        key_by_skill[s] = "uncategorized"

    skills_sorted = sorted(on_disk)
    full_desc = {s: read_description(s) for s in skills_sorted}
    short = {s: one_liner(full_desc[s]) for s in skills_sorted}
    related = build_related(skills_sorted, full_desc)

    def note_link(s, from_dir):
        """Relative link to skill s's wrapper note from a file in from_dir."""
        target = note_path(s, key_by_skill.get(s, "uncategorized"))
        return os.path.relpath(target, from_dir).replace(os.sep, "/")

    written = []

    # ---- wrapper notes -----------------------------------------------------
    for s in skills_sorted:
        key = key_by_skill.get(s, "uncategorized")
        dtitle = title_by_key.get(key, "Uncategorized")
        out_path = note_path(s, key)
        here = os.path.dirname(out_path)
        up = os.path.relpath(VAULT_DIR, here).replace(os.sep, "/")       # ../..
        to_skill = os.path.relpath(os.path.join(SKILLS_DIR, s, "SKILL.md"), here).replace(os.sep, "/")
        old_path = find_existing_note(s, key)
        ex = parse_existing(s, key) or {}
        created = ex.get("created", TODAY)
        status = ex.get("status", "untried")
        rating = ex.get("rating")
        aliases = ex.get("aliases")
        if aliases is None or FORCE_ALIASES:  # key absent => first-time auto-generate
            aliases = gen_aliases(s, full_desc[s])
        notes_block = ex.get("personal")
        L = []
        L.append("---")
        L.append(f"title: {s}")
        L += emit_alias_block(aliases)
        L.append("tags:")
        L.append("  - skill")
        if key != "uncategorized":
            L.append(f"  - domain/{key}")
        L.append(f"domain: {key}")
        L.append(f"status: {status}")
        if rating is not None:
            L.append(f"rating: {rating}")
        L.append(f"source: skills/{s}/SKILL.md")
        L.append(f"created: {created}")
        L.append("---")
        L.append("")
        L.append(f"# {s}")
        L.append("")
        L.append("> [!info] What it does")
        L.append(f"> {full_desc[s] or '(no description)'}")
        L.append("")
        nav = [f"**Source:** [{s}/SKILL.md]({to_skill})"]
        if key != "uncategorized":
            nav.append(f"**Domain:** [{dtitle}]({up}/maps/{key}.md)")
        nav.append(f"**Table:** [skills.base]({up}/skills.base)")
        nav.append(f"**Index:** [Skills Index]({up}/index.md)")
        L.append("  ·  ".join(nav))
        L.append("")
        rel = sorted(related.get(s, []))
        L.append("## Related skills")
        L.append("")
        if rel:
            for r in rel:
                L.append(f"- [{r}]({note_link(r, here)}) — {short[r]}")
        else:
            L.append("_None auto-detected. Add your own links here, e.g. `[other-skill](../<domain>/other-skill.md)`._")
        L.append("")
        # same bytes for a fresh note and a rebuilt one, so reruns are a fixed point
        L.append((notes_block or f"{PERSONAL_MARKER}\n\n## Notes\n").rstrip() + "\n")
        os.makedirs(here, exist_ok=True)
        with open(out_path, "w", encoding="utf-8") as f:
            f.write("\n".join(L))
        written.append(out_path)
        if old_path and os.path.normpath(old_path) != os.path.normpath(out_path):
            os.remove(old_path)  # recategorised: the note moved to its new domain folder
            print(f"moved note: {os.path.relpath(old_path, VAULT_DIR)} -> "
                  f"{os.path.relpath(out_path, VAULT_DIR)}", file=sys.stderr)

    # ---- map notes ---------------------------------------------------------
    for key, title, scope, related_keys, skills in CATEGORIES:
        live = sorted(s for s in skills if s in on_disk)
        L = ["---", f"title: {title}", "tags:", "  - skill-map", f"created: {TODAY}", "---", "",
             f"# {title}", "", "> [!abstract] Scope", f"> {scope}", "",
             "[Back to Skill Index](../index.md)", ""]
        rel = [f"[{title_by_key[r]}]({r}.md)" for r in related_keys if r in title_by_key]
        if rel:
            L.append("**Related maps:** " + " | ".join(rel))
            L.append("")
        L.append(f"## Skills ({len(live)})")
        L.append("")
        for s in live:
            L.append(f"- [{s}]({note_link(s, MAPS_DIR)}) — {short[s]}")
        L.append("")
        with open(os.path.join(MAPS_DIR, f"{key}.md"), "w", encoding="utf-8") as f:
            f.write("\n".join(L))

    # ---- index -------------------------------------------------------------
    total = len(on_disk)
    I = ["---", "title: Skills Index", "tags:", "  - moc", "  - skill-index",
         f"created: {TODAY}", "---", "", "# Skills Index", "",
         f"A navigable map of the **{total} agent skills** in this vault, grouped into "
         f"{len(CATEGORIES)} domains. Each entry links to a per-skill note that wraps the "
         f"original `SKILL.md` and holds your personal notes.", "",
         "> [!tip] How to navigate",
         "> - **Find by name/synonym:** quick switcher (Cmd+O); skills carry aliases like `TDD`, `CDK`, `sklearn`.",
         "> - **Browse a domain:** open a map below for grouped, cross-linked skills.",
         "> - **Filter by attribute:** open [skills.base](skills.base) to sort/filter by domain, status, rating.",
         "> - **Jump to any skill:** the **A–Z list** at the bottom.",
         "> - **See connections:** Obsidian Graph view is color-grouped by domain.", "",
         "## Quick access", "",
         "- [Filterable table — skills.base](skills.base)  ·  sort & filter all skills by domain / status / rating",
         "", "## Browse by domain", ""]
    for key, title, scope, related_keys, skills in CATEGORIES:
        live = sorted(s for s in skills if s in on_disk)
        I.append(f"### [{title}](maps/{key}.md)  ·  {len(live)} skills")
        I.append("")
        I.append(scope)
        I.append("")
        preview = live[:6]
        chips = ", ".join(f"[{s}]({note_link(s, VAULT_DIR)})" for s in preview)
        more = f" … [see all {len(live)} →](maps/{key}.md)" if len(live) > len(preview) else ""
        I.append(chips + more)
        I.append("")
    I.append("## All skills (A–Z)")
    I.append("")
    cur, bucket = None, []
    def flush():
        if bucket:
            I.append(" · ".join(bucket)); I.append("")
    for s in sorted(on_disk, key=str.lower):
        letter = s[0].upper()
        if letter != cur:
            flush(); bucket = []; cur = letter; I.append(f"**{letter}**")
        bucket.append(f"[{s}]({note_link(s, VAULT_DIR)})")
    flush()
    if unsorted:
        I.append("## Uncategorized"); I.append("")
        for s in unsorted:
            I.append(f"- [{s}]({note_link(s, VAULT_DIR)}) — {short[s]}")
        I.append("")
    with open(os.path.join(VAULT_DIR, "index.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(I))

    pruned = prune(written) if PRUNE else []

    edge_count = sum(len(v) for v in related.values()) // 2
    print(f"OK: {total} wrappers, {len(CATEGORIES)} maps, {edge_count} related-links, "
          f"unsorted={len(unsorted)}, pruned={len(pruned)}")


if __name__ == "__main__":
    main()