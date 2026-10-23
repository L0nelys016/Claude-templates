## React checklist

- **L5**: replacing the state-management or routing approach, changing auth/session handling on the client, exposing secrets in the bundle, breaking a shared component's public props used across features.
- **L4**: side effect during render; mutation of state/props; effect missing cleanup or with wrong/suppressed dependencies; hook called conditionally or in a loop; infinite render/effect loop; stale closure bug; `dangerouslySetInnerHTML` with unsanitized input; index used as `key` in a dynamic list; component defined inside another component; unhandled promise/error in a handler or effect.
- **L3**: derived state stored in `useState` and synced via `useEffect`; server data copied into local/global state; business/data logic inside the component instead of a hook/service; prop drilling beyond 2–3 levels; god-component (> ~150 lines or several responsibilities); feature importing another feature's internals; premature `memo`/`useCallback` without measurement; missing loading/error/empty state; missing a11y basics (label, semantic element, keyboard); missing test for new behavior.
- **L2**: unused props/state/imports, inline styles outside the project's styling approach, boolean-prop explosion where composition fits.
- **L1**: naming, file/folder conventions, import order.
