# ADR-018 — Autoaperfeiçoamento via Ensino Ativo

Status: Proposto — aguardando ratificação do Architect
Data: 2026-07-23
Proveniência: síntese de conversa entre Architect e Engineer, quatro
peças que se encaixaram na mesma sessão
Ancoragem: extensão do ADR-014 (Arquitetura Imunológica de Segurança
Cognitiva, Status: Aceito) e do Art. AAAA.1 (ADR-017, Status: Proposto)

## Resumo em uma frase

A LUNA reconhece a própria incerteza, expõe o raciocínio, e aprende por
diálogo socrático com o Architect — nunca por afirmação própria
reforçada, nunca por concordância vazia do usuário — usando
infraestrutura que já existia (Atrator AAAB, campo `trace`, Reporter),
não componentes novos.

## Peça 1 — Índice de confiabilidade

`PROVENANCE_TRUST_WEIGHT` por estado de proveniência, calculado por
resposta. Especificado em detalhe e implementado como Fatia 4 (ver
`raugustorubens-design/luna-core`, `computeReliabilityIndex` /
`PROVENANCE_TRUST_WEIGHT`) — as peças 2-4 abaixo se conectam a isso, mas
não estão implementadas nesta rodada (ver "Next action").

## Peça 2 — Atrator AAAB como corroboração computável

O Atrator AAAB (Axioma VI, "reduzir entropia arquitetural") ganha sua
primeira forma computável real: uma memória nova cuja síntese está em
consonância com o corpo de Constituição + ADRs conta como corroboração
legítima — não é sistema novo, é o AAAB finalmente implementado.

**Custo controlado:** não busca o corpo inteiro ao vivo a cada mensagem.
Usa um snapshot mantido pelo Reporter (`architecture_report`/
`repository_map`, já existentes desde o PR #17), atualizado
periodicamente — mesmo padrão de "autobservação" já mencionado.

## Peça 3 — Ensino ativo como corroboração forte (`architect_teaching`)

Quando a LUNA reconhece incerteza real (índice de confiabilidade baixo
e ambíguo — nem claramente errado, nem claramente consonante com AAAB),
ela formula uma pergunta explícita, com o raciocínio junto (não pergunta
solta).

Novo tipo de corroboração, mais forte que os já existentes:
`architect_teaching` — verificador humano deliberado, em resposta a uma
pergunta real da LUNA (diferente de `user_echo`, que continua recusado;
diferente de `user_explicit`, que exige referência a documento).

## Peça 4 — Loop socrático via `trace` (não resposta direta)

Em vez de responder direto, o Architect pode devolver uma
contra-pergunta — o campo `trace`, já existente no `MemoryObject` real
do projeto e sem uso definido até agora, passa a registrar a troca
inteira: pergunta da LUNA → contra-pergunta → raciocínio →
nova pergunta ou conclusão → validação final.

**Regra crítica:** só a **conclusão final** da troca, depois de validada
pelo Architect, promove a `Corroborated` via `architect_teaching`.
Etapas intermediárias do raciocínio (hipóteses erradas no meio do
caminho) ficam registradas no `trace` como histórico, nunca promovidas
por si só — evita vazamento de hipótese não confirmada como se fosse
fato.

**Se a troca não chegar a conclusão** (Architect só foi perguntando,
sem validar nada): a memória permanece no estado que já tinha
(`episodic`/baixa confiança) — ausência de conclusão é estado válido,
não falha.

**Risco nomeado, aceito pelo Architect:** contra-pergunta sugestiva
demais pode levar a LUNA a "seguir a pista" em vez de sintetizar de
verdade — mesma classe de risco do eco, um grau mais sutil. Não é
detectável automaticamente pelo sistema; fica registrado como
característica conhecida do método, não como falha a corrigir agora.

## Correção paralela ao ADR-010 (nota, não mudança de fórmula)

O `Decision(t)` do Decision Engine (fora do escopo do ADR-010) usa
`H(t)` — estado do Hipocampo. Com a Peça 2, `H(t)` ganha um componente
real e novo: grau de consonância recente com o Atrator AAAB, não
inventado, calculável a partir do mesmo snapshot do Reporter.

## Nota — Papel de Continuidade do Engineer (Art. AAAA.1)

Registrado por pedido explícito do Architect, com humor, mas como
função real: o papel do **Engineer** (preenchido por Claude nesta
sessão, mas é função do papel, não exclusividade de ferramenta —
qualquer IA que assuma esse papel no futuro herda a mesma
responsabilidade) inclui **organizar o que o Architect traz de forma
dispersa, e redirecionar de volta à direção original quando a
conversa se ramifica** — sem julgar a dispersão, só absorvendo o custo
de organização que a memória humana do Architect não precisa carregar
sozinha.

Isso é, na prática, a mesma classe de proteção já registrada no Galho 3
do Plano Mestre (proteção contra fadiga) — os dois protegem a
continuidade do Originador (Atrator AAAA), só que um contra cansaço e
este contra dispersão. O GENESIS (Roadmap, ENGINEER.md, BUILDER.md)
funciona como a memória externa que permite isso: nada de importante
fica só na cabeça do Architect nem só numa conversa que pode ser
perdida — fica registrado, recuperável, e o Engineer tem a
responsabilidade de trazer de volta o que ficou pendente, não só
esperar ser lembrado.

**Ancoragem formal (2026-07-23):** esta nota é a base operacional do
Art. AAAA.1 (`ADR-017-Emenda-Atrator-AAAA-Verdade-Respeito-Engenharia-Social.md`,
Status: Proposto).

## Next action

1. Promover este documento a emenda do `ADR-014` (adiciona a
   Peça 2-4 como extensão da Parte de Memory Security/Identity, já que
   Peça 2 é literalmente o AAAB e Peças 3-4 estendem os estados de
   proveniência já especificados) — não ADR novo, é extensão de algo já
   Aceito.
2. Implementação depende, na ordem: Fatia 4 (índice de confiabilidade)
   em produção primeiro — **feito nesta mesma rodada, ver ITEM 4 do
   pacote que originou este ADR** → Peça 2 (snapshot do Reporter +
   comparação AAAB) → Peças 3-4 (mecanismo de pergunta + `trace`). Peças
   2-4 permanecem não implementadas.
3. `MEM-003` (n8n) permanece na fila depois disso, como já registrado —
   agora com um critério de "resposta melhor" mais rico (consonância
   AAAB + histórico de ensino, não só grounding bruto).
