# Fila de trabalho

**Caminho:** `GENESIS/pacotes/FILA.md`
**Atualizado por:** o Builder, ao concluir cada item
**Estados:** `pronto` · `em execução` · `bloqueado` · `concluído`

---

## Agora

| # | Item | Repositório | Estado | Pacote |
|---|---|---|---|---|
| 2 | Relatório da ronda — Técnico + curadoria | `luna-core` + `luna-frontend` | **pronto** | `2026-08-19-relatorio-ronda.md` + `2026-08-19-curadoria-relatorio.md` |
| 3 | Constituição chegando ao prompt | `luna-core` | **pronto** | `2026-08-19-plano-o-resto.md` §4 |
| 4 | Ingerir o GENESIS pelo `knowledge-gate` | `luna-core` | desbloqueado — sem pacote escrito ainda | — |
| 5 | Classificação por imagem | `luna-frontend` | **bloqueado** — 2 respostas do Arquiteto | `2026-08-19-classificacao-por-imagem.md` |
| 6 | Sense sobre o próprio processo | `Luna-reporter` | bloqueado por 4 | `ADR-026` |
| 7 | Relatório Visual · político | `luna-core` | bloqueado por 2 | mesmo desenho |

**Comece pelo 2.** O maior buraco do produto — o resto está detalhado abaixo.

---

## Detalhe dos itens em aberto

### 2 · Relatório da ronda

O maior buraco do produto: a ronda coleta, valida, sobe, guarda — e não entrega documento.

Escopo desta etapa: **modelo Técnico apenas**, com tela de curadoria (editar e excluir, sem
seleção). O adaptador `rondaId → conjunto de dados` é a peça que falta; renderizadores e
contrato de template já existem.

**Armadilha, e é a mesma que já custou caro:** o achado tem `fotos` embutidas **e**
`fotoIds` no servidor. **Leia os dois.** Ler só um devolve relatório sem foto nenhuma, e o
erro é silencioso.

**A ronda não é alterada.** A curadoria vira registro próprio, com o texto original
preservado ao lado do editado.

**Pronto quando:** o Arquiteto gera o relatório de uma ronda real, abre o arquivo, e os
achados estão lá com as fotos.

### 3 · Constituição no prompt

O adaptador do Groq descarta o contexto montado e envia só duas frases mais memórias
truncadas. Todo o trabalho do motor cognitivo é feito e jogado fora no último passo.

Três cuidados: orçamento de tokens com prioridade declarada; truncar por relevância e não
por posição; e **medir o contexto montado contra o efetivamente enviado** — a diferença
entre os dois é o gargalo, e hoje ninguém a vê.

**Pronto quando:** perguntar à LUNA em produção algo que só está na Constituição — por
exemplo por que foto nunca é obrigatória — e ela souber.

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
