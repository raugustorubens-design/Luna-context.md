# O PPTX sai em coluna única, com muitas páginas e sem imagem

**Caminho:** `GENESIS/pacotes/2026-08-20-pptx-layout.md`
**Estado:** pronto

> ## REPOSITÓRIO-ALVO
>
> **`raugustorubens-design/luna-core`** — exclusivamente.
> Escopo: `src/convergia/renderers/pptx-renderer.ts`, `src/convergia/templates/`, e a rota
> que resolve template por formato.

---

## O sintoma

Relatório em PPTX sai *"tudo em uma coluna somente, gerando várias páginas e ou sumindo com
as imagens"*.

**O que já foi verificado, e está certo:**

- O adaptador **anexa as fotos** aos registros — lê `fotoIds` e `fotos`, as duas origens
- Os dois bloqueios da revisão do `#53` **foram corrigidos**: `wrapFieldToBudget` quebra
  campo longo por palavra, e a altura do texto é condicional à presença de foto
- Existe um `relatorio-ronda-detalhado-pptx.ts`

Então a causa está entre a escolha do template e a renderização.

---

## Etapa 1 · O diagnóstico — faça antes de mexer

**Descubra qual ramo do renderizador está rodando.** Há três, e o comportamento é
completamente diferente em cada:

| Ramo | Quando | Como fica |
|---|---|---|
| `renderVisual` | `template.visual` | Imagem de fundo com campos posicionados |
| `renderSections` | `template.layoutMode === "narrativo"` | Um achado por slide, campos empilhados, fotos embaixo |
| tabela | os outros | `addTable` com as sete colunas |

**Duas hipóteses, e o teste que separa:**

### Hipótese A — está caindo no ramo de tabela

Se o `relatorio-ronda-detalhado-pptx.ts` **não** declarar `layoutMode: "narrativo"`, o PPTX
vai para o ramo de tabela.

E aí as imagens somem por um motivo exato: **o adaptador zera a posição EMU de propósito.**

```ts
const zeroPosition = { xEmu: 0, yEmu: 0, cxEmu: 0, cyEmu: 0 };
```

O comentário explica que é para o XLSX, que posiciona por célula e ignora `position`. Mas o
ramo de tabela do PPTX **usa** esses valores:

```ts
const w = emuToInches(image.position.cxEmu);   // = 0
const h = emuToInches(image.position.cyEmu);   // = 0
slide.addImage({ ..., w: 0, h: 0 });
```

**Imagem com largura e altura zero é imagem invisível.** Ela está no arquivo e não aparece.

E os outros dois sintomas fecham: sete colunas numa página A4 retrato espremem tudo, o texto
quebra muito e parece coluna única; com 18 registros por slide, sai muita página.

### Hipótese B — está no ramo narrativo, e o desenho não é o que o Arquiteto espera

Aí "uma coluna" é literalmente o desenho: campos empilhados como texto corrido, um achado
por slide, mais os slides de continuação.

Nesse caso as imagens deveriam aparecer — e se não aparecem, é outro defeito.

### Como separar, em um minuto

Leia `relatorio-ronda-detalhado-pptx.ts` e confira se ele declara
`layoutMode: "narrativo"`. Depois confira a rota: para `formato: "pptx"`, qual template ela
resolve.

**Reporte o que encontrou antes de corrigir.**

---

## Etapa 2 · A correção, conforme o diagnóstico

### Se for a hipótese A

Duas coisas, e as duas valem mesmo assim:

**a) O template do PPTX declara `layoutMode: "narrativo"`.** É o desenho ratificado — um
slide por achado, foto grande, texto respirando. Tabela de sete colunas em slide não é
relatório, é planilha em cima de um retângulo.

**b) O ramo de tabela nunca desenha imagem com dimensão zero.** Mesmo que ninguém use esse
caminho para ronda, ele é usado por documento vindo do `pptx-parser`. Quando
`cxEmu`/`cyEmu` vierem zerados, use uma dimensão padrão razoável em vez de zero — ou não
desenhe e **registre um aviso**. Imagem invisível sem aviso é o pior dos dois mundos.

### Se for a hipótese B

O desenho está certo e o que falta é acabamento. Reporte, com uma captura de um slide, e o
Arquiteto decide o que muda — número de fotos por slide, tamanho, ordem dos campos.

**Não redesenhe por conta.** O layout narrativo foi ratificado; ajustá-lo é decisão dele.

---

## Etapa 3 · Independente do diagnóstico

Duas coisas que valem nos dois casos:

**A posição zerada precisa de nome.** `zeroPosition` com comentário explicando que é para
o XLSX é convite ao erro — quem consumir do outro lado não lê o comentário do produtor.
Deixe explícito no contrato que posição ausente significa **"o renderizador decide"**, e não
"desenhe com tamanho zero".

**Um teste que abre o arquivo.** Gerar um PPTX com um achado que tem foto, abrir como zip, e
afirmar que existe imagem com dimensão maior que zero. Os testes atuais contam slides; este
mede o que o Arquiteto vê.

---

## Pré-respostas

| Se encontrar | Faça |
|---|---|
| O template pptx sem `layoutMode` | É a hipótese A. Declare narrativo |
| A rota resolvendo o tabular para pptx | Mesma coisa; corrija a resolução |
| Imagem com `cxEmu` zero no ramo de tabela | Nunca desenhe com zero. Padrão ou aviso |
| Tudo já narrativo e as fotos aparecendo | Reporte com captura; é acabamento, e é decisão do Arquiteto |

## Condições de parada

- A correção exigir mudar o layout narrativo que já foi ratificado
- O adaptador precisar mudar para atender o renderizador — **é o renderizador que se adapta
  ao dado**, não o contrário

## Autorização de merge

Etapa 1 é diagnóstico: **reporte, não commite.**

Etapa 2, hipótese A: pode mergear com os portões verdes.
Etapa 2, hipótese B: espere o Arquiteto.

---

## Critério de pronto

Gerar o PPTX de uma ronda com fotos e descrição longa, e no arquivo aberto:

1. **As fotos aparecem**, em tamanho útil
2. Um achado por slide, com continuação quando não couber
3. Nenhum texto cortado nem por cima da imagem
4. O papel e a orientação escolhidos sendo respeitados

---

## Memórias geradas

- Posição zerada como convenção interna vira imagem invisível quando outro renderizador lê o
  mesmo campo: convenção não atravessa módulo, contrato sim
- Teste que conta slides não vê imagem de tamanho zero; teste precisa medir o que o usuário
  enxerga
