## Area: Desktop app (e.g. Tauri / Electron)

- Strict process boundary: UI (webview) contains no privileged logic; native side exposes a minimal, typed command API and validates every call.
- Least privilege: allow-list only the capabilities/permissions/filesystem scopes the app needs; no remote code loading.
- Long or blocking work runs off the UI thread; the UI never freezes.
- Persist settings and data in the OS-appropriate app-data directory; version the stored format.
- Updates and installers are part of the product: signing, auto-update channel and rollback must be considered before shipping (human approval for release config).
- Handle offline/crash/restart gracefully; log to a file with rotation.
