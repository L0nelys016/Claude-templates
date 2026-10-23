# Claude-templates

[Русская версия](README.ru.md)

Rule templates (`CLAUDE.md`, `REVIEW.md`) for Claude projects and a script that installs them.

Stacks: **C#**, **Unity** (implies C#), **Node.js**, **TypeScript**, **React** (implies TypeScript).
Areas: `backend-api`, `web-frontend`, `game`, `desktop-app`, `library-cli`.

## Usage

Requires Python 3.9+ (stdlib only).

```bash
python setup.py                       # interactive
python setup.py --target ../MyGame --stacks unity --area game --extras all --forge both --yes
python setup.py --target . --stacks react,nodejs --dry-run
```

| Flag | Meaning |
|---|---|
| `--target` | project folder |
| `--stacks` | `csharp,unity,nodejs,typescript,react` |
| `--area` | one area or `none` |
| `--extras` | `settings,pr,commitlint,editorconfig,gitignore` / `all` / `none` |
| `--forge` | `github`, `gitea`, `both` (PR template folder) |
| `--dry-run` | show changes only |
| `--yes` | no prompts |
| `--force` | overwrite existing extras |

## What gets written

- `CLAUDE.md`, `REVIEW.md`: the rules are placed between `claude-templates:begin/end` markers. Re-running updates only that block; your own text is kept.
- `settings`: `.claude/settings.json` merged (no Claude co-author/attribution, deny force-push and `reset --hard`).
- `pr`: `pull_request_template.md` in `.github/` and/or `.gitea/`.
- `commitlint`: Node stacks get commitlint + husky; others get plain `.githooks/` (commit format, title only, no co-author, branch name).
- `editorconfig`, `gitignore`: per selected stack (gitignore is a marked block).

The script never runs `npm` or `git`; it prints the follow-up commands.

## Adding a stack

Create `templates/stacks/<name>/CLAUDE.md` and `REVIEW.md`, add the name to `STACKS` (and `IMPLIES` if needed) in `setup.py`. Keep a fragment under ~60 lines.

## Tests

```bash
python -m unittest discover tests
```
