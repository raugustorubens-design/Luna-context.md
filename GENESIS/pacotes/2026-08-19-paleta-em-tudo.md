# Fundo novo em todas as superfícies — e o roxo que sobrou

**Caminho:** `GENESIS/pacotes/2026-08-19-paleta-em-tudo.md`
**Estado:** pronto

> ## REPOSITÓRIO-ALVO
>
> **`raugustorubens-design/luna-frontend`** — exclusivamente.
> Escopo: `app/globals.css` e, se necessário, `tailwind.config.ts`.
> **Nenhum componente é alterado.**

---

## O que o `#36` deixou para trás

O pacote anterior mudou os tokens `--luna-*`, que são lidos por `.luna-v2` — ou seja,
`/v2` e `/forge?layout=v2`. **As outras superfícies não leem daquele bloco.**

Duas coisas ficaram:

### 1 · Roxo literal, ainda no `body`

```css
body {
  background-image:
    radial-gradient(circle at 20% 10%, rgba(124, 58, 237, 0.24), transparent 35%),
    radial-gradient(circle at 80% 20%, rgba(34, 211, 238, 0.16), transparent 30%),
    radial-gradient(circle at 40% 80%, rgba(167, 139, 250, 0.14), transparent 35%);
}
```

**`#7C3AED` em matiz 262° e `#A78BFA` em 255°** — os dois hexes que o pacote do roxo mandou
caçar, vivos, pintando manchas atrás de **todas** as superfícies. A única que escapa é
`/ronda`, porque `.ronda-locked body` declara `background-image: none`.

O ciano do meio (`#22D3EE`, matiz 188°) também está fora da faixa, pelo lado verde.

### 2 · O Forge antigo e o Convergia leem outro conjunto

Componentes antigos leem os tokens do shadcn — `--background`, `--primary`, `--border`. O
ADR-022 os religou para **Midnight**:

```css
--background: 231 53% 25%;   /* #1E2761 */
```

É por isso que o Forge que você abriu está com o fundo antigo: **ele nunca recebeu a
inversão.** O painel do Convergia vive dentro dele e herda o mesmo.

---

## Etapa 1 · Tirar o roxo do `body`

Substituir os três degradês por dois, dentro do portão de matiz e do orçamento de luz — a
emissão fria fica abaixo de 5% da tela:

- Um azul frio, na família 204°–216°, opacidade baixa
- Um dourado quente, 34°–52°, ainda mais discreto

Comentar os valores anteriores ao lado, como os outros blocos fazem. Reverter é apagar.

**Nada de violeta.** Se algum hex fora das duas faixas sobrar, o teste do portão de matiz
deve reprovar — e se não reprovar, o teste tem um buraco e isso também precisa ser
reportado.

## Etapa 2 · A inversão alcança os tokens do shadcn

Bloco aditivo no fim do arquivo, mesmo padrão: valor anterior comentado ao lado.

| Token | Vira | Papel |
|---|---|---|
| `--background` | `#000206` | página |
| `--muted` | Midnight composto sobre `#000206` | superfície |
| `--secondary` | Midnight mais forte | superfície elevada |
| `--border` | derivado de `#7088A0` | linha |
| `--foreground` | `#DCE6F2` | texto |
| `--primary` · `--ring` | `#A0B8C8` | acento |
| `--luna-cyan` | `#A0B8C8` | usado por `.forge-accent-text` |

**Mantenha `--destructive` como está** — `#C62828` é classificação e não muda.

**Não toque em `--radius`.** Ele é global e três telas de `/ronda` usam `rounded-lg`; mexer
mudaria a ronda, que já foi validada.

**O shadcn lê `hsl(var(--token))` sem alfa**, então as superfícies entram aqui já compostas
sobre o `#000206`, como o bloco do ADR-022 já explica.

## Etapa 3 · Marcar o legado

`--luna-violet` continua declarado — pode haver componente antigo lendo. **Não remova.**
Comente como legado, proibido em superfície nova.

Mesma coisa para `luna.success` e `luna.danger` no Tailwind, se ainda não estiverem
comentados: classificação é `ok`, `warn`, `fail`.

---

## Pré-respostas

| Se encontrar | Faça |
|---|---|
| Outro hex violeta em qualquer arquivo | Troque e **reporte onde estava** |
| `.glass` usando `bg-white/5` | Deixe. É utilitário antigo; trocar mexe em componente |
| O teste do portão de matiz não pegar o roxo do `body` | **Reporte** — o teste tem buraco |
| Componente antigo ficando ilegível após a inversão | Reporte com o nome do arquivo; não altere o componente |

## Condições de parada

- A inversão exigir alterar componente, e não só token
- `/ronda` mudar de aparência de qualquer forma
- Remover um token existente parecer necessário

## Autorização de merge

**Pode mergear** após os portões automáticos. É aditivo e reversível apagando os blocos.

**Mas entra no `PENDENTE.md`:** muda o que o Arquiteto vê no Forge e no Convergia, e ele
precisa conferir.

---

## Critério de pronto

Automático: `typecheck`, testes sem alteração, `test:constitution` — **incluindo o portão de
matiz** —, `build`.

**Portão do Arquiteto:**

1. `/forge` — fundo quase preto, painéis destacando dele, sem mancha violeta
2. `/forge?tab=convergia` — mesma coisa no painel do Convergia
3. `/` — sem mancha violeta atrás do conteúdo
4. **`/ronda` sem nenhuma mudança.** É a trava: se algo lá mudar de cor, a inversão passou do
   escopo e o bloco se reverte apagando

O item 4 é o que mais importa. As cores da ronda foram validadas em campo ontem.

---

## Memórias geradas

- Religação por token alcança só quem lê aquele token; `body` tem fundo próprio e escapa de
  qualquer inversão de variável
- `#7C3AED` e `#A78BFA` estavam no `body` desde antes do ADR-022 e sobreviveram a dois
  pacotes de paleta
- Superfície escopada por classe (`.luna-v2`, `.ronda-locked`) não herda inversão feita em
  `:root` — o escopo protege nos dois sentidos
