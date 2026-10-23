## React

**Architecture**
- Function components + hooks only. A component renders; logic lives in **custom hooks**; data access lives in a service/api layer. Keep components small and single-purpose.
- Feature-based structure: `features/<name>/{components,hooks,api,model}` with a public `index.ts`; shared UI in `shared/ui`. Features do not import each other's internals.
- **State ladder** (use the lowest rung that works): local `useState`/`useReducer` → lift up → context (rarely changing values only) → server state library (TanStack Query) → global client store (Zustand/Redux) as the last resort. Never copy server data into local state.
- **Derive, don't sync**: values computable from props/state are computed during render, not stored and not set in `useEffect`.
- Composition over configuration: `children`/slots/compound components instead of a dozen boolean props; avoid prop drilling past 2–3 levels (composition or context).
- Route-level code splitting (`lazy` + `Suspense`); error boundaries around feature boundaries; explicit loading/empty/error UI states.

**Rules of hooks and rendering**
- Effects are for synchronizing with external systems only (subscriptions, timers, non-React APIs); always clean up; complete dependency arrays (no lint suppression). Event logic belongs in event handlers, not effects.
- Stable `key` from data id (never array index for dynamic lists). Don't create components inside components.
- `memo`/`useMemo`/`useCallback` only after measuring a real problem, or for referential stability a dependency needs.
- Controlled inputs; forms via a form library + schema validation (zod) for non-trivial forms.
- Never mutate state or props; no side effects during render.
- Accessibility: semantic HTML first, labels for inputs, keyboard operability, visible focus, ARIA only when semantics are missing.
- Styling through the project's single approach (CSS modules / Tailwind / styled); no inline style soup, design tokens for colors/spacing.
- Tests: React Testing Library, assert user-visible behavior (roles/text), not implementation details; test custom hooks via `renderHook`.
- TypeScript rules of this file set apply: typed props, no `any`, discriminated unions for UI state.
