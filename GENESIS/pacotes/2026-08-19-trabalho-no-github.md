# Trabalho no GitHub — Issues como unidade

**Caminho:** `GENESIS/pacotes/2026-08-19-trabalho-no-github.md`
**Estado:** pronto

> ## REPOSITÓRIOS-ALVO
>
> **`raugustorubens-design/luna-core`** e **`luna-frontend`** — Issues e rótulos.
> **`Luna-context.md`** — atualização do `COMO-FUNCIONA.md`.
>
> Nenhum código de produto muda neste pacote.

---

## Por que agora

Hoje duas sessões escreveram o mesmo relatório Detalhado, em paralelo. Os PRs `#49` e
`#51` têm o mesmo título e o mesmo `+236 −18`. Um foi fechado, o outro entrou — nada se
perdeu, mas metade do trabalho foi jogado fora.

Não foi descuido de ninguém. **Nenhuma das duas tinha como saber que a outra existia.**

Arquivo commitado não avisa. Issue avisa, tem estado nativo, e pode ser reivindicada antes
de o trabalho começar.

---

## A divisão que evita o erro comum

| | Onde vive | Por quê |
|---|---|---|
| **A especificação** | `GENESIS/pacotes/*.md` | É registro durável, versionado, e sobrevive ao fechamento |
| **A coordenação** | **Issue** | É efêmera: quem está fazendo, em que pé está, o que travou |

**Não copie o pacote para dentro da Issue.** A Issue aponta para o arquivo. Duas cópias
divergem, e a que o Builder lê nunca é a que o Arquiteto editou — foi o que aconteceu cinco
vezes esta semana com anexo.

---

## Etapa 1 · Rótulos

Criar nos dois repositórios de código:

| Rótulo | Uso |
|---|---|
| `marco-1` a `marco-4` | O marco do plano de produção |
| `duvida` | Espera resposta do Arquiteto — **notifica o celular** |
| `pendente-campo` | Mergeado, falta verificação em produção |
| `bloqueado` | Depende de outra tarefa ou de decisão |
| `decisao` | Só o Arquiteto resolve; não é trabalho de sessão |

## Etapa 2 · Abrir uma Issue por tarefa do plano

Título curto. Corpo com **três linhas apenas**:

```
Pacote: GENESIS/pacotes/<arquivo>.md · seção <n>
Depende de: #<issue> (ou nada)
Pronto quando: <o critério, em uma frase>
```

Nada além disso. O detalhe está no pacote.

## Etapa 3 · A regra que impede a duplicata

> **Antes de escrever uma linha, atribua a Issue a si mesmo e comente "iniciando".**

É o passo que faltou hoje. Custa dez segundos e torna o trabalho paralelo visível.

E ao abrir o PR, feche pelo corpo: `Closes #<n>`. O estado passa a ser automático.

**Se a Issue já estiver atribuída, não comece.** Pegue a próxima sem atribuição.

## Etapa 4 · Dúvida vira Issue, não parada

Ao esbarrar numa condição de parada:

1. Abrir Issue com rótulo `duvida`, título `[dúvida] <assunto em cinco palavras>`
2. Corpo: o que ia fazer, as opções, e **uma recomendação com o motivo**
3. Marcar a Issue da tarefa como `bloqueado`, referenciando a dúvida
4. **Pegar a próxima tarefa livre**

Uma dúvida trava uma tarefa, não a fila.

Escreva para ser lido no celular: opções numeradas, curtas. Se a resposta couber em "1" ou
"2", o Arquiteto responde em dez segundos.

## Etapa 5 · Atualizar o `COMO-FUNCIONA.md`

O ciclo passa a ser: ler Issues abertas sem atribuição, do menor marco → atribuir a si →
ler o pacote → executar → `Closes #n`.

O `FILA.md` sai. O `PLANO-DE-PRODUCAO.md` fica, como o mapa dos marcos.

O `PENDENTE.md` fica também — o rótulo `pendente-campo` cobre o mesmo, mas o arquivo é o
registro durável, e Issue fechada some da vista.

---

## Etapa 6 · Resolver a duplicação que já existe

**Primeira Issue a abrir**, rótulo `decisao`.

Hoje há **um** adaptador — `relatorio-detalhado-adapter.ts` — e **dois** templates:

| Template | Renderizador | Origem |
|---|---|---|
| `relatorio-ronda-detalhado.ts` | docx | PR `#51`, à noite |
| `relatorio-ssma-tabular.ts` | xlsx | anterior, genérico |

Investigar e reportar: são o mesmo relatório em dois formatos, ou o tabular é genérico para
outro uso — como registros de ASO — e não concorre?

**Se concorrerem:** minha recomendação é ficar com o **docx**. O relatório precisa mostrar
foto, e planilha não é formato de leitura. O tabular permanece, mas explicitamente marcado
como genérico, não como relatório de ronda.

**Registrar a decisão no `BUILDER.md`.** Sem isso, daqui a três meses ninguém sabe por que
existem dois, e alguém corrige o errado.

---

## Pré-respostas

| Se encontrar | Faça |
|---|---|
| Rótulo já existe com outro nome | Use o existente e registre a equivalência |
| Issue sem `Pronto quando` | Abra `duvida` — sem critério, tarefa não fecha |
| Tarefa maior que uma sessão | PR de rascunho, comentar na Issue o que falta e onde retomar, marcar `parcial` |
| Dois templates forem complementares | Documente a diferença e siga; não remova nada |

## Condições de parada

- A investigação da etapa 6 indicar que remover algo é necessário
- Uma tarefa do plano não tiver critério de pronto
- Issue atribuída a outra sessão cobrir o que você ia fazer

## Autorização de merge

Etapas 1 a 5: pode mergear. São rótulos, Issues e documentação.

Etapa 6: **abrir a Issue e reportar.** Não remover template sem decisão do Arquiteto.

---

## Critério de pronto

Uma sessão nova consegue começar sozinha com **uma frase**:

> *Leia `GENESIS/pacotes/COMO-FUNCIONA.md` e pegue a próxima Issue sem atribuição.*

E o Arquiteto vê, no celular, o que está em andamento, o que travou e o que espera ele —
sem abrir o computador.

---

## Memórias geradas

- Coordenação de trabalho paralelo precisa de reivindicação **antes** do início; PR de
  rascunho avisa tarde demais
- Especificação e coordenação vivem em lugares diferentes: arquivo versionado guarda,
  Issue coordena
- Duas implementações do mesmo entregável não geram conflito de merge quando estão em
  arquivos diferentes — o custo aparece meses depois
