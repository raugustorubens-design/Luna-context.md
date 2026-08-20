# Padrão SMX de Cores

**Caminho:** `GENESIS/padroes/PADRAO-SMX-CORES.md`
**Status:** vigente a partir de 17/08/2026
**Autoridade:** norma para toda superfície visual de todo projeto da SMX eXperience teCnollogy
**Companheiro:** `PADRAO-SMX-DESIGN.md` — aquele governa **como** se desenha; este, **com que cor**
**Adotado por:** ADR-024
**Emenda parcial de:** ADR-022 (`ADR/ADR-022-paleta-e-redesenho.md`, hierarquia de superfície)

---

> **Nota de nomenclatura (17/08/2026).** Este documento circulou como
> "Padrão de Cores LUNA". O nome estava errado: LUNA é produto, e estas cores
> saem da logo da **SMX** e das imagens de referência da empresa. A norma é da
> SMX e vale para todo projeto dela — a LUNA é o primeiro a adotá-la, não a dona.

## 1. De onde estes valores vêm

Nenhuma cor deste documento foi escolhida por gosto. Todas foram **extraídas por
medição** de dois conjuntos de material já existente:

**A logo `SMX eXperience`** — amostrada pixel a pixel, isolando por matiz e
saturação as regiões da lua, da estrela, das letras `SMX`, do `X`, do
`eXperience` e da assinatura.

**Três imagens de referência da LUNA** — o android com o disco `LUNA CORE`, o
busto com a constelação craniana, e a cena de escritório com holograma. Cada
imagem foi classificada pixel a pixel em quatro faixas funcionais.

O método está no anexo A e é reproduzível: rodar de novo sobre os mesmos
arquivos devolve os mesmos números.

**O que este documento não decide.** As três cores de classificação
(`#2E7D32`, `#E8A33D`, `#C62828`) não saem daqui. Vêm do protótipo de relatório
impresso, foram medidas em contraste e validadas em ronda de campo. São a única
exceção permanente às regras abaixo.

---

## 2. A regra principal — orçamento de luz

Esta é a descoberta mais importante da extração, e a mais fácil de violar sem
perceber.

Classificação por faixa, em contagem real de pixel:

| Imagem | Ambiente | Material | Emissão fria | Emissão quente |
|---|---|---|---|---|
| Android · LUNA CORE | 70,1% | 22,8% | 0,5% | 5,4% |
| Busto · constelação | 54,8% | 39,1% | 4,4% | 0,9% |
| Escritório · holograma | 78,2% | 13,9% | 0,1% | 7,6% |
| **Média** | **67,7%** | **25,3%** | **1,7%** | **4,6%** |

> **A emissão fria nunca passa de 5% da imagem.**
> Na cena com o holograma inteiro projetado, ela é **0,1%**.

O que produz a sensação de sistema tecnológico em operação **não é a cor do
brilho — é a escassez dele.** Uma interface que acende bordas, ícones, rótulos e
títulos ao mesmo tempo passa de 20% de emissão e perde a atmosfera: vira painel
de aeroporto.

**Limites operacionais derivados desta medição:**

- Num cartão: **no máximo um** elemento acima de `glow-3`
- Numa tela: **no máximo três**
- Se for preciso um quarto, algum daqueles elementos não é tão importante
  quanto parece — a solução é remover destaque, não adicionar

**Emissão quente nunca é elemento de interface.** Nas imagens ela aparece
exclusivamente como bokeh fora de foco, luz de ambiente. Na tela, o mesmo:
atmosfera de fundo, halo, partícula. Nunca botão, texto ou borda.

---

## 3. As quatro faixas

Contraste calculado contra o vazio `#000206` (WCAG 2.1, luminância relativa
sRGB).

### 3.1 Ambiente — 55% a 78% de cada imagem

| Token | Valor | Uso |
|---|---|---|
| `--luna-void` | `#000206` | Página, espaço entre seções |
| `--luna-void-1` | `#000A14` | Faixa distante, seção alternada |
| `--luna-void-2` | `#00101C` | Sombra projetada |

O preto real das imagens é quase neutro, com viés azul mínimo. **Não é `#000000`
e não é Midnight.**

### 3.2 Material — corpo, mesa, estrutura

| Token | Valor | Contraste | Uso |
|---|---|---|---|
| `--luna-str-1` | `#001428` | 1,12:1 | Cartão em repouso |
| `--luna-str-2` | `#001E3C` | 1,24:1 | Painel elevado |
| `--luna-str-3` | `#0A283C` | 1,37:1 | Hover, aba ativa |
| `--luna-str-4` | `#143A5A` | 1,76:1 | Borda visível, limite |

**Material separa por forma, borda e sombra — nunca por claridade.** Todos os
quatro ficam abaixo de 2:1. Isso é intencional: não são para carregar leitura.

### 3.3 Emissão fria — matiz 204° a 216°, dessaturada

| Token | Valor | Contraste | Uso |
|---|---|---|---|
| `--luna-glow-1` | `#3068A0` | 3,57:1 | Brasa, traço distante · só texto grande |
| `--luna-glow-2` | `#5A7896` | 4,51:1 | Linha secundária · AA no limite |
| `--luna-glow-3` | `#7088A0` | 5,65:1 | **O tom mais comum das três imagens** |
| `--luna-glow-4` | `#8098B0` | 6,96:1 | Texto sobre estrutura |
| `--luna-glow-5` | `#A0B8C8` | 10,07:1 | Holograma aceso · **acento do tema escuro** |
| `--luna-spec` | `#F8F8F8` | 19,55:1 | Especular · usar quase nunca |

**A luz é dessaturada.** `#7088A0` tem 30% de saturação. Um ciano saturado
(86%) lê como neon; este lê como projeção. É a diferença entre um holograma e
uma placa de fliperama, e é o erro mais provável de quem for aplicar isto sem
ler.

### 3.4 Emissão quente — bokeh e estrela

| Token | Valor | Contraste | Uso |
|---|---|---|---|
| `--luna-warm-1` | `#A06038` | 4,18:1 | Bokeh distante |
| `--luna-warm-2` | `#A08870` | 6,18:1 | Reflexo em material |
| `--luna-warm-3` | `#C09030` | 7,19:1 | Ponte com a logo |
| `--luna-warm-4` | `#E4B448` | 10,80:1 | O `X` da SMX |
| `--luna-warm-5` | `#F8E8A0` | 16,85:1 | Estrela, halo |
| `--luna-warm-6` | `#F8F0B0` | 17,88:1 | Núcleo da estrela |

---

## 4. O portão de matiz

> **Toda cor nova precisa cair entre 200° e 220°, ou entre 17° e 55°.**
> Fora dessas duas faixas, não entra.

Esta regra não foi inventada: é o que a medição encontrou. Toda emissão fria das
três imagens caiu entre **204° e 216°**. A faixa de azuis da logo é
**203° a 218°**. As imagens e a marca já concordavam sem ninguém ter conciliado.

**Foi assim que o roxo passou.** `#A78BFA`, matiz 275°, entrou na coloração de
sintaxe do Forge vindo de um tema de editor emprestado. Não havia portão, então
não houve o que reprovar.

**Duas cores da paleta anterior ficam fora do portão** e devem ser aposentadas
em superfície nova:

| Cor | Matiz | Desvio |
|---|---|---|
| `#1E2761` Midnight | 232° | 17° para o violeta |
| `#22D3EE` ciano | 188° | 27° para o verde |

Ver a seção 7 sobre o que fazer com o Midnight em `/ronda`.

---

## 5. Derivação de interface — tema escuro

Tema escuro é o padrão do produto.

```
--luna-bg        var(--luna-void)          página
--luna-surface   var(--luna-str-1)         cartão
--luna-surface-2 var(--luna-str-2)         elevado
--luna-surface-3 var(--luna-str-3)         hover
--luna-line      rgba(112,136,160,.16)     divisória
--luna-line-2    rgba(112,136,160,.28)     borda de controle
--luna-line-3    rgba(112,136,160,.46)     borda em foco
--luna-text      #DCE6F2                   18,9:1
--luna-text-2    #A8BBD4                   10,5:1
--luna-text-3    #7E92AE                    6,5:1
--luna-text-4    #5A6E8A                    3,9:1  só rótulo grande e borda
--luna-accent    var(--luna-glow-5)        10,1:1
--luna-on-accent var(--luna-void)
```

As linhas derivam de `glow-3` em opacidade, não de branco. É o que mantém a
divisória dentro da família de matiz em vez de introduzir cinza.

---

## 6. Tema claro — o que este padrão **não** cobre

As três imagens de referência são todas noturnas. **Não existe tema claro
derivável delas**, e inventar um a partir de material escuro seria exatamente o
tipo de suposição que este documento existe para evitar.

O tema claro deriva da **logo**, que tem fundo escuro mas cores próprias em
ambos os extremos:

```
--luna-bg        #F4F6FB
--luna-surface   #EDF0F8   #E5EBF5   #DCE3F0
--luna-text      #0A1B3D   15,7:1
--luna-text-2    #1E3A61   10,6:1
--luna-text-3    #41557A    6,9:1
--luna-accent    #003C90    9,5:1   (azul das letras SMX)
```

**O acento troca de degrau com o tema, não de família.** `glow-5` no escuro,
`#003C90` no claro. Uma cor fixa funcionaria mal em um dos dois.

**Nenhum dourado da rampa serve para texto no tema claro** — todos ficam abaixo
de 3,7:1 sobre papel. Só funcionam como preenchimento com texto escuro por cima,
que é como a classificação "Atenção" já resolve.

**O orçamento de luz não se aplica ao tema claro.** `screen` sobre papel é
papel; halo e brilho não existem ali. No claro, a hierarquia vem de sombra e
borda.

---

## 7. Escopo e o que fica de fora

| Superfície | Regime |
|---|---|
| Superfícies novas (`/v2`, `/forge?layout=v2`, tudo que vier) | Este padrão |
| `/` e `/forge` atuais | Migração por etapa, sem pressa |
| **`/ronda` — LUNA Safety Walk** | **Valores próprios preservados** |

**`/ronda` mantém `#1E2761`, `#05060B` e `#F4F6FB`.** Aqueles valores foram
validados em ronda real, estão no `themeColor` do PWA e em relatório impresso
entregue. Um documento de norma não desfaz o que passou por campo.

Alinhar o Midnight à matiz da marca é possível — preservando saturação e
luminosidade e corrigindo só a matiz para 215°, ele vira `#1E3A61`. É uma
mudança pequena a olho e grande de coerência, mas mexe em PWA instalado e em
papel já impresso. **Decisão do Arquiteto, em ADR próprio, nunca como efeito
colateral de outra tarefa.**

**Emenda — 19/08/2026:** o texto acima descreve o estado até então. **Deixou de ser
verdade.** `/ronda` migrou para a paleta deste padrão em `luna-frontend#38`, decisão
aprovada pelo Arquiteto em 19/08 — não foi efeito colateral de outra tarefa, foi a
decisão que este mesmo parágrafo pedia. Registrado aqui como decisão, sem apagar o
texto anterior: é o histórico de por que `/ronda` teve valores próprios por um tempo, e
quando isso mudou.

---

## 8. Regras de uso

**Classificação nunca é decoração.** Verde, âmbar e vermelho só aparecem quando
há um estado real por trás. Botão verde bonito, título vermelho de destaque:
não.

**Acento nunca é estado.** O acento é interação — link, foco, aba ativa, cursor.
Nunca significa "ok".

**Emissão quente nunca é interface.** Só atmosfera de fundo.

**Superfície não é tinta.** As quatro estruturais ficam abaixo de 2:1. Se algo
precisa ser lido, use a faixa de emissão.

**Nenhum cinza neutro.** Não há cinza no sistema. O que parece cinza é sempre a
família azul em opacidade ou luminosidade baixa — é isso que mantém a página
inteira numa família de matiz só.

**Classificação é sólida nos dois temas.** Sem variante clara. Um achado "não
conformidade" tem a mesma cor no celular em campo, no relatório impresso e no
site — e é essa igualdade que dá sentido a padronizar.

---

## 9. Como emendar

Cor nova exige, nesta ordem:

1. **Passar no portão de matiz** (200°–220° ou 17°–55°)
2. **Contraste calculado**, não estimado, contra o fundo em que vai viver
3. **Caber no orçamento de luz** — se acende, conta contra os 5%
4. **ADR próprio**, com o motivo e o que ela resolve que a rampa não resolvia

Exceção só com evidência de campo, no padrão das três de classificação: medida,
usada em produção e registrada.

---

## Anexo A — método de extração, para reproduzir

**Faixas funcionais**, aplicadas pixel a pixel após redução da imagem:

| Faixa | Critério |
|---|---|
| Ambiente | `v < 0,14` |
| Emissão fria | `v ≥ 0,62` e matiz entre 165° e 230° |
| Emissão quente | matiz ≤ 62° ou ≥ 330°, com `s ≥ 0,22` |
| Material | o restante com `0,14 ≤ v < 0,60` |

**Armadilha registrada.** Na logo existe uma linha divisória vertical fina em
43,2% da largura, entre o símbolo e o logotipo. Ela é dourada e é o elemento
mais alto da imagem — na primeira medição puxou o centro da estrela dez pontos
para a direita. Qualquer nova amostragem da logo precisa excluí-la.

**Coordenadas medidas na logo**, para efeito de luz:

| Elemento | Posição |
|---|---|
| Centro da estrela | 33,01% / 38,74% |
| Caixa do `X` | 78,6%–90,1% × 24,9%–44,4% |
| Linha divisória | 43,2% |

---

## Anexo B — bloco de tokens

Para colar em `luna-frontend/app/globals.css`, em bloco aditivo no fim do
arquivo. Nenhuma declaração existente é removida.

```css
/* GENESIS/padroes/PADRAO-SMX-CORES.md · ADR-024 · 17/08/2026
   Valores extraídos por medição da logo SMX e das três imagens de
   referência. Não alterar sem passar pelo portão de matiz (§4). */
:root{
  /* ambiente */
  --luna-void:#000206; --luna-void-1:#000A14; --luna-void-2:#00101C;
  /* material */
  --luna-str-1:#001428; --luna-str-2:#001E3C;
  --luna-str-3:#0A283C; --luna-str-4:#143A5A;
  /* emissão fria — matiz 204°–216°, dessaturada de propósito */
  --luna-glow-1:#3068A0; --luna-glow-2:#5A7896; --luna-glow-3:#7088A0;
  --luna-glow-4:#8098B0; --luna-glow-5:#A0B8C8; --luna-spec:#F8F8F8;
  /* emissão quente — atmosfera, nunca interface */
  --luna-warm-1:#A06038; --luna-warm-2:#A08870; --luna-warm-3:#C09030;
  --luna-warm-4:#E4B448; --luna-warm-5:#F8E8A0; --luna-warm-6:#F8F0B0;
  /* classificação — de fora deste padrão, validada em campo */
  --luna-ok:#2E7D32; --luna-warn:#E8A33D; --luna-fail:#C62828;
  --luna-on-ok:#FFFFFF; --luna-on-warn:#1E2761; --luna-on-fail:#FFFFFF;
  /* derivação — tema escuro */
  --luna-bg:var(--luna-void);
  --luna-surface:var(--luna-str-1);
  --luna-surface-2:var(--luna-str-2);
  --luna-surface-3:var(--luna-str-3);
  --luna-line:rgba(112,136,160,.16);
  --luna-line-2:rgba(112,136,160,.28);
  --luna-line-3:rgba(112,136,160,.46);
  --luna-text:#DCE6F2; --luna-text-2:#A8BBD4;
  --luna-text-3:#7E92AE; --luna-text-4:#5A6E8A;
  --luna-accent:var(--luna-glow-5);
  --luna-on-accent:var(--luna-void);
}
[data-theme="light"]{
  --luna-bg:#F4F6FB;
  --luna-surface:#EDF0F8; --luna-surface-2:#E5EBF5; --luna-surface-3:#DCE3F0;
  --luna-line:rgba(0,60,144,.12);
  --luna-line-2:rgba(0,60,144,.20);
  --luna-line-3:rgba(0,60,144,.34);
  --luna-text:#0A1B3D; --luna-text-2:#1E3A61;
  --luna-text-3:#41557A; --luna-text-4:#6B7C99;
  --luna-accent:#003C90; --luna-on-accent:#FFFFFF;
}
```

Chaves para `tailwind.config.ts`, **acrescentadas** ao namespace `luna.*` sem
remover nenhuma existente:

```ts
void: "#000206", str1: "#001428", str2: "#001E3C", str3: "#0A283C", str4: "#143A5A",
glow1: "#3068A0", glow2: "#5A7896", glow3: "#7088A0",
glow4: "#8098B0", glow5: "#A0B8C8", spec: "#F8F8F8",
warm1: "#A06038", warm2: "#A08870", warm3: "#C09030",
warm4: "#E4B448", warm5: "#F8E8A0", warm6: "#F8F0B0",
```

**Atenção às chaves legadas.** `luna.success` `#10B981` e `luna.danger`
`#EF4444` continuam declaradas e não devem ser removidas, mas **não são cores
de classificação**. Classificação é `ok` / `warn` / `fail`. Duas cores com o
mesmo significado e nomes igualmente plausíveis é armadilha conhecida — quem
escrever `text-luna-success` achando que é o verde de classificação quebra a
igualdade entre celular, papel e tela.

---

## Anexo C — documentos relacionados

| Documento | Relação |
|---|---|
| `ADR-022` — `ADR/ADR-022-paleta-e-redesenho.md` | Este padrão emenda a hierarquia de superfície dele: a página parte de `#000206`, não de Midnight |
| `ADR-023` · Padrão SMX de Design | Governa **como** se desenha; este governa **com que cor** |
| `ADR-021` | Safety Walk — fonte das três cores de classificação |
| `finding-card.tsx` | Onde a medição de 2,16:1 do branco sobre âmbar está registrada |
| `theme-provider.tsx` | Onde os valores de `/ronda` vivem, preservados |
