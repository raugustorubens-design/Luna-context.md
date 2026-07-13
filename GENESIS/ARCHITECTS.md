# ARCHITECTS

Owner: Rubens + LUNA

Use this file for architectural decisions, hypotheses, atrators, and open design questions.

## What goes here
- New organs
- New systems
- Atrators
- Frameworks
- Architectural hypotheses
- Decisions pending review

## What does not go here
- Code
- Test logs
- Operational status
- Final implementation details

## Entry format
- ID
- Date
- Topic
- Decision or hypothesis
- Impact
- Next action

## Current workplan
- Keep the Memory System aligned with Guardian, Hipocampo, Memory Index, and Metacognition.
- Keep the Cognitive Immune System separate from memory and implementation concerns.
- Keep the Genesis workspace synchronized with permanent knowledge only after validation.

## Novo item — Convergia: decisão de migração pendente
- Real implementação do Convergia (pipeline, parsers, renderers, catálogo de
  13 documentos, Guardian-passthrough correto) está no monorepo luna, não no
  repo-interface luna-convergia
- Decisão pendente: portar convergia/ para luna-convergia seguindo o mesmo
  padrão do ADR-004 (Gateway → luna-core), em vez de reescrever do zero
- Frontend com mapeamento de campo/dados ("bolhas") ainda não localizado em
  nenhum repositório — a confirmar com GPT/LUNA
- Princípio confirmado nesta sessão: cada repositório-interface (luna-convergia,
  luna-guardian, etc.) deve se tornar seu próprio MVP, preparado para
  acoplamento — não um esqueleto fino
