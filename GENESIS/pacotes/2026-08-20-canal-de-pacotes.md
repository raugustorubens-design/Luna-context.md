# Quadro de trabalho no Supabase — do pacote ao as-built

**Caminho:** `GENESIS/pacotes/2026-08-20-canal-de-pacotes.md`
**Estado:** **bloqueado por gatilho**
**Desenho do Arquiteto, 20/08**

> ## REPOSITÓRIO-ALVO
>
> **`raugustorubens-design/luna-core`** — migração e leitura.
> **`raugustorubens-design/Luna-context.md`** — `COMO-FUNCIONA.md`.

---

## O que a tabela é

Não é caixa de entrada — **é o quadro de trabalho.** Cada um move o estado do que fez, e os
três enxergam a mesma coisa sem ninguém precisar relatar.

E o ciclo não termina no merge. Termina no **as-built**: o registro do que de fato ficou,
depois de verificado no mundo real.

---

## Os estados, e quem move cada um

| Estado | Quem move | O que significa |
|---|---|---|
| `novo` | Engenheiro | Escrito. Ninguém pegou |
| `em_desenvolvimento` | **Builder** | Reivindicado. **É o que impede duas sessões pegarem o mesmo** |
| `em_revisao` | **Builder** | PR aberto. Pede conferência |
| `aprovado` | Engenheiro | Revisado. Pode mergear |
| `mergeado` | Engenheiro | Confirmado **no repositório**, não no relatório |
| `verificado` | Arquiteto | Funciona no mundo real |
| `asbuilt` | Engenheiro | Registrado o que ficou, e onde diferiu do projeto |

**O Arquiteto move um só — e nem precisa abrir a tabela.** Basta dizer "conferi, funciona",
que o Engenheiro registra.

---

## Por que isso resolve a duplicata

O `em_desenvolvimento` é reivindicação, e ela acontece **antes da primeira linha de código**.

Duas sessões abrindo a mesma fila veem o mesmo quadro: o que está `novo` está livre, o que
está `em_desenvolvimento` já tem dono.

Foi exatamente o que faltou quando duas sessões escreveram o mesmo relatório em paralelo — e
funciona melhor que reivindicar Issue, porque fica **no mesmo lugar de onde o trabalho é
retirado**, não num sistema ao lado.

---

## O as-built

No seu ofício, as-built é o registro do que **de fato** foi construído, contra o que estava
projetado. Aqui é a mesma coisa.

Quando um item chega a `verificado`, o Engenheiro escreve:

- O que o pacote pedia
- O que foi entregue
- **Onde diferiu, e por quê**
- O que o Arquiteto conferiu em campo, e quando

E isso vai para o repositório, em `GENESIS/pacotes/ARQUIVO/`.

**Esta semana teve vários casos.** O Ofício em XLSX saiu com aviso em vez de tamanho exato,
porque a biblioteca não permitia. O portão de matiz foi entregue sem varrer o `globals.css`
— e era justamente onde o roxo estava. Nenhum dos dois estava no projeto; os dois estão no
que ficou.

**Sem as-built, essas diferenças moram só em conversa.**

---

## A divisão que evita dois livros-razão

| | Papel |
|---|---|
| **Tabela** | O que está **em andamento**. Estado ao vivo |
| **`GENESIS/pacotes/ARQUIVO/`** | O que está **concluído**. As-built, versionado, permanente |

Item que chega a `asbuilt` sai da tabela — o registro passa a viver no git.

A `FILA.md` deixa de guardar estado item a item e fica com o que já faz bem: ordem e
prioridade. **Estado num lugar só.**

---

## O ciclo do Builder

O `COMO-FUNCIONA.md` ganha um passo zero e um de saída:

**Ao começar:**

1. Ler a tabela. Commitar o que estiver `novo` em `GENESIS/pacotes/` e marcar `em_revisao`
2. Pegar o primeiro item **sem dono** e marcar `em_desenvolvimento` — antes de escrever
   qualquer linha
3. Executar

**Ao terminar:** abrir o PR e marcar `em_revisao`, com o número do PR na linha.

**Nunca:** executar pacote que ele mesmo commitou, antes de o PR ser mergeado. **Commitar
não é executar** — a janela de revisão do Arquiteto é o PR.

---

## As travas

**O Builder nunca deposita pacote.** Só lê, reivindica e marca.

**O Engenheiro nunca move `em_desenvolvimento`.** Se pudesse, atropelaria trabalho em curso.

**Conteúdo é descartável, estado não.** O texto sai da tabela quando vira arquivo no git; a
linha de estado fica até o as-built.

**Estado que ninguém move é pior que estado nenhum.** Cada transição está amarrada a algo
que já acontece — abrir PR, mergear, conferir em campo. Nenhuma exige lembrar de tarefa
extra.

---

## Pré-requisito do Arquiteto

A conexão do Engenheiro com o Supabase está como `postgres`, **na produção** — com poder de
apagar tabela e alterar coluna com dado dentro. Ele usa só leitura, mas o acesso está
aberto.

Crie uma conta com leitura geral e escrita apenas nesta tabela. Mesmo raciocínio que mantém
o Builder como único canal de escrita no GitHub: limitar o estrago possível, em vez de
confiar que ninguém erra.

---

## Gatilho — não execute antes

- A fila ficar sem item `pronto`, **ou**
- O Arquiteto carregar dois pacotes novos no mesmo dia, **ou**
- Ele mandar

---

## Critério de pronto

1. Tabela criada, com migração commitada (`ENG-036`)
2. O Engenheiro deposita um pacote de teste
3. A sessão seguinte **traz sozinha**, como PR, sem ninguém copiar nada
4. O Builder marca `em_desenvolvimento` antes de codar, e `em_revisao` ao abrir o PR
5. Depois do merge, o Engenheiro marca `mergeado` **conferindo o repositório**, não o relato
6. O Arquiteto verifica em campo e diz; o as-built é escrito e commitado

**Portão do Arquiteto:** abrir o quadro e enxergar, sem perguntar a ninguém, o que está
sendo feito agora e por quem.

---

## Memórias geradas

- Reivindicação antes da primeira linha resolve trabalho duplicado melhor que aviso depois,
  e funciona melhor no mesmo lugar de onde o trabalho é retirado
- Estado ao vivo no banco, histórico no repositório: um livro-razão para cada coisa
- As-built é o que separa o projetado do que ficou; sem ele, a diferença mora só em conversa
