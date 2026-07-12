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

## Ecosystem architecture consolidation — 2026-07-09 (final macro prompt)

Full detail lives in `ECOSYSTEM_ARCHITECTURE.md` in this repository — this section is the mandatory summary. This is documentation-only work: no code moved, no repository created or restructured, per this pass's explicit closing rule.

**New inferences**
- All 10 known repositories were enumerated with an unfiltered account-wide search (previous passes only searched by name guesses). No 11th repository exists as of this date.
- `Luna-reporter`'s own `observations.json` shape (`{source, system, type, timestamp, payload}`) is a stronger candidate for the ecosystem's official Events contract than the monorepo's internal `AuditEvent` shape (`{name, at, evidence}`) — it already accounts for multiple sources, the monorepo's shape doesn't.
- A real architectural inconsistency was found while building the dependency matrix: `luna`'s `src/convergia/training/training-to-memory.ts` calls `memory-engine.ts`'s `checkpoint()` directly, bypassing Hipocampo. `checkpoint()` persists data internally, so this quietly violates "Convergia never persists directly." The existing automated check (`architecture-check.mjs`) didn't catch it because it only scans for `supabase|drizzle` tokens, not call topology. Not fixed this pass (no-implementation rule) — registered as a priority roadmap item and a future constitution test.
- No Auth/Identity contract exists anywhere in the ecosystem. The Gateway's authorization policy is allow-all. This is a real gap, not yet a blocker for anything in production.

**New strategy (confirmed, not changed)**
- This is the last macro architecture prompt. All future work ships as independent MVPs against the roadmap in `ECOSYSTEM_ARCHITECTURE.md` §7 — no more monorepo-wide consolidation passes.

**System classification (see ECOSYSTEM_ARCHITECTURE.md §2 for full table)**
- Sistema/Infraestrutura: `luna` monorepo, `Luna-context.md`
- Órgão + MVP + candidate Produto: `Luna-reporter`, Convergia (inside the monorepo)
- Legado/Experimental: `luna-convergia` (original repo, code superseded), `luna-frontend`, `Luna-API`, `Front-View`, `projeto-renascer`, `projeto-renascer-backup`
- Shared Kernel candidates: contract interfaces only (LunaContext, ProviderAdapter, ConsolidationCandidate/Decision, CanonicalDocument, AuditEvent/Observation, Capability/Manifest) — never implementations

**Reclassification — 2026-07-12 (ADR-004 executed):** `luna-core` moves out of Legado/Experimental into Infraestrutura/Órgão (hospeda Gateway + Connector Hub, `luna-core` PR #6 and PR #7). Its classification as of this 2026-07-09 consolidation (Legado, Infraestrutura possível) is preserved as history in `ECOSYSTEM_ARCHITECTURE.md` §1/§2, not deleted — this note and that document's own inline annotations are the record of the change, not a silent edit.

**Consolidated principles**
- No physical merge of systems for implementation convenience — this is the concrete lesson of ADR-004 and this document.
- Contracts are the only allowed coupling surface between systems with their own repository.
- Every new architectural rule becomes a test eventually (constitution as code) — architecture that isn't tested tends to get silently violated, as the `checkpoint()` finding above demonstrates.

**Official roadmap**
See `ECOSYSTEM_ARCHITECTURE.md` §7 for the full per-system MVP breakdown (Forge, Convergia, Hipocampo, Provider Engine, Reporter, Gateway, Memory/Índice/Context). Each line item is one independent MVP, never a macro prompt.

**Architectural impacts**
- `ECOSYSTEM_ARCHITECTURE.md` is the first artifact that lives only in this repository by design — avoids duplicating a long document in two places. The monorepo's `luna_context/LUNA_CONTEXT.md` holds only a pointer and condensed summary, not a full copy.
- No divergence found between this file and the monorepo's local copy as of this date — both independently converged on the same organ reclassification before this consolidation pass began.

## Fase 2 concluída — porte do Gateway para o luna-core, 2026-07-12 (ADR-004)

O porte do Gateway do monorepo `luna` para o `luna-core` e a migração de runtime (Python/FastAPI → Node/TypeScript) descritos no ADR-004 foram implementados, revisados e mergeados.

**Execução**
- `luna-core` PR #6 — porte do Gateway (Registry, Capability/Manifest, auditoria, política de autorização, packs GitHub e Filesystem, 17 capabilities) sem alteração de lógica; nascimento do Connector Hub (contratos + primeiro adapter, Supabase) como módulo irmão, não exposto por HTTP. Mergeado em `main`.
- `luna-frontend` PR #4 — `lib/forge/api-client.ts` passa a apontar as chamadas de Gateway (`listCapabilities`, `executeCapability`) para o `luna-core`, via `NEXT_PUBLIC_LUNA_GATEWAY_BASE_URL` nova, separada de `NEXT_PUBLIC_LUNA_API_BASE_URL`. Mergeado em `main`.
- Ambos os PRs foram validados antes do merge (typecheck, testes automatizados, e no caso do `luna-core`, um smoke test ao vivo local do `/api/gateway/execute` ponta a ponta) e só mergeados após configuração confirmada das variáveis de ambiente necessárias no Railway.

**Confirmado ao vivo em produção**
- `GET /api/gateway/capabilities` no `luna-core` (serviço `uvicorn-main`, projeto `honest-joy`) responde com as 17 capabilities registradas (Filesystem + GitHub).

**Achado registrado, não corrigido nesta etapa**
- `luna-guardian` (`strong-celebration`) tem um contrato de `/chat` incompatível com o que `luna-frontend` espera, e não implementa `/context` de forma alguma. Confirmado pelo dono do produto como serviço experimental, candidato à descontinuação — **não deve ser usado como referência de contrato daqui em diante**. `luna-frontend` continua apontando `NEXT_PUBLIC_LUNA_API_BASE_URL` para lá por ora (chat/contexto ficaram fora do escopo do ADR-004), mas isso é dívida registrada, não uma decisão de arquitetura definitiva.
- O terminal do Forge (`/forge`) segue bloqueado em produção — **por desenho, não é bug**: falta `FORGE_TERMINAL_TOKEN`/`NEXT_PUBLIC_FORGE_TERMINAL_TOKEN` configurados no ambiente `outstanding-learning`. O gate em si (rejeitar a conexão WebSocket sem token) é um achado de revisão de segurança já documentado em `DEPLOY.md` do `luna-frontend`, não uma regressão desta mudança.

**Próximo passo em aberto**
- Decidir o que fazer com `luna-guardian`'s `/chat`/`/context` (descontinuar de fato, ou redefinir contrato) não foi resolvido aqui — registrado para um MVP próprio, não uma continuação automática deste ADR.

## Expansão do Connector Hub — GitHub, Groq, DeepSeek, OpenRouter, resiliência, auth centralizada, 2026-07-12

Continuação do Connector Hub aberto no `luna-core` PR #6 (contrato + adapter Supabase). Esta rodada é execução do que ADR-002 já decidiu (gerenciar credenciais, adapters, retries, rate limiting para conectores externos incluindo GitHub e provedores de IA; regra de dependência Gateway→Connector Hub→Adapters, com "Gateway→Adapters" explicitamente listado como fluxo proibido) e do que ADR-004 já decidiu (Connector Hub nasce em TypeScript, no mesmo runtime) — **nenhuma decisão arquitetural nova foi necessária, por isso não há um ADR novo, só esta nota**, conforme combinado antes de começar.

**Execução**
- `luna-core` PR #7 — GitHub migrado do Gateway para o Connector Hub (lógica de fetch movida sem alteração, credenciais injetadas em vez de lidas de `process.env`, resiliência aplicada); Gateway passa a ser pura delegação a um `GithubConnector` injetado no composition root (`app.ts`), nunca construindo o adapter internamente — a regra "Gateway nunca importa um adapter do Hub diretamente" agora é verificada por `architecture-check.mjs`, não só documentada. Três novos conectores de IA (Groq, DeepSeek, OpenRouter — este último um meta-adapter, `model` obrigatório por chamada, roteando para múltiplos providers através de uma única credencial), preparados mas não consumidos pelo Gateway, mesmo estado em que o Supabase já estava. Camada de resiliência (retry com backoff exponencial + rate limiting básico em janela deslizante) aplicada aos cinco adapters. Auth centralizada em `connector_hub/auth/credentials.ts`, único lugar autorizado a ler `GITHUB_TOKEN`/`SUPABASE_URL`/`SUPABASE_KEY`/`GROQ_API_KEY`/`DEEPSEEK_API_KEY`/`OPENROUTER_API_KEY` — verificado repo-wide por `architecture-check.mjs`.
- `GROQ_API_KEY` reaproveitado do padrão já usado por `src/luna/adapters/groq.ts` no monorepo `luna` (mesmo endpoint, mesmo modelo default) — não uma convenção nova.
- Validado a cada adapter, não só no fim: typecheck, suíte de testes (69, de 32) e `architecture-check.mjs` verdes em cada etapa, conforme pedido. Dois smoke tests ao vivo locais (não em produção): o serviço sobe sem `GITHUB_TOKEN` configurado e lista as 17 capabilities (confirma que o boot tolerante funciona de verdade); uma chamada real `github.read_file` através do novo caminho Gateway→Hub chegou à API do GitHub e voltou com um erro estruturado real.
- **`luna-core` PR #7 está aberto, aguardando revisão — não mergeado, não deployado.** Diferente da nota de Fase 2 acima, nada aqui foi confirmado em produção ainda.

**Não resolvido nesta etapa (fora de escopo combinado)**
- Groq/DeepSeek/OpenRouter não estão ligados a nenhuma capability do Gateway nem expostos por HTTP — infraestrutura pronta, sem consumidor, mesmo estado documentado para o Supabase desde o PR #6.
- `FilesystemRestAdapter` não foi tocado — acesso a filesystem local não é "comunicação externa" sob a definição do ADR-002, então permanece adapter direto do Gateway.

**Reclassificação de `luna-core`** registrada acima (ver "Reclassificação — 2026-07-12").

## Guardian como Órgão Interno — DA-001, emenda ao ADR-002, 2026-07-12

Durante a implementação da capability `guardian.memory_index_search` (Gateway, `luna-core`, parte do MVP de arquitetura de memória — ver `luna-guardian` PR #2), a primeira versão roteou a comunicação Gateway→Guardian pelo Connector Hub, tratando o Guardian como mais um sistema externo (GitHub, Supabase, etc.). Isso seguiu o texto literal da seção "Restrições Arquiteturais" do ADR-002 (proibição de HTTP direto fora do Connector Hub, sem exceção declarada) — mas contradizia a própria seção "Arquitetura" do mesmo documento, que sempre desenhou o Guardian como filho direto do Gateway, irmão do Connector Hub, não um de seus conectores. A tensão foi sinalizada explicitamente na PR (`luna-core` #8) em vez de resolvida silenciosamente.

**Decisão dos arquitetos (DA-001):** o Guardian não é um sistema externo — é órgão interno do organismo, mesma categoria de qualquer futuro Hipocampo ou Reporter. A seção "Arquitetura" do ADR-002 estava certa; a seção "Restrições Arquiteturais" precisava de uma exceção explícita, agora formalizada como Emenda 001 no próprio `ADR-002-Gateway-ConnectorHub.md` (texto anterior preservado inline como histórico, não descartado).

**Execução**
- `luna-core` PR #8 (atualizada in-place, não recriada) — comunicação Guardian movida do Connector Hub para `src/gateway/organs/` (novo): `GuardianOrganAdapter` fala HTTP direto com o Guardian, autossuficiente (sem injeção de conector externo, mesmo padrão já usado por `FilesystemRestAdapter`); `connector_hub/` não tem mais nenhuma referência a Guardian. `scripts/architecture-check.mjs` passou a reconhecer `gateway/organs/` como exceção legítima à proibição de `fetch()` fora do Connector Hub, e como único leitor autorizado de `GUARDIAN_BASE_URL`.
- `ADR-002-Gateway-ConnectorHub.md` emendado com o texto proposto pelos arquitetos (seção "Emenda 001"), preservando o texto original da seção "Restrições Arquiteturais" como histórico em bloco de citação.
- `luna-guardian` PR #2 e `luna-frontend` PR #6 não precisaram de nenhum ajuste — a divergência era isolada na fronteira Gateway↔Guardian dentro do `luna-core`.

**Próximo passo em aberto**
- Se/quando Hipocampo ou Reporter existirem como órgãos deployados, seguem o mesmo padrão (`gateway/organs/`) por convenção já estabelecida — não é preciso uma nova ADR/DA só para replicar o padrão a um órgão adicional, a menos que surja alguma particularidade nova.
