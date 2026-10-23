## C# / .NET checklist

- **L5**: breaking change of a public API/contract, EF migration that drops/alters data, auth/permission changes, secrets in code.
- **L4**: Domain referencing Infrastructure/Application (layer violation); business logic in controller/handler (anemic domain); `.Result`/`.Wait()`/`async void`; unhandled null (`!` without invariant, missing guard on nullable); aggregate modified from outside its root; entity exposed directly through the API; static mutable state; swallowed exception; undisposed `IDisposable`.
- **L3**: repository per table instead of per aggregate root; Value Object that is mutable or compared by reference; missing `CancellationToken` on I/O methods; service locator / `new` of dependencies; interface with a single implementation and no reason; DDD ceremony for plain CRUD; string-concatenated logging; test missing for new domain logic.
- **L2**: mutable public collections, missing `readonly`/`init`, unused `using`, `var` hiding unclear type, magic numbers/strings.
- **L1**: naming (`_camelCase` fields, `Async` suffix, `I` prefix), formatting that analyzers/editorconfig would catch.
