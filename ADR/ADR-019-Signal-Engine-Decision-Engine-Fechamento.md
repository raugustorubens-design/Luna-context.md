# ADR-019 — Fechamento das Trilhas 1 e 2 (Memória e Decision Engine)

Status: Proposto — documenta código já mergeado (`luna-core` PR #19,
2026-07-23), aguardando ratificação formal do Architect como registro
histórico
Data: 2026-07-22/23
Proveniência: pesquisa (GPT-pesquisa), mapeamento (GPT-histórico),
scaffold (Claude Sonnet 5 #2), crítica (Gemini ×2), fechamento e
implementação real (Claude, sessão de 2026-07-23)

## Nota de honestidade sobre este documento

O pacote original que deu origem a este ADR descrevia uma arquitetura
alvo — `MemoryObject` com `embedding`/`entities`/`topics`/`confidence`,
`relevance` como soma ponderada de cinco componentes
(`0.35×SemanticSimilarity + ...`), um `Consolidation Engine` e um
`Signal Engine` como módulos totalmente separados do Hipocampo. **Isso
não é o que foi efetivamente implementado e mergeado.** Este ADR
documenta o código real (PR #19), não o alvo — a arquitetura alvo fica
registrada na Parte 1 como direção, explicitamente marcada como não
implementada onde diverge.

## Parte 0 — Nova capacidade registrada (idea do Architect)

Roadmap novo, P0 (junto de MEM-001/STOR-001, mesma trilha):

```markdown
- [ ] MEM-002 — LUNA compacta o próprio contexto de conversa usando a
  mesma fórmula de consolidação de memória (Memory Signals/
  Consolidation Engine, ver Parte 1), preservando um arquivo temporário
  completo (não compactado) para consulta/auditoria sob demanda — mesmo
  padrão observado no mecanismo de compactação do próprio Claude
  (resumo estruturado + transcript de backup acessível). Depende de o
  Signal Engine já calcular sinais reais sobre um objeto genérico
  (`ConversationObject` em vez de `MemoryObject`) — não implementado
  ainda, ver Parte 3.
```

Não implementado nesta rodada — só registrado.

## Parte 1 — Trilha 1 (Memória): o que foi realmente implementado

### Estrutura real (`luna-core`, PR #19)

```
MemoryObject { key?, content, createdAt? }
        ↓
DefaultSignalCalculator implements SignalCalculator (calcula, não decide, não persiste)
        ↓
MemorySignals { relevance, novelty, recurrence, entropy, impact, outcome, explanation? }
        ↓
decideAndConsolidateV2 (decide: consolidate/discard, com reason por tier)
        ↓
persistMemory (Memory Engine, via Guardian)
```

Divergências da estrutura-alvo do pacote original, registradas
explicitamente:

- Não existe um "Consolidation Engine" separado do Hipocampo —
  `decideAndConsolidateV2` vive em `hipocampo.ts` mesmo, recebendo os
  `MemorySignals` já calculados como parâmetro. Efeito equivalente
  (sinal e decisão são funções/módulos distintos), sem componente
  arquitetural novo.
- Não existe estado `update`/`episodic` como ação distinta — `action`
  é só `"consolidate" | "discard"`; a granularidade fina
  (alto/médio/baixo impacto) vive no campo `reason`
  (`"high_impact"`, `"moderate_impact_review_recommended"`,
  `"low_impact"`, `"impact_below_threshold"`).
- `MemoryObject` não tem `id`, `embedding`, `entities`, `topics`,
  `source`, nem `confidence` — só `key?`, `content`, `createdAt?` (mais
  `origin?`/`corroborated?`, adicionados depois pelo ADR-014 Emenda 1,
  não parte deste ADR).

### Sinais — o que está realmente calculado

- **relevance (R):** **só** `LexicalSimilarity` (overlap léxico via
  Jaccard sobre tokens). Não é uma soma ponderada de cinco componentes
  — os outros quatro (`SemanticSimilarity`, `GoalAlignment`, `Recency`,
  `MemoryTypeWeight`) não são calculados, nem mesmo como termos de peso
  zero numa fórmula; simplesmente não existem no código ainda,
  documentado com um comentário literal no ponto de cálculo avisando
  para não aumentar a complexidade heurística aqui até existirem
  embeddings reais.
- **novelty (Δ):** `1 − maxSimilarity` contra as memórias existentes
  passadas pelo chamador. Sem as faixas de decisão (>0.85/0.40-0.85/
  <0.40) do pacote original — o valor bruto alimenta `impact`
  diretamente (ver abaixo), sem um passo de bucketização próprio.
- **recurrence (ρ):** ocorrências com similaridade acima de um limiar
  nomeado (`RECURRENCE_SIMILARITY_THRESHOLD = 0.5`), ponderadas por
  decaimento temporal `exp(−λt)`, `λ = RECURRENCE_DECAY_LAMBDA = 0.05`
  (constante nomeada, não calibrada contra dado real ainda). Não conta
  sessões distintas — o `MemoryObject` real não carrega identificador
  de sessão.
- **entropy (E):** implementado só no escopo da Trilha 1 (conflito de
  candidato novo vs. base existente, via comparação de `key` +
  similaridade de conteúdo abaixo de um teto). Não implementa
  `Ambiguity`/`Fragmentation`/`ConfidencePenalty` do pacote original —
  só a componente de conflito.
- **impact (I):** **não** é "Utility Gain" calculado — é um proxy
  provisório e documentado como tal: `impact = novelty`. O comentário no
  código é explícito: Utility Gain real precisa de uma fonte melhor
  (ex.: detecção de palavras-chave de mudança de decisão/arquitetura),
  não implementada.
- **outcome (O):** confirmado como no pacote original — sempre `0`,
  `explanation.outcome = ["OutcomeProvider não implementado"]`. Não
  fabricado.

### Correções de código aplicadas (confirmadas, não repetidas de outra fonte)

1. **Filtro de stopword por comprimento removido.** `tokenize` usa uma
   lista explícita de stopwords PT/EN em vez de `t.length > 2`,
   preservando termos técnicos curtos (`go`, `c`, `s3`, `ui`, `ux`,
   `qa`, `pr`, `ai` — allowlist nomeada e testada).
2. **Limiares de decisão não ficam fixos no código.**
   `decideAndConsolidateV2` recebe `ConsolidationThresholds` como
   parâmetro opcional (default `{consolidateThreshold: 0.8,
   reviewThreshold: 0.6, discardThreshold: 0.3}`), não hardcoded sem
   ponto de ajuste.

### Interface formal `MemorySignals` — implementada, com ajuste

Implementada como especificado (Parte 3 do pacote original, "aceito
sem mudar escopo"), com um ajuste feito numa correção posterior à
primeira versão desta rodada: todos os campos são `readonly`
(imutabilidade), e `explanation` carrega `string[]` por sinal (não
`string`) — um sinal pode ter mais de um motivo.

### Signal Engine como função pura — implementado, como interface

Implementado como `SignalCalculator` (interface) + `DefaultSignalCalculator`
(implementação v1, lexical-only) em vez de uma função solta exportada
diretamente — mesmo efeito de pureza (nunca faz query, persistência,
chamada a provider, cache ou LLM), com a vantagem adicional de um ponto
de troca de implementação já existir (uma versão com embeddings no
futuro implementa a mesma interface, sem tocar quem consome
`MemorySignals`).

### Fatias da Trilha 1 — status real

1. Contrato `MemoryObject` + assinaturas dos Memory Signals — **concluído**.
2. Signal Engine (`DefaultSignalCalculator`) — **concluído**, escopo
   lexical-only descrito acima.
3. `decideAndConsolidateV2` (limiares parametrizados) — **concluído**.
4. Integração Hipocampo + `retrieveMemory` no fluxo real de chat (não
   só testável isoladamente) — **concluído em rodada separada**, ver
   `luna-core` PR #20 (Wire Hipocampo's Signal Engine into chat), que
   também implementa o cap de auto-alucinação (ADR-014 Emenda 1) antes
   de ligar retrieval ao prompt.
5. **Fatia de Calibração** (coletar `R/I/ρ/Δ/E/O` de produção, calibrar
   limiares empiricamente) — **não implementada**. Os limiares atuais
   (`0.8/0.6/0.3`, `λ=0.05`, `RECURRENCE_SIMILARITY_THRESHOLD=0.5`) são
   parametrizáveis mas não calibrados contra dado real.

## Parte 2 — Trilha 2 (Decision Engine): o que foi realmente implementado

O `DecisionPlan`/`CognitivePolicyEngine` completo proposto no pacote
original **não foi implementado** — nem a versão "v1 escopada" do
`H(t)`/`X(t)` chegou a virar um objeto de decisão formal. O que existe
de verdade, hoje, no `provider-router.ts`:

**`ProviderHealth`** — implementado, mas com uma diferença do que o
pacote original de origem (que citava "taxa de erro simples das
últimas N chamadas") especificava: em vez de uma janela fixa de N
chamadas, usa uma **média móvel exponencial** (`HEALTH_EMA_ALPHA =
0.1`, constante nomeada) do sucesso por chamada — decisão de uma
correção posterior nesta mesma sessão, para evitar o salto descontínuo
que uma janela fixa causa quando uma chamada antiga sai da janela. Pondera
(não substitui) a ordem estática de fallback existente via
ordenação estável por taxa de erro ascendente.

Nenhum outro componente de `H(t)`/`X(t)` (`RetrievalQuality`,
`RetrievalConflict`, `Budget` como termo de decisão formal,
`ExecutionMode`) foi implementado como parte de um `Decision(t)`
explícito — `Budget` já existia antes desta rodada
(`budget-manager.ts`) e continua operando como gate independente, não
combinado num objeto `H(t)`/`X(t)`. **`DecisionPlan`,
`CognitivePolicyEngine`, `MemoryConfidence`, `WorkingLoad`,
`ConsolidationPressure`, `LearningRate`, `Latency`,
`ProviderHistory` (matriz aprendida), `ToolsAvailable`: nada disso
existe no código — permanecem `NOT_IMPLEMENTED`, direção-alvo, não
implementação desta rodada.**

## Parte 3 — Refinamentos aceitos, status real

- **Interface formal `MemorySignals`** — implementada (ver Parte 1).
- **Signal Engine como função pura / interface** — implementada (ver
  Parte 1).
- **Campo `explanation`** — implementado, como `string[]` por sinal.
- **Nota de direção futura (`ConversationObject`/MEM-002)** — registrada
  na Parte 0, não implementada.
- **"Policy Engine" separado — rejeitado, como no pacote original.**
  `decideAndConsolidateV2` recebe `ConsolidationThresholds` como
  parâmetro de configuração, não como componente arquitetural novo —
  confirmado, é exatamente o que foi implementado.

## Next action

1. `MEM-002` fica registrado no Roadmap (Parte 0), não implementado.
2. Fatia de Calibração (Parte 1, item 5) só depois de dado real de
   produção existir — depende de `luna-core` PR #20 estar em produção
   por tempo suficiente para gerar sinais reais.
3. Trilha 2 (Decision Engine v1 completo, `H(t)`/`X(t)` como objeto
   formal) permanece como direção-alvo, sem data — não há pressão de
   escopo para implementar antes de `ProviderHealth` (já em produção)
   mostrar que o gap importa na prática.
