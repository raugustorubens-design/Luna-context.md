# Luna-reporter (scanner Python) — Relatório

Repositórios escaneados: 7

## Atividade recente — `raugustorubens-design/luna-core`

Commits analisados: 30

### Resumo interpretativo

Existem 30 commits listados, indicando uma atividade intensa no repositório 'raugustorubens-design/luna-core'. As principais mudanças observadas incluem melhorias na capacidade de gateway, expansão do connector hub, implementação de recursos de modelagem de chat e correções de bugs em vários componentes, como o Groq e o Context Hub. O padrão de atividade parece ser contínuo, com contribuições frequentes de autores como RUBENS RAMOS RODRIGUES JR e Claude, sugerindo um desenvolvimento colaborativo e dinâmico. Além disso, as mensagens de commit apontam para uma abordagem sistemática de melhoria e expansão das funcionalidades do projeto. A presença de pull requests e merges também reforça a ideia de uma equipe ativa, trabalhando em diferentes aspectos do repositório.

### Commits

- `2193f01` (2026-07-22T16:19:56Z) **RUBENS RAMOS RODRIGUES JR**: Merge pull request #16 from raugustorubens-design/claude/chat-friendly-fallback-and-dev-provider-override
- `94bed95` (2026-07-22T16:17:55Z) **RUBENS RAMOS RODRIGUES JR**: Merge pull request #17 from raugustorubens-design/claude/port-capability-packs-from-luna-pr15
- `21ac8d1` (2026-07-22T16:15:05Z) **Claude**: feat(gateway): port Railway and Reporter capability packs from luna PR #15
- `06dbc7b` (2026-07-22T13:54:39Z) **Claude**: chat: never leak raw provider errors, gate provider override behind dev header
- `4643ab8` (2026-07-21T01:48:02Z) **RUBENS RAMOS RODRIGUES JR**: Merge pull request #15 from raugustorubens-design/builder/29791773565
- `f250f2f` (2026-07-21T00:57:44Z) **luna-builder[bot]**: Builder (Claude Code headless, run 29791773565): pending-packages/2026-07-21-teste-gen-002-fase1.md
- `f1138b8` (2026-07-19T23:19:37Z) **RUBENS RAMOS RODRIGUES JR**: Merge pull request #14 from raugustorubens-design/claude/groq-model-fix
- `1142d86` (2026-07-19T22:46:56Z) **Claude**: fix(groq): replace deprecated default model "llama-3.1-8b-instant" with "openai/gpt-oss-120b"
- `211f749` (2026-07-19T22:25:33Z) **RUBENS RAMOS RODRIGUES JR**: Merge pull request #13 from raugustorubens-design/claude/reporter-analyze-project
- `971ddd3` (2026-07-19T22:25:27Z) **RUBENS RAMOS RODRIGUES JR**: Merge pull request #12 from raugustorubens-design/claude/context-hub-regex-fix
- `0fb0a91` (2026-07-19T22:25:22Z) **RUBENS RAMOS RODRIGUES JR**: Merge pull request #11 from raugustorubens-design/claude/pptx-renderer-test-rigor
- `248b163` (2026-07-19T16:28:24Z) **Claude**: fix(chat): wrap runCognitiveEngine call in try/catch
- `2e32c47` (2026-07-18T18:16:04Z) **Claude**: feat(gateway): implement reporter.analyze_project (FORGE-MVP-07 v1)
- `19ea30b` (2026-07-18T18:10:54Z) **Claude**: fix(context-hub): rewrite extraction regex for currentMvp/inferences/activeSystems/activeRepositories
- `fe5b354` (2026-07-18T15:32:43Z) **Claude**: test(convergia): harden pptx renderer test to open the real zip and read slide XML
- `ac38aee` (2026-07-18T10:21:38Z) **Claude**: ADR-012: porta Cognitive Engine + Convergia + rotas chat/context/convergia
- `069c219` (2026-07-15T08:22:38Z) **RUBENS RAMOS RODRIGUES JR**: Merge pull request #10 from raugustorubens-design/feat/model-chat-capabilities
- `047a407` (2026-07-15T08:19:17Z) **Claude**: Gateway: model.chat/model.chat_deep - primeiras capabilities do Model Router (PR #9)
- `f0a7e0a` (2026-07-12T14:30:36Z) **RUBENS RAMOS RODRIGUES JR**: Merge pull request #9 from raugustorubens-design/feat/model-routing
- `6de4549` (2026-07-12T13:48:50Z) **Claude**: feat(gateway): add automatic model routing (cost-first, escalate to Claude)
- `ef2cb5d` (2026-07-12T11:52:56Z) **RUBENS RAMOS RODRIGUES JR**: Merge pull request #8 from raugustorubens-design/feat/gateway-guardian-memory-index
- `1c3be6c` (2026-07-12T11:44:06Z) **Claude**: refactor(gateway): treat Guardian as an internal organ, not a Connector Hub adapter
- `5dcbc22` (2026-07-12T11:25:06Z) **Claude**: feat(gateway): add guardian.memory_index_search capability
- `b916f12` (2026-07-12T05:39:59Z) **RUBENS RAMOS RODRIGUES JR**: Merge pull request #7 from raugustorubens-design/feat/connector-hub-expansion
- `9656625` (2026-07-12T04:49:35Z) **Claude**: fix(readme): correct env var boot requirements - Supabase is dormant too, not just Groq/DeepSeek/OpenRouter
- `291bb03` (2026-07-12T04:48:53Z) **Claude**: refactor(connector-hub): reorganize auth/ by category, reserve generative-media
- `2dfdc7d` (2026-07-12T04:10:08Z) **Claude**: feat(connector-hub): migrate GitHub adapter, add 3 AI connectors, resilience + centralized auth
- `ae8da32` (2026-07-12T00:26:53Z) **RUBENS RAMOS RODRIGUES JR**: Port Gateway from luna monorepo, migrate runtime to Node/TypeScript, add Connector Hub (#6)
- `7f09bb5` (2026-04-16T09:13:36Z) **RUBENS RAMOS RODRIGUES JR**: force deploy
- `da92564` (2026-04-14T00:28:54Z) **RUBENS RAMOS RODRIGUES JR**: Fix newline at end of Procfile

### PRs em aberto

Total: 0 (0 marcada(s) como risco de segurança)

