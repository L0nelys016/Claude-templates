## Unity

**Architecture: MVP + state machine**
- **MVP**: `View` is a passive `MonoBehaviour` (exposes events/setters, zero logic); `Presenter` is a plain C# class holding all UI/game-flow logic, talks to View through an interface (`IXxxView`); `Model` is pure C# (no `UnityEngine` types where avoidable). Presenters are created and wired by a composition root (DI container such as VContainer/Zenject, or manual).
- **State machine** for anything with modes: game flow, player, enemy AI, UI screens. Explicit states (`IState` with `Enter/Tick/Exit`), explicit allowed transitions, one active state, no boolean-flag soup (`isJumping && !isDead && ...`).
- Decouple systems with C# events / message bus / ScriptableObject channels. No `FindObjectOfType`, no god-singletons; if a singleton is unavoidable, make it an interface-backed service.
- Data in `ScriptableObject`s (configs, balance); runtime state in plain C# models. Never mutate a ScriptableObject asset at runtime.
- Split code with Assembly Definitions (`.asmdef`) per feature/layer; Editor code in Editor-only assemblies.

**Performance and lifecycle**
- No `Find*`, `GetComponent*`, `Camera.main`, LINQ or string concatenation in `Update`/`FixedUpdate`; cache references in `Awake`/`Start`.
- Zero allocations in hot paths; pool frequently spawned objects (`ObjectPool<T>`); avoid boxing and closures per frame.
- Subscribe in `OnEnable`, unsubscribe in `OnDisable`/`OnDestroy` (every `+=` has a `-=`).
- Prefer events over polling; use `Update` only when per-frame work is really needed.
- Use `[SerializeField] private` instead of public fields; `[RequireComponent]` for hard dependencies.
- Destroyed objects: Unity overloads `== null`; do not use `?.`/`??` on `UnityEngine.Object`.
- Async: coroutines or UniTask/`Awaitable` with cancellation tied to object lifetime (`destroyCancellationToken`).
- Physics in `FixedUpdate`, input/visuals in `Update`/`LateUpdate`; never scale logic by frame count, use `Time.deltaTime`.

**Project hygiene**
- Commit `.meta` files; never commit `Library/`, `Temp/`, `Logs/`, `obj/`, `UserSettings/`.
- Keep scenes small, logic in prefabs; avoid editing scene/prefab YAML by hand; resolve merge conflicts in the Editor.
- Load heavy assets via Addressables, not `Resources`.
- Follow the C# rules of this file set (naming, nullable, no static mutable state).
