## Review levels

Every finding gets exactly one level. Report format: `[L3] path/file:line — problem → suggested fix`.

| Level | Name | Meaning | Action |
|---|---|---|---|
| L1 | Nit | style, naming, taste | suggest, never block |
| L2 | Low | small defect, minor junk, readability | may auto-fix |
| L3 | Medium | over-engineering, duplication, missing test, weak error handling | fix before merge |
| L4 | High | likely bug, broken pattern of the stack, perf problem on hot path, null deref | block merge, fix required |
| L5 | Critical | data loss, security hole, breaking public contract, migration, architecture change | **STOP. Human decides.** Never auto-fix; describe options and risks |

End the review with a verdict (`approve` / `changes requested` / `needs human`) and a separate list of all L5 items.

## General checklist (all stacks)

**Junk and noise**
- dead code, unreachable branches, unused imports/variables/parameters/files
- commented-out code, stray logs/prints, debug leftovers, TODO without owner
- empty `catch`, empty methods/classes kept "for later"

**Null and empty references**
- unchecked null/undefined/None, missing guard on optional input
- blind `?.`/`??`/default that hides a bug instead of handling it
- empty collections/strings assumed non-empty; off-by-one on first/last element

**Simplicity (KISS is the dominant criterion)**
- Is there a simpler way with the same result? If yes → L3.
- interface/abstract/factory/wrapper with a single implementation and no real need
- speculative generality: options, flags, hooks, generics nobody uses
- nesting deeper than 3, functions over ~30 lines, more than 4 parameters
- clever one-liner that needs decoding; cleverness must come from simplicity, not density

**Principles**
- DRY: copy-paste beyond the third occurrence; but also wrong early abstractions
- SOLID: class doing several jobs, dependency on concretions at boundaries, fat interfaces, inheritance where composition fits
- naming: vague (`data`, `manager`, `helper`), misleading, inconsistent with the codebase

**Correctness and safety**
- error handling: swallowed errors, lost context, exceptions used as flow control
- security: secrets in code, injection, missing authn/authz, unvalidated input → L4/L5
- concurrency: races, blocking calls in async paths, unawaited work
- resources: unreleased handles/subscriptions/listeners
- performance: allocations or I/O in hot paths, N+1, needless work in loops

**Tests**
- new logic without a test; tests asserting nothing; tests coupled to implementation

**Git hygiene**
- branch name matches `feature|bugfix|hotfix|refactor|docs|chore|temp|wip/<what>`
- every commit is Conventional Commits, title only, Russian text, **no co-author / no Claude mention** (violation → L3)
- one task per branch, no unrelated changes mixed in
- PR: title with prefix and Russian text; description starts with `# Что сделано` in Russian
