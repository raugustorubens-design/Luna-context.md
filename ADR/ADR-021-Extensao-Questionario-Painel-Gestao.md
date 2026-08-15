# ADR-021 — Extensão: Questionário Gerado, Painel de Gestão e Pendências

Status: Pendências P1-P3 resolvidas (2026-08-09) — escopo técnico de
Decisão 1/2 ainda por detalhar antes de instrução de Builder; ver também
revisão de arquitetura de achado dinâmico, que pode afetar como P2 é
implementada. Feedback do primeiro teste real em campo (2026-08-10/11)
registrado na última seção deste documento — dois itens sem escopo
técnico e dois princípios permanentes.
Data: 2026-08-09
Decisor: Architect (Rubens)
Contexto: Engineer (Claude, chat) — consolida uma sessão longa de divagação
(2026-08-07/08) sobre o ADR-021 (Convergia Mobile: Ronda Fotográfica), para
não depender de segurar tudo de cabeça numa conversa só. Registrado como
extensão separada, não como edição do corpo do ADR-021 original — mesma
convenção já usada por `ADR-011-Emenda-Simbolos-M-X-A-Gamma.md` (emenda ao
ADR-010) e `ADR-014-Emenda-1-...` (emenda ao ADR-014).

## Como chegamos aqui

Comparação com o Checklist Fácil (RZ2), ferramenta comercial de mercado
usada como referência de estrutura — não como fonte de conteúdo. O
conteúdo real (categorias, campos, questionários) vem da experiência e
pesquisa do próprio Architect, que já elaborou muitos desses questionários
antes, não de observar uma empresa específica. Duas coisas ficaram claras
dessa comparação:

1. O wizard de ronda (Fase 1 do ADR-021, já em produção) resolve só a
   ponta de coleta — falta a outra metade, um painel de gestão olhando
   todas as rondas ao longo do tempo (a referência de mercado tem
   Dashboard, Planos de Ação, Agendamentos — nós temos só o wizard).
2. O wizard hoje tem fluxo fixo por categoria de risco. A conversa evoluiu
   pra: e se o questionário que guia a ronda não fosse fixo, e sim montado
   a partir de modelo + dado real + IA?

## Decisão 1 — Questionário por modelo, não fluxo fixo nem construção livre

Descartamos duas ideias intermediárias antes de chegar aqui:
- Fluxo fixo por categoria de risco (o que existe hoje) — rígido demais
  pro que o Architect quer.
- Construção 100% livre no chat da Luna, no Forge — esbarra num problema
  técnico real: o chat da Luna hoje só devolve texto, não tem mecanismo de
  "decidir sozinha o que salvar" no meio da conversa (mesmo achado que
  pausou o `A(t)`/modo sombra mais cedo na sessão — `runCognitiveEngine`
  não tem tool-calling; ligado a `FORGE-WORKSPACE-001`, já registrado em
  `ENG-038`).

**Decisão final:** três modelos prontos como ponto de partida, extensíveis
(não lista fechada em código):

| Modelo | Fonte de dado real |
|---|---|
| Riscos Críticos | `controle_risco`/`atividade_risco` — categorias que exigem PT (altura, espaço confinado, elétrico, LOTO) |
| Procedimentos | `biblioteca_protocolo` — as ferramentas do PGR (APR, OPAI, IPS, AP, etc.) |
| 5S | Checklist específico de organização/limpeza |

A pessoa escolhe o modelo → Luna sugere a estrutura com dado real da
categoria (usando o banco já populado hoje) → pessoa revisa e ajusta →
**confirma antes de salvar**. IA nunca grava sozinha — mesmo princípio de
cautela já usado em `A(t)` e na separação sensível/lógica do ADR-021
(Decisão 5). Isso é construível agora, sem esperar tool-calling existir.

**Por que "3 modelos fixos" não pode virar arquitetura fechada:** o
Architect já elaborou, na prática profissional, bem mais de 3 tipos de
questionário/rotina de inspeção ao longo do tempo (alerta preventivo,
análise de risco/PT, compliance, acompanhamento de perícia, boas práticas,
campanhas, controle de exame ocupacional, diálogo de segurança,
housekeeping/5S, inspeção de meio ambiente, entre outros). Isso confirma,
com experiência real, que os 3 modelos iniciais são ponto de partida, não
teto — a base de dados (tabela, não enum) já aguenta crescer sem
redesenho, e o catálogo de modelos deve ser editável, não fixo no código.

**Estrutura de campo de referência**, no padrão de um "alerta preventivo"
já elaborado pelo Architect — usada como referência concreta pro modelo
"Riscos Críticos", não inventar nome de campo do zero:

| Campo de referência | Equivalente no wizard hoje |
|---|---|
| Descrição detalhada do desvio | Descrição |
| Tipo de desvio | Classificação (mais granular que o Positivo/Atenção/Não Conformidade atual) |
| Ação imediata | Ação recomendada |
| Criticidade do desvio | Gravidade |
| **Desvio identificado foi tratado?** | **Não existe hoje** — campo de status de resolução, ciclo de vida, pertence ao painel de gestão (Decisão 2), não à captura inicial |
| Plano de ação → Responsável pela aprovação | **Não existe hoje** — hierarquia/aprovação |
| Plano de ação → Local/área do desvio | Departamento |
| Plano de ação → Responsável da área | Responsável |

A estrutura do wizard já bate de perto com esse padrão de referência — os
dois campos que faltam ("tratado?", "aprovação") são exatamente os dois
que fazem mais sentido no painel de gestão (Decisão 2) do que na captura
em campo, porque são sobre o que acontece *depois* da ronda, não durante.

## Decisão 2 — Painel de gestão (novo, sem código ainda)

Inspirado na estrutura de referência de mercado (não na estética —
identidade visual continua sendo a do Forge, paleta Midnight já definida
anteriormente):

- Dashboard com contagem agregada de status ao longo do tempo (em
  andamento, atrasado, aguardando solução) — não só resultado de uma
  ronda.
- Lista filtrável (status, período, unidade) reaproveitada em telas
  diferentes.
- Achados viram itens rastreáveis tipo Plano de Ação (aberto → em
  andamento → resolvido/atrasado).

Ainda sem ID de roadmap formal (`CONV-0XX` a definir) nem escopo técnico
detalhado — fica para quando as pendências abaixo fecharem.

## Decisão 3 — Fase 2 (`CONV-014`, geração do relatório): templates multi-página enviados pela empresa

Especificação dada pelo Architect (2026-08-09/10), registrada antes de
qualquer código:

**Estrutura mínima do template**, todas opcionais de upload (se ausente,
cai no padrão nosso — ver abaixo):
- Capa
- Página de KPI/dashboard (gráficos)
- Página de achado — **repete automaticamente uma vez por achado da
  ronda**, não é uma página por tipo de achado. Confirmado pelo
  Architect: as 19 páginas do protótipo original eram capa(1) +
  dashboard(1) + achado repetido(16) + contracapa(1) — não 16 templates
  diferentes.
- Contracapa

**Formatos de upload aceitos, com diferença real de dificuldade —
registrado para não prometer os cinco como se fossem do mesmo tamanho:**

| Formato | Caminho técnico | Dificuldade |
|---|---|---|
| PPT | Converter a página relevante em imagem, mesmo mecanismo do CONV-001 (imagem de fundo + campo posicionado) | Viável, reaproveita infraestrutura existente |
| docx | Mesmo caminho — converter em imagem | Viável |
| PDF | Mesmo caminho — já era plano cogitado antes (primeira página → imagem) | Viável |
| XLS | Não é template visual — é o formato de exportação de dado (ver abaixo), não de layout de capa/contracapa | N/A como template |
| Power BI | **Não é template de upload** — confirmado pelo Architect: o que importa é migrar o *dado* pra lá, não importar `.pbix` como layout. Resolvido pela exportação CSV/XLS abaixo — Power BI importa CSV/Excel nativamente, não precisamos escrever `.pbix` nunca. Deixa de ser caso difícil. |

**Fallback:** se a empresa não subir template próprio, usamos o nosso
padrão (Midnight Executive, já validado no protótipo). Mesma lógica pros
gráficos — se não houver gráfico customizado, usamos os nossos.

**Exportação de dado sempre disponível:** independente do template usado,
o relatório vem acompanhado de uma tabela em CSV/XLS com os dados brutos
(achados, contagem por classificação/severidade) — pra o cliente gerar o
gráfico que quiser, na ferramenta que quiser, direto a partir do
relatório. **Esse é também o caminho de migração pro Power BI** — CSV/
Excel é formato de importação nativa do Power BI, não precisamos gerar
`.pbix` nem entender o formato interno dele.

**Posicionamento automático — grade fixa, não reconhecimento de layout
(correção do Engineer, 2026-08-10):** a primeira leitura do Engineer supôs
que "posicionamento automático" exigiria visão computacional inferindo
onde cada campo cabe dentro do design específico de cada cliente — isso
seria trabalho real de investigação técnica incerta. Correção do
Architect: não é isso. É uma grade fixa, definida uma vez, aplicada a
qualquer cliente — a identidade visual do cliente (cor, logo, fundo)
preenche a moldura por trás; a posição dos campos em si segue a mesma
grade sempre, sem precisar inferir nada por cliente. Isso já é o que o
CONV-001 faz hoje (campo em posição percentual sobre uma imagem de
fundo) — só a origem da posição muda, de "alguém arrastou" pra "grade
padrão pré-definida pelo Engineer/Architect uma vez, aplicada sempre".

**Correção do Engineer (2026-08-10), com base em dois arquivos reais
fornecidos pelo Architect** — a grade original desta seção (caixa de
texto de 600-800 palavras à esquerda) foi especulação verbal, sem
arquivo de referência. Com os dois arquivos reais em mãos, fica claro
que **não existe uma grade só — existem dois modelos de saída
distintos, que devem coexistir como opções**, não um substituindo o
outro:

**Modelo "Detalhado"** (referência real: relatório "Rotina SSMA -
Avaliação de Risco Crítico", Manserv/Checklist Fácil — nome do cliente
e da unidade removidos do registro, mesmo cuidado de sempre) — já
documentado como Decisão 8 do ADR-021 original: por categoria de risco,
Severidade/Probabilidade, texto corrido de complemento/observação
(NR citada, causa, medida imediata/longo prazo). Denso em texto,
formato de auditoria técnica.

**Modelo "Visual"** (referência real: `Ronda_Diaria_5S_05-08.pptx`,
19 slides, arquivo real de campo) — foto-primeiro, texto mínimo (uma
linha de departamento + uma linha de descrição), estrutura confirmada:
- Capa: título, subtítulo, data, resumo de uma linha.
- Sumário/dashboard: 4 cartões de KPI (total/positivo/atenção/não
  conformidade) + 2 gráficos (podem ser imagem estática, como no
  arquivo real, ou gráfico nativo — não decidido).
- Página de achado (**paisagem**, a orientação confirmada no arquivo
  real): departamento (1 linha) + descrição (1 linha) + selo de
  classificação sólido (cor exata já definida) + severidade quando Não
  Conformidade + **1 ou 2 fotos empilhadas verticalmente** (não lado a
  lado) ocupando quase a largura toda do slide.
- Página de achado (**retrato**, variação para quando o cliente
  preferir — sem arquivo real de referência ainda, mantém a decisão
  verbal anterior do Architect, ordem de cima pra baixo): 1)
  identificação do local e do risco, 2) fotos, 3) legenda/descrição.
- Contracapa: encerramento + resumo final.
- **Fotos confirmadas panorâmicas** no arquivo real (proporção ~3.8:1
  a 4.6:1) — a foto **encolhe pra caber inteira dentro da caixa** (sem
  cortar, sem esticar/distorcer; mesmo princípio "contain" já corrigido
  no CONV-001) — se sobrar espaço por causa da proporção, fica em
  branco ali, a foto nunca deforma.

**Decisão nova do Architect (2026-08-10):** os dois modelos (Detalhado
e Visual) ficam disponíveis como opções no catálogo de templates da
Fase 2 — a pessoa escolhe qual estilo de saída quer pra aquele
relatório, nenhum substitui o outro. Isso é **modelo de relatório**
(como o resultado final aparece), distinto de **modelo de
questionário** (o que perguntar durante a coleta, ver documento de
revisão de arquitetura de achado dinâmico/flags) — os dois usam a
palavra "modelo", mas são conceitos diferentes, não confundir.

**Rodapé fixo, não editável pelo cliente** — presente em toda página do
relatório, em qualquer modelo (Detalhado ou Visual), independente da
orientação ou do template enviado pelo cliente:
- Identificação "LUNA Safety Walk".
- Número da página.
- Quando aplicável, a nota de auditoria de edição ("Editado em [data]",
  ver logo abaixo) também vive nesta área.

O cliente pode customizar cor/logo/fundo do resto da página — o rodapé em
si (conteúdo e presença) não é customizável, garante rastreabilidade
mínima em qualquer relatório gerado pelo sistema.

**Densificação automática por IA ao trocar de modelo (decisão do
Architect, 2026-08-10):** ao gerar um relatório no modelo Visual a
partir de achados escritos no formato Detalhado (texto corrido, tipo
"Complemento de Observação"), a descrição longa passa por resumo
automático via IA (mesmo provedor já usado no projeto), virando a
legenda curta que o modelo Visual exige — **sem confirmação humana a
cada geração**, roda direto no fluxo.

**Por que isso não contradiz o princípio de "IA nunca decide sozinha"
já usado no resto do ADR-021** (`A(t)`, questionário por modelo, Fase
4): nos outros casos, a IA decide algo que **vira dado novo, gravado
como verdade** (um achado, uma classificação de risco). Aqui é
diferente — o achado original, escrito pela pessoa, **nunca é alterado
nem sobrescrito**; a densificação só afeta como o relatório *exibe*
aquele texto no modelo Visual. O dado de origem permanece intacto e
consultável a qualquer momento (trocar de volta pro modelo Detalhado
mostra o texto completo, sem perda). Não é a IA decidindo o que
aconteceu — é reformatação de exibição sobre algo já decidido e salvo
pelo humano. Essa é a distinção que torna a automação aceitável aqui,
mesmo mantendo confirmação humana obrigatória em todos os outros pontos
do sistema.

**Auditoria de edição pós-geração:** toda vez que um relatório for gerado
a partir de uma ronda que foi editada depois da geração original (ver
Tarefa 3, `PATCH /convergia/ronda/:id`, já em execução), o documento final
precisa mostrar uma nota visível — **canto inferior esquerdo**, tipo
"Editado em [data]" — deixando claro que o conteúdo não é o original
intocado. Isso é requisito da Fase 2 (o relatório gerado), não da Fase 1
(a ronda em si, que já está em produção) — fica registrado aqui pra não se
perder até a Fase 2 ser construída.

## Pendências — respostas necessárias do Architect antes de qualquer instrução de Builder

**P1 — PT: só sinalizar, ou gerenciar de verdade?**
O sistema aponta "esta categoria exige PT" (referência/lembrete, pequeno)
— ou o sistema emite, aprova e arquiva a Permissão de Trabalho em si
(sistema à parte, grande)? Isso muda o tamanho do trabalho em uma ordem de
grandeza.

**P1 (resolvida, 2026-08-09):** PT só sinaliza — o sistema aponta que a
categoria exige PT, a emissão/aprovação real continua sendo do dono da
área, fora do software.

**P2 — Passivo trabalhista: qual dos três?**
(a) Repositório de documento por pessoa/cargo (ASO, certificado de
treinamento, com alerta de vencimento) — conecta com o que já existe.
(b) Base de referência de direito trabalhista (tipo uma "biblioteca_risco"
de lei, não de pessoa) — conhecimento consultável.
(c) Rastreamento de passivo jurídico real (processo em andamento, valor,
prazo) — mais sensível, mais perto de sistema jurídico que de SSMA.

**P2 (resolvida, 2026-08-09):** Passivo trabalhista vira uma 8ª categoria
de risco, no mesmo mecanismo de 3 estados já usado pelas 7 atuais (não
avaliado/identificado/inexistente) — quando identificado, descrito em
texto livre pelo profissional de SSMA, sem categoria fixa pré-definida
(situações "quase infinitas", nas palavras do Architect). A Luna aprende
com as descrições ao longo do tempo (conecta com Decisão 5 do ADR-021
original — sensível/lógica antes de virar memória), em vez de tentar
catalogar antecipadamente.
**Nota de reconciliação:** essa resposta assume o mecanismo de "categoria
fixa com 3 estados" que estava em produção em 2026-08-09. Uma revisão de
arquitetura posterior, no mesmo dia
(`GENESIS/RESEARCH/revisao-arquitetura-achado-dinamico-flags-foto.md`),
questiona se esse mecanismo continua existindo como "categoria fixa" ou
vira "flag" dentro de uma lista dinâmica de achado — sem resposta ainda. A
essência da decisão de P2 (descrição livre, aprendizado ao longo do
tempo, sem categorização antecipada) continua válida de qualquer forma;
só o mecanismo técnico exato pode mudar.

**P3 — Sequenciamento**
Dado tudo que já está na fila (Ctrl+V no Template Visual, cores de
classificação, tema claro/escuro, e agora isso) — esta extensão inteira
entra depois do que já está pronto pra colar, ou o Architect quer
priorizar diferente?

**P3 (resolvida, 2026-08-09):** ordem de prioridade após a extensão de
edição de ronda (Fase 1/CONV-013) já entregue: 1) esta extensão
(questionário por modelo + painel de gestão), 2) `CONV-012` (pipeline
assíncrono), 3) validação de campo real do wizard offline.

Sem resposta às pendências, não se prepara instrução de Builder para
nenhuma parte desta extensão — só o que já estava aprovado antes desta
divagação continua valendo (as três instruções já prontas: Ctrl+V, cores
de classificação, tema claro/escuro).

## Consequência

Se aceito, o ADR-021 ganha uma segunda metade — um painel de gestão que
fecha o ciclo aberto pelo wizard de coleta (Fase 1) — e o questionário de
ronda deixa de ser fluxo fixo por categoria para virar modelo extensível
composto com dado real + IA, sempre com confirmação humana antes de
salvar (mesma disciplina de confiança já exigida em Decisão 6 do ADR-021
original e no Art. AAAB.9 da Constitution). Não conflita com o ADR-021
original — estende Decisão 2 (estrutura de entrada) e a tabela de Fases,
sem alterar nenhuma decisão já aceita. Escopo técnico e ID de roadmap
formal (`CONV-0XX`) ficam para quando P1-P3 fecharem.

## Feedback de teste real (2026-08-10/11) — quatro decisões registradas

**Toda edição de TST vira memória — extensão real do Hipocampo, maior
que o que `CONV-018`/Rodada 2 entregou.** Hoje `persistSuggestionCorrection`
só captura a diferença entre sugestão de IA (flag ou Fase 4) e o que o
humano salvou — **não** captura edição que não veio de sugestão nenhuma
(TST preenchendo do zero, sem "+" de sugestão por trás). Decisão do
Architect: isso precisa mudar — toda edição relevante de TST deve
alimentar o Hipocampo, não só a correção sobre sugestão. **Sem escopo
técnico definido ainda** — precisa de investigação antes de virar
instrução de Builder (o que conta como "edição relevante"? Todo campo
alterado, ou só na conclusão da ronda? Mesmo `tipo` de registro em
`memoria_luna` ou um novo?).

**Contagem/frequência de padrão ao longo do tempo — na prática, isto é
o painel de gestão (Decisão 2 da extensão do ADR-021), não uma extensão
do Hipocampo.** "Que risco aparece mais" é consulta agregada sobre
`convergia_rondas`/achados já existentes (`COUNT`/`GROUP BY` real), não
precisa de IA nem de memória de longo prazo pra funcionar — é
exatamente o "dashboard com contagem agregada de status ao longo do
tempo" já especificado na Decisão 2, ainda sem código. Registrado aqui
como esclarecimento: quando o painel de gestão for escopado
tecnicamente, este pedido do Architect já está coberto por ele, não é
peça nova a somar.

**Princípio permanente: usuário final nunca vê nome de provedor de
IA (Groq, Claude, GPT, etc.) — sempre "Luna".** Confirmado, investigando
o código em 2026-08-10, que o produto voltado a usuário final (LUNA
Safety Walk) já respeita isso hoje (o selo de baixa confiança da Fase 4
diz "IA não teve certeza", nunca nome de modelo/provedor). O seletor de
modelo visível no Forge (`"GPT"`/`"Claude"`/`"Groq"`) é ferramenta de
desenvolvedor (Architect/Engineer escolhendo modelo pra construir o
sistema), não produto de usuário final — não é violação deste
princípio, é contexto diferente. Registrado como regra permanente a
respeitar em qualquer superfície nova voltada a usuário final
(Convergia, painel de gestão, relatório gerado) — nenhuma delas deve
expor nome de provedor.

**Princípio: até existir mecanismo de comparação de imagem, o relato
escrito do TST é a fonte principal de conhecimento, não a leitura de
imagem por IA.** A leitura de foto (Fase 4) continua sendo só sugestão,
nunca fonte de verdade — o texto que o TST escreve (confirmado ou
corrigido por ele) é o que prevalece. Nenhuma mudança de código
necessária — já é assim hoje (Fase 4 nunca grava sozinha, humano sempre
confirma) — registrado aqui como confirmação explícita do princípio,
não como conserto.
