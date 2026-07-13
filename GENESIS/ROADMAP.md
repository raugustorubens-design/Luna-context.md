# ROADMAP

Sequência de prioridades consolidada em 2026-07-13, agora incluindo a evolução do Genesis, o Framework Curator, o Sistema Metabólico e o Research Pipeline.

## P1 — Pronto para concluir (Builder, sem decisão de Architects pendente)
- [ ] Configurar GROQ_API_KEY, DEEPSEEK_API_KEY, OPENROUTER_API_KEY, ANTHROPIC_API_KEY em luna-core/honest-joy (Railway) — ativa model routing do PR #9
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
