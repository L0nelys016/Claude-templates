#!/usr/bin/env python3
"""Install CLAUDE.md / REVIEW.md rule templates (and optional extras) into a project.

Interactive:  python setup.py
Scripted:     python setup.py --target ../MyGame --stacks unity --area game --extras all --forge both --yes
"""
import argparse
import json
import os
import sys
from pathlib import Path

VERSION = "0.1.0"
ROOT = Path(__file__).resolve().parent / "templates"  # build.py swaps this line in the bundle
STACKS = ["csharp", "unity", "nodejs", "typescript", "react"]
IMPLIES = {"unity": ["csharp"], "react": ["typescript"]}
WEB = {"nodejs", "typescript", "react"}
AREAS = sorted(p.stem for p in (ROOT / "areas").glob("*.md"))
EXTRAS = ["settings", "pr", "commitlint", "editorconfig", "gitignore"]
FORGES = {"github": [".github"], "gitea": [".gitea"], "both": [".github", ".gitea"]}
MD_MARKS = ("<!-- claude-templates:begin -->", "<!-- claude-templates:end -->")
HASH_MARKS = ("# claude-templates:begin", "# claude-templates:end")


def read(path):
    return path.read_text(encoding="utf-8").replace("\r\n", "\n")


def expand(stacks):
    """Add implied stacks (unity -> csharp, react -> typescript), keep canonical order."""
    chosen = set(stacks)
    for s in stacks:
        chosen.update(IMPLIES.get(s, []))
    return [s for s in STACKS if s in chosen]


def upsert(path, body, marks, header=""):
    """Put body between markers; replace an existing block, append otherwise. Returns (text, how)."""
    begin, end = marks
    block = f"{begin}\n{body.strip(chr(10))}\n{end}\n"
    if not path.exists():
        return header + block, "create"
    old = read(path)
    i, j = old.find(begin), old.find(end)
    if i != -1 and j > i:
        return old[:i] + block.rstrip("\n") + old[j + len(end):], "update"
    return old.rstrip("\n") + "\n\n" + block, "append"


def merge(dst, src):
    """Deep-merge src into dst: dicts recurse, lists union, scalars take src."""
    for k, v in src.items():
        if isinstance(v, dict) and isinstance(dst.get(k), dict):
            merge(dst[k], v)
        elif isinstance(v, list) and isinstance(dst.get(k), list):
            dst[k] += [x for x in v if x not in dst[k]]
        else:
            dst[k] = v
    return dst


def build(target, stacks, area, extras, forge, force=False):
    """Return ([(path, text|None, how)], [next-step notes]). Touches nothing on disk."""
    stacks = expand(stacks)
    extras = set(extras)
    acts, notes = [], []

    def put(rel, text):
        p = target / rel
        if p.exists() and not force:
            acts.append((p, None, "skip (exists, use --force)"))
        else:
            acts.append((p, text, "overwrite" if p.exists() else "create"))

    def block(rel, body, marks, header=""):
        p = target / rel
        text, how = upsert(p, body, marks, header)
        acts.append((p, text, how))

    for kind in ("CLAUDE", "REVIEW"):
        parts = [read(ROOT / "core" / f"{kind}.md")]
        parts += [read(ROOT / "stacks" / s / f"{kind}.md") for s in stacks]
        if kind == "CLAUDE" and area:
            parts.append(read(ROOT / "areas" / f"{area}.md"))
        block(f"{kind}.md", "\n\n".join(p.strip("\n") for p in parts), MD_MARKS, f"# {kind}.md\n\n")

    ex = ROOT / "extras"
    web = bool(WEB & set(stacks))

    if "settings" in extras:
        p = target / ".claude" / "settings.json"
        data = json.loads(read(ex / "settings.json"))
        if p.exists():
            try:
                data = merge(json.loads(read(p)), data)
            except json.JSONDecodeError as e:
                raise SystemExit(f"error: {p} is not valid JSON ({e}); fix it or remove it first")
        acts.append((p, json.dumps(data, indent=2, ensure_ascii=False) + "\n", "merge" if p.exists() else "create"))

    if "pr" in extras:
        for d in FORGES[forge]:
            put(f"{d}/pull_request_template.md", read(ex / "pull_request_template.md"))

    if "commitlint" in extras:
        if web:
            put("commitlint.config.mjs", read(ex / "commitlint.config.mjs"))
            put(".husky/commit-msg", read(ex / "hooks" / "commit-msg.husky"))
            put(".husky/pre-push", read(ex / "hooks" / "pre-push"))
            notes.append("npm i -D husky @commitlint/cli @commitlint/config-conventional && npm pkg set scripts.prepare=husky && npm run prepare")
        else:
            put(".githooks/commit-msg", read(ex / "hooks" / "commit-msg.githooks"))
            put(".githooks/pre-push", read(ex / "hooks" / "pre-push"))
            notes.append("git config core.hooksPath .githooks   (Windows: git update-index --chmod=+x .githooks/*)")

    if "editorconfig" in extras:
        parts = [read(ex / "editorconfig" / "base.ini")]
        if "csharp" in stacks:
            parts.append(read(ex / "editorconfig" / "csharp.ini"))
        if web:
            parts.append(read(ex / "editorconfig" / "web.ini"))
        put(".editorconfig", "".join(parts))

    if "gitignore" in extras:
        names = [n for n, on in (("unity", "unity" in stacks), ("dotnet", "csharp" in stacks), ("node", web)) if on]
        body = "\n".join(read(ex / "gitignore" / f"{n}.gitignore").strip("\n") for n in names)
        block(".gitignore", body, HASH_MARKS)

    return acts, notes


def apply(acts):
    for path, text, _ in acts:
        if text is None:
            continue
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(text.encode("utf-8"))
        if ".githooks" in path.parts:
            os.chmod(path, 0o755)


def parse_list(raw, options):
    """'1,3' / 'unity react' / 'all' -> option names; raises ValueError on junk."""
    out = []
    for tok in raw.replace(",", " ").split():
        if tok == "all":
            return list(options)
        name = options[int(tok) - 1] if tok.isdigit() and 0 < int(tok) <= len(options) else tok
        if name not in options:
            raise ValueError(tok)
        out.append(name)
    return out


def choose(title, options, multi):
    print(f"\n{title}")
    for i, o in enumerate(options, 1):
        print(f"  {i}) {o}")
    while True:
        try:
            picked = parse_list(input("> ").strip(), options)
            if multi or len(picked) <= 1:
                return picked
        except ValueError as e:
            print(f"unknown option: {e}")
        print("try again" if multi else "pick one")


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--version", action="version", version=f"claude-templates {VERSION}")
    ap.add_argument("--target", help="project folder (default: ask, '.' if empty)")
    ap.add_argument("--stacks", help=f"comma list of: {', '.join(STACKS)}")
    ap.add_argument("--area", help=f"one of: {', '.join(AREAS)}, none")
    ap.add_argument("--extras", help=f"comma list of: {', '.join(EXTRAS)}, all, none")
    ap.add_argument("--forge", choices=list(FORGES), help="where the PR template goes")
    ap.add_argument("--dry-run", action="store_true", help="show what would change, write nothing")
    ap.add_argument("--yes", action="store_true", help="no prompts; missing values take defaults")
    ap.add_argument("--force", action="store_true", help="overwrite existing extras (never needed for CLAUDE.md/REVIEW.md)")
    a = ap.parse_args(argv)
    ask = not a.yes

    try:
        if a.target is None:
            a.target = (input("Target project folder [.]: ").strip() or ".") if ask else "."
        stacks = parse_list(a.stacks, STACKS) if a.stacks else (choose("Stacks (multi, e.g. 1,3):", STACKS, True) if ask else [])
        area = a.area if a.area is not None else (choose("Project area:", ["none"] + AREAS, False) or ["none"])[0] if ask else "none"
        extras = parse_list(a.extras, EXTRAS) if a.extras and a.extras != "none" else (
            choose("Extras (multi, 'all' or Enter for none):", EXTRAS, True) if a.extras is None and ask else [])
        forge = a.forge or ("github" if not ask or "pr" not in extras else (choose("PR template folder (Enter = github):", list(FORGES), False) or ["github"])[0])
    except ValueError as e:
        sys.exit(f"error: unknown value {e}")
    if not stacks:
        sys.exit("error: choose at least one stack (--stacks)")
    if area != "none" and area not in AREAS:
        sys.exit(f"error: unknown area '{area}'")
    target = Path(a.target).expanduser().resolve()
    if not target.is_dir():
        sys.exit(f"error: {target} is not a directory")

    acts, notes = build(target, stacks, None if area == "none" else area, extras, forge, a.force)
    print(f"\nTarget: {target}\nStacks: {', '.join(expand(stacks))}   Area: {area}")
    for path, _, how in acts:
        print(f"  {how:<10} {path.relative_to(target)}")
    if a.dry_run:
        print("\n(dry run: nothing written)")
        return
    if ask and input("\nProceed? [y/N] ").strip().lower() != "y":
        sys.exit("aborted")
    apply(acts)
    print("\nDone. Next steps:")
    for n in notes + ["commit the new files on a task branch (e.g. chore/claude-rules) and push"]:
        print(f"  {n}")


if __name__ == "__main__":
    main()
