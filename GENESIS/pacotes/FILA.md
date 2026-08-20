# Fila de trabalho

**Caminho:** `GENESIS/pacotes/FILA.md`
**Atualizado por:** o Builder, ao concluir cada item
**Estados:** `pronto` · `em execução` · `bloqueado` · `concluído`

> **Atualização 2026-08-20:** `GENESIS/pacotes/PLANO-DE-PRODUCAO.md` passa a ser o mapa —
> quatro marcos, com tarefas dimensionadas para caber numa sessão. Este arquivo fica como
> visão do que vem a seguir, não reescrito.

---

## Fila de 20/08 (tarde) — pacotes soltos, fora do Plano de Produção

Seis pacotes chegaram por anexo em vez de já estarem na `main` — commitados agora junto com
esta atualização. Ordem de execução, do `0_LEIA-PRIMEIRO.md` do lote:

| # | Pacote | Repositório | Por quê nesta posição |
|---|---|---|---|
| 1 | `2026-08-20-exif-colunas.md` | `luna-core` | **Urgente** — `luna-core#52` já mergeado grava em colunas que não existem; gravação falhando em produção agora |
| 2 | `2026-08-20-pptx-layout.md` | `luna-core` | O relatório em PPTX é o portão do Marco 1 |
| 3 | `2026-08-19-paleta-em-tudo.md` | `luna-frontend` | O roxo literal ainda está no `body` |
| 4 | `2026-08-20-tudo-novo.md` | `luna-frontend` | Promove `/` e `/forge`, refaz o painel do Convergia |
| 5 | `2026-08-20-tres-correcoes.md` | `luna-frontend` | Retorno do login errado, imagem da LUNA disputando o texto, Forge quebrando no celular |
| 6 | `2026-08-19-trabalho-no-github.md` | `luna-core` + `luna-frontend` + `Luna-context.md` | Issues como unidade de trabalho, reivindicar antes de começar |

`2026-08-19-ronda-demo.md` fica **bloqueado** — depende da decisão do Arquiteto sobre a
leitura por IA na demonstração (ver o próprio pacote).

`2026-08-19-acesso-publico.md` está **concluído** — etapas 1 e 2 mergeadas via
`Luna-context.md#41`/`#42` (que na verdade eram os PRs `luna-frontend`, ver histórico);
fica como registro, sem trabalho pendente do Builder.

**Itens 1-3 mergeados nesta sessão:** `exif-colunas` (`luna-core#55`), `pptx-layout`
(diagnóstico só — hipótese B confirmada, sem código a mudar) e `paleta-em-tudo`
(`luna-frontend#47`). Faltam os itens 4-6 e o `ronda-demo` bloqueado.

**`2026-08-20-canal-de-pacotes.md`** — desenho do Arquiteto para um quadro de trabalho no
Supabase (estado ao vivo por item — `novo`/`em_desenvolvimento`/`em_revisao`/`aprovado`/
`mergeado`/`verificado`/`asbuilt` — substituindo a reivindicação por Issue do item 6 acima).
**Bloqueado por gatilho** — não executar até a fila ficar sem item `pronto`, ou o Arquiteto
carregar dois pacotes novos no mesmo dia, ou ele mandar. Nenhuma dessas três condições
estava presente quando o pacote chegou (ainda havia itens `pronto` na fila), então só
commitado como registro nesta rodada — nada migrado, nenhuma tabela criada.

**Nota de nomenclatura:** o pacote de retorno de login/imagem da LUNA/Forge no celular se
autodeclara `GENESIS/pacotes/2026-08-20-tres-correcoes.md` no próprio cabeçalho — é esse o
nome usado aqui e no arquivo commitado, ainda que uma lista de commit anterior o tenha
chamado de `2026-08-20-imagem-e-mobile.md`.

---

## Agora

| # | Item | Repositório | Estado | Pacote |
|---|---|---|---|---|
| 2 | Relatório da ronda — Técnico + curadoria | `luna-core` **concluído** + `luna-frontend` **pronto** | **em execução** | `2026-08-19-relatorio-ronda.md` + `2026-08-19-curadoria-relatorio.md` |
| 3 | Constituição chegando ao prompt | `luna-core` | concluído — falta portão real | `2026-08-19-plano-o-resto.md` §4 |
| 4 | Ingerir o GENESIS pelo `knowledge-gate` | `luna-core` | desbloqueado — sem pacote escrito ainda | — |
| 5 | Classificação por imagem | `luna-frontend` | **bloqueado** — 2 respostas do Arquiteto | `2026-08-19-classificacao-por-imagem.md` |
| 6 | Sense sobre o próprio processo | `Luna-reporter` | bloqueado por 4 | `ADR-026` |
| 7 | Relatório Visual · político | `luna-core` | bloqueado por 2 | mesmo desenho |

**No 2 agora.** Backend mergeado (`luna-core#50`) — adaptador, XLSX e curadoria (editar/
excluir) prontos e testados. Falta só `luna-frontend`: tela de curadoria + botão "Gerar
relatório" na tela de rondas anteriores. O maior buraco do produto — o resto está
detalhado abaixo.

---

## Detalhe dos itens em aberto

### 2 · Relatório da ronda

O maior buraco do produto: a ronda coleta, valida, sobe, guarda — e não entrega documento.

**`luna-core` concluído (PR `#50`, sobre o adaptador do PR `#47`):** adaptador
`rondaId → conjunto de dados` (só achados `identificado`, as duas origens de foto lidas —
`fotoIds` e `fotos`, sempre a versão de campo), renderizador XLSX com cabeçalho/cor/foto,
armazenagem de 7 dias, e a curadoria (`convergia_relatorio_curadoria`): editar
`descricao`/`acaoRecomendada` e excluir achado com motivo obrigatório, sem tocar a ronda
salva — o original fica sempre. Rotas: `GET/PATCH/DELETE .../curadoria`,
`POST .../relatorio`, `GET .../relatorio/:id`. 433 testes, `typecheck` e
`test:architecture` limpos; geração real ponta a ponta fora da suíte (não contra Guardian
de produção).

**Falta `luna-frontend`:** botão "Gerar relatório" na tela de rondas anteriores (só em
ronda já confirmada pelo servidor, nunca da fila pendente) + a tela de curadoria (lista de
achados, miniaturas com selo de classificação, descrição/ação editáveis ali mesmo,
classificação/gravidade visíveis e não editáveis, excluir com confirmação + motivo,
contagem no rodapé, botão Gerar) — ver `2026-08-19-curadoria-relatorio.md`.

**Pronto quando:** o Arquiteto gera o relatório de uma ronda real pela tela, abre o
arquivo, e os achados estão lá com as fotos.

### 3 · Constituição no prompt

**Concluído**, mergeado em `luna-core` antes desta reconciliação (sem PR numerado
registrado — ver `GENESIS/BUILDER.md` de `luna-core`, entrada "Item 4 do Plano"). O
adaptador do Groq agora monta um bloco de contexto com prioridade declarada
(Constitution > identidade > estado do projeto > roadmap > tarefas abertas),
`packPromptBlocks` trunca por prioridade (nunca o bloco de maior prioridade primeiro), e
`LUNA_CONSTITUTION.md` passou a ser buscada de verdade (antes, nunca era sequer lida).

**Falta só o portão real:** perguntar à LUNA em produção algo que só está na Constituição
— por exemplo por que foto nunca é obrigatória — e confirmar que ela sabe. Isso é clique
do Arquiteto, não commit — ver `PENDENTE.md`.

---

## Concluído

| Item | PRs | Data |
|---|---|---|
| Gate do cliente espelhando o servidor | `#30` | 18/08 |
| Câmera: dois caminhos, decode reduzido, instrumentação | `#31` `#32` `#33` `#34` `#35` | 18/08 |
| ADR-022 · paleta e Forge v2 | `#28` + `#37` doc | 18/08 |
| Padrões SMX no GENESIS | `#38` doc | 18/08 |
| Tirar o roxo · fundo `#000206` | `#36` | 19/08 |
| Gate com link até o campo | `#37` | 19/08 |
| Cores do `/ronda` | `#38` | 19/08 |
| Vetores faltantes na memória (`luna-core`) | `#44` `#47` | 19/08 |
| Constituição no prompt (`luna-core`) | sem PR numerado — ver `BUILDER.md` de `luna-core` | 19/08 |
| Relatório da ronda — backend (`luna-core`) | `#47` (adaptador) + `#50` (curadoria) | 19/08 |

**Vetores faltantes — nota:** critério de aceite 1 (`count(*) - count(embedding) = 0`)
atingido, 46/46 linhas. Critério de aceite 2 (busca semântica por "correção de sugestão"
trazendo as 3 linhas de 18/08 no topo) **não atingido** — as 3 linhas ficam nas posições
10ª/13ª/24ª de 46, atrás de linhas de assunto mais concentrado. Não é falha de embedding
(scores plausíveis e diferenciados), é diluição de sinal pelo texto usado em
`construirTextoParaEmbedding`, que embute o `conteudo` inteiro. Mudar isso é decisão de
design de recuperação, não correção técnica — registrado como dúvida em
[`luna-core#48`](https://github.com/raugustorubens-design/luna-core/issues/48), com
recomendação de aceitar o comportamento atual por ora. Item marcado concluído porque o
escopo literal ("preencher os vetores faltantes") foi cumprido; a pendência de ranking
segue rastreada na Issue, não neste item.

---

## Esperando o Arquiteto

Não são trabalho do Builder — são decisão ou commit documental.

| O quê | O que falta |
|---|---|
| Documentos de campo de 16/08 | commitar em `achados-campo/`, `decisoes/`, `pendencias/`, `patches/` |
| `ADR-025` e `ADR-026` | commitar como **Proposto** |
| Classificação por imagem | soma ou substitui o veredito? E o nome do quarto valor |
| Relatório Visual | o que vem marcado por padrão? O Positivo entra? |
| Faixas de prazo do Sense | tempo de ação de cada tipo de pendência |
| `.ppt` em produção | instalar LibreOffice no contêiner do Railway |
| `luna-core#48` | ranking de busca semântica dilui por texto de embedding — ver nota acima |
| IA dentro do Forge (`2026-08-19-nota-ia-no-forge.md`) | quem é o usuário do Forge — só você, ou produto com mais de um usuário? Muda o passo 4 (contrato de plugin) inteiro |
| Terminal como cockpit (`2026-08-19-nota-terminal-cockpit.md`) | serviço separado no Railway para o terminal, ou mesmo contêiner do `luna-frontend`? Única decisão que trava o desenho — recomendação registrada é serviço separado |
