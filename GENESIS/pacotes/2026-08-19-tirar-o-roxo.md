# Pacote do Engenheiro — tirar o roxo do site

> ## REPOSITÓRIO-ALVO
>
> **`raugustorubens-design/luna-frontend`** — exclusivamente.
> Escopo: `app/globals.css`, `tailwind.config.ts`, `components/site/**`,
> `components/forge/**` (só os arquivos `*-v2` e novos).
>
> **NÃO TOCAR:** `app/ronda/`, `components/ronda/`, `lib/ronda/`. As cores do
> Safety Walk têm pacote próprio e portão de campo próprio.

**Norma que este pacote aplica:** `GENESIS/padroes/PADRAO-SMX-CORES.md`, na `main` do
`Luna-context.md`. Adotada pelo `ADR-024`.

---

## O problema, medido

O que está no ar em `/v2` usa **Midnight `#1E2761` como fundo de página**. Ele tem matiz
**232°**. O azul da logo SMX está em **215°**.

Dezessete graus para o violeta. Em selo pequeno ninguém nota; cobrindo a tela inteira, com
69% de saturação, vira a impressão dominante. **O Arquiteto leu como roxo, e está certo.**

E há roxo literal em pelo menos dois lugares, herdados de tema de editor emprestado.

---

## Etapa 1 — caçar o roxo declarado

Antes de qualquer troca, **procure e reporte** estes valores no repositório:

```
#7C3AED   #A78BFA   #8B5CF6   #6D3FD1   #9333EA   violet   purple
```

Onde eles aparecerem:

| Lugar | O que fazer |
|---|---|
| `tailwind.config.ts`, chave `luna.violet` | **Não remova.** O Modo Usuário v1 pode usar. Comente como token legado, proibido em superfície nova |
| Coloração de sintaxe do Forge v2 (`--t-key` ou equivalente) | **Trocar.** Palavra-chave passa a ser `#48A8E4`; no tema claro, `#003C90` |
| Qualquer degradê ou sombra em `components/site/**` | Trocar pelos azuis da rampa |

**Reporte a lista antes de trocar.** Se aparecer roxo em lugar que eu não previ, quero
saber onde.

---

## Etapa 2 — inverter a hierarquia de superfície

Bloco de religação **no fim** de `app/globals.css`, com o valor anterior comentado em cada
linha. Reverter = apagar o bloco.

| Token | Antes | Depois |
|---|---|---|
| Página | `#1E2761` | **`#000206`** |
| Degradê do herói | `#05060B → #1E2761` | `#1E2761 → #000206` |
| Superfície | branco 3% | `rgba(30,39,97,.38)` — Midnight translúcido |
| Superfície 2 / 3 | branco 6% / 9% | Midnight 55% / 78% |
| Linhas | branco 10 / 15 / 25% | `rgba(112,136,160,.16 / .28 / .46)` |
| Texto | `#F4F6FB` | `#DCE6F2` |
| Acento | `#22D3EE` | **`#A0B8C8`** |

**O Midnight não sai do sistema — muda de papel.** Deixa de cobrir a página e passa a ser
a superfície que emerge dela. Continua idêntico no `themeColor` do PWA, no relatório
impresso e no texto sobre âmbar. É a única correção que não pede para desfazer nada já
validado.

**Sobre o acento:** `#22D3EE` está em matiz 188° — 27° para o lado verde. Também está fora
da família. `#A0B8C8` é o tom em que o holograma aparece nas imagens de referência, com
10:1 de contraste sobre o fundo novo.

**Texto `#DCE6F2` e não `#F4F6FB`:** sobre quase preto, branco quase puro cintila.

---

## Etapa 3 — acrescentar a rampa ao Tailwind

**Só acrescentar.** Nenhuma chave existente sai:

```ts
void: "#000206", str1: "#001428", str2: "#001E3C", str3: "#0A283C", str4: "#143A5A",
glow1: "#3068A0", glow2: "#5A7896", glow3: "#7088A0",
glow4: "#8098B0", glow5: "#A0B8C8", spec: "#F8F8F8",
warm3: "#C09030", warm4: "#E4B448", warm5: "#F8E8A0",
```

**Armadilha conhecida:** já convivem `luna.success` `#10B981` com `luna.ok` `#2E7D32`, e
`luna.danger` `#EF4444` com `luna.fail` `#C62828`. Dois verdes e dois vermelhos com nomes
igualmente plausíveis. Comente as antigas como legado — classificação é `ok` / `warn` /
`fail`, sempre.

---

## Etapa 4 — o portão de matiz, em teste

Para o roxo não voltar em três meses, acrescente ao `constitution-check` uma regra sobre
`components/site/**` e os arquivos `*-v2`:

> Toda cor literal em hexadecimal precisa cair entre **200° e 220°** (azul) ou **17° e 55°**
> (dourado). Exceções declaradas: `#2E7D32`, `#E8A33D`, `#C62828`, `#1E2761`, `#FFFFFF`,
> `#000206` e derivados da rampa.

É a mesma disciplina do check de módulo de banco: a regra existe porque a intenção não
sobrevive à pressa. **Trave em teste**, com um caso positivo e um negativo — `#A78BFA` em
275° tem que reprovar.

---

## Verificação

`pnpm typecheck` · `pnpm test` (nenhum existente alterado) · `pnpm run test:constitution` ·
`pnpm build`.

**Portão real, do Arquiteto:**

1. Abrir `/v2` e o fundo estar **quase preto**, não azul-violeta
2. Cartão e painel aparecerem em Midnight, distintos do fundo
3. Alternar para o tema claro e conferir
4. Abrir `/ronda` **no celular** e confirmar que **nada mudou** — é a trava que prova que a
   religação não vazou de escopo

O item 4 é o que importa mais. `/ronda` usa valores diretos e classes próprias; se algo lá
mudar de cor, o bloco de religação passou do limite e deve ser revertido.

---

## O que este pacote não faz

- Não migra as cores do `/ronda` — pacote próprio, portão de campo próprio
- Não troca a página inicial `/` por `/v2` — é um PR de uma linha, depois da sua aprovação
- Não mexe na tipografia. Archivo continua; a troca para Manrope é etapa separada
