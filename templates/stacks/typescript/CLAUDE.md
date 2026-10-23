## TypeScript

- `tsconfig`: `"strict": true`, plus `noUncheckedIndexedAccess`, `exactOptionalPropertyTypes`, `noImplicitOverride`, `noFallthroughCasesInSwitch`. Lint with typescript-eslint (`no-explicit-any`, `no-floating-promises`, `consistent-type-imports`).
- **No `any`.** Use `unknown` and narrow it. No `@ts-ignore`; `@ts-expect-error` only with a reason.
- Avoid type assertions (`as`) and non-null `!`; if unavoidable, comment the invariant. Prefer type guards and `satisfies`.
- Model states with **discriminated unions** (`{ kind: 'loading' } | { kind: 'ok'; data: T }`), handle them with an exhaustive `switch` ending in a `never` check. Make illegal states unrepresentable.
- Prefer `type` unions and string literal unions over `enum`; `interface` for object shapes meant to be extended.
- Immutability by default: `const`, `readonly`, `ReadonlyArray<T>`, `as const`.
- Runtime data (HTTP, JSON, env, storage) is `unknown` until validated by a schema (zod/valibot); derive the static type from the schema (`z.infer`) instead of writing it twice.
- Explicit types on exported function signatures; let inference work inside bodies.
- Generics only when they remove duplication; keep constraints narrow; no type gymnastics that need a comment to decode.
- `import type` for type-only imports; no circular imports; no barrel files that hide dependencies in large modules.
- Naming: `PascalCase` types/classes, `camelCase` values, `UPPER_SNAKE` constants; no `I` prefix, no `Type` suffix.
- Errors: throw `Error` subclasses or return a `Result` union; never throw strings; narrow `catch (e: unknown)`.
