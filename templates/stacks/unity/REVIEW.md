## Unity checklist

- **L5**: changes to serialized data layout that break existing saves/prefabs/scenes (renamed serialized fields without `FormerlySerializedAs`), deleting assets referenced elsewhere, save-data format changes, changes to build/platform settings.
- **L4**: logic inside a View `MonoBehaviour` (MVP violation); Presenter/Model depending on concrete View or scene objects; behavior driven by tangled bool flags instead of a state machine; `Find*`/`GetComponent*`/LINQ/allocations in `Update`; event subscription without unsubscription; `?.`/`??`/`== null` misuse on destroyed `UnityEngine.Object`; runtime mutation of a ScriptableObject asset; missing null-check on a serialized reference that can be unassigned; coroutine/async not cancelled on destroy.
- **L3**: public fields instead of `[SerializeField] private`; god-singleton / static state; no `.asmdef` separation in a growing feature; `Resources.Load` for heavy assets; per-frame polling where an event fits; missing pooling for frequently spawned objects; frame-dependent logic instead of `Time.deltaTime`; state machine with implicit/unchecked transitions.
- **L2**: `.meta` missing for new asset, unused serialized fields, magic numbers instead of config, `Debug.Log` leftovers, `Camera.main` not cached.
- **L1**: naming, region/ordering conventions (`Awake` → `OnEnable` → `Start` → `Update`).
