# ADR-011 — Emenda ao ADR-010: resolução das colisões de símbolo `M(t)` e `A`

Status: Aceito
Data: 2026-07-19
Decisor: Architect (Rubens)

## Contexto

Ao formalizar o ADR-010, uma fórmula de Decision Engine (`Decision(t) = H(t) +
A(t)`) foi inventada sem verificação contra `context.txt` — corrigida em
2026-07-19 (ver `GENESIS/BUILDER.md`, entrada "Correção: remove fórmula
inventada de Decision Engine"). Essa correção expôs duas colisões de símbolo
reais, nenhuma delas coberta pelo ADR-010:

1. **`M(t)` tem dois significados incompatíveis** no mesmo arquivo:
   - Seção Cognitive Model: `M(t)` = *machine state* (`Decision(t) = H(t) +
     M(t)`).
   - Seção Alignment (pré-existente, nunca tocada pelo ADR-010): `M(t)` no
     mesmo papel de machine state (`A(t) = 1 − d(H(t), M(t))`) — terceira
     ocorrência encontrada só ao auditar o arquivo inteiro em busca de
     `M(t)`, não pelas duas linhas originalmente citadas.
   - Seção Memory Architecture / Memory Update: `M(t)` = *long-term memory*,
     o mesmo símbolo que a fórmula canônica de consolidação do ADR-010 §8
     atualiza.

2. **`A` já estava reservado para *Alignment*** na seção Alignment
   (`A(t) = 1 − d(H(t), M(t))`, pré-existente, mais antiga que a decisão de
   hoje). O ADR-010 §3 decidiu `A = Action` sem visibilidade dessa seção —
   os dois usos de `A` conflitam.

## Decisão

### 1. `M(t)` fica reservado para memória
`M(t)` = **long-term memory** (Memory Engine), sem exceção — é o uso mais
central do arquivo: fórmula canônica de consolidação (ADR-010 §8),
referenciado em Memory Architecture, Memory Update, Compression e
Continuity/Checkpoint.

*Machine state* (Decision Engine) recebe um símbolo novo, sem parentesco
visual com símbolos já em uso: **`X(t)`**. Rejeitado `S_m(t)` por colidir
visualmente com `S(t)` (short-term context, já em uso na seção Memory
Architecture) — mesmo critério usado no item 2 abaixo.

Isso corrige as 3 ocorrências de `M(t)`-como-machine-state em `context.txt`
(Cognitive Model: definição e fórmula; Alignment: fórmula), preservando as
2 ocorrências de `M(t)`-como-memória (Memory Architecture, Memory Update)
sem nenhuma mudança.

### 2. `A(t)` fica reservado para Alignment
A seção Alignment é anterior à decisão de hoje e é o próprio gate de
execução do organismo (`if A(t) < τ_a → do not execute`) — não cede o
símbolo. **Supera e substitui o ADR-010 §3** (`A = Action`), que foi
decidido sem visibilidade da colisão com Alignment.

*Action* (Decision Engine) recebe **`γ(t)`** (gamma) — símbolo novo, sem
colisão com nenhum símbolo já em uso em `context.txt` (`α, η, μ, θ, β, κ,
λ, σ, ρ, Δ, X` já ocupados; `Ac(t)` foi rejeitado por colidir visualmente
com `A(t)`, mesmo critério do item 1).

### 3. Tabela de símbolos consolidada (Decision + Memory Engine)

| Símbolo | Significado | Engine |
|---|---|---|
| `H(t)` | human intention | Decision |
| `X(t)` | machine state | Decision |
| `A(t)` | alignment score | Decision (gate de execução) |
| `γ(t)` | action | Decision |
| `M(t)` | long-term memory | Memory |
| `ρ(t)` | recurrence | Memory |
| `τ_c` | Content Threshold | Memory |
| `τ_a` | Alignment Threshold | Decision |

## Consequências

- `context.txt` § Cognitive Model: `M(t) → machine state` vira `X(t) →
  machine state`; `Decision(t) = H(t) + M(t)` vira `Decision(t) = H(t) +
  X(t)`.
- `context.txt` § Alignment: `A(t) = 1 − d(H(t), M(t))` vira `A(t) = 1 −
  d(H(t), X(t))`.
- `context.txt` § Memory Update: comentário sobre Action atualizado para
  citar `γ(t)` como o símbolo real, em vez de só dizer "Action" em prosa.
- `ADR-010` §3 permanece como registro histórico do que foi decidido em
  2026-07-18, com nota apontando para esta emenda — não editado
  silenciosamente (Princípio 8 da Constituição).
- Nenhuma implementação de código afetada — MEM-001/STOR-001 continuam
  bloqueados por ARCH-001, como já registrado no ADR-010.
