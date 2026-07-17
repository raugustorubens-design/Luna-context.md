# ROADMAP

Sequência de prioridades consolidada em 2026-07-13, agora incluindo a evolução do Genesis, o Framework Curator, o Sistema Metabólico e o Research Pipeline.

## P00 — Forge v0.1: ferramenta de uso diário (prioridade máxima)

- [ ] FORGE-MVP-01 — Interface web funcional
- [ ] FORGE-MVP-02 — Chat sequencial com seleção de agente + metadado de atribuição (ver GENESIS/FORGE.md)
- [ ] FORGE-MVP-03 — Projetos com contexto próprio (LUNA, RENASCER, SMX, CURSO EMPILHADEIRA)
- [ ] FORGE-MVP-04 — Storage Contract: Forge → Guardian → Storage Contract → Supabase Adapter
- [ ] FORGE-MVP-05 — Execution Metadata em toda memória salva (ver GENESIS/FORGE.md)
- [ ] FORGE-MVP-06 — Botões GitHub (commit/push/pull/branch) sob credencial de Builder
- [ ] FORGE-MVP-07 — Reporter manual: botão "Analisar Projeto"
- [ ] FORGE-MVP-08 — Workspace v0.1: integração com Claude Code (não reimplementação de IDE)

## FORGE-WORKSPACE-001 — Workspace nativo equivalente a Cursor + VS Code (pós-v0.1, sem prazo)

## P0 — Continuidade Cognitiva Distribuída (CONGELADO, ver ARCH-001 — retomar após Forge v0.1 em uso diário)

- [ ] MEM-001 — Especificar a Operational Memory Layer
- [ ] STOR-001 — Redesenhar storage.query/storage.insert do Gateway mediado pelo Hipocampo
- [ ] GEN-001 — Adotar IDs estáveis por domínio em todo item de Roadmap/Framework
- [ ] REP-001 — Redefinir escopo do Reporter (propagação por evidência)
- [ ] INFRA-001 — Corrigir permissão do GitHub App

## P1 — Pronto para concluir (Builder, sem decisão de Architects pendente)
- [x] ~~Configurar GROQ_API_KEY... — ativa model routing do PR #9~~ — correção (2026-07-13, ver ENG-005/BLD-001): o PR #9 só trazia infraestrutura sem consumidor; não havia capability para as env vars "ativarem" ainda. Implementadas agora: `model.chat`, `model.chat_deep`, `storage.query`, `storage.insert`.
- [ ] Aplicar o patch de `model.chat`/`model.chat_deep`/`storage.query`/`storage.insert` no luna-core (bloqueado: GitHub App conectado com "Contents"/"Pull requests" somente leitura nesta sessão — ver ENG-005) e então configurar GROQ_API_KEY, DEEPSEEK_API_KEY, OPENROUTER_API_KEY, ANTHROPIC_API_KEY, SUPABASE_URL, SUPABASE_KEY em luna-core/honest-joy (Railway) — sem essas credenciais as 4 capabilities continuam ausentes de `/api/gateway/capabilities` (design condicional, não bug)
- [ ] Ajustar permissão do GitHub App (Contents + Pull requests: Read and write) para viabilizar commits e fechamento de PR direto em sessões futuras
- [ ] Fechar PRs #3, #4 e #5 no luna-core (obsoletas, versão Python pré-ADR-004) — bloqueado pelo mesmo motivo de permissão
- [ ] Corrigir tabela de classificação de sistemas em ECOSYSTEM_ARCHITECTURE.md e LUNA_CONTEXT.md (luna-core sai de "Legado/Experimental")

## P2 — Requer decisão de Architects antes de execução
- [ ] Escolher caminho de delegação API+GitHub (GitHub Action com @claude / Claude Code headless em cron / Gateway próprio via API)
- [ ] Decidir futuro de luna-guardian /chat e /context (deprecar vs. redefinir)
- [ ] Escolher 1 dos 4 candidatos a Skill (auditoria de compliance, geração de ADR/checkpoint, assistente Reporter, scaffolding de capability)
- [ ] Formalizar a fronteira entre repo-interface e MVP acoplável: cada repositório é uma interface evolutiva, não o órgão em si
- [ ] Consolidar a decisão arquitetural sobre Convergia: portar a implementação real do monorepo luna para luna-convergia ou manter a arquitetura atual

## P3 — Genesis e coordenação do organismo
- [ ] Criar/atualizar os arquivos do Genesis para coordenação em tempo real: STATUS.md, HISTORY.md e TASKS.md
- [ ] Manter COORDINATION.md como barramento de memória de trabalho, sem virar memória permanente
- [ ] Fazer o Reporter atuar como gestor operacional: comparar proposto × executado e calcular percentual de conclusão
- [ ] Criar um Framework Curator para transformar aprendizados consolidados em Frameworks reutilizáveis

## P4 — Atividades de framework
- [ ] Confirmar com GPT/LUNA o paradeiro do frontend de mapeamento de campo ("bolhas") — não encontrado em nenhum repositório auditado
- [ ] Decisão de Architects: portar convergia/ do monorepo luna para luna-convergia (padrão ADR-004), ou manter arquitetura atual
- [ ] Escrever ADR de migração do Convergia (Engineer), análogo ao ADR-004
- [ ] Implementar templates reais dos 13 tipos de documento corporativo — bloqueado por revisão de especialista (regulatoryStatus: pending_specialist_review), não é tarefa de Builder sozinho
- [ ] luna-convergia: acoplar frontend (uma vez localizado) ao pipeline real
- [ ] Engineer: especificar Fluxo A do Sistema Sensorial (Playwright vs. Computer Use API)
- [ ] Builder: implementar Fluxo A — acompanhamento de vídeos de curso organizados por tópico
- [ ] Builder: implementar Fluxo B — aplicação do conhecimento em sessões de projeto frontend
- [ ] Fluxo C (interrupção em tempo real): pendência sem prazo, fora deste ciclo

## P5 — Sistema de crescimento e sustentabilidade
- [ ] Definir Atrator AAAB — Sustentabilidade
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
