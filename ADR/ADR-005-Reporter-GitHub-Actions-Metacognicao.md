# ADR-005 — Reporter via GitHub Actions + Princípios de Metacognição

Status: Aceito (redigido em sessão anterior; redraft aplicado em 2026-07-18
por ausência do texto original — ver nota de reconstrução no pacote de
aplicação)

## Contexto

O Reporter precisa observar o estado do organismo de forma independente de
uma sessão de chat ativa, com cadência própria.

## Decisão

O Reporter roda como GitHub Action (agendada e/ou sob demanda via Forge, ver
ADR-008), gerando relatórios versionados no próprio repositório.

## Princípios de metacognição

- **Autoconsciência estrutural**: comparar o que está documentado (GENESIS)
  com o que está de fato implementado.
- **Consciência situacional**: estado corrente do organismo (bugs, pendências,
  progresso do Roadmap).

Essas duas funções são complementares, não concorrentes.
