## Node.js

**Architecture: layered, composition root**
- Layers: `routes/controllers` (HTTP only: parse, validate, call, respond) → `services` (business logic, no HTTP/framework types) → `repositories` (data access behind interfaces). Dependencies point inward.
- One composition root (`main`/`app.ts`) builds the dependency graph; modules receive dependencies via parameters/constructors, never import singletons from deep inside.
- Organize by feature/module (`users/`, `orders/`), not by technical type across the whole app.
- Config: read `process.env` in exactly one place, validate it at startup (zod/envalid), fail fast on missing values; never commit secrets, provide `.env.example`.
- Validate **all** external input at the boundary (body, query, params, headers); map to typed DTOs; never trust it deeper.

**Runtime rules**
- ESM modules, `async`/`await` everywhere; never leave a promise unhandled (`no-floating-promises`); never block the event loop (no sync fs/crypto/CPU loops in request paths; use workers/queues).
- Central error handling: typed domain errors → one error middleware maps them to HTTP codes; no `try/catch` that only logs and continues.
- Graceful shutdown: handle `SIGTERM`/`SIGINT`, stop accepting, drain, close DB/queues.
- Structured JSON logging (pino) with request id; never log secrets or PII.
- Security: `helmet`, rate limiting, parameterized queries only, CORS allow-list, dependency audit, least-privilege tokens.
- API: consistent error shape, pagination for lists, idempotency for retried writes, version the contract.
- Tests: unit for services (mock repositories), integration for routes against a real/test DB (vitest or `node:test`).
- Prefer the standard library (`fetch`, `node:test`, `node:crypto`) over new packages; pin and review dependencies.
