# Três correções — retorno do login, imagem da LUNA, Forge no celular

**Caminho:** `GENESIS/pacotes/2026-08-20-tres-correcoes.md`
**Estado:** pronto

> ## REPOSITÓRIO-ALVO
>
> **`raugustorubens-design/luna-frontend`** — exclusivamente.
> Escopo: `auth.ts`, `components/site/**`, `components/forge/forge-layout-v2.tsx`.

---

## 1 · O login volta para o lugar errado

**Sintoma:** entra pelo `/ronda`, o Google aprova, e cai no site antigo.

**Causa:** o `middleware.ts` monta o endereço de login **com** `callbackUrl` apontando para
onde a pessoa estava. Mas o `auth.ts` **não tem o callback `redirect`** — e sem ele o
Auth.js devolve sempre a raiz, ignorando o `callbackUrl` que o middleware teve o cuidado de
montar.

**Correção:** acrescentar `redirect` em `callbacks`, no `auth.ts`:

- Endereço relativo → `baseUrl + url`
- Mesma origem → o próprio `url`
- Origem diferente → `baseUrl`

A terceira regra não é detalhe: sem ela, um `callbackUrl` forjado apontando para fora vira
redirecionamento aberto.

**Isso resolve o sintoma inteiro.** Entrou pelo `/ronda`, volta para o `/ronda`. Entrou
pelo Forge, volta para o Forge.

**Teste:** um por rota — `/ronda`, `/forge`, `/forge?layout=v2&tab=convergia` — e um caso
com origem externa, que deve cair na raiz.

---

## 2 · A imagem da LUNA está concorrendo com o texto

**Pedido do Arquiteto:** plano de fundo, transparente, sem concorrer com o texto.
**Como está:** acima do início do site, disputando espaço.

Ela é **camada de fundo**, e isso significa cinco coisas:

- **Atrás do conteúdo**, com `pointer-events: none` — não recebe clique, não seleciona
- **Não empurra nada.** Posicionamento absoluto ou fixo; não ocupa espaço no fluxo
- **Não fica atrás do título.** Ancorada à direita, com o rosto fora da coluna de texto
- **Bordas dissolvidas** por máscara radial, para não ter recorte visível
- **Opacidade baixa** — ver a regra abaixo

### A regra que não pode ser estimada

Se a imagem ficar atrás de qualquer texto, **o fundo daquele texto deixa de ser
`#000206`** — passa a ser a composição do `#000206` com a imagem.

Os contrastes do `PADRAO-SMX-CORES.md` foram calculados contra o fundo puro. **Meça o
composto**, na região mais clara da imagem, e confirme que o texto continua acima de 4,5:1.
Se não passar, **baixe a opacidade até passar** — não mude a cor do texto.

Ponto de partida: 12% a 18%. Mas o número vale menos que a medição.

### E ela conta no orçamento de luz

A imagem tem regiões claras. Pelo padrão, emissão fria fica abaixo de 5% da tela — a
imagem entra nessa conta. Se ela acender demais, o resto da página precisa apagar.

### No celular

Em tela estreita ela quase certamente atrapalha, porque não há coluna livre à direita.
**Ou some, ou fica bem mais fraca e recuada.** Testar nos dois.

---

## 3 · O Forge quebra no celular

O layout v2 é grade de várias colunas — Explorer, editor, chat, gaveta do terminal. Isso
não cabe em 390 pixels de largura, e forçar produz o que você viu.

**Não tente espremer a grade.** Em tela estreita, o Forge vira **um painel por vez**, com
troca por aba ou pela trilha de atividade.

Ordem de prioridade quando só cabe um: **chat**, depois **terminal**, depois **Convergia**.
Explorer e editor não servem para nada num celular.

**O terminal continua montado**, mesmo invisível — desmontar mata a sessão do shell. É a
mesma razão registrada no ADR-022.

**Se o esforço for grande**, a alternativa honesta é mostrar, em tela estreita, um aviso de
que o Forge é ambiente de trabalho para tela grande, com atalho para o Safety Walk. É melhor
que uma tela quebrada — e o Arquiteto decide qual dos dois.

---

## Pré-respostas

| Se encontrar | Faça |
|---|---|
| `redirect` já existir no `auth.ts` | Confira as três regras; a de origem externa é a que costuma faltar |
| A imagem estiver no fluxo, ocupando espaço | Tire do fluxo; não ajuste margem para compensar |
| O contraste composto reprovar | Baixe a opacidade. **Nunca clareie o texto** |
| A grade do Forge exigir refazer o componente | Reporte antes; talvez o aviso em tela estreita resolva por ora |

## Condições de parada

- Adaptar o Forge exigir refazer o layout v2 que o Arquiteto aprovou
- A imagem não conseguir passar no contraste em nenhuma opacidade útil
- Qualquer correção exigir remover comportamento existente

## Autorização de merge

**Item 1 pode mergear sozinho, e primeiro.** É pequeno, é o que mais incomoda, e não depende
dos outros dois.

Itens 2 e 3: abra o PR e reporte — são visuais, e quem julga é o Arquiteto.

---

## Critério de pronto

**1 ·** Entrar pelo `/ronda` e voltar ao `/ronda`. Mesma coisa pelo Forge.

**2 ·** A imagem atrás do conteúdo, sem empurrar nada, sem recorte visível, e o contraste
do texto **medido** sobre o composto.

**3 ·** Abrir o Forge no celular e ter algo utilizável — um painel por vez, ou o aviso.

**Portão do Arquiteto:** os três, no aparelho dele.

---

## Memórias geradas

- `callbackUrl` montado no middleware não vale nada sem o callback `redirect` no `auth.ts`
- Imagem de fundo atrás de texto muda o fundo efetivo: o contraste precisa ser medido sobre
  o composto, não sobre a cor da página
- Grade de várias colunas não vira celular por ajuste; vira um painel por vez
