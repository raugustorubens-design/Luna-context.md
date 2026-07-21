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

## ID: ARCH-001
Data: 2026-07-16
Tópico: Congelamento confirmado — Forge v0.1 é a única prioridade de execução

Decisão: Architect confirma o congelamento de Hipocampo, Fórmula de memória,
Reporter automático e Genome. Nenhuma proposta de arquitetura nova entra na
fila de implementação até o Forge v0.1 estar em uso diário. Meta-Cognitive
Memory (camada de memória sobre qual agente/estratégia funciona melhor por
tipo de problema) é registrada como Research Hypothesis em
GENESIS/RESEARCH/meta-cognitive-memory.md — não implementação.

Impacto: qualquer item de Roadmap fora do escopo Forge v0.1 (incluindo
MEM-001/STOR-001 do P0 "Continuidade Cognitiva Distribuída", já sinalizados
como congelados) permanece bloqueado até o critério de uso diário do Forge
v0.1 ser atingido.

Próxima ação: nenhuma implementação de arquitetura nova até então; Builder
persiste este registro e o stub de Research Hypothesis.
Status: decidido.
