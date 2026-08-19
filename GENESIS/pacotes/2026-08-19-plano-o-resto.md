# O resto — plano de execução

**19/08/2026 · estado verificado no GitHub e no Supabase agora**

Documento autossuficiente. Os três pacotes que faltavam estão escritos aqui dentro.

---

## Onde estamos

**`luna-frontend`: fila zerada.** Oito PRs mergeados — `#28` ao `#35`. Nenhum aberto.

**Memória:** 46 linhas, **10 sem vetor**. Menos do que eu supunha, e isso muda a
prioridade: é uma consulta, não um projeto.

**Fora do repositório ainda:** documentos de campo de 16/08, `ADR-025`, `ADR-026`.

---

## Ordem, por retorno sobre esforço

| # | O quê | Quem | Esforço |
|---|---|---|---|
| 1 | Vetores faltantes | Builder | minutos |
| 2 | Commits documentais | **Arquiteto** | minutos |
| 3 | Gerador de relatório | Builder | o item de maior valor |
| 4 | Constituição no prompt | Builder | médio, destrava o Hipocampo |
| 5 | Gate com link até o campo | Builder | pacote já escrito |
| 6 | Cores do `/ronda` | Builder | pacote já escrito |

---

# 1 · Vetores faltantes

> **REPOSITÓRIO-ALVO: `raugustorubens-design/luna-core`**

**Problema:** 10 das 46 memórias estão com `embedding` nulo — tudo que entrou de julho em
diante, incluindo as três correções de sugestão da ronda. Elas existem no banco e **não
aparecem em busca semântica**. É memória gravada que ninguém alcança.

**Causa:** entradas que chegam por `persistMemory` direto, sem passar pelo
`knowledge-gate`, não recebem embedding.

**Tarefa:**

1. Rotina que varre `memoria_luna` onde `embedding IS NULL`, gera o vetor pelo mesmo
   gerador já em uso, e grava. Idempotente — rodar duas vezes não duplica nada
2. **Fechar a torneira:** `persistMemory` passa a gerar embedding na escrita. Sem isso o
   problema volta amanhã
3. Se o gerador falhar para uma linha, **registre e siga** — uma linha problemática não
   pode travar as outras nove

**Verificação:** `count(*) - count(embedding)` volta zero. E uma busca semântica por
"correção de sugestão" precisa devolver as três linhas de 18/08, que hoje não aparecem.

**Não faça:** não apague nem reescreva linha nenhuma. Só preencher o que está nulo.

---

# 2 · Commits documentais

> **REPOSITÓRIO-ALVO: `raugustorubens-design/Luna-context.md`**
> **Executor: o Arquiteto** — não toca código, não precisa de teste

**a) Documentos de campo de 16/08.** Oito arquivos, só criação, nos caminhos:
`GENESIS/achados-campo/`, `GENESIS/decisoes/`, `GENESIS/pendencias/`, `GENESIS/patches/`.
Preservar as datas nos nomes. **Não reescrever conteúdo para "atualizar"** — é registro
histórico.

**b) `ADR-025` e `ADR-026`**, ambos com status **Proposto**. Confirmar que 025 e 026 estão
livres; se não, usar o próximo e ajustar referências, sem renumerar o que existe.

**c) A análise de canais e idade da fonte** vai para `GENESIS/RESEARCH/`, não para `ADR/`.

---

# 3 · Gerador de relatório da ronda

> **REPOSITÓRIO-ALVO: `raugustorubens-design/luna-core`**

**É o maior buraco do produto.** A ronda coleta, valida, sobe e guarda — e não produz
documento. O que o cliente recebe não existe.

## O que já existe

| Peça | Onde |
|---|---|
| Renderizadores pptx, docx, xlsx, csv, html, markdown, json | `src/convergia/renderers/` |
| Template tabular de relatório SSMA | `src/convergia/templates/relatorio-ssma-tabular.ts` |
| Template visual com campos posicionados | `templates/visual-template-store.ts`, `slide-layout.ts` |
| Ronda salva | `convergia_rondas` |
| Fotos por id | `convergia_ronda_fotos` |

**O que falta é a peça do meio:** pegar a ronda salva, resolver as fotos por `fotoId`,
montar o conjunto de dados no formato que o template espera, chamar o renderizador.

## Escopo desta etapa — um modelo só

**Comece pelo "Detalhado"**, o técnico. Motivos: usa o template tabular que já existe,
não depende de posicionamento visual, e é o que serve para auditoria. O "Visual", que vai
ao cliente, entra depois e reusa o mesmo conjunto de dados.

## O adaptador

Entrada: `rondaId`. Saída: o documento.

1. Carrega a ronda de `convergia_rondas`
2. Para cada achado, resolve `fotoIds` em `convergia_ronda_fotos` — **use a versão de
   campo, nunca a original.** 1280px é suficiente para o documento, e a original são
   vários MB por foto
3. Monta o conjunto de dados: metadados no cabeçalho, achados como linhas, classificação
   com as três cores sólidas, e as fotos de cada achado
4. Chama o renderizador

**Armadilha que já custou caro:** o achado tem `fotos` (embutidas, caminho de contingência)
**e** `fotoIds` (no servidor, caminho normal). **Leia os dois.** Ler só um devolve
documento sem foto nenhuma, e o erro é silencioso — vazio parece intencional.

## Armazenagem provisória

Documento gerado vai para armazenamento temporário, **com descarte em 7 dias**. É seguro
porque é reconstruível: as partes ficam. E impede que o documento gerado vire mais uma
coisa que cresce sem limite.

## Verificação

`typecheck`, testes existentes sem alteração, `build`.

**Portão real:** gerar o relatório de uma ronda de verdade, abrir o arquivo, e conferir
que os achados estão lá **com as fotos**. Documento gerado que ninguém abriu não conta.

**Fora de escopo:** o modelo "Visual"; a conversão para PDF, que depende do LibreOffice
ainda não instalado no contêiner do Railway.

---

# 4 · A Constituição no prompt

> **REPOSITÓRIO-ALVO: `raugustorubens-design/luna-core`**

**O maior gargalo registrado.** O motor cognitivo recupera memória, monta contexto e
escolhe provedor — e o adaptador do Groq **descarta o contexto montado**, enviando apenas
duas frases de instrução mais memórias truncadas.

Todo o trabalho do motor é feito e jogado fora no último passo. **A LUNA em produção não
tem conhecimento operacional da própria governança.**

**Tarefa:** o adaptador passa a enviar o contexto que recebeu, em vez de montar o seu.

Três cuidados:

1. **Orçamento de tokens.** A Constituição inteira em toda chamada estoura a cota. Envie o
   que couber, com prioridade declarada: identidade e regras canônicas antes de memória
   episódica
2. **Truncar por relevância, não por posição.** Hoje o corte é onde acabou o espaço.
   Com os vetores do item 1 funcionando, dá para cortar pelo que importa
3. **Medir antes e depois.** Registre o tamanho do contexto montado e o efetivamente
   enviado. A diferença entre os dois **é o gargalo**, e hoje ninguém a vê

**Portão real:** perguntar à LUNA, em produção, algo que só está na Constituição — por
exemplo por que foto nunca é obrigatória. Se ela souber, chegou.

---

# 5 e 6 · Pacotes já escritos

Estes não precisam ser reescritos, só enviados:

| Pacote | O que faz |
|---|---|
| `GENESIS_2026-08-17_gate-com-link-ao-campo.md` | Gate na tela de edição, que hoje não tem nenhum, e link até o campo faltando |
| `GENESIS_2026-08-17_safety-walk-padrao-cores.md` | Migração de cores do `/ronda` |

O primeiro tem valor próprio e independente: **a tela de edição não valida nada.** Uma
ronda recusada pode ser salva incompleta e recusada de novo.

---

## Regras que valem em tudo acima

**Nada é removido ou substituído** — se uma instrução parecer exigir remoção, pare e
pergunte.

**Nenhum teste existente pode ser alterado** para um novo passar.

**Foto nunca é obrigatória**, em nenhum caminho.

**Feito = clicado e visto funcionando em produção.** Teste verde é estado intermediário.

**`git merge-base origin/main HEAD`** batendo com a ponta de `origin/main` antes do
primeiro commit de cada branch.

**Um pacote por vez.** O que mais custou nesta semana não foi capacidade — foi repasse.
