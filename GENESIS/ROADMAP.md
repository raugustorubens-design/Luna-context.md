# ROADMAP

Sequência de prioridades consolidada em 2026-07-13, agora incluindo a evolução do Genesis, o Framework Curator, o Sistema Metabólico e o Research Pipeline.

## P00 — Forge v0.1: ferramenta de uso diário (prioridade máxima)

- [x] FORGE-MVP-01 — Validated Existing Capability (auditado, não implementado — ver GENESIS/BUILDER.md)
- [x] FORGE-MVP-02 — Chat sequencial com seleção de agente + metadado de atribuição (ver GENESIS/FORGE.md) — `luna-frontend` PR #7 (commit `f358752`), mergeada em `main` em 2026-07-17.
- [x] FORGE-MVP-03 — Projetos com contexto próprio (LUNA, RENASCER, SMX, CURSO EMPILHADEIRA) — `luna-frontend` PR #7 (commit `d7fddb5`), mergeada em `main` em 2026-07-17.
- [x] FORGE-MVP-04 — Storage Contract: Forge → Guardian → Storage Contract → Supabase Adapter — `luna-frontend` PR #7 (commit `322bba0`), mergeada em `main` em 2026-07-17.
- [x] FORGE-MVP-05 — Execution Metadata em toda memória salva (ver GENESIS/FORGE.md) — `luna-frontend` PR #7 (commit `5e0c57a`), mergeada em `main` em 2026-07-17.
- [x] FORGE-MVP-06 — Botões GitHub (commit/push/pull/branch) sob credencial de Builder — `luna-frontend` PR #7 (commit `1df218d`), mergeada em `main` em 2026-07-17.
- [x] FORGE-MVP-07 — Reporter manual: botão "Analisar Projeto" — `luna-frontend` PR #7 (commit `03dddc4`), mergeada em `main` em 2026-07-17.
- [x] FORGE-MVP-08A — Claude Activity Panel (nó "AI Coding" do Workspace, integração honesta sem PTY — ver GENESIS/FORGE.md) — já satisfeito pelo commit `04d84fe` (mesma PR #7, mergeada em 2026-07-17); `components/forge/claude-code-panel.tsx` lê `GENESIS/BUILDER.md` via `github.read_file`, sem sessão embutida, e está de fato ligado como aba no `forge-layout.tsx`, não órfão. Confirmado 2026-07-19: nenhuma implementação nova foi necessária, a renomeação de "08" para "08A" no Roadmap (2026-07-17) já tinha sido só reclassificação do item, não indicava código faltante.

## FORGE-WORKSPACE-001 — Workspace nativo equivalente a Cursor + VS Code (pós-v0.1, sem prazo)

## P0 — Continuidade Cognitiva Distribuída (CONGELADO, ver ARCH-001 — retomar após Forge v0.1 em uso diário)

- [ ] MEM-001 — Especificar a Operational Memory Layer — **especificação
  decidida via ADR-010 (2026-07-18)**; implementação segue bloqueada pelo
  congelamento do P0 (ARCH-001), não é mais bloqueio de decisão.
- [ ] STOR-001 — Redesenhar storage.query/storage.insert do Gateway mediado
  pelo Hipocampo — **especificação decidida via ADR-010 (2026-07-18)**;
  implementação segue bloqueada pelo congelamento do P0 (ARCH-001), não é
  mais bloqueio de decisão.
- [ ] GEN-001 — Adotar IDs estáveis por domínio em todo item de Roadmap/Framework
- [ ] REP-001 — Redefinir escopo do Reporter (propagação por evidência)
- [x] ~~INFRA-001 — Corrigir permissão do GitHub App~~ — correção (2026-07-18, ver BLD-003): confirmado resolvido (ver item correspondente em P1); registrado aqui só por consistência com o ID, não é trabalho novo sob o congelamento do P0.

## P1 — Pronto para concluir (Builder, sem decisão de Architects pendente)
- [x] ~~Configurar GROQ_API_KEY... — ativa model routing do PR #9~~ — correção (2026-07-13, ver ENG-005/BLD-001): o PR #9 só trazia infraestrutura sem consumidor; não havia capability para as env vars "ativarem" ainda. Implementadas agora: `model.chat`, `model.chat_deep`, `storage.query`, `storage.insert`.
- [x] ~~Aplicar o patch de `model.chat`/`model.chat_deep`/`storage.query`/`storage.insert` no luna-core (bloqueado: GitHub App conectado com "Contents"/"Pull requests" somente leitura nesta sessão — ver ENG-005)~~ — correção (2026-07-18, ver BLD-003): aplicado apenas `model.chat`/`model.chat_deep`, via `luna-core` PR #10 (mergeada em 2026-07-15). `storage.query`/`storage.insert` foram deliberadamente deixadas de fora — violam o Princípio 4 da Constitution (persistência deve rotear por Guardian/Hipocampo, nunca Gateway→Supabase direto); permanecem bloqueadas até o Architect decidir o redesenho (ver STOR-001, ENG-011). Configurar GROQ_API_KEY, DEEPSEEK_API_KEY, OPENROUTER_API_KEY, ANTHROPIC_API_KEY em luna-core/honest-joy (Railway) segue como pendência separada, fora do escopo desta sessão (ação de infraestrutura, sem acesso ao Railway) — sem essas credenciais `model.chat`/`model.chat_deep` continuam ausentes de `/api/gateway/capabilities` (design condicional, não bug).
- [x] ~~Ajustar permissão do GitHub App (Contents + Pull requests: Read and write) para viabilizar commits e fechamento de PR direto em sessões futuras~~ — correção (2026-07-18, ver BLD-003): confirmado resolvido — esta sessão comentou com sucesso em `luna-core` PR #3/#4/#5 (sem 403), ver evidência abaixo.
- [x] ~~Fechar PRs #3, #4 e #5 no luna-core (obsoletas, versão Python pré-ADR-004) — bloqueado pelo mesmo motivo de permissão~~ — correção (2026-07-18, ver BLD-003): as 3 PRs já estavam fechadas por Rubens diretamente em 2026-07-14 (comentário "arquivo obsoleto" em cada uma); esta sessão adicionou comentário de rastreabilidade referenciando ADR-004 em cada uma (2026-07-18).
- [x] ~~Corrigir tabela de classificação de sistemas em ECOSYSTEM_ARCHITECTURE.md e LUNA_CONTEXT.md (luna-core sai de "Legado/Experimental")~~ — correção (2026-07-18, ver BLD-003): já corrigido em 2026-07-12 (ver nota "Reclassificação" em ambos os documentos) — luna-core já aparece como "Infraestrutura, Órgão" na tabela de classificação atual de LUNA_CONTEXT.md §Sistemas, não mais em "Legado/Experimental"; a linha antiga é preservada explicitamente como snapshot histórico, não apagada.
- [ ] GEN-002 — Workflow de aplicação automática de ADRs via GitHub Actions, acionável pelo Forge (ver ADR-008). Movido de P2 para P1 em 2026-07-18: a decisão de caminho já foi tomada (ADR-008), o que resta é implementação, sem decisão de Architect pendente.

## P2 — Requer decisão de Architects antes de execução
- [x] ~~Escolher caminho de delegação API+GitHub (GitHub Action com @claude / Claude Code headless em cron / Gateway próprio via API)~~ — resolvido por ADR-008 (2026-07-18, ver `ADR/ADR-008-GitHub-Genoma-Delegacao-Automatica-Forge.md`): caminho escolhido é GitHub Actions, acionável sob demanda pelo Forge. Implementação passa a ser GEN-002 em P1.
- [x] ~~Decidir futuro de luna-guardian /chat e /context (deprecar vs. redefinir)~~ — resolvido por ADR-012 (2026-07-19, ver `ADR/ADR-012-Consolidacao-Backend-luna-core-Interface-Convergia.md`): deprecadas e removidas de `luna-guardian` (commit `28c1c6e`) — o backend único de chat/contexto passa a ser `luna-core`, portado do monorepo `luna`.
- [ ] Escolher 1 dos 4 candidatos a Skill (auditoria de compliance, geração de ADR/checkpoint, assistente Reporter, scaffolding de capability)
- [ ] Formalizar a fronteira entre repo-interface e MVP acoplável: cada repositório é uma interface evolutiva, não o órgão em si
- [x] ~~Consolidar a decisão arquitetural sobre Convergia: portar a implementação real do monorepo luna para luna-convergia ou manter a arquitetura atual~~ — resolvido por ADR-012 (2026-07-19): nem um nem outro exatamente — o Convergia completo foi portado para `luna-core` (não para `luna-convergia`, que segue como esqueleto de 1 endpoint, órfão), com interface de usuário em `luna-frontend`. Decisão formal registrada no ADR, não a mesma alternativa binária que este item original enumerava.

## P3 — Genesis e coordenação do organismo
- [ ] Criar/atualizar os arquivos do Genesis para coordenação em tempo real: STATUS.md, HISTORY.md e TASKS.md
- [ ] Manter COORDINATION.md como barramento de memória de trabalho, sem virar memória permanente
- [ ] Fazer o Reporter atuar como gestor operacional: comparar proposto × executado e calcular percentual de conclusão
- [ ] Criar um Framework Curator para transformar aprendizados consolidados em Frameworks reutilizáveis

## P4 — Atividades de framework
- [ ] Confirmar com GPT/LUNA o paradeiro do frontend de mapeamento de campo ("bolhas") — não encontrado em nenhum repositório auditado
- [x] ~~Decisão de Architects: portar convergia/ do monorepo luna para luna-convergia (padrão ADR-004), ou manter arquitetura atual~~ — resolvido por ADR-012 (2026-07-19): portado para `luna-core`, não `luna-convergia` — ver nota equivalente em P2.
- [x] ~~Escrever ADR de migração do Convergia (Engineer), análogo ao ADR-004~~ — é o próprio ADR-012 (2026-07-19).
- [ ] Implementar templates reais dos 13 tipos de documento corporativo — deixa de ser "bloqueado por revisão de especialista": ADR-012 define que o conteúdo passa a ser alimentado via `/api/convergia/training` pelo especialista diretamente (mecanismo já portado), não mais uma revisão externa a esperar.
- [x] ~~Convergia: renderer PPTX marcado como "parcialmente feito" em ECOSYSTEM_ARCHITECTURE.md~~ — correção (2026-07-19): a doc estava desatualizada, não o código. O renderer já era completo (título + tabela paginada, 18 linhas/slide) antes desta entrada; faltava rigor de teste (só buffer não-vazio). Endurecido em `luna-core` commit `fe5b354` (branch `claude/pptx-renderer-test-rigor`, PR aberto para `main`): teste abre o `.pptx` como zip real, lê XML dos slides, confere título/cabeçalho/valores com dados SSMA/ASO, mais teste de paginação. Ver ECOSYSTEM_ARCHITECTURE.md §Convergia para o texto completo. Templates reais dos 13 tipos de documento (item acima) seguem como pendência separada, não afetada por esta correção.
- [x] ~~ADR-012 Decisão 2: Interface de Convergia em `luna-frontend`~~ — concluído (2026-07-19, ver `GENESIS/BUILDER.md`): nova área "Convergia" no Forge (`components/forge/convergia-panel.tsx`), mesmo padrão visual/estrutural de `components/forge/` (Tabs, ScrollArea, Button), com o fluxo Catálogo & Upload → Transformação → Conhecimento consumindo `/api/convergia/{catalog,templates,parse,transform,training}` em `luna-core` — `luna-frontend` commit `673b29c` (`main`). Correção adicional no mesmo commit: `sendChatMessage`/`fetchOrganismContext` ainda apontavam para a base antiga de `luna-guardian` (rotas removidas pelo porte da Decisão 1) — atualizados para `LUNA_GATEWAY_BASE_URL` (`luna-core`), junto de `.env.example`/`DEPLOY.md`.
- [ ] luna-convergia: acoplar frontend (uma vez localizado) ao pipeline real
- [ ] Engineer: especificar Fluxo A do Sistema Sensorial (Playwright vs. Computer Use API)
- [ ] Builder: implementar Fluxo A — acompanhamento de vídeos de curso organizados por tópico
- [ ] Builder: implementar Fluxo B — aplicação do conhecimento em sessões de projeto frontend
- [ ] Fluxo C (interrupção em tempo real): pendência sem prazo, fora deste ciclo

## P5 — Sistema de crescimento e sustentabilidade
- [ ] Definir Atrator AAAC — Sustentabilidade (renomeado de AAAB em 2026-07-19: AAAB já é o Atrator Cognitivo, ver ADR-009/LUNA_CONSTITUTION.md)
- [ ] Definir indicadores econômicos por MVP
- [ ] Definir telemetria econômica para o Reporter
- [ ] Conectar valor econômico ao Atrator Evolução
- [ ] Modelar o Sistema Metabólico da LUNA
- [ ] Criar o Research Pipeline com n8n e IA open source
- [ ] Padronizar fontes contínuas de pesquisa e classificação automática de conteúdo
- [ ] Enviar conhecimento validado ao Guardian apenas após revisão do Reporter
- [ ] Garantir que cada MVP gere valor mensurável sempre que possível

## P6 — Arquitetura maior, sem prazo definido
- [ ] Connector Hub: adapters além do Supabase
- [ ] Extrair Hipocampo do Guardian para módulo próprio
- [ ] Implementar Sistema Imunológico Cognitivo (CIS)
- [ ] Tornar o Reporter funcional além do scanner básico
