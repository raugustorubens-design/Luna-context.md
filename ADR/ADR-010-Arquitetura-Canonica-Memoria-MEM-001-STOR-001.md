# ADR-010 — Arquitetura Canônica de Memória: context.txt v1.1, resolução MEM-001/STOR-001

Status: Aceito
Data: 2026-07-18
Decisor: Architect (Rubens), formalizado pelo Engineer a partir de DECISÃO ARQ-001

## Contexto

Duas especificações de memória coexistiam sem hierarquia clara: `memory_core.alg`
(v1.0.0, autodeclarada "OFFICIAL") e `context.txt` (v1.1, `BASE = memory_core_v2`,
artefato inexistente). Os símbolos colidiam entre as duas (`A` = Recurrence numa,
Action na outra; `τ` = threshold de conteúdo numa, de alinhamento na outra).
`ECOSYSTEM_ARCHITECTURE.md` referenciava um `ADR-003` inexistente na pasta `ADR/`.
Nenhuma das duas fórmulas está implementada hoje — o Hipocampo real é v1
determinística (filtra só vazio/duplicado) e o Memory Engine recupera só por
recência, sem semântica.

## Decisão

### 1. Fonte de verdade
`context.txt` v1.1 é a especificação canônica da arquitetura cognitiva.
`memory_core.alg` v1.0.0 é reclassificado como **histórico** (preservado, não
apagado, sem validade arquitetural vigente). Justificativa: a Fonte A modela
memória como pipeline de classificação-e-persistência; o Atrator AAAB (Art.
AAAB.3 da Constituição) redefine memória como reconstrução — há incompatibilidade
conceitual, e a arquitetura segue o Atrator.

```
CANÔNICO: context.txt v1.1 → Cognitive Engine → Hipocampo → Memory Engine
HISTÓRICO: memory_core.alg (apenas referência)
```

### 2. Definição oficial de memória
Substitui todas as definições anteriores:

> Memória é um processo de reconstrução de estado cognitivo a partir de
> conhecimento, identidade, contexto e traços persistidos.

Isso promove o Axioma IV do Art. AAAB.4 ("Memória é reconstrução") de hipótese
de pesquisa para conhecimento consolidado, conforme o próprio mecanismo previsto
no Art. AAAB.7 (promoção por ADR específico).

### 3. Símbolo `A`
`A` = **Action** (pertence ao Decision Engine, não ao Memory Engine).
Recorrência passa a ser `ρ` (rho). Nunca mais compartilhar símbolo entre os dois
conceitos.

### 4. Threshold `τ`
Dois thresholds nomeados, nunca um `τ` genérico:
- `τ_c` (Content Threshold) — decide persistir ou descartar.
- `τ_a` (Alignment Threshold) — autoriza ou bloqueia ações.

### 5. `memory_core_v2`
Considerado artefato inexistente — sem evidência documental. A referência
`BASE = memory_core_v2` em `context.txt` é inválida e deve ser corrigida.

### 6. `ADR-003`
Considerado inexistente até prova documental. Toda referência a ele deve ser
marcada como `Missing Reference`, não removida silenciosamente. Não possui
autoridade retroativa — se recuperado no futuro, entra como Documento
Candidato pelo processo normal de ADR.

### 7. CLASSIFY / `λ_tipo`
Deixa de ser etapa do pipeline. Vira **metadado** do objeto de memória:

```
Memory Object { embedding, trace, checkpoint, classification, metadata }
```

`λ_tipo` continua existindo, mas agora influencia retrieval, priorização e
compressão — não a decisão de persistência.

### 8. Fórmula canônica de consolidação (Memory Engine)

```
M(t+1) = σ[ α( M(t)(R + θρ) + IΔ + βO − μE ) ]
```

Onde `R` = relevância, `I` = impacto, `ρ` = recorrência, `O` = resultado
observado, `E` = entropia, `Δ` = novidade. **Action não entra nesta equação** —
pertence ao Decision Engine (`Decision(t) = H(t) + A(t)`, fora do escopo deste
ADR).

### 9. Hierarquia de decisão (regra permanente)

```
ATRATOR → CONSTITUIÇÃO → ADR → ARQUITETURA → ENGENHARIA → IMPLEMENTAÇÃO
```

Nunca a ordem inversa. Nenhuma linha de código de MEM-001/STOR-001 antes deste
ADR — condição já cumprida pela sequência desta decisão.

## Consequências

- `MEM-001` e `STOR-001` (P0, congelado por ARCH-001) têm agora especificação
  fechada — a implementação segue bloqueada pelo congelamento do P0 (retomar
  após Forge v0.1 em uso diário), mas a decisão arquitetural em si está
  resolvida e não é mais um bloqueador de especificação.
- `context.txt` precisa de correção de conteúdo (símbolos, thresholds, remoção
  da referência a `memory_core_v2`).
- `memory_core.alg` precisa de um cabeçalho marcando-o como histórico.
- `ECOSYSTEM_ARCHITECTURE.md` precisa marcar a referência a `ADR-003` como
  `Missing Reference`.
- `LUNA_CONSTITUTION.md` incorpora a hierarquia de decisão (item 9) como
  princípio permanente, e remove a marca "(hipótese de pesquisa)" do Axioma IV
  do Art. AAAB.4.
