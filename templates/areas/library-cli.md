## Area: Library / CLI

- The public API is a promise: keep it small, documented and stable; follow semantic versioning; breaking change needs human approval.
- No global state, no I/O or logging side effects at import time; configuration is passed in.
- Minimal dependencies — every dependency is inherited by all consumers.
- CLI: predictable exit codes, human output to stdout/errors to stderr, `--help` for every command, machine-readable output option, non-interactive mode for CI.
- Examples in docs are tested (compiled/run in CI) so they never rot.
- Changelog entry for every user-visible change.
