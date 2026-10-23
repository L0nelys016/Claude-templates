## C# / .NET

**Architecture: DDD with clean layering**
- Layers: `Domain` → `Application` → `Infrastructure` → `Api/UI`. Dependencies point inward only; `Domain` references nothing (no EF, no HTTP, no logging frameworks).
- Use the ubiquitous language of the domain in names; one bounded context = one module.
- Building blocks: **Entity** (identity), **Value Object** (immutable `record`/`readonly struct`, equality by value), **Aggregate** (single root, invariants enforced inside, referenced from outside by id only), **Repository** (one per aggregate root, interface in Domain/Application, implementation in Infrastructure), **Domain Event** (state changes announced, handled in Application).
- Domain logic lives in the domain model, not in services or controllers (no anemic model). Application services only orchestrate: load → call domain → save.
- Map at boundaries: DTOs/contracts ≠ domain entities ≠ persistence models.
- Start simple: do not introduce DDD ceremony (aggregates, events) for plain CRUD.

**Language and style**
- `<Nullable>enable</Nullable>` and `TreatWarningsAsErrors`; never silence nullable warnings with `!` without a comment explaining the invariant.
- Constructor injection only; no service locator, no static mutable state, no `new` of services inside logic.
- Prefer immutability: `init`/`readonly`/`record`; collections exposed as `IReadOnlyList<T>`.
- `async`/`await` end to end: never `.Result`/`.Wait()`, accept `CancellationToken`, no `async void` (except event handlers), `ConfigureAwait(false)` in libraries.
- Dispose with `using`; implement `IDisposable` only when owning unmanaged/disposable resources.
- Exceptions for exceptional cases; expected failures return a result type. Never `catch (Exception)` without rethrow or logging with context.
- Guard clauses over deep nesting; LINQ only while it stays readable.
- Naming: `PascalCase` types/methods/properties, `_camelCase` private fields, `I` prefix for interfaces, `Async` suffix for async methods.
- Structured logging (`ILogger<T>` with message templates), never string-concatenated logs, never log secrets.
- Tests: xUnit, arrange-act-assert, one behavior per test, domain tested without infrastructure.
