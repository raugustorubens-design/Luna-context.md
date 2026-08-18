# ADR-014 — Emenda 1: Estado FIRST_OBSERVATION e cap de memória não corroborada

Status: Proposto — aguardando aprovação do Architect
Data: 2026-07-23
Decisor: pendente (Architect/Originador via Atrator AAAA)
Implementação de referência: `raugustorubens-design/luna-core`,
`src/luna/signal-engine.ts` (`MemoryTrustState`,
`resolveMemoryTrustState`) e `src/luna/hipocampo.ts`
(`decideAndConsolidateV2`, cap `UNCORROBORATED_CAP_TIER`)

## Contexto

Incidente real observado (2026-07-23, sessão Claude Code): perguntada
sobre seu próprio sistema de memória, a LUNA (via Groq) inventou uma
arquitetura inteira plausível e falsa — IDs fictícios, um "jarvis_mode"
tratado como capacidade descrita quando na verdade é só uma tag interna
de `contexto`, e uma capacidade de apagar memória por ID que não existe
em lugar nenhum do código.

O ADR-014 já nomeia esse risco (Parte III, "Crenças": *"Non-self = crença
injetada sem lastro evidencial"*; Parte V.3, quarentena semântica) mas não
definia, até esta emenda, um mecanismo concreto e implementável para o
ponto exato onde o risco se materializa no Hipocampo: `persistMemory` +
`retrieveMemory` juntos criam um ciclo de reforço — a LLM inventa algo →
o Hipocampo consolida com alta confiança porque `impact`/`novelty`
calculados são altos → uma recuperação futura traz esse conteúdo de volta
como "memória real" → a LLM passa a tratar a própria fabricação como fato
estabelecido.

Uma primeira versão desta proteção foi revisada por uma segunda IA
(Gemini) e teve 5 fragilidades reais apontadas. O desenho abaixo já
incorpora essas correções — em particular, evita qualquer tentativa de
extrair "qual alegação é verdadeira" via NLP/regex, por ser um problema de
pesquisa em aberto (ADR-014 Parte VIII.1), não uma função computável hoje.
Fabricar essa distinção seria repetir o mesmo erro que a Parte VIII já
recusa: uma abstração não-computável apresentada como se resolvida
(mesma classe de recusa já registrada para a fórmula de Decision Engine
via ADR-011).

## Decisão

### 1. Concordância do usuário nunca promove tier

Não existe tentativa de distinguir "usuário confirmou de verdade" de
"usuário só repetiu de volta o que a LLM disse" via regex/NLP — essa
distinção não é computável de forma confiável hoje, e errar nela é pior
que não tentar (abre exatamente a brecha de câmara de eco que motivou
esta emenda). Nenhum sinal derivado de texto do usuário conta como
corroboração.

### 2. Único caminho de corroboração real

Corroboração exige referência a um artefato externo verificável e
**checado de fato** — não apenas mencionado. Ex.: o texto cita "ADR-014"
— só conta como corroboração se o sistema efetivamente confirmar (ex.:
via leitura real do repositório de contexto) que esse ADR existe e
contém o que está sendo alegado. Menção a um nome de ADR/commit sem essa
verificação não conta sozinha.

Nesta primeira implementação (`luna-core`, 2026-07-23), o verificador de
corroboração em si **não está construído** — é trabalho futuro,
explicitamente fora de escopo desta emenda (mesmo critério de adiamento
já usado para o "Evidence Engine" e para `SemanticSimilarity` no Signal
Engine). O campo que carregaria o resultado dessa verificação
(`MemoryObject.corroborated`) existe desde já; nada ainda o define como
`true`.

### 3. Cap aplicado ao `MemoryObject` inteiro, não por alegação

Todo `MemoryObject` de origem `assistant` (resposta gerada pela LLM, não
confirmada por evidência externa) nasce em estado `unverified` (ou
`first_observation`, ver item 4) — nunca pode ser classificado por
`decideAndConsolidateV2` acima do tier mais fraco de consolidação
(`low_impact`) só por ter `impact`/`novelty` altos, até existir
corroboração real (item 2).

O cap se aplica à mensagem inteira, não a alegações individuais dentro
dela — mais simples e mais conservador: trata com cautela qualquer
conteúdo misto (fato real + fabricação no mesmo texto) em vez de tentar
decompor por granularidade fina que não é confiável hoje.

Importante: o cap nunca promove um `discard` para `consolidate` — ele só
rebaixa o teto de tiers acima do cap. Um candidato cujo `impact` já cairia
em `discard` continua sendo descartado, independentemente do
`MemoryTrustState`.

### 4. Estado `FIRST_OBSERVATION` (cold start)

Quando não há nenhuma memória existente para comparar (nesta
implementação: `retrieveMemory` não retornou nada), o `MemoryObject`
nasce em `first_observation` — um estado anterior a `unverified`. Nesse
estado, o cap do item 3 se aplica **independentemente da origem**
(mesmo conteúdo de origem `user` seria capado nesta condição, embora a
implementação de referência hoje só invoque isso para o par
pergunta/resposta completo, de origem `assistant`). Evita o problema de
"primeira troca sem baseline pra proteger contra o quê" — sem histórico,
não há como o Signal Engine calcular `novelty`/`impact` com significado
real, e um "alto impacto" calculado nessas condições é artefato da
ausência de dado, não evidência de importância real.

### 5. Verificação pós-resposta — sinalização, não bloqueio

Toda resposta gerada é varrida por um padrão simples de palavras-chave
(ex.: "o sistema usa/tem/faz X", "a LUNA tem/possui X") que sinaliza
possível alegação técnica nova sem corroboração conhecida. Isso é log
apenas (`grounding.unverified_technical_claim_detected`, via Reporter) —
alimenta auditoria humana e o Grounding Report de retrieval, nunca
bloqueia ou altera a resposta ao usuário. Não há confiança suficiente
nesta heurística para deixá-la decidir sozinha.

## Consequências

- Nenhuma memória de origem `assistant` pode virar "norma" (tier alto de
  consolidação) sem corroboração real — quebra o ciclo de reforço descrito
  no Contexto, sem exigir um classificador de verdade que não existe.
- O custo é conservador por padrão: conteúdo de origem `assistant`
  genuinamente correto também fica capado até existir um verificador de
  corroboração real (item 2) — aceitável porque o ADR-014 já estabelece
  (Parte III, "Crenças") que rotular "não verificada" é preferível a
  autoimunidade por descarte silencioso, e o conteúdo capado continua
  sendo persistido (não é `discard`), só não com autoridade de norma.
- Constrói a base para o "caminho de corroboração real" (item 2) e para a
  "Verificação pós-resposta" (item 5) evoluir de sinalização para gate
  real, quando (e só quando) houver um verificador confiável — não
  antes.

## Referências

- ADR-014 — Arquitetura Imunológica de Segurança Cognitiva (Parte III
  "Crenças"/"Memória"; Parte V.3 Quarentena Semântica; Parte VIII.1 "O
  Problema do Drift Semântico vs. Aprendizado Legítimo")
- ADR-011 — Emenda ao ADR-010 (precedente de correção pós-"Aceito" via
  arquivo de emenda separado, mesmo padrão seguido aqui)
