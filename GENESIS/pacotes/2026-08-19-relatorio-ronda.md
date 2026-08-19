# Como o relatório da ronda será gerado

**19/08/2026 · desenho, para ratificação**

---

## O que já existe

| Peça | Onde |
|---|---|
| Renderizadores — pptx, docx, xlsx, csv, html, markdown, json | `src/convergia/renderers/` |
| Contrato de template — `TemplateDescriptor`, com `renderer`, `layout`, `variables` | `src/convergia/contracts.ts` |
| Registro de templates | `templates/registry.ts` |
| Template visual com campos posicionados | `visual-template-store.ts`, `slide-layout.ts`, `position-store.ts` |
| Roteamento de payload grande | `async-routing.ts` |
| Ronda salva | `convergia_rondas` |
| Fotos, versão de campo e original | `convergia_ronda_fotos` |

**Falta uma peça só, e ela é pequena:** o adaptador que transforma uma ronda salva no
conjunto de dados que o template consome.

---

## Uma distinção que libera o caminho

O template existente é genérico de propósito. O comentário no próprio arquivo diz por quê:
os 13 documentos corporativos — APR, PGR, DDS, Certificados — **são formatos regulatórios
brasileiros reais**, e inventar a estrutura deles sem especialista entregaria documento de
conformidade confiantemente errado.

**O relatório de ronda não é um deles.** Não é formato regulado: é o seu relatório, com o
seu layout, que você já validou em protótipo. Construir não tem esse risco — e é por isso
que ele pode vir antes dos outros treze.

---

## A peça que falta — o adaptador

`src/convergia/ronda/report.ts`. Entrada: `rondaId`. Saída: o conjunto de dados
normalizado.

O que ele monta:

**Cabeçalho** — título, cliente, setor, turno, data, responsável. Vem de `metadata`.

**Achados**, na ordem em que foram registrados. Cada um com: flag ou "achado manual",
estado, departamento, classificação, gravidade, descrição, ação recomendada, responsável,
prazo, e **as fotos resolvidas**.

**Resumo** — contagem por classificação, e a lista de não conformidades em destaque.

**Encerramento** — o que veio de `encerramento`.

### A regra das fotos, que é onde mora a armadilha

Cada achado tem **dois** campos de foto: `fotos`, embutidas — caminho de contingência,
quando não havia rede — e `fotoIds`, no servidor, que é o caminho normal.

> **Leia os dois, sempre.**

Ler só um devolve relatório sem foto nenhuma, e o erro é **silencioso**: campo vazio é
estado legítimo, então nada reclama. É o mesmo padrão que já nos custou uma investigação
inteira esta semana.

E use a **versão de campo**, nunca a original. 1280px é suficiente para o documento — foto
em meia largura de slide a 150 dpi pede cerca de 1000px. A original são vários MB e não
melhora nada no papel.

**Exceção por proporção:** panorâmica reduzida a 1280px de largura fica com 320px de
altura, ilegível justamente no detalhe que a justificou. Acima de 2,5:1, o teto sobe para
2000px.

---

## Os dois modelos, um conjunto de dados

| | **Detalhado** | **Visual** |
|---|---|---|
| Para quem | você, auditoria | o cliente |
| Renderizador | `docx` | `pptx` |
| Estrutura | uma seção por achado, texto completo, foto abaixo | um slide por achado, foto grande, texto curto |
| Base | template novo, tabular estendido | `visual-template-store` com campos posicionados |

**O mesmo adaptador alimenta os dois.** Trocar de modelo é trocar de `TemplateDescriptor`,
não refazer a extração.

**Comece pelo Detalhado.** Ele não depende de posicionamento visual, e é o que serve para
auditoria — que é onde o erro custa caro.

---

## De onde o usuário dispara

Botão **"Gerar relatório"** na tela de rondas anteriores, em cada ronda já confirmada pelo
servidor. Escolha do modelo ali mesmo.

Ronda pequena gera na hora. Ronda grande — muitas fotos — vai pelo roteamento assíncrono
que já existe, e a tela mostra que está preparando.

**Nunca gerar de ronda pendente na fila.** Só do que o servidor confirmou.

---

## Armazenagem e entrega

Arquivo gerado vai para armazenamento temporário, **com descarte em 7 dias**, como você
propôs. É seguro porque é reconstruível: as partes ficam no banco, e o documento se refaz
a qualquer momento.

Isso também impede que o documento vire mais uma coisa que cresce sem limite — o mesmo
problema que a Camada 2 resolveu na foto e que a original no servidor ainda tem.

**Entrega:** link para baixar. E-mail e WhatsApp entram depois, quando existir o Sense —
são o mesmo canal, com o mesmo desenho de urgência.

---

## O que fica de fora nesta etapa

**PDF.** Depende da conversão via LibreOffice, que ainda não está instalado no contêiner do
Railway — está registrado no `ENG-041`, e é ação de infraestrutura sua. Enquanto isso,
DOCX e PPTX abrem em qualquer aparelho.

**Os 13 documentos corporativos.** Formatos regulados, esperando validação de especialista.
Não confunda com este.

**A comparação com APR.** É a Decisão 9 do ADR-021, e depende de `questao` preenchida.

---

## Escopo da primeira etapa

Um adaptador, um template, um botão, um formato.

**Portão real:** você gera o relatório de uma ronda de verdade, abre o arquivo, e os
achados estão lá **com as fotos**. Documento gerado que ninguém abriu não conta.

---

## Uma decisão sua antes do pacote

**O relatório mostra o Positivo?**

Um achado classificado como Positivo é registro de que estava certo naquele dia. Num
relatório de auditoria isso vale — mostra que a ronda cobriu a área, não só apontou defeito.
Num relatório para o cliente, pode diluir as não conformidades.

Minha inclinação: **Detalhado mostra tudo; Visual mostra o Positivo em seção separada, no
fim.** Mas isso é conhecimento seu de campo, não meu.
