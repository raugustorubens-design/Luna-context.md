# LUNA Context

## Current state
- The LUNA architecture is transitioning from feature-oriented organization to organism-oriented organization.
- The current guiding principle is: Discover → Integrate → Create.
- The backend is the intelligence layer; the frontend is only the face of LUNA.
- The Project Renascer repository is intended to become the official LUNA frontend.
- The Modo Dev must preserve LUNA visual identity and borrow UX ideas from Cursor without copying the interface.
- The official name for the Cursor-like development environment is **LUNA Forge**.
- Every capability in LUNA Forge must be delivered as its own MVP, with a clear scope, tests, and integration path.
- Every organ of the LUNA ecosystem should be treated as an independently evolvable MVP product with its own responsibility, documentation, tests, and integration contracts.

## Consolidated decisions
- The user speaks only with LUNA.
- The system must automatically choose the provider for each task.
- Providers considered: ChatGPT, Claude, Grok, Manus, and future models.
- The backend must include or evolve the following organs:
  - Gateway
  - Cognitive Engine
  - Planner
  - Hipocampo
  - Memory Engine
  - Provider Engine
  - Provider Router
  - Budget Manager
  - Reporter
  - Filtro Cognitivo
  - Índice Cognitivo
  - Context Hub
- The index in Supabase should evolve into a Contexto Evolutivo do Projeto / Contextual reconstruction layer.
- The Context Hub must provide shared context to all providers so they know the project state, principles, inferential history, and current mission.
- Memory should be consolidated through the Hipocampo; persistence is executed by the Memory Engine.
- The provider selection must minimize cost and prefer one provider by default.
- The Modo Dev / LUNA Forge must behave like a Cognitive IDE with observability, memory, diagnostics, costs, providers, and infrastructure panels.
- The Forge should include the same core coding capabilities expected from Cursor, including Python library integration.
- Organs are not just internal modules: they must be able to exist as independent MVPs and commercial products while staying integrated through shared contracts.
- The monorepo is an integration surface, not the owner of every organ’s identity.

## Audit findings
- A full architectural audit was performed.
- The audit confirmed that the documentation is more mature than the implementation.
- Existing code contains reusable capabilities, orphaned components, dead code, and duplicated frontend variants.
- The Renascer repository is effectively a broken/generated artifact rather than a mature product.
- n8n references were not found in the audited monorepo scope.
- A plaintext database credential was found in `.env`; rotate it before further development.

## Planned actions
1. Derive a capability map from the audit.
2. Align repository responsibilities with organs and L-Cells.
3. Consolidate reusable code into the canonical backend organs.
4. Rebuild or adapt the Project Renascer repository as the official frontend.
5. Implement the provider routing and budget management strategy in the backend.
6. Evolve the Supabase index into a hybrid semantic + logical context reconstruction layer.
7. Add the shared Context Hub so every provider receives the same project context.
8. Build the Modo Dev as a LUNA-branded Cognitive IDE.
9. Treat each Forge capability as an MVP with an explicit scope, tests, and integration path.
10. Treat each organ as an independent MVP product that can evolve, ship, and generate revenue without losing organism-level integration.

## Safety / process rules
- Do not create new components when an equivalent exists.
- Do not commit if there is conflict, regression risk, or unresolved architectural inconsistency.
- Prefer reporting conflicts and alternatives over forcing implementation.
- Preserve LUNA identity and avoid unnecessary substitutions.
- Any AI or agent that codes in GitHub must update LUNA_CONTEXT.md with the realized actions and architectural decisions before finishing, unless a blocking conflict or regression risk prevents it.
- Architecture tests must be treated as part of the constitution: provider, gateway, hipocampo, memory, context, and frontend boundaries must remain enforced.

## Convergence check — luna monorepo, 2026-07-09 (ADR-004)

A separate work session on `raugustorubens-design/luna` (backend consolidation of the 12 organs, then Convergia) independently reached the same conclusion recorded above — organs as independent MVPs, monorepo as integration surface — and wrote it up as `docs/architecture/adr-004-organs-as-independent-mvps.md` in that repo. Recording the convergence here, plus the concrete findings from that session this file didn't yet have:

- **Reporter identity conflict resolved.** `raugustorubens-design/luna-reporter` is confirmed as the official Reporter organ (situational awareness of the whole organism, GitHub/Supabase/Railway observation → diagnostics → recommendations, per its own `docs/constitution/luna_constitution_v1.md`). The `luna` monorepo had independently built `src/luna/reporter.ts` — an in-process audit log for its cognitive pipeline, not the same thing. It is not being renamed yet (needs an isolated pass: architecture-check.mjs, tests, imports); the monorepo's `luna_context/LUNA_CONTEXT.md` §10 tracks this as an open action.
- **Convergia** (`raugustorubens-design/luna-convergia`) was physically absorbed into the `luna` monorepo (`src/convergia/`) in the pass before ADR-004, before this file's "independent MVP" guidance was discovered by that session. ADR-004 reclassifies it as a priority candidate for independent productization again, but does not move it back out yet — there is no API contract today between a Convergia service and Hipocampo/Memory Engine, only a direct in-process function call. Moving it out before that contract exists would break the monorepo's automated boundary checks with nothing to replace them.
- **`apps/core`/`apps/api` inside the `luna` monorepo are near-duplicates of `raugustorubens-design/luna-core` and `raugustorubens-design/luna-api`.** `luna-core`'s last commit is literally "force deploy" — it may be the live production instance. Neither monorepo copy was removed; deciding which one is the real deploy target is flagged as a product decision, not resolved.
- **`raugustorubens-design/luna-frontend`** (Next.js visual prototype: cognitive dashboard, pipeline view, chat terminal, observability panel — all thin/mocked, ~130 lines of components total) was found but not evaluated against the "Project Renascer becomes the official frontend" plan recorded above. Worth a dedicated look before committing to Renascer as the frontend path, given Renascer's own repo is confirmed to be a broken generated artifact.

No repository was created, deleted, or had code moved as part of this convergence check. Both `LUNA_CONTEXT.md` files (this one and the monorepo's `luna_context/LUNA_CONTEXT.md`) should be treated as needing to stay consistent — divergence between them is itself an architectural conflict to record, not ignore.
