# Plano de produção

**Caminho:** `GENESIS/pacotes/PLANO-DE-PRODUCAO.md`
**Substitui:** `FILA.md`
**Atualizado por:** o Builder, ao concluir cada tarefa

---

## Como este plano é feito

**A unidade é a sessão, não a funcionalidade.** Toda tarefa aqui foi dimensionada para
caber numa sessão do Claude Code, do começo ao merge. Tarefa que não cabe perde estado no
meio — e recomeçar custa mais que ter dividido.

Cada tarefa traz: repositório-alvo, do que depende, e **o que a torna pronta**. Sem
critério de pronto, tarefa não fecha — só é abandonada.

**Pegue a primeira tarefa `pronta`.** Se estiver bloqueada, pule para a seguinte. Uma
dúvida trava uma tarefa, não o plano.

**Marco não é prazo.** É o ponto em que algo passa a existir de forma visível.

---

# MARCO 1 · A ronda entrega documento — **concluído em 20/08/2026**

> As seis tarefas abaixo já fecharam quando este marco foi revisado: 1.1/1.2 (`luna-core`
> `#47`, `#51`), 1.3/1.4 (`luna-core` `#50`, curadoria), 1.5 (`luna-frontend#44`, mais o
> botão anterior mergeado com a curadoria), 1.6 (armazenagem de 7 dias, junto de `#50`) —
> e a etapa de formato/página do relatório (`luna-core#53` + `luna-frontend#44`) estendeu
> o marco para PPTX/XLSX/DOCX. Tabela preservada como registro do plano original, não
> reescrita.

**Por que primeiro:** a ronda coleta, valida, sobe e guarda — e não entrega nada. O que o
cliente recebe não existe. É o maior buraco do produto.

| # | Tarefa | Repo | Depende | Pronto quando |
|---|---|---|---|---|
| 1.1 | Adaptador `rondaId → conjunto de dados` | `luna-core` | — | Uma ronda real vira estrutura com achados, fotos resolvidas e metadados. Coberto por teste de função pura |
| 1.2 | Template `ronda_tecnico`, renderizador `docx` | `luna-core` | 1.1 | O arquivo abre, tem cabeçalho, um bloco por achado e as fotos |
| 1.3 | Tela de curadoria — editar e excluir | `luna-frontend` | — | Editar descrição e ação; excluir pede motivo; a **ronda não é alterada** |
| 1.4 | Registro de curadoria no banco | `luna-core` | 1.3 | Texto original preservado ao lado do editado; exclusões com motivo |
| 1.5 | Botão "Gerar relatório" no histórico | `luna-frontend` | 1.2, 1.4 | Só em ronda confirmada pelo servidor. Nunca em pendente |
| 1.6 | Armazenagem com descarte em 7 dias | `luna-core` | 1.2 | Arquivo tem link e expira. Reconstruível a qualquer momento |

**Armadilha da 1.1, e já custou caro:** o achado tem `fotos` embutidas **e** `fotoIds` no
servidor. **Leia os dois.** Ler só um devolve documento sem foto nenhuma, e o erro é
silencioso — campo vazio é estado legítimo.

**Fecha o marco:** o Arquiteto gera o relatório de uma ronda real, abre, e os achados estão
lá com as fotos.

---

# MARCO 2 · A LUNA lembra

**Por que segundo:** hoje ela grava e não recupera. Dez memórias estão sem vetor, o GENESIS
inteiro está fora da memória, e a Constituição não chega ao prompt. É a descontinuidade que
originou o projeto, ainda presente.

| # | Tarefa | Repo | Depende | Pronto quando |
|---|---|---|---|---|
| 2.1 | Preencher os `embedding` nulos | `luna-core` | — | `count(*) − count(embedding)` devolve zero |
| 2.2 | `persistMemory` gera vetor na escrita | `luna-core` | 2.1 | Linha nova nasce com vetor. Sem isso o problema volta |
| 2.3 | Ingerir ADRs e achados pelo `knowledge-gate` | `luna-core` | 2.2 | Buscar "por que foto nunca é obrigatória" devolve a decisão com procedência |
| 2.4 | Constituição chegando ao prompt | `luna-core` | 2.3 | Perguntar à LUNA em produção algo que só está na Constituição, e ela saber |
| 2.5 | Medir contexto montado × enviado | `luna-core` | 2.4 | O número aparece em log. **A diferença entre os dois é o gargalo**, e hoje ninguém a vê |

**Comece pela 2.1.** São dez linhas e uma consulta — a tarefa mais barata do plano inteiro,
e destrava o marco todo.

---

# MARCO 3 · O sistema se observa

**Por que terceiro:** todo defeito desta semana foi descoberto pelo Arquiteto olhando o
celular. Nenhum por instrumento. Funciona com uma pessoa; não escala.

| # | Tarefa | Repo | Depende | Pronto quando |
|---|---|---|---|---|
| 3.1 | `STATUS.md` atualizado ao fim de cada tarefa | `Luna-context.md` | — | O Engenheiro lê um arquivo em vez de consultar cinco fontes |
| 3.2 | Contrato de sinal do Sense | `Luna-reporter` | — | Sinal novo vira dado, não código |
| 3.3 | Cinco invariantes do processo | `Luna-reporter` | 3.2 | PR com conflito, portão pendente há mais de 2 dias, teste que caiu, pacote parado, documento citado e inexistente |
| 3.4 | Leitura de Supabase pelo Gateway | `Luna-reporter` | 3.2 | O Sense propõe candidato, **nunca grava** |

**Os cinco invariantes da 3.3 foram todos violados esta semana.** É banco de teste real com
dado que já existe — e quando os sinais do cliente forem construídos, o motor já terá
rodado semanas.

---

# MARCO 4 · A ronda ensina

**Por que por último:** depende do marco 1 existir (a curadoria é onde a ratificação
acontece) e do marco 2 funcionar (senão o que entra some).

| # | Tarefa | Repo | Depende | Pronto quando |
|---|---|---|---|---|
| 4.1 | Classificação por imagem | `luna-frontend` | decisão do Arquiteto | Cada foto tem rótulo próprio; o achado mantém o veredito |
| 4.2 | Curadoria alimentando o `knowledge-gate` | `luna-core` | 1.4, 2.3 | O que foi editado e o que foi excluído viram candidato |
| 4.3 | Leitura acumulada por achado — `ADR-025` | ambos | 2.4, ratificação | Foto 2 soma ao contexto da 1 **sem reenviar imagem** |
| 4.4 | Pergunta opcional ao técnico | ambos | 4.3 | No máximo uma por leitura, sempre ignorável, nunca bloqueia concluir |

**Regra de custo na 4.3:** reenviar todas as imagens a cada foto nova faz o custo crescer ao
quadrado e estoura a cota do Groq na primeira ronda séria. Envia-se a imagem nova mais o
**texto** do que já foi entendido.

---

## Quando uma tarefa não couber na sessão

Acontece. Nesse caso:

1. **Não deixe pela metade sem registro.** Abra PR de rascunho com o que existe
2. Escreva no PR: o que foi feito, o que falta, e **onde parar de ler** para retomar
3. Marque a tarefa como `parcial` neste arquivo, com o número do PR
4. A próxima sessão retoma dali, sem reconstruir

**Isso é o mesmo problema da LUNA, aplicado a nós.** Sessão que acaba sem registro perde o
que aprendeu.

---

## Fora do plano, de propósito

**A LUNA em 3D no site.** Espera um `.glb`. Reconstruir a partir de foto foi o caminho
errado — seis rodadas provaram.

**Os 13 documentos corporativos.** APR, PGR, DDS, Certificados são formatos regulatórios
reais. Inventar a estrutura sem especialista entrega documento de conformidade
confiantemente errado.

**`.ppt` e PDF em produção.** Dependem do LibreOffice no contêiner do Railway — ação de
infraestrutura do Arquiteto.

**Trocar `/` por `/v2`.** PR de uma linha, depois da aprovação.

---

## Esperando decisão do Arquiteto

| O quê | A pergunta |
|---|---|
| Classificação por imagem | Soma ao veredito do achado ou substitui? E o nome do quarto valor |
| Relatório Visual | O que vem marcado por padrão? O Positivo entra? |
| Faixas de prazo do Sense | Quanto leva, na prática, agendar treinamento, revisar APR, trocar um controle |
| `ADR-025` e `ADR-026` | Ratificar |

Cada uma dessas é uma Issue com rótulo `duvida` esperando resposta — não precisa de sessão
para responder.
