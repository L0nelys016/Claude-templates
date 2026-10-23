## Core principles

- **KISS first.** Solutions must be clever but simple: the simplest design that fully solves the task wins. If you can't explain it in two sentences, simplify it.
- **YAGNI.** Build only what was asked. No speculative options, hooks, layers or "for later" code.
- **DRY with judgment.** Extract duplication on the third occurrence (rule of three). Wrong abstraction costs more than a copy.
- **SOLID.** Single responsibility per class/module; depend on abstractions at boundaries; prefer small interfaces; extend by composition, not inheritance.
- Fail fast: validate at trust boundaries, never swallow errors, never return silent defaults.
- Small functions (about 30 lines), shallow nesting (max 3), few parameters (max 4).
- Names say what a thing is or does; comments explain only *why*, never *what*.
- No dead code, no commented-out code, no stray debug output, no unused imports/variables, no TODO without owner.
- Handle null/empty explicitly: never assume a reference is set; never hide a bug with a blind `?.` or default.
- Reuse what already exists in the codebase (helpers, patterns, dependencies) before writing new code. Match surrounding style.
- Add a dependency only if the standard library or existing dependencies can't do it.
- Every non-trivial logic change ships with a test.

## Git workflow

**One task = one branch.** Never commit to `main`/`master` directly. Create the branch before the first change and push it immediately (`git push -u origin <branch>`).

| Branch | Purpose |
|---|---|
| `feature/<what>` | new functionality |
| `bugfix/<what>` | bug fix |
| `hotfix/<what>` | urgent production fix |
| `refactor/<what>` | refactoring |
| `docs/<what>` | documentation |
| `chore/<what>` | housekeeping |
| `temp/<what>` or `wip/<what>` | draft / experiment |

**Commits: Conventional Commits, title only.**

| Type | Meaning |
|---|---|
| `feat:` | new feature |
| `fix:` | bug fix |
| `docs:` | documentation |
| `style:` | formatting (indent, whitespace) |
| `refactor:` | refactoring without logic change |
| `perf:` | optimization |
| `test:` | tests |
| `build:` | build system (Tauri, webpack, ...) |
| `ci:` | CI/CD settings |
| `chore:` | misc (.gitignore, dependencies) |
| `revert:` | revert |

- Commit has a **title only**: no body, no description.
- Commit titles are written in **Russian** (after the English type prefix), e.g. `feat: добавить экран настроек`.
- **Never** add `Co-Authored-By` or any mention of Claude/AI to commits or PRs.
- Auto-commit after every action (every plan step) and **push immediately** (`git push`). Never leave unpushed work.
- Never force-push, never rewrite pushed history, never skip hooks.

**Pull requests: only when the user asks.**

1. Title: type prefix + body **in Russian only**, e.g. `feat: добавить экран настроек`.
2. Description starts with the heading `# Что сделано`, followed by a description in Russian.

## Human-in-the-loop (stop and ask)

Do **not** decide alone, present options and wait for the user, before:

- data/schema migrations, deleting or overwriting data, irreversible operations;
- breaking changes of a public API/contract;
- authentication, authorization, secrets, security-sensitive code;
- adding/removing/upgrading a major dependency;
- changing architecture or project structure;
- anything you are unsure about.

## Definition of done

Builds without warnings you introduced; tests and linters pass; no junk left; changes committed and pushed on the task branch.
