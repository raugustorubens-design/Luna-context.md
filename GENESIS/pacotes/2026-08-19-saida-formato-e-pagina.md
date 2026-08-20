# Saída do relatório — formato, página e as quatro regras

**Caminho:** `GENESIS/pacotes/2026-08-19-saida-formato-e-pagina.md`
**Estado:** pronto

> ## REPOSITÓRIO-ALVO
>
> **`raugustorubens-design/luna-core`** — renderizadores, templates, contrato.
> **`raugustorubens-design/luna-frontend`** — a tela de escolha.

---

## Contexto

Os procedimentos e APRs da Manserv saem em XLS. **O formato não é escolha estética — é
interoperabilidade.** Documento que o cliente precisa reconverter à mão é pior que planilha
que ele abre e usa.

Então o usuário escolhe, e o sistema entrega nas três formas, com página configurável.

---

## Etapa 1 · A escolha

Na tela de curadoria, antes de gerar:

| Campo | Opções | Padrão |
|---|---|---|
| **Formato** | PPTX · XLSX · DOCX | PPTX |
| **Orientação** | Retrato · Paisagem | conforme o formato |
| **Papel** | A4 · Ofício · Carta | A4 |

**Padrões por formato**, porque cada um tem um uso natural:

- **PPTX** — paisagem. É apresentação; retrato existe para quem imprime
- **XLSX** — paisagem. Sete colunas não cabem em retrato sem espremer
- **DOCX** — retrato. É documento de leitura

O usuário muda tudo. O padrão só evita escolher três coisas para o caso comum.

**Medidas exatas**, e vale conferir porque erram com frequência:

| Papel | Milímetros |
|---|---|
| A4 | 210 × 297 |
| **Ofício (Ofício II, Brasil)** | **216 × 330** |
| Carta | 216 × 279 |

**Ofício não é o Legal americano** (216 × 356). Usar o valor errado corta a última linha na
impressora do cliente, e ninguém entende por quê.

---

## Etapa 2 · Nada truncado

**É o requisito mais importante do pacote.** Documento que corta texto obriga o usuário a
refazer o trabalho fora do nosso processo.

**XLSX** — quebra de linha na célula ligada, altura da linha ajustada ao conteúdo, largura
de coluna proporcional ao que ela guarda. Descrição longa **nunca** some atrás da borda.

**DOCX** — fluxo natural. Nenhum contêiner de altura fixa. Imagem redimensionada pela
largura útil da página, respeitando a margem, e **nunca** recortada.

**PPTX** — texto que não couber gera **slide de continuação**, não texto reduzido a corpo 6
nem recorte. Um achado com descrição longa vira dois slides; é melhor que um slide
ilegível.

**Regra geral:** quando o conteúdo não couber no espaço, **o espaço cede**, nunca o
conteúdo.

---

## Etapa 3 · Sem proteção nenhuma

**Nada de senha de alteração, nada de proteção de planilha, nada de campo de formulário
travado.**

O arquivo sai editável por completo. O usuário muda o que quiser, acrescenta linha, apaga
coluna, refaz o texto.

Confira que os renderizadores **não** estão adicionando proteção — em planilha, algumas
bibliotecas escrevem `sheetProtection` por padrão em certos caminhos. Se houver, remova.

---

## Etapa 4 · O template nunca sai vazio

Esta é a regra do Arquiteto, e ela não é técnica: **é de qualidade e rastreabilidade.**

> **Nenhum arquivo sai do nosso processo sem dado.**

Não existe "baixar modelo em branco". Motivo: modelo em branco vira estoque. Alguém guarda,
usa daqui a seis meses, preenche à mão — e produz um documento com a nossa cara, baseado
numa versão que já mudou. **Documento vencido processado por nós**, sem ter passado por nós.

Todo arquivo emitido carrega, num rodapé discreto:

- Identificador da ronda de origem
- Data e hora da emissão
- Versão do template

Assim, qualquer arquivo que apareça depois pode ser conferido contra o registro.

### A tensão que isso cria, e como se resolve

Arquivo totalmente editável **pode ser alterado depois de emitido**. Isso é intencional — é
o que você pediu, e está certo.

Consequência: **o arquivo não é a prova; o registro é.** O documento é cópia de trabalho, e
o que vale é o que está no sistema — a ronda original, mais a curadoria com o texto anterior
preservado ao lado do editado.

É a mesma disciplina da curadoria: a ronda não muda, o relatório é derivado. Aqui só se
estende para depois da emissão.

O identificador no rodapé é o que liga uma coisa à outra.

---

## Pré-respostas

| Se encontrar | Faça |
|---|---|
| Renderizador sem suporte a tamanho de papel | Reporte qual, e siga com os outros |
| Biblioteca escrevendo proteção por padrão | Remova e registre onde estava |
| Texto que não cabe no slide | Slide de continuação; nunca reduzir fonte abaixo do legível |
| Imagem maior que a largura útil | Redimensione proporcional; **nunca recorte** |

## Condições de parada

- Um formato não suportar orientação ou papel sem biblioteca nova
- Evitar truncamento exigir mudar o `CanonicalDocument` de forma que quebre os outros dois
- Alguma parte pedir para emitir arquivo sem dado

## Autorização de merge

Pode mergear após os portões automáticos. Entra no `PENDENTE.md` — o Arquiteto precisa abrir
os três formatos e conferir.

---

## Critério de pronto

Gerar a **mesma ronda nos três formatos**, e em cada um:

1. Abrir e **nenhum texto estar cortado** — inclusive o achado de descrição mais longa
2. Editar livremente, sem pedir senha
3. Conferir o tamanho da página nas propriedades do arquivo
4. O rodapé trazer ronda, data e versão do template

**Portão do Arquiteto:** imprimir um em Ofício e conferir que nada foi cortado na margem. É
onde o erro de milímetro aparece.

---

## Memórias geradas

- Ofício brasileiro é 216 × 330 mm, não o Legal americano de 216 × 356
- Quando o conteúdo não cabe, o espaço cede — nunca o conteúdo
- Documento emitido sem dado vira estoque, e estoque vira documento vencido com a nossa cara
- Arquivo editável não é prova; o registro é. O identificador no rodapé liga os dois
