## TypeScript checklist

- **L5**: public type/contract changes that break consumers (exported types, API schemas), disabling `strict` or other compiler safety flags project-wide.
- **L4**: `any` (explicit or leaked from untyped input); unvalidated external data cast to a type with `as`; `@ts-ignore`; non-null `!` hiding a real undefined; non-exhaustive `switch` over a union; floating promise; unsafe `catch` usage (assuming `e` is `Error`).
- **L3**: boolean-flag soup instead of a discriminated union; type duplicated by hand next to its runtime schema; `enum` where a literal union is simpler; overly clever generics/conditional types; missing explicit return type on exported function; circular imports; missing test for new logic.
- **L2**: mutable where `readonly`/`const` fits, `Array<T>` vs `T[]` inconsistency with the codebase, missing `import type`, unused types/exports.
- **L1**: naming (`I` prefix, `Type` suffix), formatting caught by the linter.
