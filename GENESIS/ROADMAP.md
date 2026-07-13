# ROADMAP

Sequência de prioridades consolidada em 2026-07-13, a partir de pendências identificadas em sessões anteriores e no estado atual dos repositórios.

## P1 — Pronto para concluir (Builder, sem decisão de Architects pendente)
- [ ] Configurar GROQ_API_KEY, DEEPSEEK_API_KEY, OPENROUTER_API_KEY, ANTHROPIC_API_KEY em luna-core/honest-joy (Railway) — ativa model routing do PR #9
- [ ] Corrigir tabela de classificação de sistemas em ECOSYSTEM_ARCHITECTURE.md e LUNA_CONTEXT.md (luna-core sai de "Legado/Experimental")

## P2 — Requer decisão de Architects antes de execução
- [ ] Escolher caminho de delegação API+GitHub (GitHub Action com @claude / Claude Code headless em cron / Gateway próprio via API)
- [ ] Decidir futuro de luna-guardian /chat e /context (deprecar vs. redefinir)
- [ ] Escolher 1 dos 4 candidatos a Skill (auditoria de compliance, geração de ADR/checkpoint, assistente Reporter, scaffolding de capability)

## P3 — Atividades de framework (atualizado 2026-07-13)
- [x] Auditoria real do luna-convergia (repo-interface): confirmado como
      esqueleto de 1 endpoint, não a fonte de verdade
- [x] Localizada implementação real do Convergia dentro do monorepo luna
      (apps/frontend/artifacts/api-server/src/convergia/) — pipeline completo,
      Guardian-passthrough já correto via knowledge-gate.ts
- [ ] Confirmar com GPT/LUNA o paradeiro do frontend de mapeamento de campo
      ("bolhas") — não encontrado em nenhum repositório auditado
- [ ] Decisão de Architects: portar convergia/ do monorepo luna para
      luna-convergia (padrão ADR-004), ou manter arquitetura atual
- [ ] Escrever ADR de migração do Convergia (Engineer), análogo ao ADR-004
- [ ] Implementar templates reais dos 13 tipos de documento corporativo —
      bloqueado por revisão de especialista (regulatoryStatus:
      pending_specialist_review), não é tarefa de Builder sozinho
- [ ] luna-convergia: acoplar frontend (uma vez localizado) ao pipeline real
- [ ] Engineer: especificar Fluxo A do Sistema Sensorial (Playwright vs. Computer Use API)
- [ ] Builder: implementar Fluxo A — acompanhamento de vídeos de curso organizados por tópico
- [ ] Builder: implementar Fluxo B — aplicação do conhecimento em sessões de projeto frontend
- [ ] Fluxo C (interrupção em tempo real): pendência sem prazo, fora deste ciclo

## P4 — Arquitetura maior, sem prazo definido
- [ ] Connector Hub: adapters além do Supabase
- [ ] Extrair Hipocampo do Guardian para módulo próprio
- [ ] Implementar Sistema Imunológico Cognitivo (CIS)
- [ ] Tornar o Reporter funcional além do scanner básico
