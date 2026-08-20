# Ajustes do hero, barra e acesso — liberar relatórios aos colegas

**Caminho:** `GENESIS/pacotes/2026-08-20-hero-desktop-e-acesso.md`
**Estado:** pronto · **prioridade: o bloco de acesso tem prazo desta semana**

> ## REPOSITÓRIO-ALVO
>
> **`raugustorubens-design/luna-frontend`** — hero, barra, middleware.
> **`raugustorubens-design/luna-core`** — só o item 5b, atribuição de autor na ronda.

---

## Contexto

O hero foi aprovado no celular. **No PC ele fica espremido**: a coluna de texto mantém a
largura do celular e o título quebra quase uma palavra por linha — "Nada / do que / foi /
decidido".

E o acesso virou gargalo: o Arquiteto quer **liberar os relatórios aos colegas TSTs nesta
semana**.

---

## 1 · O hero no PC

**A composição vertical aprovada permanece** — imagem em cima, frase embaixo, centralizada.
O que muda é a escala.

Sintoma a corrigir: em 1366 px, a coluna de texto ocupa cerca de 200 px. O título quebra a
cada uma ou duas palavras.

**Alvo:** em telas de 1024 px ou mais, o título quebra em **duas ou três linhas**, não em
cinco. A imagem cresce proporcionalmente e ocupa a tela sem ficar perdida no meio.

Sugestão de pontos de partida, a conferir na tela real:

| | Celular | ≥ 1024 px |
|---|---|---|
| Largura da imagem | `min(78vw, 360px)` | `min(38vw, 460px)` |
| Largura da frase | `24ch` | `18ch` |
| Corpo do título | `clamp(2rem, 8.5vw, 3.6rem)` | até `4.6rem` |

**Investigue a causa antes de ajustar o número.** Uma coluna de 200 px em 1366 px não vem
do `max-width: 24ch` — 24 caracteres a 57 px dariam bem mais que isso. Há outra restrição
no caminho, e trocar o valor sem achá-la pode não resolver.

## 2 · A barra de ferramentas

**Fonte 50% maior, só na barra.** Os itens — Produtos, Estado, Como funciona, Tema claro —
estão pequenos demais em tela grande.

Não mexa em nenhuma outra tipografia da página.

## 3 · O nome dela no hero

Entre a linha "SISTEMA COGNITIVO PERSISTENTE" e o título, entra **LUNA**.

Como assinatura, não como segundo título: espaçamento de letra largo, corpo menor que o
título e maior que a linha de cima, na cor de acento. Ela nomeia quem está na imagem logo
acima.

## 4 · Migrar o que o site antigo faz

O `/v2` tem "Produtos", "Estado" e "Como funciona" na barra, e essas âncoras precisam de
destino.

**Levante o que existe hoje em `/` e reporte a lista antes de portar.** O Arquiteto vai
dizer o que vem e o que fica.

**Não porte texto explicativo.** A regra do painel do Convergia vale aqui: a página mostra
estado e produto; explicação mora na documentação.

---

## 5 · Acesso — o bloco com prazo

### 5a · A página é pública; a ferramenta é que pede login

Confirme o `matcher` do `middleware.ts`: só `/forge`, `/api/forge` e `/ronda` devem estar
lá. **Nenhuma rota de página.**

E o mais importante para o gargalo: **em nenhum lugar da página pública pode haver link
que leve à tela de acesso negado** sem avisar. Se houver botão que exija login, ele deve
ser visível apenas com sessão — como já foi feito com o Dev Mode.

### 5b · Antes de liberar aos colegas — a ronda não registra quem fez

**Este é o achado que bloqueia a liberação.**

Verificado no schema: `convergia_rondas` tem `id`, `ronda_id`, `metadata`, `achados`,
`encerramento`, `created_at`. **Nenhuma coluna de autor.**

Se três TSTs usarem esta semana, o histórico vira uma pilha só, sem saber de quem é cada
ronda. E o relatório sai sem identificar quem constatou — num documento técnico que a
pessoa assina, isso não se sustenta.

**Correção, e é pequena:**

- Coluna de autor em `convergia_rondas`, **com migração commitada antes de aplicar**
  (`ENG-036` — contornada três vezes esta semana, com produção quebrada em duas)
- Anulável: as rondas que já existem não têm autor e nunca terão
- Gravada a partir da sessão autenticada, **nunca vinda do cliente**
- A tela de histórico mostra só as rondas de quem está logado
- O relatório traz o nome de quem constatou

### 5c · Liberar os colegas

Acrescentar os e-mails em `RONDA_ALLOWED_EMAILS`, separados por vírgula, no painel do
Railway. **É configuração, não código.**

**Só depois do 5b.** Liberar antes significa misturar as rondas de todo mundo sem forma de
separar depois — e desfazer mistura custa muito mais que evitá-la.

---

## Pré-respostas

| Se encontrar | Faça |
|---|---|
| A coluna estreita vindo de outro componente | Corrija na origem e **reporte onde estava** |
| `convergia_rondas` já com coluna de autor | Confirme e siga para o 5c |
| Rota de página no `matcher` | Remova e reporte qual era |
| Âncora da barra sem destino | Reporte a lista; **não invente seção** |

## Condições de parada

- O item 5b exigir alterar coluna existente com dado dentro
- A adaptação do hero exigir mudar a composição aprovada no celular
- Migrar o site antigo exigir decisão sobre o que entra — **é do Arquiteto**

## Autorização de merge

**Itens 1, 2, 3 e 5a:** pode mergear com os portões verdes.

**Item 5b:** abra o PR e reporte. Toca schema em produção.

**Item 4:** reporte a lista antes de portar qualquer coisa.

---

## Critério de pronto

1. No PC, o título quebra em duas ou três linhas, e a imagem ocupa a tela
2. No celular, **nada mudou** — a versão aprovada continua igual
3. A barra legível em tela grande
4. LUNA entre a linha de sistema e o título
5. Nenhuma rota de página no `matcher`
6. A ronda registra quem a fez, e o histórico mostra só as próprias

**Portão do Arquiteto:** abrir o `/v2` no PC e no celular, e um colega TST entrar, fazer uma
ronda e gerar um relatório com o nome dele.

---

## Memórias geradas

- Layout aprovado no celular não sobe para tela grande sozinho: composição vertical
  centralizada precisa de escala declarada por faixa
- Ferramenta de campo multiusuário exige atribuição de autor **antes** do primeiro usuário
  extra; depois, separar o que se misturou custa muito mais
- Documento técnico que a pessoa assina precisa dizer quem constatou
