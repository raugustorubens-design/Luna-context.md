# Como ficou a saída da ronda

**19/08/2026 · verificado no código, não nos pacotes**

---

## O que está construído e funciona

**O adaptador — `relatorio-detalhado-adapter.ts`.** É a peça que faltava, e está boa:

- **Lê as duas fontes de foto** — `fotoIds` do servidor e `fotos` embutidas do caminho
  offline. A armadilha que eu marquei no pacote está citada no próprio código
- **Usa sempre a versão de campo**, nunca a original
- **Aplica a curadoria por cima**, e a ronda nunca é tocada — o `RondaStore` não é chamado
  depois da leitura
- **As três cores de classificação** são os hex do relatório impresso, fixos, sem variante
  por tema — porque o documento é artefato exportado
- **Achado `nao_avaliado` ou `inexistente` não vira linha.** Faz sentido: não há o que
  reportar sobre risco que não foi encontrado

**A curadoria — `curadoria-store.ts`** existe, com edições e exclusões guardadas em registro
próprio.

**O botão** está na tela de edição de ronda confirmada, do `#39`.

---

## A divergência que precisa da sua decisão

**Existem dois formatos, e o código está dividido entre eles.**

| Peça | Diz o quê |
|---|---|
| `relatorio-ronda-detalhado.ts` | template com `renderer: "docx"` |
| Comentário do adaptador | *"o chamador passa o resultado a `XlsxRenderer.render(document, relatorioSsmaTabularTemplate)`"* |

O template docx foi declarado, mas o adaptador ainda instrui a usar o **xlsx** com o
template genérico antigo. Vieram de dois PRs diferentes — o `#45` de manhã, xlsx, e o `#51`
à noite, docx — e ninguém decidiu qual vale.

**Isso significa que a saída de hoje provavelmente é uma planilha**, não um documento.

### Por que isso importa

O adaptador monta **uma linha por achado, tabular**, com sete colunas. Isso é planilha.

Mas o desenho que a gente ratificou dizia: *"uma seção por achado, texto completo, foto
abaixo"* — que é documento, e é o que o comentário do template docx repete.

**São formatos diferentes de verdade.** Numa planilha, a descrição de um achado fica espremida
numa célula e a foto é ancorada por coluna. Num documento, o achado ganha um bloco com o
texto respirando e a imagem em tamanho útil.

Para auditoria, e para entregar a alguém, **documento serve; planilha não.**

---

## Minha recomendação

**Ficar com o docx**, e ajustar o adaptador para produzir seções em vez de linhas.

O `CanonicalDocument` já carrega o que precisa — cabeçalho, registros, imagens por registro.
O que muda é o template consumir isso como blocos, não como tabela.

**O xlsx não some.** Ele continua útil para outra coisa: a planilha de acompanhamento, onde
você quer ver trinta achados de uma vez e filtrar. Só não é o relatório.

Se concordar, isso vira uma Issue com rótulo `decisao` e uma tarefa pequena — o adaptador já
está pronto, é o formato de saída que muda.

---

## O que ainda não existe

**Armazenagem com descarte em 7 dias.** O `relatorio-store.ts` existe, mas eu não verifiquei
se o prazo está implementado. Vale conferir antes de considerar o marco fechado.

**O modelo Visual.** Está declarado como fora de escopo no próprio adaptador, e a decisão
sobre o que vem marcado por padrão continua com você.

**PDF.** Depende do LibreOffice no contêiner do Railway — ação sua, registrada no `ENG-041`.

---

## O portão que fecha o marco 1

Nenhuma dessas verificações eu consigo fazer: **gerar o relatório de uma ronda real, abrir o
arquivo, e os achados estarem lá com as fotos.**

Se abrir e for planilha, você já sabe o motivo — e a correção é a decisão acima.
