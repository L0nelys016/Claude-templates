## Area: Web frontend

- Design tokens for color/spacing/typography; reusable UI primitives in one shared place, no one-off styles.
- Responsive from mobile up; accessibility is a requirement (WCAG AA contrast, keyboard, screen-reader labels).
- Every async view has loading, empty and error states; optimistic updates only with rollback.
- Performance budget: route-level code splitting, lazy images, no heavy dependency for a small feature; check bundle impact before adding a package.
- Routing and data fetching live at feature boundaries; URL is the source of truth for shareable state.
- All user-facing strings go through one i18n layer if the app is (or may become) multilingual.
- Never trust the client: authorization is enforced by the server; no secrets in the bundle.
