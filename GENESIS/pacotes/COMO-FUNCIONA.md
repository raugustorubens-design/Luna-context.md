# Como funciona a fila

**Caminho:** `GENESIS/pacotes/COMO-FUNCIONA.md`
**Vigente desde:** 19/08/2026

Este arquivo é lido pelo Claude Code no início de cada sessão. Ele diz o que pegar, quando
parar, e como perguntar.

---

## O ciclo

1. Ler **`FILA.md`** e pegar o primeiro item com estado `pronto`
2. Ler o pacote correspondente em `GENESIS/pacotes/`
3. Executar, **um PR por etapa**
4. Ao concluir: atualizar `FILA.md`, `PENDENTE.md` e `GENESIS/STATUS.md`
5. Voltar ao passo 1

**Um item por vez.** Não começar dois.

---

## Emenda — `GENESIS/pacotes/2026-08-20-canal-de-pacotes.md`, 20/08/2026

O ciclo acima continua valendo como descrição geral — mas o **estado ao vivo** de cada
item deixa de morar item a item na `FILA.md` e passa a morar na tabela
`genesis_pacote_fila`, no Supabase (`jdbzhrtovpoaafpytgza`), criada por
`luna-core/supabase/migrations/20260820_genesis_pacote_fila.sql`. `FILA.md` continua
existindo, mas volta a fazer só o que sempre fez bem: ordem e prioridade — não mais o
lugar onde o estado de cada item é registrado.

**Colunas:** `pacote` (caminho do arquivo), `repositorio`, `estado`, `pr_url`, `dono`,
`notas`, `criado_em`, `atualizado_em`. Sete estados possíveis (`CHECK` na coluna):
`novo` → `em_desenvolvimento` → `em_revisao` → `aprovado` → `mergeado` → `verificado` →
`asbuilt`.

| Estado | Quem move | O que significa |
|---|---|---|
| `novo` | Engenheiro | Escrito. Ninguém pegou |
| `em_desenvolvimento` | **Builder** | Reivindicado — impede duas sessões pegarem o mesmo |
| `em_revisao` | **Builder** | PR aberto. Pede conferência |
| `aprovado` | Engenheiro | Revisado. Pode mergear |
| `mergeado` | Engenheiro | Confirmado **no repositório**, não no relatório |
| `verificado` | Arquiteto | Funciona no mundo real |
| `asbuilt` | Engenheiro | Registrado o que ficou, e onde diferiu — o item então sai da tabela |

### Passo zero — antes do passo 1 de sempre

1. Ler a tabela `genesis_pacote_fila`. Para cada linha em `novo`: commitar o texto do
   pacote em `GENESIS/pacotes/` (PR documental próprio) e marcar essa linha
   `em_revisao` — o commit em si é o que pede conferência do Arquiteto, não a execução.
2. Entre as linhas **sem dono** (nenhuma marcada `em_desenvolvimento`), pegar a
   primeira — e marcar `em_desenvolvimento` **antes de escrever qualquer linha de
   código**. É o que substitui a reivindicação de Issue do pacote
   `2026-08-19-trabalho-no-github.md` para itens que vierem por esta tabela.
3. Executar, como sempre — um PR por etapa (passo 3 do ciclo original).

### Passo de saída — além do passo 4 de sempre

Ao abrir o PR do que foi executado: marcar a linha `em_revisao`, com o `pr_url`
preenchido. Depois do merge (confirmado no repositório, não relatado), quem revisa move
para `mergeado`. Quando o Arquiteto confirmar em campo, a linha vai para `verificado`, e
o Engenheiro escreve o as-built — o que o pacote pedia, o que foi entregue, onde
diferiu e por quê, o que foi conferido em campo e quando — em
`GENESIS/pacotes/ARQUIVO/`. Só então a linha sai da tabela (`asbuilt` é terminal, o
registro passa a viver no git).

**Trava permanente:** o Builder nunca deposita pacote na tabela (só o Engenheiro
escreve `novo`) e nunca executa um pacote que ele mesmo acabou de commitar antes de o
PR do commit ser mergeado — commitar não é executar; a janela de revisão do Arquiteto é
o PR. O Engenheiro nunca move `em_desenvolvimento` — só o Builder, e só antes de
codar.

---

## Quando parar e perguntar

Pare **apenas** nestes casos:

- O pacote pressupõe algo que não existe mais no repositório
- Duas soluções possíveis, e a escolha depende de intenção, não de técnica
- A correção exigiria **remover** ou **reescrever** algo existente
- Um teste que passava começou a falhar por motivo não relacionado
- O pacote manda parar explicitamente

**Fora desta lista, decida e siga.** Registre o que decidiu no corpo do PR.

Isto inverte o padrão anterior: em vez de decidir se deve perguntar, a regra diz quando
**não** perguntar. Rebase, conflito de posição cronológica, contagem de teste que subiu,
arquivo já alterado por outro PR — tudo isso é decidível, e o pacote traz a pré-resposta.

---

## Como perguntar

**Abra uma Issue** no repositório onde o trabalho acontece.

- **Título:** `[dúvida] <pacote> — <assunto em cinco palavras>`
- **Rótulo:** `duvida`
- **Corpo:** o que você ia fazer, as opções que enxerga, e o que cada uma implica.
  **Recomende uma** e diga por quê

Issue notifica o celular do Arquiteto; arquivo commitado não notifica ninguém. Ele responde
por comentário, você lê o comentário e segue.

**Escreva para ser lido no celular:** curto, com as opções numeradas. Se a resposta couber
em "1" ou "2", ele responde em dez segundos.

---

## O que fazer enquanto espera

**Não fique parado.** Marque o item como `bloqueado` na `FILA.md`, com o número da Issue, e
**pegue o próximo item `pronto`**.

Uma dúvida trava um pacote, não a fila.

---

## Ao concluir um pacote

**`FILA.md`** — item vai para `concluído`, com o número do PR e a data.

**`PENDENTE.md`** — se ficou alguma verificação que só o Arquiteto pode fazer (abrir no
celular, conferir em produção), **acrescente ali**. Esta é a trava mais importante do
processo: trabalho autônomo acumula mudança não verificada, e sem esse registro o estoque
fica invisível.

**`GENESIS/STATUS.md`** — atualize PRs mergeados, contagem de teste e o que mudou de
estado. É o arquivo que o Engenheiro lê no início da sessão para não reconstruir o quadro
do zero.

**`GENESIS/BUILDER.md`** — autoatestação no padrão em uso: o que foi verificado neste
ambiente **versus** o que foi reportado sem confirmação.

**Memórias geradas** — se o pacote pedir, submeta as afirmações verificáveis pelo
`knowledge-gate`. É o que faz a LUNA aprender da engenharia, não só das rondas.

---

## Regras permanentes

- **Nada é removido ou substituído.** Se parecer necessário, é caso de parar
- **Nenhum teste existente pode ser alterado** para um novo passar
- **Foto nunca é obrigatória**, em nenhum caminho
- **`git merge-base origin/main HEAD`** batendo com a ponta de `origin/main` antes do
  primeiro commit de cada branch
- **Repositório-alvo explícito** no topo de todo pacote — nunca assumir pelo contexto
- **Feito = clicado e visto funcionando em produção.** Teste verde é estado intermediário

---

## Autorização de merge

Cada pacote declara o que pode ser fechado. **Fora do declarado, não mergeie.**

Etapa com portão de campo **pode** mergear sem esperar o Arquiteto, desde que entre no
`PENDENTE.md`. Foi o que funcionou em 18/08; o que faltou naquele dia foi exatamente o
registro.
