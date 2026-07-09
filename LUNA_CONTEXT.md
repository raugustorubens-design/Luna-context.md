# LUNA Context

## Current state
- The LUNA architecture is transitioning from feature-oriented organization to organism-oriented organization.
- The current guiding principle is: Discover → Integrate → Create.
- The backend is the intelligence layer; the frontend is only the face of LUNA.
- The Project Renascer repository is intended to become the official LUNA frontend.
- The Modo Dev must preserve LUNA visual identity and borrow UX ideas from Cursor without copying the interface.
- The official name for the Cursor-like development environment is **LUNA Forge**.
- Every capability in LUNA Forge must be delivered as its own MVP, with a clear scope, tests, and integration path.

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

## Safety / process rules
- Do not create new components when an equivalent exists.
- Do not commit if there is conflict, regression risk, or unresolved architectural inconsistency.
- Prefer reporting conflicts and alternatives over forcing implementation.
- Preserve LUNA identity and avoid unnecessary substitutions.
- Any AI or agent that codes in GitHub must update LUNA_CONTEXT.md with the realized actions and architectural decisions before finishing, unless a blocking conflict or regression risk prevents it.
- Architecture tests must be treated as part of the constitution: provider, gateway, hipocampo, memory, context, and frontend boundaries must remain enforced.
