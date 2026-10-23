## Node.js checklist

- **L5**: DB schema/data migrations, auth/session/token logic, public API contract break, secrets or credentials in code/history, new production dependency.
- **L4**: unvalidated external input; SQL/command/NoSQL injection; floating (unawaited) promise; sync/blocking call in a request path; business logic inside a controller/route; service importing HTTP framework types; missing error handling that crashes the process or leaks stack traces; no graceful shutdown for resources that need closing; `process.env` read all over the code.
- **L3**: no composition root (hidden singletons/imports instead of injected dependencies); layered-by-type structure that couples features; inconsistent error shape; missing pagination/limits on list endpoints; unstructured `console.log` in server code; missing test for a new service/route; dependency added where stdlib suffices.
- **L2**: missing `.env.example` entry, unused dependency, callback style where `async` fits, magic numbers for timeouts/limits.
- **L1**: naming, import order, file layout conventions.
