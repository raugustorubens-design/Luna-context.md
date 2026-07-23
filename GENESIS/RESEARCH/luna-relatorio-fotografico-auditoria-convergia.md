# Relatório Fotográfico de Auditoria via Convergia — Especificação (Theory)

Status: Theory — especificação completa fornecida pelo Originador
(2026-07-23), ainda sem execução de campo (diferente do documento irmão
`luna-treinamento-adaptativo.md`, que já tem resultado real confirmado).
Une capacidades já registradas isoladamente no Roadmap (`CONV-001`,
`CONV-003`, `CONV-005`, `CONV-007`, `CONV-009`) em um único fluxo de
produto concreto. Não implementado.

## O pipeline completo (como especificado)

1. Usuário informa o contexto do relatório antes de iniciar: empresa,
   atividade (ex.: logística).
2. Usuário sobe as fotos de auditoria.
3. Para cada foto, a IA gera automaticamente: setor, atividade, e
   descrição da não conformidade identificada na imagem.
4. Cada campo gerado pela IA (setor/atividade/NC) é editável pelo
   usuário — a IA nunca tem a palavra final sozinha.
5. Usuário pode inserir NCs adicionais que a IA não identificou — o
   relatório final não fica limitado ao que a IA percebeu.
6. Ao final, geração de uma conclusão consolidada do relatório, no
   mesmo padrão do documento real já usado como referência (Relatório
   de Acompanhamento Operacional, Sylvamo — Unidade Luís Antônio:
   Objetivo + Atividades Acompanhadas → Tabela de Oportunidades de
   Melhoria → Legenda de critérios → Conclusão → Anexo de fotos →
   Referências normativas).
7. Usuário sobe o template visual da empresa (logo, cabeçalho,
   identidade visual).
8. A IA renderiza o relatório dentro do template enviado — o documento
   final sai com a identidade visual do cliente, não um formato
   genérico do Convergia.

## Como isto se encaixa no que já está registrado

Este fluxo não introduz uma capability nova isolada — é uma composição
de itens que já existem no Roadmap, hoje tratados como pendências
separadas sem um consumidor concreto amarrando-os:

- Passos 1-2: upload real de imagem — depende do adapter de imagem
  ainda inexistente no `luna-core` (nenhum provider hoje processa
  imagem — ver `CONV-009`).
- Passo 3: leitura de cena para achado de risco (uma das duas saídas de
  `CONV-009` identificadas a partir das 4 fotos reais analisadas nesta
  conversa — a outra saída, OCR de rótulo/etiqueta, não é usada neste
  fluxo específico de auditoria fotográfica, mas usa o mesmo adapter de
  imagem de base).
- Passos 4-5: interface de edição/complementação humana sobre saída de
  IA — não existe hoje em nenhuma tela do Convergia; mais próximo do
  padrão de "candidato a conhecimento, não fato aceito" já usado para
  `CONV-009` (estado `unverified`→`corroborated`) e para o método de
  treinamento (`luna-treinamento-adaptativo.md`) — mesmo princípio de
  proveniência aplicado a um terceiro caso.
- Passo 6: geração de relatório a partir de documentos/dados enviados —
  é `CONV-007`, hoje registrado como dependente de `CONV-001` a
  `CONV-004`.
- Passos 7-8: upload de template real + renderização — é `CONV-001`
  (upload de template visual, hoje só catálogo pré-codificado) e
  `CONV-005` (renderizador de PDF, hoje ausente — só existem
  CSV/HTML/JSON/Markdown/PPTX/XLSX).

## Achado de dependência (não estava explícito no Roadmap antes desta conversa)

`CONV-009` (leitura de foto) e `CONV-007` (relatório de auditoria) já
citavam depender de `CONV-001` a `CONV-004`, mas essa dependência estava
registrada em abstrato. Esta especificação mostra o motivo concreto: o
relatório fotográfico não tem como terminar sem template/render
funcionando — não são frentes paralelas de prioridade independente, o
Bloco de imagem (leitura de foto) precisa do Bloco de documento
(template/preview/PDF) para fechar o próprio fluxo, mesmo que a leitura
de imagem em si funcione isoladamente antes disso.

## O que ainda não está definido (não fabricado, sinalizado como aberto)

- Formato de armazenamento das fotos enviadas (base64 direto vs. objeto
  em storage) — já era uma pendência citada em `CONV-009` no Roadmap,
  ainda sem decisão.
- Se a edição do usuário sobre o campo gerado pela IA (passo 4) é
  registrada como correção (alimentando aprendizado futuro do
  reconhecimento de NC) ou é só edição pontual do documento, sem
  retorno ao Hipocampo/Guardian — não especificado.
- Se NCs inseridas manualmente pelo usuário (passo 5) recebem o mesmo
  tratamento de proveniência (`corroborated` direto, já que vêm de
  humano autorizado) ou passam por algum outro fluxo — não
  especificado, mas provavelmente `corroborated` direto por analogia ao
  padrão já estabelecido (confirmação humana = corroborated).
- Nenhum ADR foi aberto ainda ligando estes itens de Roadmap como um
  único épico de produto.

## Próximo passo sugerido

Esta Theory está pronta para virar ADR assim que o adapter de imagem
básico (`CONV-009`, bloco de infraestrutura) e o motor de
template/PDF (`CONV-001`/`CONV-005`) tiverem pelo menos uma decisão de
caminho técnico tomada (qual modelo de visão, qual motor de
renderização de PDF) — hoje nenhum dos dois tem decisão registrada, só
a necessidade.
