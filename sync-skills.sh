#!/usr/bin/env bash
# sync-skills.sh — mirror ~/.agents/skills (managed by `npx skills`) into this repo.
#
# One-way: ~/.agents/skills -> repo root. Install/update with
#   npx skills add <owner/repo> -s <name> -g -a universal -y
#   npx skills update -g
# and edit skills in ~/.agents/skills, never here (the next sync overwrites).
#
# Usage: ./sync-skills.sh [-c] [-u] [-p] [-n] [-f]
#   -c  copy only: no git add / commit / push
#   -u  run `npx skills update -g` first (pull from upstream)
#   -p  git push after committing
#   -n  dry run: show what would change, touch nothing
#   -f  force: overwrite uncommitted edits in the repo's skill folders
set -euo pipefail

SRC="${SKILLS_SRC:-$HOME/.agents/skills}"
LOCK="${SKILLS_LOCK:-$HOME/.agents/.skill-lock.json}"
REPO="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd -P)"

update=0 push=0 dry=0 force=0 copy_only=0
usage() { sed -n '2,16p' "$0" | sed 's/^# \{0,1\}//'; }
while getopts "cupnfh" opt; do
  case $opt in
    c) copy_only=1 ;;
    u) update=1 ;;
    p) push=1 ;;
    n) dry=1 ;;
    f) force=1 ;;
    h) usage; exit 0 ;;
    *) usage >&2; exit 2 ;;
  esac
done

die()  { echo "error: $*" >&2; exit 1; }
info() { echo "==> $*"; }

[ "$copy_only" = 1 ] && [ "$push" = 1 ] && die "-c (copy only) and -p (push) can't be combined"

# ---- safety checks -------------------------------------------------------
[ -d "$SRC" ] || die "$SRC does not exist"
[ -L "$SRC" ] && die "$SRC is a symlink. Keep it a real directory: the skills CLI deletes through links."
src_real="$(cd "$SRC" && pwd -P)"
case "$src_real/" in "$REPO"/*) die "$SRC resolves inside the repo ($src_real)";; esac
case "$REPO/" in "$src_real"/*) die "repo is inside $SRC";; esac
git -C "$REPO" rev-parse --is-inside-work-tree >/dev/null 2>&1 || die "$REPO is not a git repo"

# ---- 1. optional upstream update ----------------------------------------
if [ "$update" = 1 ]; then
  if [ "$dry" = 1 ]; then info "would run: npx skills update -g"
  else info "npx skills update -g"; npx skills update -g; fi
fi

# ---- 2. work out what to copy and what to remove -------------------------
synced=()    # skill names present in SRC
removed=()   # skill folders in repo that are gone from SRC
for dir in "$SRC"/*/; do
  [ -d "$dir" ] || continue
  name="$(basename "$dir")"
  if [ ! -f "$dir/SKILL.md" ]; then
    echo "skip (no SKILL.md in source): $name"; continue
  fi
  dest="$REPO/$name"
  if [ -d "$dest" ] && [ ! -f "$dest/SKILL.md" ] && [ -n "$(ls -A "$dest")" ]; then
    echo "skip (repo already has a non-skill folder named '$name')"; continue
  fi
  synced+=("$name")
done

for dir in "$REPO"/*/; do
  [ -d "$dir" ] || continue
  name="$(basename "$dir")"
  [ -f "$dir/SKILL.md" ] || continue          # not a skill folder: leave it alone
  [ -e "$SRC/$name" ] || removed+=("$name")
done

paths=(${synced[@]+"${synced[@]}"} ${removed[@]+"${removed[@]}"})

# Refuse to clobber edits made in the repo copy (tracked changes vs HEAD).
# Skipped with -c: after a copy-only run the repo legitimately differs from HEAD.
if [ "$force" = 0 ] && [ "$copy_only" = 0 ] && [ "${#paths[@]}" -gt 0 ] \
   && git -C "$REPO" rev-parse --verify -q HEAD >/dev/null \
   && ! git -C "$REPO" diff --quiet HEAD -- "${paths[@]}"; then
  git -C "$REPO" diff --stat HEAD -- "${paths[@]}" >&2
  die "uncommitted edits in the repo's skill folders above would be overwritten. Commit/discard them, or rerun with -f."
fi

# ---- 3. copy / remove ----------------------------------------------------
# --checksum: compare content, not size+mtime (same-size edits in the same second were skipped)
rsync_flags=(-a --checksum --delete --exclude .DS_Store)
[ "$dry" = 1 ] && rsync_flags+=(-n -v)

for name in ${synced[@]+"${synced[@]}"}; do
  if [ "$dry" = 1 ]; then info "would sync: $name"; else info "sync: $name"; fi
  rsync "${rsync_flags[@]}" "$SRC/$name/" "$REPO/$name/"
done

for name in ${removed[@]+"${removed[@]}"}; do
  if [ "$dry" = 1 ]; then info "would remove (gone from $SRC): $name"
  else info "remove (gone from $SRC): $name"; rm -rf "${REPO:?}/$name"; fi
done

if [ -f "$LOCK" ]; then
  if ! cmp -s "$LOCK" "$REPO/.skill-lock.json"; then
    if [ "$dry" = 1 ]; then info "would update .skill-lock.json"
    else info "update .skill-lock.json"; cp "$LOCK" "$REPO/.skill-lock.json"; fi
  fi
  paths+=(.skill-lock.json)
else
  echo "warn: no lock file at $LOCK" >&2
fi

if [ "$dry" = 1 ]; then info "dry run, nothing changed"; exit 0; fi
if [ "$copy_only" = 1 ]; then info "copied (not committed)"; exit 0; fi

# ---- 4. commit only what this script touched -----------------------------
cd "$REPO"
to_stage=()
for p in ${paths[@]+"${paths[@]}"}; do
  # existing paths, or deleted paths git still tracks
  if [ -e "$p" ] || git ls-files --error-unmatch -- "$p" >/dev/null 2>&1; then
    to_stage+=("$p")
  fi
done

if [ "${#to_stage[@]}" -eq 0 ]; then info "nothing to sync"; exit 0; fi

git add -A -- "${to_stage[@]}"
if git diff --cached --quiet -- "${to_stage[@]}"; then
  info "no changes to commit"
else
  git commit -q -m "sync skills from ~/.agents ($(date +%F))" -- "${to_stage[@]}"
  info "committed: $(git log -1 --format='%h %s')"
fi

if [ "$push" = 1 ]; then info "git push"; git push; fi
