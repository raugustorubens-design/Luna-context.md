# ADR-021 — Convergia Mobile: Ronda Fotográfica com Aprendizado de Padrão

Status: Reconciliado com pesquisa prévia (`convergia-spec-tecnica-consolidada.md`,
`luna-tabela-risco-iso-outcome.md`) e com o relatório real da Manserv,
aguardando ratificação final do Architect
Data: 2026-08-05 (atualizado; proposto originalmente em 2026-08-05, mesma sessão)
Decisor: Architect (Rubens)
Contexto: Engineer (Claude, chat) — consolida ADR-020 (relatório de ronda
fotográfica, protótipo validado) com decisões tomadas nesta sessão:
superfície mobile standalone, gravidade sugerida por procedimento +
histórico, separação sensível/lógica no aprendizado, comparação de imagem
via visão computacional. Reaproveita registro já existente de CONV-009
(`GENESIS/ROADMAP.md`, ENG-028) para a peça de visão — não redecide o
caminho técnico de lá, só conecta ao caso de uso real.

## Decisão 1 — Superfície nova, não o Forge, com funcionamento offline

O Forge continua exclusivamente para desenvolvedor. A coleta de dado de
ronda (foto + campo + observação) roda numa superfície nova, separada,
mobile-first — mesmo backend (`luna-core`), interface diferente.

**Correção do Architect (2026-08-05):** rodar só via web (depender de
rede o tempo todo) é problema real — latência e queda de rede em campo
industrial não são exceção, são esperadas. O app precisa **rodar no
dispositivo** e funcionar sem rede: foto e formulário ficam guardados
localmente enquanto não há conexão, e o envio ao servidor acontece
sozinho assim que a rede voltar — sem o usuário precisar lembrar de
tentar de novo.

Caminho recomendado pelo Engineer (decisão do Architect, não fechada
aqui): **PWA** (Progressive Web App), não app nativo separado — reaproveita
o mesmo `luna-frontend`/stack já existente, evita abrir uma frente de
desenvolvimento inteiramente nova (Swift/Kotlin, loja de aplicativo,
outro pipeline de build). Mecanismo: service worker mantém a interface
utilizável offline; fila local no dispositivo (IndexedDB) guarda
foto+formulário de cada achado enquanto não há rede; reenvio automático
ao detectar rede novamente (evento `online`, não dependência de
Background Sync API — suporte inconsistente no Safari/iOS, mais
confiável reenviar ao reabrir o app ou detectar reconexão). Instalável na
tela inicial, acesso à câmera nativa via input padrão do navegador.

Ditado por voz continua de graça (teclado nativo Android/iOS em qualquer
campo de texto simples), independente da escolha PWA vs. nativo.

**Impacto no tamanho da Fase 1** (ver tabela de fases): isso é mais
trabalho do que "página responsiva simples" — service worker + fila
offline + sincronização automática são peças reais de engenharia, não
ajuste de CSS. Fase 1 cresce, mas continua sendo a entrega que resolve o
problema mais urgente (perder dado de ronda por falta de rede/papel).

## Decisão 2 — Estrutura de entrada, não deriva do modelo tabular

Confirma o modelo canônico do ADR-020 (metadata + achados[] +
encerramento) como uma segunda "forma" de entrada da Convergia, paralela
à tabular (planilha) já existente — não força achado/foto numa estrutura
de linha/coluna. Cada achado carrega: departamento, foto(s), classificação
(positivo/atenção/não conformidade), gravidade, descrição, ação
recomendada, responsável, prazo.

## Decisão 3 — Gravidade sugerida, não fixa

A gravidade/ação recomendada de uma não conformidade é **sugerida**
automaticamente por busca semântica contra duas fontes, ambas via Guardian
(Princípio 4 da Constitution — nunca acesso direto):
1. Procedimentos já ingeridos no Hipocampo (NR, PGR, etc. — depende de
   haver conteúdo real carregado; se não houver, a sugestão não tem o
   que buscar, mesmo gap dos 13 templates corporativos).
2. Achados anteriores já registrados (ver Decisão 5) — o sistema fica
   mais preciso a cada ronda.

Sempre editável pelo usuário antes de confirmar — sugestão nunca é
decisão automática.

**Correção 2026-08-05 (ver Decisão 6):** quando há foto, esta busca não
é um passo separado depois de o usuário classificar manualmente — é
parte da própria leitura de risco da imagem. A gravidade nasce junto com
a interpretação da foto, fundamentada em procedimento real, não como
lookup posterior a uma classificação já feita à mão.

**Correção 2026-08-05 (motor de risco unificado, achado em
`GENESIS/RESEARCH/luna-tabela-risco-iso-outcome.md`):** a gravidade não
é um número solto — usa a **mesma fórmula e metodologia** já desenhada
para `outcome` (`O`) do Signal Engine (ADR-019): Probabilidade (1-4) +
Gravidade (1-4) = Resultado, nomenclatura de perigo ISO/IEC 42001/23894,
critério `<5 Aceitável, =5 Tolerável, >5 Não Aceitável`. Não inventar uma
segunda fórmula de gravidade para o Convergia — parametrizar o mesmo
motor por domínio (trabalhador real, via `algoritmo_smx`/
`biblioteca_risco`, em vez do domínio de continuidade cognitiva da
LUNA). Esse motor está em Status Theory (documentado, não implementado
em código) — construí-lo pensando nos dois consumidores desde o início.

## Decisão 4 — Saída

**Correção 2026-08-05 (reconciliação):** `GENESIS/RESEARCH/
convergia-spec-tecnica-consolidada.md` rebaixa PDF de prioridade —
recomenda **docx** (lib `docx`, npm, custo zero de licença) como formato
editável prioritário, com PDF virando "bom ter depois", não bloqueador.
PPT continua válido no curto prazo (Architect confirmou "resolver com os
parsers que já temos" antes desta reconciliação) — docx é o próximo
formato a priorizar, não substituição imediata obrigatória do PPT.

"BI" nesta fase = o estilo visual dashboard já validado (KPI cards +
gráfico nativo), não exportação real para Power BI — evolução para
exportação real fica para quando o PPT for descontinuado como formato
principal (decisão já expressa pelo Architect, não cronograma fixo
aqui).

## Decisão 5 — Separação sensível/lógica no aprendizado

Cada achado gera dois destinos, nunca um só:

| Destino | Conteúdo | Onde persiste |
|---|---|---|
| Relatório específico daquela ronda | Foto, nome do responsável/pessoas envolvidas, local exato, cliente (razão social) — tudo em texto claro, é o relatório real daquele cliente | Guardian Storage, ligado só àquele relatório (mesmo padrão de `convergia_visual_templates`) |
| Aprendizado de longo prazo da Luna | Categoria de risco, gravidade, descrição da situação, medida preventiva, resultado prático observado depois, **departamento, local e cliente — só que tokenizados** (ver abaixo) | `memoria_luna`, mesmo caminho que `knowledge-gate.ts`/`memory-engine.ts` já usam para a aba Conhecimento |

**Confirmado pelo Architect (2026-08-05):** nome de pessoa (responsável ou
envolvida na imagem) nunca entra no aprendizado, em nenhuma forma —
diferente de departamento/local/cliente, que o Architect quer disponíveis
para mapear risco por setor e unidade ao longo do tempo. A solução: não
excluir esses três campos do aprendizado, **tokenizar**. Cliente (razão
social) e local/unidade viram um código estável (ex. `CLI-042`,
`UNI-007-S3`) nos registros de `memoria_luna` — nunca o nome real em
texto claro ali. Uma tabela separada, pequena, mapeia código → nome real
(mesmo padrão de coleção genérica do Guardian, nenhuma peça de
infraestrutura nova).

**Controle de acesso ao decodificador — faseado, decisão explícita do
Architect:**
- **Fase inicial (agora):** só o Architect decodifica. A Luna nunca
  converte código para nome real sozinha, nem para gerar o relatório
  específico — o que não é conflito, porque o relatório específico usa o
  dado real direto da entrada do wizard daquela ronda (nunca passa pelo
  código; a tokenização só existe na cópia que vai para `memoria_luna`).
  Quando a Luna referencia um padrão do aprendizado (ex. "situação
  parecida ocorreu antes em `UNI-007-S3`"), o código fica como código —
  só o Architect, com acesso à tabela de mapeamento, sabe a que unidade
  isso corresponde.
- **Fase futura ("quando estiver mais treinada", critério de maturidade
  não definido nesta sessão — fica para quando o Architect decidir que
  chegou a hora):** a Luna passa a decodificar automaticamente quando o
  contexto justificar (ex. respondendo diretamente ao Architect sobre um
  cliente específico), mas continua nunca expondo nome real numa busca
  de padrão geral/relatório de risco agregado (ex. "quais unidades têm
  mais não conformidade de X" mostra códigos, não nomes, mesmo depois de
  madura).

Fundamentação constitucional: Axioma III (conhecimento não é código),
Axioma IV (memória é reconstrução) — a memória de longo prazo guarda o
padrão reconstruível e tokenizado quando necessário, não o dado bruto
identificável.

**Refinamento 2026-08-05 (reconciliação):** a especificação consolidada
já distingue duas categorias de achado, com sensibilidade diferente —
incorporar essa distinção em vez da separação binária simples desta
decisão:
- **Estrutural** (empilhamento, centro de carga, sinalização de área —
  sem pessoa identificável na cena): sensibilidade mais baixa, mais
  próximo de "lógica pura".
- **EPI/comportamental** (envolve pessoa — uso de equipamento, postura,
  ação de operador): mesma disciplina de dado sensível já aplicada ao
  ASO — nunca entra no aprendizado com identificação de pessoa, mesmo
  tokenizado, pelo mesmo motivo que nome nunca entra.

## Decisão 6 — Leitura de risco na imagem, não descrição da imagem

**Correção do Architect (2026-08-05):** o objetivo não é a IA descrever o
que aparece na foto (objeto, cena, ambiente) — é interpretar a
**implicação de risco** que a cena representa, usando o mesmo
conhecimento de procedimento da Decisão 3. Exemplos concretos dados pelo
Architect: uma pilha de bobinas tortas não é "bobinas empilhadas
tortas" — é "indicação de peso fora do centro de carga"; uma empilhadeira
em ação não é "empilhadeira em operação" — é, se aplicável,
"atividade proibida por procedimento". A leitura tem que nascer
diagnóstica, não descritiva.

Isso significa que Decisão 6 e Decisão 3 **não são fases sequenciais
independentes** (ver correção na tabela de fases abaixo) — são a mesma
capacidade: ler a foto **à luz do procedimento já ingerido no Hipocampo**,
não ler a foto isolada e só depois, separadamente, buscar gravidade.

Reaproveita CONV-009 (já registrado, `GENESIS/ROADMAP.md` P4, ENG-028) —
não é capacidade nova a especificar do zero, é o caso de uso real que
justifica finalmente implementá-la.

**Correção 2026-08-05 (reconciliação com `GENESIS/RESEARCH/
convergia-spec-tecnica-consolidada.md`):** o caminho técnico registrado
em CONV-009 (estender `AnthropicHubConnector`) está **superado** pela
especificação consolidada, que recomenda **Qwen-VL via Groq** — provider
já configurado em `luna-core`, evita depender de imagem via Anthropic.
Não estender `AnthropicHubConnector`; usar o provider Groq já existente,
com modelo da família Qwen-VL.

A interpretação (a leitura diagnóstica, não uma legenda genérica) gera
também um **embedding**, armazenado junto no `memoria_luna` —
reaproveitando `pgvector`/índice HNSW/função de busca semântica já ativos
em produção (migrations de 2026-07-25), hoje usados só para busca de
texto. Quando uma foto nova chega, compara-se o embedding dela contra os
já guardados — "isso se parece com um achado anterior, mesma implicação
de risco" — sem guardar a foto em si na memória de comparação (Decisão 5).

**Disciplina de confiança, herdada do registro original de CONV-009 e do
ADR-014 Emenda 1 — ainda mais importante agora que a leitura é
diagnóstica, não descritiva:** toda interpretação de imagem nasce com
`provenance_state: "unverified"`. A foto é evidência real; a leitura que
a IA faz dela — e principalmente a implicação de risco que ela infere —
pode errar, do mesmo jeito que pode alucinar texto, e um erro aqui tem
consequência prática maior do que uma legenda errada (pode gerar uma não
conformidade que não existe, ou deixar passar uma que existe). Promove a
`corroborated` só depois de confirmação explícita do responsável pela
ronda — nunca decisão automática definitiva a partir só da leitura de
imagem.

**Confirmação do Architect (2026-08-05):** só a lógica da imagem entra
no aprendizado — nunca a imagem em si (Decisão 5 confirmada nesse ponto).
Revisão do usuário é obrigatória sempre, mas **precisa ser destacada com
prioridade quando a leitura da IA conflita com o que já está
estabelecido** — ex. a leitura sugere uma classificação/gravidade
diferente do que o procedimento indicaria, ou diferente de um achado
anterior semelhante já confirmado. Não é o mesmo nível de atenção que
uma leitura "sem precedente" (só nova) — conflito com algo já
estabelecido é o caso que mais precisa de olho humano antes de aceitar,
porque é onde um erro da IA teria mais chance de gerar uma decisão
errada silenciosamente aceita.

## Fases (ordem recomendada pelo Engineer)

| Fase | Entrega | Depende de |
|---|---|---|
| 1 | Wizard PWA de coleta (foto + campo + voz nativa + fila offline com reenvio automático), gravidade escolhida manualmente | Nada novo de infraestrutura de backend — service worker + IndexedDB são só front |
| 2 | Geração do relatório PPT a partir do que foi coletado, com a segunda forma de entrada (Decisão 2) | Fase 1 |
| 3 | Separação sensível/lógica alimentando `memoria_luna` (Decisão 5) | Fase 2 |
| 4 | Leitura de risco na imagem (Decisão 6, já incorpora Decisão 3 — gravidade nasce da mesma leitura, fundamentada em procedimento, não de um passo separado) + embedding + comparação com achados anteriores | Fase 3 + confirmar que `AnthropicHubConnector` aceita imagem + **`CONV-012` (pipeline assíncrono) — sem ele, não há como ingerir procedimento real no Hipocampo** |
| 5 | PDF, depois exportação BI real | CONV-005 (não existe ainda) |

Cada fase entrega valor sozinha — não é preciso esperar a Fase 6 pra Fase
1 já resolver o problema real (parar de perder foto/observação em papel).

## Pendências / decisões ainda abertas

- **Confirmado (2026-08-05):** linha sensível/lógica completa —
  departamento/local/cliente entram no aprendizado, mas tokenizados
  (código, não nome real); nome de pessoa nunca entra, em nenhuma forma;
  imagem em si nunca entra, só a lógica dela. Decodificador começa
  restrito só ao Architect, evolui para decodificação automática da Luna
  em contexto específico quando o Architect decidir que a maturidade
  justifica — ver Decisão 5.
- **Resolvido (2026-08-05):** não há procedimento real ingerido no
  Hipocampo hoje — os arquivos grandes (ex. cartilhas de treinamento)
  nunca subiram porque `CONV-012` (pipeline assíncrono) não existe.
  Existe pelo menos um arquivo real já disponível para quando
  `CONV-012` existir: cartilha de treinamento de operador de
  empilhadeira (Manserv), hoje só acessível como arquivo enviado ao
  Engineer, não ingerida no organismo. Fase 4 (ver tabela) passa a
  depender explicitamente de `CONV-012`, não é mais suposição em
  aberto.
- Formato exato do wizard mobile: **PWA**, recomendado pelo Engineer e
  aceito na direção geral (Decisão 1) — detalhe de implementação (que
  bibliotecas, estrutura exata da fila offline) fica para quando a Fase
  1 virar tarefa de Builder.

## Decisão 7 — Pontos adicionais da reconciliação (2026-08-05)

- **Regra do Gateway confirmada, sem violação:** nada neste ADR propõe
  Convergia virar capability do Gateway — permanece rota irmã
  (`/api/convergia/*`), inclusive a leitura de imagem (Decisão 6) e o
  motor de risco unificado (Decisão 3), consistente com
  `convergia-spec-tecnica-consolidada.md`.
- **Modelo de "3 chaves"** (Primária/Secundária 1/Secundária 2),
  generalização do RE/Nome/Cargo já usado em `CONV-011`: adotado como
  padrão de identificação de sujeito de documento em todo o Convergia,
  não só ronda fotográfica — achado sem inconsistência com o resto do
  ADR, só complementa.
- **NRs como banco de perguntas:** a leitura de risco da Decisão 6
  formula a pergunta que a foto responde no mesmo formato que um
  técnico de segurança (TST) usaria para inspecionar manualmente —
  mesma pergunta, dois avaliadores possíveis (humano ou IA). Mecanismo
  concreto de como a leitura de imagem se ancora em procedimento real,
  não só referência solta a "consultar Hipocampo".

## Decisão 8 — Referência de dado real (Manserv), layout continua sendo o nosso

Achado nesta sessão: relatório real da Manserv (`Rotina SSMA -
AVALIAÇÃO DE RISCO CRÍTICO`, unidade Sylvamo/Mogi Guaçu, 28/05/2026) —
não é hipotético, é um relatório de campo real, com estrutura de 7
categorias de risco (Trabalho em Altura, Espaço Confinado, Energia
Perigosa/LOTO, Eletricidade, Inflamáveis/Atmosfera Explosiva,
Movimentação de Cargas, Máquinas e Equipamentos), cada uma com
Severidade × Probabilidade, e um "Complemento de Observação" em texto
corrido (exemplo real: bujão de gás mal armazenado, citando NR-16,
causa, risco, medida imediata/longo prazo) — formato de saída
diagnóstica que bate exatamente com o que a Decisão 6 pede da leitura
de imagem.

**Uso decidido pelo Architect (2026-08-05): só informação, categorias
de risco e conceito de gráfico — não o layout.** O layout/design visual
do relatório final continua sendo o nosso, já validado no protótipo do
ADR-020 (paleta Midnight Executive, KPI cards, gráfico nativo doughnut/
barra). Não clonar a estrutura de página do PDF da Manserv (tabelas com
foto em rack, layout de formulário).

**O que aproveitar deste documento, concretamente:**
- As 7 categorias de risco como candidatas reais para popular
  `biblioteca_risco`/`biblioteca_atividade` (Decisão 3/Etapa 6 do plano
  de ação) — taxonomia real da Manserv, não genérica inventada.
- O texto de "Complemento de Observação" como modelo do estilo de
  escrita que a leitura de imagem (Decisão 6) deve produzir — parágrafo
  diagnóstico (causa, risco, referência normativa, medida), não legenda
  solta.
- O par Severidade × Probabilidade por achado confirma, com evidência
  real de campo, a fórmula já adotada na Decisão 3 (Probabilidade+
  Gravidade=Resultado, ISO/IEC 42001/23894).

Status do documento: reconciliado com `convergia-spec-tecnica-consolidada.md`,
`luna-tabela-risco-iso-outcome.md` e o relatório real da Manserv em
2026-08-05 — pronto para ratificação final do Architect, sem pendência
de investigação adicional conhecida.

## Consequência

Se aceito, Convergia ganha uma terceira forma de entrada (não-tabular),
uma superfície de uso nova (mobile, fora do Forge), e a primeira aplicação
real de CONV-009 (visão), já conectada à disciplina de confiança que a
Constitution exige. Não conflita com nenhum ADR existente — estende
ADR-012 (Convergia), ADR-014 (disciplina de confiança), CONV-009 (visão,
já registrado).
