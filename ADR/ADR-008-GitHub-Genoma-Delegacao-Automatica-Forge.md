# ADR-008 — GitHub como Genoma: Delegação Automática de ADRs via GitHub Actions, acionável sob demanda pelo Forge

Status: Aceito
Data: 2026-07-18
Decisor: Architect (Rubens)

## Contexto

O Roadmap (P2) tinha como pendência de decisão: "Escolher caminho de
delegação API+GitHub (GitHub Action com @claude / Claude Code headless em
cron / Gateway próprio via API)". Além disso, ADR-005/006/007 foram redigidas
em sessões de chat anteriores e nunca chegaram a ser aplicadas ao repositório
— o processo de handoff manual (Engineer redige → cola no Claude Code →
Claude Code commita) tem se mostrado um gargalo recorrente.

## Decisão

O caminho escolhido é **GitHub Actions**. GitHub é tratado como o genoma da
LUNA — registro permanente, versionado, e a única fonte de verdade. A
aplicação de ADRs (e outras atualizações de documentação GENESIS) passa a
ser executável via workflow do GitHub Actions, acionável sob demanda a
partir do Forge (painel de controle da LUNA), em vez de depender de um
handoff manual por chat a cada decisão.

## Observação técnica relevante

O `GITHUB_TOKEN` usado por um workflow do GitHub Actions tem escopo de
permissão próprio (definido no arquivo do workflow ou nas configurações do
repositório), **independente** da permissão do GitHub App instalado que hoje
bloqueia escrita (403) para as sessões de chat/MCP. Ou seja, esse caminho
tem potencial de contornar o bloqueio de permissão atual (ver INFRA-001) sem
depender do ajuste manual do GitHub App — a ser confirmado na implementação.

## Escopo desta decisão (o que fica definido agora)

- O caminho é GitHub Actions, não Claude Code headless em cron nem Gateway
  próprio via API.
- O gatilho é sob demanda a partir do Forge (não puramente automático por
  push/schedule, embora isso possa ser adicionado depois).
- Toda execução do workflow deve gravar sua própria entrada em
  `GENESIS/BUILDER.md`, com o run ID do Actions como evidência (equivalente
  à autoatestação "eu fiz" do Builder humano/Claude Code).

## Fora de escopo desta decisão (implementação, Builder)

- O arquivo `.yml` do workflow em si.
- O botão/integração no Forge que aciona o workflow (relacionado a
  FORGE-MVP-06, já no Roadmap).
- Autenticação e escopo exato do token usado pelo workflow.

Este ADR resolve a pendência de decisão do Roadmap P2 "Escolher caminho de
delegação"; a implementação correspondente deve ser adicionada como item
novo no Roadmap (sugestão: `GEN-002 — Workflow de aplicação automática de
ADRs via GitHub Actions, acionável pelo Forge`).
