# ADR-024 — Padrão SMX de Cores

Status: Aceito
Data: 2026-08-17
Decisor: Architect (Rubens)
Contexto: Engineer — a partir da medição descrita em
`GENESIS/padroes/PADRAO-SMX-CORES.md`

## Contexto

Duas cores em uso estavam fora da família de matiz da marca: Midnight
(`#1E2761`, matiz 232°) e o ciano de acento (`#22D3EE`, matiz 188°), contra
203°–218° medidos na logo SMX. Não havia regra que reprovasse cor nova —
foi assim que um roxo (`#A78BFA`, matiz 275°) entrou na coloração de sintaxe
do Forge, vindo de um tema de editor emprestado, sem ninguém ter o que
reprovar.

A correção parte de medição, não de gosto: a logo `SMX eXperience` e três
imagens de referência da empresa (o android com o disco `LUNA CORE`, o busto
com a constelação craniana, a cena de escritório com holograma) foram
amostradas pixel a pixel. O achado mais importante da medição é que a
emissão fria (o brilho tecnológico) nunca passa de 5% de nenhuma das três
imagens — a atmosfera vem da escassez do brilho, não da cor dele.

## Decisão

Adotar `GENESIS/padroes/PADRAO-SMX-CORES.md` como norma. Instituir o
**portão de matiz** (toda cor nova precisa cair entre 200° e 220°, ou entre
17° e 55° — fora dessas faixas, não entra) e o **orçamento de luz** (emissão
fria abaixo de 5% da tela; no máximo um elemento acima de `glow-3` por
cartão, três por tela).

As três cores de classificação (`#2E7D32` conforme, `#E8A33D` atenção,
`#C62828` não conformidade) ficam fora do escopo desta decisão — vêm do
protótipo de relatório impresso do Safety Walk, medidas em contraste e
validadas em campo, e são a única exceção permanente ao portão de matiz.

## Consequências

- O acento do tema escuro passa a ser `--luna-glow-5` (`#A0B8C8`).
- A página parte de `--luna-void` (`#000206`), não de Midnight.
- O tema claro deriva da logo (não das três imagens, que são todas
  noturnas): acento `#003C90`.
- `/ronda` (LUNA Safety Walk) preserva seus valores próprios —
  `#1E2761`, `#05060B`, `#F4F6FB` — validados em campo, no `themeColor` do
  PWA e em relatório impresso entregue. Este padrão não os desfaz.
- O bloco de tokens (`GENESIS/padroes/PADRAO-SMX-CORES.md`, Anexo B) é
  aditivo em `luna-frontend/app/globals.css` e `tailwind.config.ts` —
  nenhuma declaração existente é removida, incluindo as chaves legadas
  `luna.success`/`luna.danger`, que continuam declaradas mas deixam de ser
  as cores de classificação (`ok`/`warn`/`fail` passam a sê-lo).

## Emenda

Esta decisão emenda a hierarquia de superfície do ADR-022: a página parte de
`#000206`, não de Midnight, para as superfícies novas cobertas por este
padrão.

## Em aberto

Alinhar o Midnight à matiz da marca (preservando saturação e luminosidade,
corrigindo só a matiz para 215°, resultando em `#1E3A61`) é decisão futura,
em ADR próprio — mexe em PWA instalado e em relatório impresso já entregue,
nunca como efeito colateral de outra tarefa.

## Fontes

| Fonte | O que forneceu |
|---|---|
| Logo `SMX eXperience` | Faixa de matiz da marca (203°–218°), o dourado de classificação de atenção/acento quente |
| Três imagens de referência da LUNA (android, busto, escritório) | O orçamento de luz e as quatro faixas funcionais (ambiente, material, emissão fria, emissão quente) |
| Protótipo de relatório impresso do Safety Walk | As três cores de classificação, únicas fora do portão de matiz |

## Relação com outros documentos

- `GENESIS/padroes/PADRAO-SMX-CORES.md` — texto integral da norma adotada
  por esta ADR, incluindo método de extração reproduzível (Anexo A) e bloco
  de tokens (Anexo B).
- `ADR-023` — Padrão SMX de Design, companheiro: este decide **com que
  cor**, aquele decide **como se desenha**.
- `ADR-022` — Paleta e Redesenho Frontend, emendado por esta decisão na
  hierarquia de superfície.
- `ADR-021` — Safety Walk, fonte das três cores de classificação.
