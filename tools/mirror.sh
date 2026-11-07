#!/bin/sh
# The mirror: a git bundle of this repo and one of the private work folder
# beside it (this folder's name plus "-work"), each holding its repo's whole
# history, kept in the mirrors folder under one fixed name per repo,
# <folder name>.bundle (Garrett, 2026-11-03). Each run writes the new bundle
# under a temporary name, <folder name>.bundle.new, checks it with git bundle
# verify and its HEAD against its repo's, and only then renames it over the
# old one, so the old one is never removed before the new one verifies. Each
# bundle's HEAD is printed beside its repo's HEAD. A new bundle that fails
# either check is deleted, the old one stays as it was, and the run fails
# (exit 1). Only commits are mirrored: a repo with a detached HEAD, or with
# anything not committed (changes or new files), stops it before anything is
# written. Shaped like PrivateApp's scripts/mirror.sh. When to run it:
# WORKFLOW.md, "Mirror, tag, export".
# Run from Git Bash. Usage: sh tools/mirror.sh [TARGET]
#   TARGET is the mirrors folder: by default ~/dev/mirrors. It must exist.
# To restore a repo: git clone -c core.autocrlf=false <bundle> <folder>, so
# its files come back with the bytes they were committed with.

# git here is a Windows program: Git Bash must turn /c/... paths into
# Windows paths for it, which a shell set up for containers may turn off.
unset MSYS_NO_PATHCONV

here=$(cd "$(dirname "$0")/.." && pwd) || exit 2
work=$here-work
target=${1:-$HOME/dev/mirrors}

stop() { # a refusal before anything is written
    echo "FAILED: $*" >&2
    exit 1
}

[ -d "$target" ] || {
    echo "FAILED: there's no folder $target." >&2
    exit 2
}
target=$(cd "$target" && pwd) || exit 2

# Both repos are checked before either bundle is written.
for repo in "$here" "$work"; do
    name=$(basename "$repo")
    [ -d "$repo/.git" ] || stop "$repo isn't a git repo. Nothing was written."
    git -C "$repo" symbolic-ref -q HEAD >/dev/null ||
        stop "$name's HEAD is detached: check out its branch, then mirror. Nothing was written."
    changed=$(git -C "$repo" -c core.quotePath=false status --porcelain | cut -c4- | tr '\n' ' ')
    [ -z "$changed" ] ||
        stop "$name has changes or files not committed (${changed% }): commit them, then mirror. Nothing was written."
done

failed=0
written=""
for repo in "$here" "$work"; do
    name=$(basename "$repo")
    bundle=$target/$name.bundle
    new=$bundle.new
    head=$(git -C "$repo" rev-parse HEAD) || exit 2
    rm -f "$new" # a temporary file left by a run that was cut short, never the bundle
    if ! out=$(git -C "$repo" bundle create "$new" --all 2>&1); then
        rm -f "$new"
        echo "FAILED: git couldn't write $new ($(printf '%s\n' "$out" | tail -1)); $name.bundle is as it was." >&2
        failed=1
        continue
    fi
    held=$(git -C "$repo" bundle list-heads "$new" 2>/dev/null | awk '$2 == "HEAD" { print $1 }')
    if ! git -C "$repo" bundle verify --quiet "$new" >/dev/null 2>&1; then
        verdict="FAILED: git bundle verify"
    elif [ "$held" != "$head" ]; then
        verdict="FAILED: the bundle's HEAD isn't the repo's"
    elif ! mv -f "$new" "$bundle"; then
        verdict="FAILED: it couldn't be renamed over $name.bundle"
    else
        verdict="verified"
        written="$written $name.bundle"
    fi
    if [ "$verdict" != verified ]; then
        rm -f "$new"
        verdict="$verdict; $name.bundle is as it was"
        failed=1
    fi
    echo "$name HEAD $head  bundle HEAD ${held:-none}  $verdict"
done
[ "$failed" -eq 0 ] || exit 1
echo "Mirrored to $target:$written."
