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
