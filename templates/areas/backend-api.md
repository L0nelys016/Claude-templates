## Area: Backend API

- Contract first: stable, versioned endpoints; additive changes only, breaking change = new version (needs human approval).
- One consistent error shape (RFC 9457 problem details); correct HTTP status codes; no stack traces to clients.
- Lists are paginated and bounded; writes that clients may retry are idempotent.
- DTOs at the edge, domain/persistence models inside; never expose storage entities.
- Authn/authz on every endpoint by default (deny unless allowed); validate all input.
- Observability: request id, structured logs, health/readiness endpoints, metrics for latency and errors.
- Database changes via reviewed, reversible migrations; no destructive migration without human approval.
