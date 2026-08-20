# Três saídas, três destinos — e o que o XLS da Manserv revela

**19/08/2026 · correção de rumo**

---

## Eu recomendei errado

Sugeri manter o docx e aposentar o xlsx, julgando pelo formato: planilha espreme texto,
documento deixa respirar.

**Julguei pela leitura, não pelo destino.** Se os procedimentos e APRs da Manserv saem em
XLS, então planilha não é resquício — é o formato que entra no processo de quem recebe. Um
documento bonito que o cliente precisa reconverter à mão é pior que uma planilha que ele
abre e usa.

Sua decisão está certa: **três saídas.**

---

## As três, e para quem cada uma serve

| Formato | Destino | Por que existe |
|---|---|---|
| **XLSX** | quem trabalha em planilha — a Manserv | Encaixa no processo deles. Filtra, ordena, cruza com o que já têm |
| **DOCX** | auditoria e leitura | Achado com texto respirando e foto em tamanho útil. É o que se anexa a processo |
| **PPTX** | o cliente — e o que você usa | O modelo Visual, com a foto grande. É o que se apresenta numa reunião |

**Um adaptador só alimenta os três.** É exatamente o que o `relatorio-detalhado-adapter.ts`
já faz: monta o `CanonicalDocument` e não conhece formato. Trocar de saída é trocar de
`TemplateDescriptor`, não refazer extração.

O `xlsx-renderer`, o `docx-renderer` e o `pptx-renderer` já existem, os três.

### O que precisa mudar no adaptador

Hoje ele monta **uma linha por achado, sete colunas** — forma de planilha. Serve ao xlsx e
não serve aos outros dois.

O `CanonicalDocument` precisa carregar o achado como **registro com campos e imagens**, e
cada template decide como apresentar: linha na planilha, seção no documento, slide na
apresentação. A estrutura já é essa — falta o docx e o pptx consumirem como bloco em vez de
tabela.

---

## O que a informação do XLS revela, e é maior que a saída

**Se a APR chega em XLS, a ingestão também muda — e fica mais fácil.**

O motor de conformidade precisa preencher `documento_normativo` e `norma_item`, e eu vinha
supondo entrada em PDF ou Word, onde extrair estrutura é o problema difícil.

**Planilha de APR já é estrutura.** Linha é item, coluna é campo. Perigo, risco, controle,
responsável — cada um na sua coluna, sem ambiguidade nenhuma.

Isso muda três coisas:

**A ingestão fica determinística.** Ler planilha é aritmética de célula, não interpretação.
Nada de IA na extração — só na normalização do nome, quando o cliente escreve "NR-35" de um
jeito e "Trabalho em Altura" de outro.

**O `norma_item` sai quase pronto.** A numeração do item já está lá; a citação que o achado
precisa referenciar já existe na planilha.

**E o `questao` ganha ponto de partida.** Cada linha de APR é candidata a uma asserção
observável — que é exatamente o caminho C que a gente discutiu, com a máquina rascunhando e
você aprovando.

**O formato que você acha ruim é o mais fácil de digerir.** Vale registrar isso, porque
muda a prioridade da ingestão: o parser de planilha já existe no Convergia, e o de PDF é
que era o obstáculo.

---

## Ordem que eu sugiro agora

**1 · Terminar o xlsx.** É o que já está construído e é o que a Manserv consome. Fechar
primeiro o que atende o processo real.

**2 · DOCX como seção**, não linha. Mesmo adaptador, template consumindo em bloco.

**3 · PPTX Visual.** Reusa o `visual-template-store` e o `slide-layout`, que já existem com
campos posicionados.

**4 · Ingestão de APR em planilha** — e essa passa na frente de várias coisas do marco 4,
porque destrava a comparação com muito menos esforço do que eu tinha estimado.

---

## Uma pergunta que vale fazer à Manserv

Se eles emitem APR e procedimento em XLS, **a planilha tem formato padrão?** Colunas com
nome fixo, ou cada emissor monta do jeito dele?

Se for padrão, a ingestão é quase direta. Se cada um monta o seu, aí entra o mapeamento de
coluna — e aí sim a IA ajuda, na primeira vez, com você confirmando, e vira regra guardada
para aquele cliente.

É o mesmo mecanismo de detectar o vazio e corrigir que a gente desenhou para o Sense,
aplicado à entrada de documento.
