# my-skill

A personal collection of AI agent skills (each folder contains a `SKILL.md` plus its supporting agents, references, templates, or scripts).

This repo is a **backup mirror** of `~/.agents/skills`. Skills are installed and updated from their upstream repos with the [Vercel `skills` CLI](https://github.com/vercel-labs/skills), then copied here by [`sync-skills.sh`](sync-skills.sh).

```
upstream repos ──npx skills add / update──▶ ~/.agents/skills/            (source of truth)
                                            ~/.agents/.skill-lock.json   (records upstream sources)
                                                   │
                                                   │ ./sync-skills.sh  (one-way copy + commit)
                                                   ▼
                                            this repo: <skill>/  .skill-lock.json
```

## Skills

| Skill | Upstream |
|---|---|
| [deep-research](deep-research/) | [Imbad0202/academic-research-skills](https://github.com/Imbad0202/academic-research-skills) |

The full, authoritative list with sources and content hashes is [`.skill-lock.json`](.skill-lock.json).

## Install a skill

```bash
npx skills add <owner/repo> -s <skill> -g -a universal -y
./sync-skills.sh
```

- `-g` installs globally into `~/.agents/skills/`.
- `-a universal` writes only to `~/.agents/skills` and never touches `~/.claude/skills`. Always pass it; otherwise the CLI reuses the last selected agents.
- Install from the upstream `owner/repo`, so the lock records it and `update` can pull from it. Local paths (`add .`) and private repos are skipped by `update`.

## Update from upstream

```bash
./sync-skills.sh -u -p    # npx skills update -g, then sync, commit, push
```

## sync-skills.sh

```bash
./sync-skills.sh          # copy ~/.agents/skills into the repo root and commit
./sync-skills.sh -c       # copy only: no git add / commit / push
./sync-skills.sh -u       # run `npx skills update -g` first
./sync-skills.sh -p       # git push after committing
./sync-skills.sh -n       # dry run: show what would change
./sync-skills.sh -f       # overwrite uncommitted edits in the repo's skill folders
```

What the script does:

- Mirrors every folder in `~/.agents/skills` that has a `SKILL.md`, and removes a skill folder here once it has been uninstalled there.
- Copies `.skill-lock.json`.
- Commits only the paths it touched.
- Leaves `.git`, `README.md`, `.obsidian/`, `.vault/` and any folder without a `SKILL.md` alone.
- Refuses to run if `~/.agents/skills` is a symlink, or if a skill folder here has uncommitted edits (unless you pass `-f`).

## Rules

1. **Edit skills in `~/.agents/skills`, not here.** The next sync overwrites this copy. Your own skills also go in `~/.agents/skills/<name>/`. They have no lock entry, so `update` leaves them alone.
2. **Keep `~/.agents/skills` a flat, real directory.** Don't symlink it (or `~/.agents`) to this repo, and never run `npx skills add . -g` from here. The CLI compares paths as strings, so through a link it can `rm -rf` the source.

## Restore on a new machine

```bash
git clone git@github.com:LukeJYK/my-skill.git ~/Desktop/my-skill
cd ~/Desktop/my-skill
mkdir -p ~/.agents/skills
for d in */; do [ -f "$d/SKILL.md" ] && rsync -a "$d" ~/.agents/skills/"$d"; done
cp .skill-lock.json ~/.agents/
npx skills update -g
```
