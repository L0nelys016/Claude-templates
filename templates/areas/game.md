## Area: Game

- Separate simulation (rules, state) from presentation (views, VFX, audio): the simulation must be runnable and testable without the engine's scene.
- Game flow is an explicit state machine (boot → menu → loading → gameplay → pause → result); no hidden mode flags.
- All tuning values (speeds, costs, drops) live in data/config assets, not in code.
- Save data is versioned with a migration path; changing its format needs human approval.
- Frame budget is a requirement: no per-frame allocations, pooling for frequent spawns, profile before and after optimization.
- Deterministic randomness through one injectable RNG so bugs are reproducible.
- Input goes through an abstraction layer (actions), never read directly in gameplay logic.
