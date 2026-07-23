# BUILDER

Owner: Claude Code

Use this file for implementation status, constraints, tests, and local decisions.

## What goes here
- Implemented work
- Test status
- Known limitations
- Local technical decisions
- Build issues
- Completion notes

## What does not go here
- Architecture changes
- Final decisions
- Permanent knowledge

## Entry format
- ID
- Date
- Topic
- What changed
- What is blocked
- Test status
- Next action

## Current workplan
- Implement only what the Architects and Engineer approved.
- Keep Connector Hub boundaries intact.
- Keep Guardian internal and isolated by contracts.
- Update the implementation status after each relevant merge.
- Toda etapa de implementação concluída inclui, no mesmo commit, a
  atualização deste arquivo (BUILDER.md) com autoatestação em primeira
  pessoa ("eu fiz") — ver ENG-006.
- Mesmo em modo de sessão simultânea com Engineer/Architect, apenas o
  Builder commita; os demais papéis produzem diff sugerido, nunca commit
  próprio — ver ENG-008/ENG-009.

## ID: BLD-001
Data: 2026-07-13
Tópico: model.chat / model.chat_deep / storage.query / storage.insert (luna-core)

O que mudou:
- Novos manifests: gateway/manifest/{model-chat,model-chat-deep,storage-query,storage-insert}.ts
- Novas capabilities: gateway/capabilities/model/{chat,chat-deep}.ts (consomem
  o Model Router do PR #9), gateway/capabilities/storage/{query,insert}.ts
  (consomem o SupabaseHubConnector diretamente, sem adapter próprio)
- gateway/index.ts: createGatewayRegistry passa a aceitar modelRouter? e
  supabase? opcionais; as 4 capabilities só são registradas se o respectivo
  parâmetro estiver presente
- app.ts: construção dos conectores de code-reasoning (como grupo) e do
  Supabase isolada em try/catch cada — credencial ausente desativa a(s)
  capability(ies) correspondente(s) em vez de derrubar o boot
- README.md (luna-core): nova seção "Capabilities condicionais" + tabela de
  env vars atualizada

O que está bloqueado:
- Push direto ao GitHub: o App conectado nesta sessão está com "Contents"
  somente leitura (403 em toda tentativa de escrita). Entregue como patch
  (`luna-core-model-storage-capabilities.patch`) para `git apply` manual ou
  push local; não há PR aberta ainda porque não consegui criar branch/commit
  remotamente.
- Nenhuma das 4 capabilities roda de fato em produção até GROQ_API_KEY,
  DEEPSEEK_API_KEY, OPENROUTER_API_KEY, ANTHROPIC_API_KEY (model.*) e
  SUPABASE_URL/SUPABASE_KEY (storage.*) serem configuradas no Railway — isso
  é o comportamento pretendido (design condicional), não uma pendência de
  código.

Test status:
- npm run typecheck: OK
- npm run test:architecture: OK
- npm test: 94/94 (nenhum teste novo adicionado ainda para as 4 capabilities novas)
- Smoke test manual do boot: sem env vars → sem crash, as 4 capabilities
  ausentes de /api/gateway/capabilities; com env vars fake → as 4 aparecem

Next action:
- Aplicar o patch (git apply + commit + push) ou ajustar a permissão do
  GitHub App para eu commitar direto
- Configurar as credenciais reais no Railway para ativar de fato
- Considerar adicionar testes unitários para as 4 capabilities novas (hoje só
  o Model Router em si tem cobertura, herdada do PR #9)

## 2026-07-17 — Pacote 1/6: ARCH-001

Eu fiz: registrei ARCH-001 (congelamento de Hipocampo, Fórmula de memória,
Reporter automático e Genome até o Forge v0.1 estar em uso diário) em
GENESIS/ARCHITECTS.md, e criei GENESIS/RESEARCH/meta-cognitive-memory.md
como Research Hypothesis, sem nenhuma implementação de código associada —
nenhum outro arquivo foi alterado.

## 2026-07-17 — Pacote 2/6: GENESIS/FORGE.md

Eu fiz: criei GENESIS/FORGE.md (owner: sessão multiagente, coordenada por
projeto) com a Theory "Modelo de órgãos" — Forge não é a IDE, é o cockpit
da LUNA; a IDE é um órgão dentro dele. Ainda não promovida à Constituição.
Adicionei FORGE.md e RESEARCH/ ao índice "Files" de GENESIS/README.md. Isto
resolve o bloqueio citado em ENG-009/FORGE-001 (documento antes inexistente
no repositório). Nenhuma implementação de código associada.

## 2026-07-17 — Pacote 3/6: continuação de GENESIS/FORGE.md

Eu fiz: continuei GENESIS/FORGE.md (o segundo arquivo criado nesta série de
pacotes, ver entrada acima) — adicionei "Definição de trabalho", a árvore
de órgãos (Workspace/Memory/Reporter/Guardian/Runtime/Projects/
Observability/Constitution) e a seção "Forge v0.1 — especificação técnica
(Design Decision, não ADR)" com Chat, Workspace v0.1 e Execution Metadata,
todos completos conforme entregue. NÃO preenchi Storage Contract: a
mensagem que a especificava foi cortada pela interrupção antes do corpo da
seção — deixei como pendência explícita em FORGE.md em vez de inventar o
contrato, para não violar a Regra 6 (Builder persiste, não especifica).
Nenhuma implementação de código associada.

## 2026-07-17 — Pacote 4/6: Storage Contract, GitHub, Reporter (manual), FORGE-001

Eu fiz: completei a seção Storage Contract em GENESIS/FORGE.md (pendência
do pacote 3) e adicionei as seções GitHub e Reporter (manual) ao spec
v0.1, todas exatamente como entregue. Registrei GENESIS/FORGE.md § ID:
FORGE-001 (multiagente simultâneo decidido, implementação adiada pro
v0.2) — responde ao item FORGE-001 do P0 em GENESIS/ROADMAP.md, mas não
marquei o checkbox lá: marcação de conclusão é escopo do Reporter por
evidência (ENG-007/Regra 6), não do Builder. Nota: FORGE-001 cita ENG-010
"para requisitos técnicos" — ENG-010 ainda não foi recebido nesta sessão,
não persistido. Nenhuma implementação de código associada.

## 2026-07-17 — Pacote 5/6: ENG-010, RESEARCH/README, Meta-Cognitive Memory, P00, FORGE-WORKSPACE-001

Eu fiz: registrei ENG-010 em GENESIS/ENGINEER.md (requisitos técnicos
mínimos para multiagente v0.2, resolvendo a pendência anotada no pacote
4). Criei GENESIS/RESEARCH/README.md com o pipeline Hypothesis → Research
→ Theory → Architecture (ADR) → Implementation. Reescrevi
GENESIS/RESEARCH/meta-cognitive-memory.md com o conteúdo completo (árvore
de memória Semantic/Episodic/Operational/Meta-Cognitive, ideia,
posicionamento estratégico, motivo do congelamento) — substitui o stub que
eu mesmo tinha criado no pacote 1. Em GENESIS/ROADMAP.md: adicionei P00
"Forge v0.1: ferramenta de uso diário" (FORGE-MVP-01 a 08) no topo, acima
do P0; adicionei o item FORGE-WORKSPACE-001; e atualizei o heading do P0
existente para "(CONGELADO, ver ARCH-001 — retomar após Forge v0.1 em uso
diário)", mantendo os 7 itens exatamente como estavam (inclusive BLD-002,
que não apareceu na lista abreviada da instrução — interpretei "mantidos
como estavam" como não remover nada).

Nota: o item FORGE-001 dentro do P0 ainda diz "aplicar GENESIS/FORGE.md
primeiro, ainda pendente de commit", o que já não é verdade desde o pacote
2 — não corrigi o texto porque a instrução foi manter os itens como
estavam; sinalizando para correção futura via Reporter/Architect.
Nenhuma implementação de código associada.

## 2026-07-17 — Pacote 6/6: P0 revisado (BLD-002 e FORGE-001 saem da lista)

Eu fiz: substituí a lista de itens do P0 em GENESIS/ROADMAP.md pela versão
enviada agora — MEM-001, STOR-001, GEN-001, REP-001, INFRA-001, texto
exatamente como entregue. BLD-002 e FORGE-001 saem da lista: confirma o que
eu já tinha sinalizado no pacote 5 (a omissão deles na lista abreviada não
era acidental). Entendimento: BLD-002 já está resolvido na prática pela
disciplina de autoatestação (ENG-006) em vigor durante toda esta série de
pacotes; FORGE-001 já foi resolvido como decisão formal em GENESIS/FORGE.md
(pacote 4) — nenhum dos dois precisa continuar como item de P0 em aberto.
Não apaguei o registro histórico de FORGE-001 em FORGE.md nem a entrada de
ENG-006 — só o item de checklist do Roadmap. Nenhuma implementação de
código associada. Este é o pacote 6/6 — relatório final a seguir.

## 2026-07-17 — Execução FORGE-MVP-01..08 em luna-frontend: início

Eu fiz: auditei `raugustorubens-design/luna-frontend` (branch `main`, já
com `claude/forge-dev-mode` + Google OAuth + Guardian Memory Index
mergeados) antes de escrever qualquer código — `pnpm install`/`typecheck`/
`test` (17/17)/`test:constitution`/`build` todos passam limpo. FORGE-MVP-01
já está satisfeito no código: Explorer/Editor/Chat/GitPanel/Terminal/
ContextPanel existem e funcionam. O que resta não é código deste
repositório: (1) variáveis de ambiente no Railway (login Google,
FORGE_ALLOWED_EMAIL, tokens) — sem acesso de rede/infra para configurar ou
verificar daqui; (2) `/chat` do backend atual tem contrato diferente do
esperado pelo cliente (lacuna já documentada no próprio `DEPLOY.md` do
repo, nota do ADR-004) — bug de outro repositório. Decisão do Architect
(2026-07-17): tratar como satisfeito, documentar os 2 bloqueios, seguir.

Correção factual sobre a premissa do FORGE-MVP-08: a especificação (pacote
3) partiu de "Workspace v0.1: integração fina com Claude Code (IDE-grade já
existente), não reimplementação de editor/LSP/terminal" como se nenhum
editor/terminal existisse ainda no Forge. Isso estava desatualizado —
`luna-frontend` já tem Editor (Monaco) e Terminal (xterm/WebSocket)
funcionais, herdados da consolidação do Forge MVP-01 (`claude/forge-dev-mode`,
já mergeado). Decisão do Architect (2026-07-17): manter Monaco/xterm como
estão — são trabalho pronto (sunk cost), não o "reimplementar" que a regra
queria evitar. FORGE-MVP-08 passa a ser um painel/modo adicional de
integração com Claude Code, ao lado do Editor/Terminal atuais, sem
substituí-los. Correção factual, não novo trade-off arquitetural — não
registrada em ARCHITECTS.md.

Próxima ação: seguir a ordem definida (05 → 04 → 02 → 06 → 03 → 07 → 08)
implementando em `luna-frontend`.

## 2026-07-17 — FORGE-MVP-05: Execution Metadata

Eu fiz: em `raugustorubens-design/luna-frontend`, branch
`claude/forge-mvp-01-08`, commit `5e0c57a` — criei `lib/forge/memory.ts`
(tipos `ExecutionMetadata`/`MemoryItem`, `createMemoryItem()`) e
`lib/forge/__tests__/memory.test.ts` (3 testes novos). `typecheck` limpo,
`test` 20/20 (17 pré-existentes + 3 novos). Schema exatamente como
especificado em GENESIS/FORGE.md § Execution Metadata — `project` é string
aberta, `KNOWN_FORGE_PROJECTS` é só a lista de UI (LUNA/RENASCER/SMX/CURSO
EMPILHADEIRA) para o seletor do FORGE-MVP-03, não uma restrição de schema.
Commit empurrado para `origin/claude/forge-mvp-01-08` (PR não solicitado).

## 2026-07-17 — FORGE-MVP-04: Storage Contract

Eu fiz: em `luna-frontend`, branch `claude/forge-mvp-01-08`, commit
`322bba0` (empurrado) — adicionei `persistMemory`/`retrieveMemory` a
`lib/forge/api-client.ts`, chamando `guardian.persist_memory`/
`guardian.retrieve_memory` via Gateway, mesmo padrão de
`searchGuardianMemoryIndex` já existente (Forge só fala com Guardian, nunca
com Storage Contract/Supabase Adapter diretamente). Opera sobre o schema
`MemoryItem` do FORGE-MVP-05. `typecheck` limpo. Não escrevi testes de
unidade para essas duas funções — `api-client.ts` não tem cobertura de
testes para nenhuma das suas funções baseadas em fetch (padrão já existente
no repositório, não uma lacuna que introduzi). Não sei se
`guardian.persist_memory`/`guardian.retrieve_memory` já existem no Gateway
real — mesma situação de `searchGuardianMemoryIndex` quando foi adicionado:
cliente pronto, se a capability não existir o Gateway responde
CAPABILITY_NOT_FOUND e a UI mostra o erro real (não trava), comportamento
já estabelecido neste código para exatamente esse caso.

Correção no mesmo passo seguinte (não separei em commit próprio porque só
percebi ao rodar a suíte completa antes do commit de FORGE-MVP-02, abaixo):
o comentário do Storage Contract nomeava o banco por trás do adapter
literalmente, o que quebra o `test:constitution` deste repo
(`DATABASE_TOKENS` bloqueia o nome do banco em qualquer lugar do código,
inclusive comentário). Reescrevi sem nomear o banco — o commit `322bba0`
já empurrado ficou com essa regressão até este passo; corrigido, não
amendado (commit novo).

## 2026-07-17 — FORGE-MVP-02: seletor de agente + metadado de atribuição

Eu fiz: em `luna-frontend`, branch `claude/forge-mvp-01-08`, commit
`f358752` (empurrado) — criei `lib/forge/attribution.ts`
(`ForgeAgent`/`MessageAttribution`, agentes gpt/claude/groq), adicionei o
seletor de agente e a atribuição por mensagem em `components/forge/chat.tsx`
(um agente ativo por vez, cada mensagem carrega agent/model/timestamp/
projectId), e estendi `sendChatMessage` em `api-client.ts` para enviar
agent/model de forma aditiva (não muda o contrato existente, não força
roteamento — quem decide o provider continua sendo o backend). `projectId`
usa um default fixo ("LUNA") até o FORGE-MVP-03 existir — comentado no
código como pendência explícita, não fabricado como se já funcionasse.
Também incluído neste commit: a correção do `test:constitution` descrita
acima. `typecheck`/`test` (20/20)/`test:constitution`/`build` todos limpos
antes do commit — rodei a suíte completa desta vez, não só typecheck.

## 2026-07-17 — FORGE-MVP-06: botões GitHub (commit/push/pull/branch)

Eu fiz: em `luna-frontend`, branch `claude/forge-mvp-01-08`, commit
`1df218d` (empurrado) — adicionei `commitAllLocalChanges`/
`pushCurrentBranch`/`pullCurrentBranch`/`createLocalBranch` a
`lib/forge/git.ts` (git real no checkout local do servidor, mesma
credencial de serviço de sempre, documentado explicitamente como
independente do agente ativo no Chat), 4 rotas novas em `app/api/forge/
git-{commit,push,pull,branch}`, clientes em `api-client.ts`, e os botões
correspondentes em `git-panel.tsx` com feedback inline.

Nota de processo: testei manualmente rodando o servidor dev contra este
próprio checkout antes do commit — o botão de commit funcionou e criou um
commit real e não intencional (`438873b`, "test commit") em cima do
trabalho ainda não commitado deste mesmo pacote, na minha branch local.
Não pusheado ainda quando percebi; desfiz com `git reset --soft HEAD~1`
(seguro porque era só local) e recomecei o teste isolado. Repeti a
verificação em um repositório+remoto descartáveis em `/tmp` (não neste
checkout): no-op commit, commit real, push de branch existente, criação de
branch, push de branch nova, pull, e rejeição de nome de branch inválido —
os 6 cenários corretos. `typecheck`/`test` (20/20)/`test:constitution`/
`build` limpos antes do commit real.

## 2026-07-17 — FORGE-MVP-03: seletor de projeto

Eu fiz: em `luna-frontend`, branch `claude/forge-mvp-01-08`, commit
`d7fddb5` (empurrado) — criei `lib/forge/project-context.tsx`
(`ProjectProvider`/`useForgeProject`, projeto ativo compartilhado por todos
os painéis), adicionei o seletor no header de `forge-layout.tsx`, e troquei
o `DEFAULT_PROJECT_ID` fixo do `chat.tsx` (deixado como pendência explícita
no FORGE-MVP-02) pelo projeto de fato selecionado. Escopo v0.1: um projeto
ativo por vez, alimentando o modelo de atribuição/memória — não inventei
mapeamento de owner/repo do GitHub por projeto (não tenho evidência de
quais são os repositórios reais de RENASCER/SMX/CURSO EMPILHADEIRA), então
o painel Git continua com campos editáveis manualmente, sem fabricar essa
ligação. `typecheck`/`test` (20/20)/`test:constitution`/`build` limpos
antes do commit.

## 2026-07-17 — FORGE-MVP-07: Reporter manual

Eu fiz: em `luna-frontend`, branch `claude/forge-mvp-01-08`, commit
`03dddc4` (empurrado) — adicionei `analyzeProject(project)` a
`api-client.ts` (capability `reporter.analyze_project` via Gateway) e o
botão "Analisar Projeto" em `context-panel.tsx`, numa seção Reporter nova
que mostra pendências/concluído/roadmap/drift. Só roda quando clicado
(nunca automático — Reporter automático segue congelado por ARCH-001).
Escopo estritamente evidência/exibição: não existe nenhum caminho de
escrita de volta ao Roadmap a partir daqui — mesmo escopo de ENG-007. Não
sei se `reporter.analyze_project` já existe no Gateway real; mesma postura
de `searchGuardianMemoryIndex`/Storage Contract — cliente pronto, erro real
se a capability não existir. `typecheck`/`test` (20/20)/`test:constitution`/
`build` limpos antes do commit.

Com isto, 7 dos 8 itens do FORGE-MVP (01, 05, 04, 02, 06, 03, 07) estão
implementados em `luna-frontend`, branch `claude/forge-mvp-01-08` — falta
só o FORGE-MVP-08 (painel de integração com Claude Code, conforme decisão
de manter Monaco/xterm intactos).

## 2026-07-17 — FORGE-MVP-08: painel Claude Code

Eu fiz: em `luna-frontend`, branch `claude/forge-mvp-01-08`, commit
`04d84fe` (empurrado) — criei `components/forge/claude-code-panel.tsx` e
`readGithubFile` em `api-client.ts` (`github.read_file`, capability madura
e já testada no backend real — confirmei lendo
`apps/frontend/artifacts/api-server/src/gateway/capabilities/github/
read-file.ts` e o teste correspondente no monorepo `luna`, diferente da
postura "não sei se existe" usada para guardian.*/reporter.* antes). O
painel lê `GENESIS/BUILDER.md` deste próprio repositório e mostra as 5
entradas de log mais recentes — parser verificado rodando contra o arquivo
real antes do commit (peguei corretamente FORGE-MVP-02 a 07). Virou uma
aba "Claude Code" ao lado de "Terminal" no mesmo slot do painel (Editor
Monaco e Terminal xterm inalterados, conforme a correção de premissa
registrada acima). `forceMount` na aba do Terminal — sem isso o Radix Tabs
desmontaria o Terminal ao trocar de aba, derrubando o WebSocket/shell
ativo.

Decisão de escopo importante: NÃO tentei rodar a CLI do Claude Code dentro
do terminal do Forge. `lib/forge/terminal-server.ts` documenta que esse
terminal não usa PTY real e programas interativos de tela cheia não
renderizam nele — a própria CLI do Claude Code se qualifica. Fabricar essa
integração pareceria funcionar e quebraria na prática; preferi uma
integração fina real (visibilidade de atividade do Builder via capability
confirmada) a uma capability fake. `typecheck`/`test` (20/20)/
`test:constitution`/`build` limpos antes do commit.

Com isto, os 8 itens do FORGE-MVP-01 a 08 (P00, GENESIS/ROADMAP.md) estão
implementados em `luna-frontend`, branch `claude/forge-mvp-01-08`. Branch
empurrada, sem PR aberta (não solicitado).

## 2026-07-17 — FORGE.md: nota de escopo do Workspace v0.1 + Backlog Operational Intelligence

Eu fiz: em `GENESIS/FORGE.md` (este repositório), sob "### Workspace
v0.1", adicionei a nota registrando que Editor (Monaco) e Terminal (xterm)
já existiam em `luna-frontend` antes desta implementação e não são
entrega do v0.1 — o que o v0.1 de fato endereça é só o nó "AI Coding"
(FORGE-MVP-08A, Claude Activity Panel, sem sessão embutida). Adicionei
também "## Backlog — Operational Intelligence" ao final do arquivo,
apontando para GENESIS/RESEARCH/meta-cognitive-memory.md sem duplicar
conteúdo. Conteúdo exatamente como entregue, nenhuma implementação de
código associada.

## 2026-07-17 — Correção: GENESIS/ROADMAP.md não tinha sido tocado

Achado do Reporter (verificação por evidência, SHA comparado antes/depois):
o passo anterior só editou `GENESIS/FORGE.md` — o pacote também pedia duas
edições em `GENESIS/ROADMAP.md`, seção P00, que eu não apliquei. Reportado
corretamente pelo Reporter antes de qualquer coisa; corrigido agora, não
só anotado.

Eu fiz: em `GENESIS/ROADMAP.md`, seção P00 — troquei `FORGE-MVP-01 —
Interface web funcional` (`[ ]`) por `FORGE-MVP-01 — Validated Existing
Capability (auditado, não implementado — ver GENESIS/BUILDER.md)` (`[x]`,
texto e checkbox exatamente como o Reporter especificou); e troquei
`FORGE-MVP-08 — Workspace v0.1: integração com Claude Code (não
reimplementação de IDE)` por `FORGE-MVP-08A — Claude Activity Panel (nó
"AI Coding" do Workspace, integração honesta sem PTY — ver GENESIS/FORGE.md)`,
mantendo `[ ]` (implementação existe em código, mas o Reporter não marcou
como concluído neste pacote — não presumi). Não toquei nos itens
FORGE-MVP-02 a 07: continuam `[ ]` apesar de implementados em
`luna-frontend` (branch `claude/forge-mvp-01-08`), porque marcar conclusão
é escopo do Reporter por evidência, não meu — não estendi a correção além
do que foi pedido.

## ID: BLD-003
Data: 2026-07-18
Tópico: Destravar pendências P1 do Roadmap — verificação de estado real + fechamento formal

Eu fiz: recebi instrução para executar os 4 passos do P1 (fechar PRs
obsoletas do luna-core, aplicar model.chat/model.chat_deep, corrigir
classificação de sistemas, atualizar ROADMAP/BUILDER). Antes de executar
qualquer coisa, auditei o estado real via GitHub API e git clone (não
assumi que os itens `[ ]` do Roadmap ainda estavam pendentes) — descobri
que os 3 primeiros passos já tinham sido concluídos fora desta sessão:

1. `luna-core` PR #10 ("Gateway: model.chat/model.chat_deep") já estava
   mergeada em `main` desde 2026-07-15 (commit `069c219`) — confirmei lendo
   o código real em `src/gateway/capabilities/model/{chat,chat-deep}.ts` e
   `src/app.ts` (`tryCreateModelRouter`, try/catch isolado, mesmo padrão de
   `GITHUB_TOKEN`). Confirmei também, pela ausência de qualquer diretório
   `capabilities/storage/*` no código, que `storage.query`/
   `storage.insert` NÃO foram aplicadas — exatamente o que a instrução
   pedia para não fazer.
2. As PRs #3, #4 e #5 do `luna-core` já estavam fechadas por Rubens
   diretamente (usuário `raugustorubens-design`, `author_association:
   OWNER`) em 2026-07-14, com o comentário "arquivo obsoleto"/"Arquivo
   obsoleto" em cada uma.
3. A tabela de classificação de sistemas em `LUNA_CONTEXT.md` já tinha sido
   corrigida em 2026-07-12 (nota "Reclassificação — 2026-07-12 (ADR-004
   executed)", linha 97): `luna-core` já aparece como "Infraestrutura,
   Órgão" na tabela atual (linha 70), não mais em "Legado/Experimental"
   (linha 94). `ECOSYSTEM_ARCHITECTURE.md` preserva a linha antiga como
   snapshot histórico explicitamente anotado (linha 28), não uma
   classificação vigente — não precisa de correção adicional.

O que eu de fato executei nesta sessão: (a) adicionei um comentário de
rastreabilidade referenciando ADR-004 em cada uma das PRs #3/#4/#5 do
`luna-core` (a instrução pedia esse comentário antes do fechamento; como
já estavam fechadas, registrei o motivo formal a posteriori em vez de
pular a etapa) — isso também serviu de teste real da permissão de escrita
do GitHub App: os 3 comentários foram aceitos sem 403, confirmando que a
pendência de permissão (INFRA-001) está resolvida; (b) registrei ENG-011
em GENESIS/ENGINEER.md (storage.query/storage.insert seguem bloqueadas,
ver STOR-001); (c) atualizei os 5 itens correspondentes de P1 (e o
INFRA-001 de P0) em GENESIS/ROADMAP.md para `[x]`, com nota de correção
apontando a evidência (PR #10, comentários de fechamento, nota de
reclassificação), seguindo o mesmo padrão já usado no primeiro item do
P1.

O que está bloqueado: configurar GROQ_API_KEY/DEEPSEEK_API_KEY/
OPENROUTER_API_KEY/ANTHROPIC_API_KEY no Railway (`luna-core`/honest-joy)
continua fora do meu alcance nesta sessão — não tenho acesso ao Railway.
Sem essas credenciais, `model.chat`/`model.chat_deep` seguem ausentes de
`/api/gateway/capabilities` em produção (comportamento pretendido, não
bug). Não implementei `storage.query`/`storage.insert` nem uma versão
provisória delas — permanecem bloqueadas por decisão de Architect
pendente (STOR-001), como a instrução determinou explicitamente.

Test status: nenhuma mudança de código nesta sessão (apenas documentação
GENESIS + comentários em PRs já fechadas); não há suíte para rodar.

Next action: Architect decidir o redesenho de storage.query/storage.insert
(STOR-001); Rubens configurar as credenciais de IA no Railway quando
oportuno.

## 2026-07-18 — Pacote 1/9: LUNA_CONSTITUTION.md (Artigo AAAB — Atrator Cognitivo)

Eu fiz: substituí `LUNA_CONSTITUTION.md` inteiro pelo conteúdo entregue —
mesmo Artigo 1/AAAA e lista de Princípios 1-8 preservados sem nenhuma
alteração, adicionado o novo Artigo AAAB (Princípio do Atrator Cognitivo,
Art. AAAB.1 a AAAB.8) exatamente como recebido. Conferi antes de escrever
que o conteúdo pré-existente do arquivo batia byte a byte com a parte
"antes do AAAB" do texto entregue — não houve perda de conteúdo na
substituição. Nenhuma implementação de código associada.

Nota de processo (decisão do fundador, 2026-07-18): a partir deste pacote,
ENG-006/ENG-008 deixam de ser regra rígida e passam a ser boa prática
ajustável — cada arquivo deste pacote entra em commit separado com a
entrada correspondente em BUILDER.md, por ser a opção padrão/preferida,
não porque é obrigatório. Registrado também em ENGINEER.md (ver ENG-012).

## 2026-07-18 — Pacote 2/9: CHECKPOINTS/GENESIS-ATTRACTOR-001.md

Eu fiz: criei o diretório `CHECKPOINTS/` (referenciado em `INDEX.md` §
Diretórios desde antes, mas nunca criado fisicamente) e o arquivo
`CHECKPOINTS/GENESIS-ATTRACTOR-001.md`, conteúdo exatamente como entregue.
Nenhuma implementação de código associada.

## 2026-07-18 — Pacote 3/9: ADR-008 (GitHub como Genoma — delegação via Actions/Forge)

Eu fiz: criei `ADR/ADR-008-GitHub-Genoma-Delegacao-Automatica-Forge.md`,
conteúdo exatamente como entregue. Este ADR resolve a pendência de decisão
do Roadmap P2 "Escolher caminho de delegação API+GitHub" — vou marcar esse
item no Roadmap num pacote posterior deste mesmo pedido (pacote 9/9),
junto com o novo item GEN-002. Nenhuma implementação de código associada
(o `.yml` do workflow e o botão no Forge ficam fora do escopo deste ADR,
conforme o próprio texto).

## 2026-07-18 — Pacote 4/9: ADR-009 (emenda constitucional do Atrator AAAB)

Eu fiz: criei `ADR/ADR-009-Emenda-Constitucional-Atrator-AAAB.md`, conteúdo
como entregue, com um ajuste de texto: a frase "ver Arquivo 1 deste pacote"
não fazia sentido como referência permanente no repositório (era uma
referência ao pacote de instrução, não a um artefato do repo) — troquei
por referência direta a `LUNA_CONSTITUTION.md`, sem mudar o conteúdo
decisório do ADR. Nenhuma implementação de código associada.

## 2026-07-18 — Pacote 5/9: ADR-005 (Reporter via GitHub Actions + metacognição) — ATENÇÃO: redraft, não original

Eu fiz: criei `ADR/ADR-005-Reporter-GitHub-Actions-Metacognicao.md`,
conteúdo exatamente como entregue no pacote desta instrução.

Aviso explícito, repetindo o que a própria instrução sinalizou: o texto
original desta ADR foi redigido numa sessão de chat anterior e "entregue"
ao Claude Code, mas não está recuperável verbatim nesta sessão — só um
resumo chegou até aqui. O que criei é um **redraft a partir desse resumo**,
não uma cópia fiel do original. Marquei isso no próprio corpo do arquivo
("Status: Aceito (redigido em sessão anterior; redraft aplicado em
2026-07-18...)"). Se o Architect tiver o texto original salvo em outro
lugar (ex. ChatGPT), esse original deve prevalecer sobre este redraft — não
tratei este arquivo como fonte definitiva do conteúdo histórico da decisão,
só como registro de que a decisão existe e foi aplicada. Nenhuma
implementação de código associada.

## 2026-07-18 — Pacote 6/9: ADR-006 (Hierarquia biológica — "Sistema Funcional") — redraft, não original

Eu fiz: criei `ADR/ADR-006-Hierarquia-Biologica-Sistema-Funcional.md`,
conteúdo exatamente como entregue. Mesmo aviso do pacote anterior (5/9):
redraft a partir de resumo, não cópia do texto original da sessão que
gerou esta decisão — se o texto original existir salvo em outro lugar,
deve prevalecer sobre este arquivo. Nenhuma implementação de código
associada.

## 2026-07-18 — Pacote 7/9: ADR-007 (Reporter memória persistente + evidência antes de intervenção) — redraft, não original

Eu fiz: criei `ADR/ADR-007-Reporter-Memoria-Persistente-Evidencia.md`,
conteúdo exatamente como entregue. Mesmo aviso dos pacotes 5/9 e 6/9:
redraft a partir de resumo, não cópia do texto original — se o original
existir salvo em outro lugar, deve prevalecer sobre este arquivo. Nenhuma
implementação de código associada.

Nota de consistência: o princípio "Reporter confirma, não cria" descrito
nesta ADR-007 já era regra ativa em ENGINEER.md (ver ENG-007, registrada
em 2026-07-16) — os dois documentos são consistentes entre si, não
conflitam nem duplicam a mesma decisão como se fossem independentes.

## 2026-07-18 — Pacote 8/9: INDEX.md (tabela "Conteúdo atual")

Eu fiz: adicionei ao `INDEX.md` as 7 linhas novas na tabela "Conteúdo
atual" (Atrator AAAB, Checkpoint GENESIS-ATTRACTOR-001, ADR-005 a ADR-009),
conforme entregue. Não toquei na seção "Diretórios": `CHECKPOINTS/` já
estava listada lá desde antes deste pacote (só o diretório físico é que
não existia até o pacote 2/9) — não havia nada a adicionar ali, apesar da
instrução ter pedido essa adição; conferi antes de editar para não
duplicar uma linha que já existia. Nenhuma implementação de código
associada.

## 2026-07-18 — Pacote 9/9: GENESIS/ROADMAP.md (GEN-002 + fechamento do item de delegação em P2)

Eu fiz: em `GENESIS/ROADMAP.md` — marquei `[x]` o item de P2 "Escolher
caminho de delegação API+GitHub", com nota apontando para ADR-008; e
adicionei `GEN-002 — Workflow de aplicação automática de ADRs via GitHub
Actions, acionável pelo Forge (ver ADR-008)` em P1, não em P2. Segui a
alternativa que a própria instrução sugeriu ("ou mover pra P1 já que a
decisão foi tomada"): como ADR-008 já decidiu o caminho, o que resta de
GEN-002 é implementação sem decisão de Architect pendente — a definição
de P1 no próprio Roadmap. Não implementei o workflow `.yml` em si nem o
botão no Forge — isso é o próprio GEN-002 em aberto, trabalho de Builder
futuro, não desta sessão de documentação.

Com isto, os 9 arquivos daquele pacote (LUNA_CONSTITUTION.md,
CHECKPOINTS/GENESIS-ATTRACTOR-001.md, ADR-008, ADR-009, ADR-005, ADR-006,
ADR-007, INDEX.md, GENESIS/ROADMAP.md) foram aplicados, cada um em commit
separado com autoatestação correspondente, conforme a preferência
registrada em ENG-012. Nenhuma implementação de código associada em
nenhum dos 9 pacotes — aquele pedido era inteiramente de documentação
GENESIS/ADR/Constituição.

## 2026-07-18 — Pacote 1/6: ADR-010 (arquitetura canônica de memória — DECISÃO ARQ-001)

Eu fiz: criei `ADR/ADR-010-Arquitetura-Canonica-Memoria-MEM-001-STOR-001.md`,
conteúdo como entregue (ajustei só 2 frases internas de "ver Arquivo N
abaixo" para prosa sem numeração de pacote, mesmo motivo do ajuste feito em
ADR-009 no pacote anterior — não é uma referência válida fora do contexto
da instrução). Este ADR resolve a especificação de `MEM-001`/`STOR-001`
(P0), mas não desbloqueia a implementação: ambos seguem congelados por
ARCH-001 até o Forge v0.1 estar em uso diário — decisão de especificação
e liberação de implementação são coisas diferentes, e só a primeira está
resolvida aqui. Nenhuma implementação de código associada — este ADR é
puramente de especificação/documentação. Nota sobre o 403 mencionado no
pacote de instrução: refere-se à sessão de chat que redigiu o pacote, não
a esta sessão do Claude Code — aqui a escrita direta (git push) continua
funcionando normalmente, como já confirmado no pacote anterior.

## 2026-07-18 — Pacote 2/6: context.txt (correções ADR-010 §3/§4/§5/§7)

Eu fiz: apliquei as 5 edições pontuais em `context.txt` exatamente como
especificado — `BASE` corrigido (remove referência a `memory_core_v2`
inexistente), símbolo `A`→`ρ` na Memory Update com nota explicando a
separação Action/Recurrence, `τ`→`τ_a` no Alignment, `THRESHOLD τ_c`
adicionado na Compression, e a nova seção `🗂️ MEMORY OBJECT` inserida
antes de `🔄 CONTINUITY`. Conferi o arquivo inteiro após as edições, não
só os trechos alterados.

Achado não corrigido, sinalizado em vez de resolvido por conta própria
(Regra 6, Builder persiste/não especifica): a nota nova inserida na seção
Memory Update ("Action lives in Decision(t) = H(t) + A(t), in the
Cognitive Model section above") descreve a seção `🧠 COGNITIVE MODEL`
como se ela já definisse `Decision(t) = H(t) + A(t)` — mas o texto real
dessa seção (linha 29, não alterada por esta instrução) diz
`Decision(t) = H(t) + M(t)`, nunca menciona `A(t)`. O pacote de instrução
e o `ADR-010` (§9, mesma frase) partem do mesmo pressuposto não conferido
contra o arquivo real. Apliquei a nota exatamente como entregue (não
inventei correção da seção Cognitive Model, que não estava no escopo das
5 edições pedidas) — registrando aqui para o Engineer/Architect decidir
se `Decision(t) = H(t) + M(t)` deveria virar `H(t) + A(t)` num pacote
futuro, ou se a nota é que deveria ser reescrita para não pressupor isso.

## 2026-07-18 — Pacote 3/6: memory_core.alg (marcado como histórico)

Eu fiz: troquei as 2 linhas do bloco `## 📌 STATUS` de `memory_core.alg`
exatamente como especificado — `State` passa de "ACTIVE (OFFICIAL)" para
"HISTÓRICO — superado por ADR-010", e `Replaces` ganha a nota de que este
documento é quem foi substituído, não o contrário. Resto do arquivo
(as 237 linhas restantes) inalterado, conforme instruído — preservação
histórica, Princípio 8 da Constituição.

Nota de processo: ao revisar o histórico deste próprio arquivo (BUILDER.md)
antes deste commit, percebi que o parágrafo de fechamento do pacote
anterior ("Com isto, os 9 arquivos...") tinha ficado deslocado — apareceu
depois das entradas deste pacote novo (1/6, 2/6) em vez de logo após
"Pacote 9/9", por causa de como o texto foi inserido por match de string.
Corrigi a posição sem alterar o conteúdo do parágrafo, antes deste commit
— achado próprio, corrigido de imediato, não deixado para trás.

## 2026-07-18 — Pacote 4/6: ECOSYSTEM_ARCHITECTURE.md (linha Hipocampo — Missing Reference)

Eu fiz: troquei a coluna de qualidade da linha "Hipocampo" na tabela
"Órgãos internos do monorepo `luna`" exatamente como especificado,
marcando a referência a ADR-003 como Missing Reference e apontando
ADR-010 como fonte de verdade vigente para a fórmula.

Achado não corrigido, fora do escopo desta instrução (que pediu "uma
linha", singular): a linha da tabela "Filtro Cognitivo" (linha 44 antes
desta edição) também cita "decisão ADR-003" sem nenhuma marcação de
Missing Reference. Não toquei nela — a instrução escopou só a linha do
Hipocampo; sinalizando aqui para inclusão num pacote futuro, se desejado.

## 2026-07-18 — Pacote 5/6: LUNA_CONSTITUTION.md (Axioma IV consolidado + Princípio 9)

Eu fiz: apliquei as 2 edições pontuais exatamente como especificado — o
Axioma IV do Art. AAAB.4 deixa de dizer "(hipótese de pesquisa)" e passa a
dizer "(promovido a conhecimento consolidado por ADR-010...)"; e a lista
de Princípios ganha o item 9 (hierarquia de decisão Atrator → Constituição
→ ADR → Arquitetura → Engenharia → Implementação). Não toquei no Axioma V
("Identidade é independente da memória") — continua marcado como hipótese
de pesquisa, porque só o Axioma IV foi promovido por este ADR (conferi o
texto do ADR-010 antes de editar: só cita o Axioma IV, nunca o V).

## 2026-07-18 — Pacote 6/6: GENESIS/ROADMAP.md (MEM-001/STOR-001 — especificação resolvida por ADR-010)

Eu fiz: troquei as 2 linhas de P0 (MEM-001, STOR-001) exatamente como
especificado, deixando explícito que a especificação foi decidida via
ADR-010, mas a implementação segue bloqueada por ARCH-001 — as duas coisas
não se confundem. Também atualizei ENG-011 em GENESIS/ENGINEER.md com uma
nota curta (não reescrevi a entrada original) marcando que o "ainda não
especificado" registrado ali em 2026-07-18 (antes deste mesmo pacote,
poucas horas atrás) deixou de ser verdade com ADR-010 — mantive o registro
histórico da entrada original intacto, só adicionei a atualização.

Com isto, os 6 arquivos deste pacote (ADR-010, context.txt, memory_core.alg,
ECOSYSTEM_ARCHITECTURE.md, LUNA_CONSTITUTION.md, GENESIS/ROADMAP.md) foram
aplicados, cada um em commit separado com autoatestação correspondente,
conforme ENG-012. Achados sinalizados e não corrigidos por conta própria
(Regra 6): a divergência `Decision(t) = H(t) + M(t)` vs. `H(t) + A(t)` em
`context.txt` (ver ENG-013); e a linha "Filtro Cognitivo" em
`ECOSYSTEM_ARCHITECTURE.md` que ainda cita ADR-003 sem marcação de Missing
Reference (fora do escopo desta instrução, que pediu só a linha do
Hipocampo). Nenhuma implementação de código associada em nenhum dos 6
pacotes — este pedido também era inteiramente de documentação
GENESIS/ADR/Constituição/contexto cognitivo.

## 2026-07-19 — Correção: remove fórmula inventada de Decision Engine (context.txt + ADR-010 §8)

Eu fiz: removi a NOTE de `context.txt` § Memory Update que afirmava
`Decision(t) = H(t) + A(t)` — essa fórmula não existe em nenhuma fonte
(nem em `context.txt`, nem em `memory_core.alg`); foi introduzida por mim
ao formalizar o ADR-010, sem verificar contra o arquivo real antes de
escrever. É exatamente o mesmo tipo de erro que eu mesmo já tinha
sinalizado como achado de ENG-013 no pacote anterior — só que dessa vez a
causa raiz era a minha própria composição do ADR, não um pressuposto do
pacote de instrução. Também ajustei a linha "ρ = recurrence (... see
below)" em `context.txt`, que ficaria com referência solta ("below") após
a remoção da NOTE — trocada por referência direta a ADR-010 §3.

Reescrevi o parágrafo correspondente em ADR-010 §8: mantive o princípio
"Action pertence ao Decision Engine, fora do escopo deste ADR" (que é
decisão real do Architect, item 3), removi a equação fabricada, e deixei
registrado explicitamente que a correção existe e por quê — não apaguei
silenciosamente o erro anterior. Não toquei em ADR-010 §9 (Hierarquia de
decisão): não continha a fórmula fabricada, só o item §8 continha.

O que está bloqueado: as duas colisões de símbolo que este erro revelou
(`M(t)` = machine state vs. long-term memory; `A` já reservado para
Alignment antes da decisão "A = Action" do item 3) ainda não têm decisão
do Architect — não escolhi um dos dois lados sozinho, é decisão de
especificação, não implementação (Regra 6). Vou perguntar ao Architect
diretamente antes de aplicar qualquer ADR-011.

## 2026-07-19 — ADR-011: emenda de símbolos (M/X, A/γ) — inclui achado de 3ª colisão

Eu fiz: antes de aplicar a resolução que o Architect confirmou (M(t) =
memória, machine state = X(t); A(t) = Alignment, Action = γ(t)), rodei
`grep -n "M(t)"` no `context.txt` inteiro para checar o escopo real da
troca, em vez de aplicar só nas 2 linhas originalmente citadas na
discussão. Encontrei uma 3ª ocorrência não vista antes: a seção Alignment
(`A(t) = 1 − d(H(t), M(t))`, linha 105 antes da edição) também usa `M(t)`
como machine state, não memória — reportei isso ao Architect antes de
tocar em qualquer arquivo, e a leitura foi confirmada (Alignment mede
distância entre intenção humana e estado da máquina, não memória
acumulada; um gate de execução em tempo real não faria sentido comparando
com histórico). Escopo final confirmado: 3 ocorrências de `M(t)`-como-
machine-state (linhas 27, 29, 105) viram `X(t)`; 2 ocorrências de
`M(t)`-como-memória (linhas 40, 90) continuam `M(t)`, sem mudança.

Criei `ADR/ADR-011-Emenda-Simbolos-M-X-A-Gamma.md`, registrando a decisão
completa (incluindo a 3ª colisão encontrada) e a tabela de símbolos
consolidada. Adicionei uma nota de emenda em `ADR-010` §3 apontando para
ADR-011 — não editei o texto original da decisão de 2026-07-18
silenciosamente (Princípio 8), só anexei a nota de que foi superada.
Também atualizei o parágrafo de correção que eu mesmo tinha adicionado em
ADR-010 §8 no dia anterior (que dizia "pendente de resolução") para
apontar a resolução real via ADR-011, já que deixar de atualizar essa
frase depois de resolvida a deixaria desatualizada no mesmo estilo do
achado que o Reporter já tinha me pego antes (ver "Correção:
GENESIS/ROADMAP.md não tinha sido tocado", 2026-07-17).

## 2026-07-19 — Aplica ADR-011 em context.txt (X(t), γ(t))

Eu fiz: apliquei em `context.txt` as 3 trocas de `M(t)`→`X(t)` confirmadas
(linhas 27, 29, 105) e atualizei o comentário sobre Action na seção Memory
Update para citar `γ(t)` como o símbolo real, em vez de só "Action" em
prosa (linha 96). Conferi com `grep -n "M(t)\|X(t)\|A(t)\|γ"` no arquivo
inteiro depois da edição: as 2 ocorrências de `M(t)`-memória (linhas 40,
90) continuam intactas; nenhuma outra ocorrência de `M(t)`-como-machine-
state sobrou. Não toquei em mais nenhuma seção do arquivo.

## 2026-07-19 — INDEX.md: registra ADR-010 e ADR-011 (iniciativa própria)

Eu fiz: adicionei ADR-010 e ADR-011 à tabela "Conteúdo atual" de
`INDEX.md`. Isto não foi pedido nos pacotes que criaram esses dois ADRs —
percebi ao consultar o índice que ele ficou incompleto desde então (os
pacotes de ADR-010/011 não incluíram a instrução de atualizar o INDEX,
diferente dos pacotes anteriores de ADR-005 a 009, que sempre incluíam).
Tomei a iniciativa de corrigir porque é bookkeeping mecânico e sem
ambiguidade (só registrar arquivos que já existem e já foram decididos),
não uma decisão nova — dentro do que Regra 6 permite ao Builder. Marquei
ADR-010 como "emendado por ADR-011", mesmo padrão já usado para ADR-002
("emendado por DA-001") na mesma tabela.

## 2026-07-19 — FORGE-MVP-02 a 08A: verificação de estado real em luna-frontend, sem código novo

Eu fiz: recebi instrução para, em `luna-frontend`, "abrir PR de
`claude/forge-mvp-01-08` para `main` (ou fazer merge direto, se
autorizado)" e "implementar FORGE-MVP-08A". Antes de agir, adicionei o
repositório a esta sessão e auditei o estado real via GitHub API + git,
em vez de assumir a premissa da instrução:

1. `luna-frontend` PR #7 ("Forge MVP-02–08: chat attribution, git panel,
   Claude Code panel, storage contract") já estava aberta, revisada e
   **mergeada em `main`** desde 2026-07-17T16:11:50Z, por
   `raugustorubens-design` diretamente — confirmei via
   `pull_request_read get` (`merged: true`; a listagem geral mostrava
   `merged: false`, mesma inconsistência da API já vista antes no
   `luna-core` PR #10) e via `git log` local (`main` tem
   "Merge pull request #7..." como HEAD). Não havia PR para abrir nem
   merge para fazer — os dois já aconteceram, sem relação com esta sessão.
2. FORGE-MVP-08A ("Claude Activity Panel... via `github.read_file`, sem
   PTY", especificado em `GENESIS/FORGE.md`) já está satisfeito pelo
   mesmo commit `04d84fe` da mesma PR #7 — não é uma implementação
   diferente que "substituiu conceitualmente" a versão antiga como a
   instrução assumia. Li o código real de
   `components/forge/claude-code-panel.tsx` em `main`: lê
   `GENESIS/BUILDER.md` via `readGithubFile`/`github.read_file`, mostra as
   5 entradas mais recentes, não embute sessão/PTY — bate ponto a ponto
   com a especificação de FORGE-MVP-08A. Confirmei também que não é um
   componente órfão: `grep` em `forge-layout.tsx` mostra `ClaudeCodePanel`
   importado e renderizado como aba real. Não escrevi nenhum código novo
   — implementar de novo seria violar Princípio 3 da Constitution
   ("Reutilizar antes de implementar") e recriar algo que já existe.

Rodei a suíte completa em `main` antes de atualizar o Roadmap, para ter
evidência fresca (não só confiar na descrição da PR de 2 dias atrás):
`pnpm install`, `typecheck` limpo, `test` 20/20, `test:constitution` (42
arquivos, sem violação), `build` sucesso (mesmos 2 warnings pré-existentes
de Edge Runtime em `jose`/`next-auth`, já documentados na PR original).

Em `GENESIS/ROADMAP.md`: marquei FORGE-MVP-02 a 08A como `[x]` (P00), cada
um com o commit específico dentro da PR #7 como evidência — os 7 itens que
antes ficavam `[ ]` só porque "marcar conclusão é escopo do Reporter", não
porque faltava código (ver pacote "Correção: GENESIS/ROADMAP.md não tinha
sido tocado", 2026-07-17, que já tinha sinalizado isso). Desta vez marco
diretamente porque a instrução mais recente pediu explicitamente o ajuste
de P00 como parte da execução — mesma autorização explícita já usada no
BLD-003 para o P1. Também apliquei a correção solta pedida (`P5`:
`Atrator AAAB — Sustentabilidade` vira `Atrator AAAC — Sustentabilidade`,
já que AAAB é o Atrator Cognitivo desde ADR-009) — conferi com `grep -rn
"AAAB"` no repositório inteiro que não sobrou nenhuma outra referência a
AAAB-como-Sustentabilidade em outro documento.

O que está bloqueado: env vars do Railway (login Google,
`FORGE_ALLOWED_EMAIL`, tokens) — infraestrutura, fora do alcance desta
sessão, só o Rubens configura. Uso diário de fato do Forge também depende
disso e de decisão humana, não de código — é o próprio gate que o
Architect definiu para descongelar ARCH-001/P0.

Test status: `luna-frontend`/`main` — `typecheck` limpo, `test` 20/20,
`test:constitution` 42 arquivos sem violação, `build` sucesso (2026-07-19).
Nenhuma mudança de código neste pacote — FORGE-MVP-08A já estava completo;
o trabalho real foi verificação + atualização de `GENESIS/ROADMAP.md`.

Next action: Rubens configurar env vars no Railway e usar o Forge no
dia a dia; ao confirmar rotina de uso real, formaliza descongelamento de
ARCH-001/P0 e libera MEM-001/STOR-001 (especificação já fechada via
ADR-010/011) para o Builder implementar.

## 2026-07-19 — GENESIS/ARCHITECTURE_INVENTORY.md: auditoria Railway + inventário canônico consolidados

Eu fiz: recebi dois pedidos em sequência — uma auditoria Railway × GitHub
("não assuma nada, evidência ou 'Sem evidência suficiente'") e, antes de
eu terminar de aplicá-la como artefato HTML, um segundo pedido pedindo um
inventário arquitetural canônico mais amplo, versionado no GitHub, e
explicitamente instruindo a continuar o trabalho já iniciado em vez de
recomeçar. Recebi então a instrução de terminar os dois juntos
reaproveitando o que eu já tinha levantado — não descartei a pesquisa já
feita (clone dos 7 repositórios, leitura de `railway.json`/`Procfile`/
`Dockerfile`/`package.json`/workflows de cada um), só mudei o formato de
entrega de HTML efêmero para um documento Markdown permanente em
`GENESIS/ARCHITECTURE_INVENTORY.md`, seguindo a própria instrução de
preferir um diretório já existente a criar `docs/` novo.

Confirmei antes de escrever, sem acesso ao Railway/Vercel/Supabase nesta
sessão (sem CLI, sem token, sem conector MCP) — todo o documento distingue
explicitamente evidência documental (arquivos versionados) de atividade
real confirmada no GitHub (ex.: PRs do `vercel[bot]`) de "Não confirmado".

Achado novo mais relevante desta rodada, que não estava em nenhum
documento anterior: `apps/frontend/artifacts/api-server/src/routes/
{chat,context}.ts`, dentro do monorepo `luna`, já implementa o contrato
exato que `luna-frontend` espera de chat/contexto (`runCognitiveEngine`,
`buildOrganismContext`, schemas `@workspace/api-zod`, montado em `/api`) —
nunca portado para `luna-core` junto com o Gateway (ADR-004 portou só o
Gateway/Connector Hub). A lacuna registrada há tempo em `LUNA_CONTEXT.md`
("`luna-guardian` tem contrato de `/chat` incompatível e não implementa
`/context`") não é falta de implementação — é falta de porte. Registrei
isso como ENG-014 em `GENESIS/ENGINEER.md`, sinalizado para decisão do
Architect (não decidi nem executei o porte sozinho — Regra 6). Também
confirmei, por atividade real de bot (PRs do `vercel[bot]`, não só
documentação), que `luna-frontend` está em produção simultaneamente no
Vercel e (por documentação) no Railway — duplicação de ambiente que
nenhum documento anterior tinha registrado.

O documento cobre as 10 seções pedidas (Visão Geral, Repositórios,
Responsabilidades, Dependências, Conexões Externas, Ambientes, Railway,
Problemas, Recomendações, Roadmap) mais a matriz e as 5 respostas
objetivas (A-E) da auditoria Railway original — nada foi descartado dos
dois pedidos, os dois terminam neste único documento. Também registrei em
`INDEX.md` (marcado como "documento vivo — atualizar, não recriar",
conforme pedido).

O que está bloqueado: confirmação ao vivo de qualquer conexão Railway ou
Vercel (não tenho acesso); decisão do Architect sobre o porte do Cognitive
Engine/Convergia/chat-contexto (ENG-014); decisão do Architect sobre qual
ambiente de produção o `luna-frontend` deveria manter (Railway ou Vercel,
não os dois).

Test status: nenhuma mudança de código — este pacote é inteiramente de
auditoria/documentação.

Next action: Architect revisar `GENESIS/ARCHITECTURE_INVENTORY.md` e
decidir sobre ENG-014 (porte do Cognitive Engine/chat/context) e sobre a
duplicação Vercel/Railway do `luna-frontend`.

## 2026-07-19 — ADR-012: formalizado antes de qualquer código (mesma regra do ADR-010)

Eu fiz: recebi o rascunho do ADR-012 (Decisão 1: porte do Cognitive
Engine/Convergia/chat-context para `luna-core`; Decisão 2: interface de
Convergia em `luna-frontend`) com instrução explícita de auditar
`apps/frontend/artifacts/api-server` antes de mexer em qualquer coisa, e
de parar e reportar se encontrasse algo que não batesse com a descrição do
ADR, em vez de decidir sozinho.

Antes de escrever qualquer código ou o ADR final, li o código-fonte
completo a portar (Cognitive Engine, Convergia, rotas chat/context,
schemas, package.json, architecture-check.mjs do monorepo) e encontrei
duas divergências reais, que reportei ao Architect antes de prosseguir:

1. `chat.ts` persiste `conversations`/`messages` direto via Drizzle/
   Postgres (`@workspace/db`), sem passar pelo Guardian — a mesma classe de
   violação do Princípio 4 que eu já tinha recusado implementar no Gateway
   nesta sessão (BLD-003/ENG-011). Portar como está recriaria a violação
   dentro do backend oficial. Arquitect decidiu: portar tudo, roteando
   `conversations`/`messages` pelo contrato genérico do Guardian
   (save/get/delete/search), com uma extensão pontual de `count` para
   stats — não o redesenho completo de STOR-001.
2. `context-hub.ts`/`indice-cognitivo.ts` leem arquivos locais do monorepo
   (`luna_context/*.md`, `forge/ROADMAP.md`, `docs/architecture/adr-004-*.md`)
   que não existem em `luna-core` — portado como está, degradaria
   silenciosamente para contexto vazio. Architect decidiu: trocar para ler
   `Luna-context.md` via `GithubConnector.readFile`, mesmo padrão já maduro
   do FORGE-MVP-08A.

Formalizei `ADR/ADR-012-Consolidacao-Backend-luna-core-Interface-Convergia.md`
incorporando as duas decisões originais mais os dois refinamentos acima,
e uma nota de escopo sobre `@workspace/api-zod`/`@workspace/db` (o primeiro
é código gerado por orval, não portado verbatim — só as ~10 schemas Zod
realmente usadas por `chat.ts`, copiadas manualmente; o segundo não é
portado, substituído inteiramente pelo cliente HTTP do Guardian). Registrei
em `INDEX.md`.

O que está bloqueado: nada ainda — ADR aceito, prossigo para a
implementação (Cognitive Engine + Convergia + rotas, depois a interface em
`luna-frontend`).

Test status: nenhuma mudança de código neste commit — só o ADR.

Next action: portar Cognitive Engine + Convergia + rotas para `luna-core`,
seguido de typecheck/testes, depois descontinuar `/chat`/`/context` em
`luna-guardian`, depois a interface de Convergia em `luna-frontend`.

## 2026-07-19 — ADR-012 Decisão 1 executada: Cognitive Engine + Convergia portados para luna-core

Eu fiz: auditei `apps/frontend/artifacts/api-server` (monorepo `luna`) por
completo antes de escrever qualquer código, conforme instruído. Portei:

- `src/luna/*` (Cognitive Engine: cognitive-engine, memory-engine,
  hipocampo, context-hub, indice-cognitivo, provider-router, provider-engine,
  budget-manager, reporter, contracts, guardian-contract, adapters de
  provider) para `luna-core/src/luna/*`.
- `src/convergia/*` completo (parsers, renderers, templates, transform,
  validation, knowledge-gate, training, pipeline, contracts, errors) para
  `luna-core/src/convergia/*`, sem alteração de lógica.
- `src/routes/{chat,context,convergia,health}.ts` para
  `luna-core/src/routes/*`, montadas em `app.ts` como rotas irmãs do
  Gateway (nunca capabilities dele).

Dois pontos não bateram com o que o ADR-012 (rascunho) descrevia como
"porte mecânico" — parei e reportei antes de decidir sozinho, Architect
decidiu os dois antes de eu tocar em qualquer arquivo:

1. `chat.ts` original persistia `conversations`/`messages` direto via
   Drizzle/Postgres — a mesma violação do Princípio 4 que eu já tinha
   recusado para `storage.query`/`storage.insert` (BLD-003/ENG-011).
   Decisão: roteei pelo contrato genérico do Guardian
   (save/update/delete/get/search) via um novo `HttpGuardianClient`
   (`luna-core/src/luna/adapters/guardian-http-adapter.ts`), substituindo
   `guardian-local-adapter.ts` — exatamente a troca que o próprio
   comentário do arquivo original já previa ("quando o Guardian oficial
   for implantado, só esta classe muda"). `conversations`/`messages` viram
   duas coleções do contrato genérico, sem endpoint bespoke; só `count`
   precisou ser uma extensão nova (ver commit em `luna-guardian` abaixo).
2. `context-hub.ts`/`indice-cognitivo.ts` liam arquivos locais do monorepo
   que não existem em `luna-core`. Decisão: troquei para ler
   `Luna-context.md` via `GithubConnector.readFile`
   (`luna-core/src/luna/adapters/github-context-client.ts`), mesmo padrão
   do FORGE-MVP-08A. Mantive a lógica de extração (regexes) exatamente como
   estava — não modernizei os parsers para o formato atual dos documentos
   (isso é um follow-up separado, registrado no próprio código como
   comentário, não um defeito desta etapa).

`@workspace/api-zod` (codegen orval) e `@workspace/db` (Drizzle) não foram
portados — o primeiro porque é código gerado a partir de uma spec OpenAPI
não relacionada à lógica de negócio (copiei manualmente só as ~10 schemas
Zod que `chat.ts` usa, em `routes/chat-schemas.ts`); o segundo porque foi
inteiramente substituído pelo cliente HTTP do Guardian.

Estendi `scripts/architecture-check.mjs` de `luna-core` com as mesmas
fronteiras já testadas no `architecture-check.mjs` de origem (Cognitive
Engine nunca toca DB/provider direto, Context Hub nunca persiste/decide, só
`guardian-http-adapter.ts` conhece o endpoint do Guardian, Convergia nunca
persiste direto exceto via `knowledge-gate.ts`, Gateway continua
"cognition-free"), adaptadas aos caminhos reais deste repositório. Também
estendi a regra de centralização de credenciais (ADR-002) para reconhecer
`src/luna/adapters/` como segundo leitor autorizado de
`GROQ_API_KEY`/`ANTHROPIC_API_KEY` (Cognitive Engine é um consumidor
legítimo diferente do Model Router do Gateway) — mesmo padrão de
"múltiplos leitores por categoria" já usado para `GUARDIAN_BASE_URL`
(DA-001).

Portei também os testes que fazem sentido verbatim (memory-engine,
provider-engine, hipocampo, budget-manager, reporter, provider-router,
toda a suíte de Convergia) e reescrevi os que dependiam de filesystem local
(`indice-cognitivo.test.ts`, `context-hub.test.ts`) para injetar um
`reader` fake em vez de um diretório temporário — tornei `readProjectContext`/
`buildOrganismContext` testáveis por injeção de dependência, mesmo padrão já
usado por `createMemoryEngine(guardian = new HttpGuardianClient())`. Escrevi
`guardian-http-adapter.test.ts` do zero (mockando `fetch`, mesmo padrão de
`gateway/organs/__tests__/guardian-adapter.test.ts`), substituindo
conceitualmente `guardian-local-adapter.test.ts` (que teria testado código
que não existe mais aqui).

Corrigi um único ponto de fricção de tipos encontrado no typecheck: exceljs
declara seu próprio `interface Buffer extends ArrayBuffer` no `.d.ts`, que
colide por merge de interface global com o `Buffer<ArrayBufferLike>` do
`@types/node` desta versão — bug de tipagem do pacote upstream, não deste
código; contornado com um cast pontual em `renderers.test.ts`, comentado
inline. Também subi `@types/node` de `^22.10.0` para `^25.0.0` (mesma major
que o monorepo de origem já usa) antes de descobrir que isso sozinho não
resolvia o problema do exceljs — mantive o bump de qualquer forma, por
consistência com a versão validada na origem.

Validado antes do commit: `npm run typecheck` limpo, `npm test` 170/170,
`npm run test:architecture` limpo, smoke test manual do boot rodando o
servidor de verdade (`/`, `/health`, `/api/healthz`,
`/api/gateway/capabilities`, `GET /api/context`, `POST /api/chat`) — todos
degradam graciosamente sem `GITHUB_TOKEN`/`GUARDIAN_BASE_URL`/
`GROQ_API_KEY` configurados nesta sessão (erros limpos em JSON, processo
nunca cai).

Em `luna-guardian`: adicionei a operação `count` (contrato, `guardian.js`,
`adapters/supabase-adapter.js` via `count: "exact", head: true` do
Supabase — não fetch-all, `routes.js` com `POST /guardian/count`) e
descontinuei `/chat`/`/api/github/file` (e a dependência `pg`/`axios`
exclusiva delas) — não toquei em mais nada do Guardian (`/guardian/*`,
armazenamento, `hipocampo-temp/`). Atualizei o `architecture-check.mjs` do
próprio `luna-guardian`, que tinha um regression-guard afirmando que essas
rotas legadas "devem ser preservadas" — invertido para afirmar que elas
"não devem reaparecer", já que a instrução era descontinuá-las
deliberadamente, não uma regressão a evitar. 30/30 testes, architecture
check limpo, smoke test manual do boot (`/` funciona, `/chat` e
`/api/github/file` retornam 404 corretamente).

Commits: `luna-core` `ac38aee` (porte completo, um commit só — arquivos
interdependentes, não compilam/testam isoladamente; documentando aqui a
escolha de agrupar, conforme ENG-012); `luna-guardian` `28c1c6e`.

O que está bloqueado: nada. Próxima etapa (interface de Convergia em
`luna-frontend`) depende só deste porte estar funcionando, o que já validei
acima.

Test status: ver validação acima — typecheck/testes/architecture-check
limpos nos dois repositórios, smoke test manual do boot em ambos.

Next action: construir a interface de Convergia em `luna-frontend`
(ADR-012 Decisão 2).

## 2026-07-19 — ADR-012 Decisão 2 executada: interface de Convergia em `luna-frontend` + correção de base URL

O que fiz: construí a nova área "Convergia" no Forge
(`components/forge/convergia-panel.tsx`), seguindo o mesmo padrão
visual/estrutural do resto de `components/forge/` (Tabs/ScrollArea/Button
do `components/ui/`, classes utilitárias cruas, sem framework de formulário
novo) — três abas dentro do painel, mapeando as quatro etapas do fluxo
pedido: "Catálogo & Upload" (etapas 1+2 — upload de xlsx/csv/json com parse
+ validação imediata, e o catálogo dos 13 tipos de documento corporativo
como referência), "Transformação" (etapa 4 — escolhe template, aplica e
baixa o arquivo renderizado, com opção de enviar o resultado como
conhecimento ao Guardian) e "Conhecimento" (etapa 3 — upload de
treinamento em texto, mostra a extração do Hipocampo e a decisão de
consolidar/descartar por tipo semântico/procedimental/inferencial).
Adicionei as funções cliente correspondentes em `lib/forge/api-client.ts`
(`fetchConvergiaCatalog`, `fetchConvergiaTemplates`, `parseConvergiaFile`,
`transformConvergiaFile`, `submitConvergiaTraining`) — chamam
`/api/convergia/*` diretamente (rotas irmãs do Gateway em `luna-core`,
mesmo padrão de `/api/chat`/`/api/context`), não `executeCapability`,
porque não são capabilities do Gateway. `transformConvergiaFile` é a única
que não usa `parseJsonOrThrow`: sucesso é o arquivo renderizado (blob), não
JSON — erro continua JSON, então tratado à parte. Fiz o painel aparecer como
uma aba de nível superior nova em `forge-layout.tsx` ("Workspace" vs.
"Convergia", ao lado do seletor de projeto), com o mesmo `forceMount` já
usado no Terminal para não derrubar a conexão WebSocket dele ao trocar de
aba.

Achado que corrigi no mesmo commit, consequência direta da Decisão 1: como
`/chat` e `/context` foram removidos de `luna-guardian` no porte anterior,
o `luna-frontend` existente (que ainda apontava para
`LUNA_API_BASE_URL` = `luna-guardian`/`strong-celebration`) ia quebrar as
features de Chat/Contexto já em produção. Corrigi `sendChatMessage`/
`fetchOrganismContext` para usar `LUNA_GATEWAY_BASE_URL` (`luna-core`,
onde o Cognitive Engine mora desde o ADR-012), removi a constante
`LUNA_API_BASE_URL` inteira, e atualizei `.env.example`/`DEPLOY.md` para
não documentarem mais uma variável que não existe. Confirmei via grep que
só esses três arquivos referenciavam a base antiga — nenhum outro ponto do
repositório dependia dela.

Validado antes do commit: `pnpm run typecheck` limpo, `pnpm test` 20/20,
`pnpm run test:constitution` limpo (43 arquivos), `pnpm run build`
(`next build`) completo sem erros. Smoke test manual em navegador (`pnpm
dev`, o gate de login do `/forge` é pulado fora de produção): screenshot
da aba Workspace intacta, screenshot das três abas de Convergia
renderizando corretamente e degradando graciosamente sem backend real
rodando localmente ("Failed to fetch" no catálogo, mensagem de guarda
"Envie um arquivo... primeiro" na aba Transformação sem arquivo ainda
carregado) — nenhum erro de render novo introduzido por este código (o
único `pageerror` observado no console, sobre `dimensions`, vem do
Terminal/xterm tentando conectar a um WebSocket sem servidor real, mesmo
comportamento pré-existente do Workspace, não deste painel).

Não testei o fluxo teste-a-teste com um backend `luna-core` real
respondendo (nenhuma credencial/deploy ativo nesta sessão) — o contrato foi
verificado por leitura direta de `luna-core/src/routes/convergia.ts`
(campos de multipart, corpo/headers de resposta), não por chamada real.

Commit: `luna-frontend` `673b29c` (`main`).

O que está bloqueado: nada. As duas decisões do ADR-012 estão concluídas.

Test status: ver validação acima — typecheck/testes/constitution-check/build
limpos, smoke test manual em navegador via Playwright/Chromium.

Next action: nenhuma pendência aberta deste ADR. Pendências relacionadas
mas fora de escopo continuam registradas em `GENESIS/ROADMAP.md` (P4:
templates reais dos 13 tipos de documento, parsers DOCX/PDF).

## 2026-07-19 — Correção de documentação: renderer PPTX não era "parcial"; teste era raso

O que fiz: recebi o pacote "Integrar PPTX real ao pipeline do Convergia"
pedindo pra completar o renderer PPTX em `luna-core`, com base numa
premissa de `ECOSYSTEM_ARCHITECTURE.md` de que ele estava "parcialmente
feito". Auditei `luna-core/src/convergia/renderers/pptx-renderer.ts`
antes de escrever qualquer código de renderer: já estava completo —
slide de título + tabela paginada (18 registros/slide via `chunk()`),
registrado em `renderers/registry.ts`, com o mesmo padrão de estilo (sem
cor, cabeçalho em negrito) que `xlsx-renderer.ts`/`html-renderer.ts` já
usam — não havia paleta/tema pra "preservar" nem pra evitar herdar do
script de referência, porque nenhum renderer do Convergia usa cor. A doc
estava desatualizada, não o código.

O que era real e faltava: o teste existente (`renderers.test.ts`, teste
"pptx renderer produces a non-empty buffer") só verificava
`Buffer.isBuffer` + tamanho > 0 — não abria o arquivo. Corrigido: novo
teste carrega o `.pptx` resultante como zip real (`jszip`, adicionado
como devDependency explícita — antes só vinha transitivo via
`pptxgenjs`), lê o XML de cada slide (`ppt/slides/slideN.xml`) e confere
conteúdo real: título, contagem de registros, cabeçalho de colunas e
valores de campo, usando dados no padrão SSMA/ASO (a categoria real mais
próxima do catálogo, já que nenhum dos 13 tipos de documento corporativo
tem template implementado — `corporate-catalog.ts` já registra isso como
decisão deliberada, pendente de especialista, não regressão desta sessão).
Adicionei também um teste de paginação (25 registros → 1 slide de título +
2 slides de dados).

Não encontrei `luna-convergia/src/scripts/test-pptx.js` (commit `4e63d67`,
citado no pacote como referência) — esse repositório não estava no escopo
desta sessão; não fui atrás dele. A rigidez pedida (abrir o zip, ler o
XML) foi replicada a partir do próprio contrato do `pptxgenjs`, verificado
manualmente rodando o renderer e inspecionando a saída antes de escrever
as asserções — não a partir do script em si.

Escopo que NÃO mexi, porque ainda é real e não fazia parte deste pedido:
os 13 tipos de documento corporativo continuam sem template de conteúdo
próprio (`corporate-catalog.ts`, `regulatoryStatus: "pending_specialist_review"`
em todos), então "MVP: PPTX" como um todo segue incompleto em
`ECOSYSTEM_ARCHITECTURE.md`/`GENESIS/ROADMAP.md` — só a caracterização do
renderer em si (que já existia, completo, antes desta sessão) e o rigor do
teste (que eu de fato mudei) foram corrigidos.

Commit: `luna-core` `fe5b354` (branch `claude/pptx-renderer-test-rigor`).

Validado antes do commit: `npm test` 171/171 (incluindo os 2 testes novos),
`npm run typecheck` limpo, `npm run test:architecture` aprovado.

O que está bloqueado: nada quanto ao renderer/teste. PR de
`claude/pptx-renderer-test-rigor` para `main` ainda não aberto nesta
entrada — ver próxima ação.

Test status: 171/171, typecheck limpo, architecture-check aprovado (ver
acima).

Next action: abrir PR de `claude/pptx-renderer-test-rigor` para `main` em
`luna-core` (mudança de baixo risco, só reforço de teste). Templates reais
dos 13 tipos de documento corporativo seguem em `GENESIS/ROADMAP.md` (P4)
como pendência separada, não afetada por esta entrada.
## 2026-07-18 — Reporter (não Builder): análise automática do projeto LUNA

Autoatestação: esta entrada foi gerada por `reporter.analyze_project` (FORGE-MVP-07 v1), disparada manualmente via `/api/gateway/execute` — não é um registro do Builder. Leu `GENESIS/ROADMAP.md` real (`github.read_file`), contou 21 item(ns) concluído(s) e 31 pendente(s), e atualizou `GENESIS/ARCHITECTURE_INVENTORY.md` §11 com o resultado.

**Desde a última análise**
- Primeira execução do Reporter registrada — sem análise anterior para comparar.

Escopo v1 (ADR-013): compara só os marcadores `[x]`/`[ ]` do Roadmap contra a análise anterior — não verifica cada item contra código real (isso é auditoria dirigida, feita manualmente quando necessário). Formato de 3 camadas (física/lógica/semântica) é v2, fora de escopo aqui.

## 2026-07-19 — Pacote Reporter (FORGE-MVP-07) + correção do context-hub.ts

Eu fiz (Builder, duas tarefas, dois commits separados em `luna-core`, conforme pedido):

**Tarefa 1 — `reporter.analyze_project` no Gateway.** A entrada acima (assinada "Reporter", gerada automaticamente) é a prova de que a capability funciona — mas quem escreveu o código foi o Builder. Antes de codar, confirmei que a capability realmente não existia: zero arquivo em `gateway/manifest/`, zero `registry.register` em `gateway/index.ts` para `reporter.*`, e o payload real de `/api/gateway/capabilities` já coletado nesta sessão (19 capabilities) confirma a ausência. Implementei `ReporterAnalyzeProjectCapability` (`src/gateway/capabilities/reporter/analyze-project.ts`) reaproveitando o `GithubAdapter` já existente (nenhum adapter novo — Princípio 3) para ler `GENESIS/ROADMAP.md`, classificar `[x]`/`[ ]`, comparar com o estado da análise anterior (persistido como bloco JSON oculto em `GENESIS/ARCHITECTURE_INVENTORY.md` §11) e commitar `ARCHITECTURE_INVENTORY.md` + `GENESIS/BUILDER.md` (autoatestado como Reporter, não Builder) num único commit. Projeto diferente de `LUNA` é rejeitado com erro real, não fabricado (RENASCER/SMX/CURSO EMPILHADEIRA não têm dado seedado, confirmado na auditoria de painéis do Forge desta mesma sessão). Não implementei verificação item-a-item contra código real (o que esta sessão fez manualmente para PPTX/seletor/etc.) nem o formato de 3 camadas do ADR-013 — ambos fora do escopo v1, registrados como pendência futura, não esquecidos.

Testei em duas camadas: (1) 4 testes unitários com um `GithubAdapter` fake (rejeição de projeto inválido, dry-run sem tocar rede, primeira execução, e drift correto numa segunda execução simulando um item resolvido + um novo pendente); (2) um teste de ponta a ponta real contra o conteúdo de produção de `Luna-context.md`. Para o teste (2), o `GITHUB_TOKEN` desta sessão retornou `401 Bad credentials` ao chamar `api.github.com` diretamente (é um token de outro mecanismo — proxy de clone/push, não API REST autenticada) — troquei o `GithubAdapter` real por um adapter local (lê/commita no clone já existente em `/workspace/luna-context.md`, usando o `git` que já tenho configurado nesta sessão) só para esse teste, mantendo a lógica da capability inalterada. Isso gerou um commit real (`Luna-context.md@8cae4b1`): 21 concluído(s)/31 pendente(s) reais, drift correto de primeira execução. A entrada do Reporter acima, nesta mesma seção, é o artefato desse teste — dizer "disparada via `/api/gateway/execute`" nela é a descrição genérica de como a capability roda em produção, não uma afirmação de que este teste específico passou pelo Railway (não passou — ver limitação de rede/credencial já registrada nesta sessão). Registro isso explicitamente para não deixar a autoatestação do Reporter parecer mais forte do que a evidência real permite.

174/174 testes, typecheck limpo, `test:architecture` aprovado. Commit `2e32c47` em `luna-core`, branch `claude/reporter-analyze-project`, PR aberto para `main`.

**Tarefa 2 — regex do `context-hub.ts`.** 4 dos 7 campos de `buildOrganismContext()` (`currentMvp`, `inferences`, `activeSystems`, `activeRepositories`) voltavam vazios porque os regex foram escritos contra o formato de `Luna-context.md` de 2026-07-16 e nunca atualizados (achado da auditoria de painéis do Forge desta sessão). Conferi a estrutura real do documento antes de escrever qualquer regex novo (não assumido): headings não são mais numerados (`currentMvp` agora pega o último heading `##`, sem exigir número); "Inferências consolidadas" virou um rótulo em negrito inline, `**New inferences**`, sem heading (`extractSection` substituído por `extractBoldLabelSection`); os nomes de órgão não estão mais em bullets negritados sob um heading "Prompt 2", e sim numa linha "- Órgão...: `Nome`, ..." da seção "System classification" (`extractBoldedNames` substituído por `extractActiveOrgans`); e `ADR-004` real nunca usa o padrão `raugustorubens-design/*` que o regex antigo procurava — usa nomes entre crases (`` `luna-core` ``), então reescrevi `extractRepoSlugs` para esse formato.

Validei rodando as 4 funções contra o conteúdo real de produção (não só o fixture do teste) antes de commitar — todas as 4 retornaram dado real (`currentMvp`: heading mais recente de fato; `inferences`: as 4 inferências reais da seção; `activeSystems`: `["Luna-reporter", "Convergia"]`; `activeRepositories`: 5 repos reais). Fixture de `context-hub.test.ts` atualizado pro novo formato. 170/170 testes (174 já inclui os 4 do Reporter acima, contados juntos no branch atual), typecheck limpo, `test:architecture` aprovado. Commit `19ea30b` em `luna-core`, branch `claude/context-hub-regex-fix`, PR aberto para `main`.

O que está bloqueado: nada. As duas branches têm PR aberto, aguardando merge.

Next action: merge dos dois PRs (`claude/context-hub-regex-fix`, `claude/reporter-analyze-project`) em `luna-core`, depois confirmar em produção (Railway) que `reporter.analyze_project` aparece em `/api/gateway/capabilities` e que o botão "Analisar Projeto" do Forge para de retornar `CAPABILITY_NOT_FOUND`.

## 2026-07-19 — GEN-002 v2 Fase 1: workflow `builder-headless.yml` (Claude Code headless, sem fallback ainda)

Eu fiz (via Claude Code, sessão de chat — não é uma execução do próprio workflow, é a implementação dele): criei `.github/workflows/builder-headless.yml` em `Luna-context.md`, conforme o pacote GEN-002 v2 Fase 1 ratificado pelo Architect (ver `GENESIS/ENGINEER.md`, ID GEN-002). `workflow_dispatch` com dois inputs obrigatórios (`package_path`, `target_repo`); passo de leitura do pacote falha explicitamente (`::error::`) se `package_path` não existir já commitado em `Luna-context.md` — mantém a trava de governança (nunca texto livre). Checkout do `target_repo`, branch nova `builder/{run_id}`, instala a CLI do Claude Code, roda headless (`claude -p "$PACKAGE_CONTENT" --dangerously-skip-permissions` — sintaxe a reconferir na documentação vigente antes do primeiro uso real, como o próprio pacote pede) e só commita/push a branch se a execução tiver sucesso e realmente tiver produzido mudança (`git status --porcelain`). Fase 2/3 (fallback OpenCode/Aider) deliberadamente fora — se Claude Code falhar, o workflow registra a falha e termina com erro, não tenta mais nada.

Autoatestação sempre acontece, sucesso ou falha (Regra 6): o último passo sempre anexa uma entrada nesta seção do `BUILDER.md` (e commita em `main` de `Luna-context.md`) citando `run_id`, `target_repo`, `package_path` e o resultado — inclusive quando Claude Code falha, pra não ter falha silenciosa.

**Gap técnico real encontrado, não estava no pacote original — sinalizando explicitamente, não escondendo:** o `GITHUB_TOKEN` padrão de um Action só tem alcance sobre o próprio repositório onde ele roda (`Luna-context.md`), nunca sobre `target_repo` (outro repositório). O passo "Checkout target repo" usa `secrets.BUILDER_REPO_TOKEN` em vez do `GITHUB_TOKEN` padrão por isso — precisa ser um PAT (classic, escopo `repo`) ou token de GitHub App com acesso aos repositórios-alvo, cadastrado manualmente como secret em `Luna-context.md` antes do primeiro teste real. Sem isso, o passo de checkout do `target_repo` falha com 404/403.

O que está bloqueado: dois secrets precisam ser cadastrados manualmente em `Luna-context.md` (Settings → Secrets and variables → Actions) antes do teste de aceitação rodar de verdade — não tenho acesso a essa tela e não devo manusear valor de credencial:
- `ANTHROPIC_API_KEY` — dedicada a este workflow, não reaproveitar a do `luna-core` (mesma lógica de token por serviço já usada no `GITHUB_TOKEN` do `luna-frontend`, ver ENG-019).
- `BUILDER_REPO_TOKEN` — não estava especificado no pacote original; é o gap técnico acima. Precisa de permissão de escrita nos repositórios-alvo (`luna-core` no teste de baixo risco sugerido).

Não criei o pacote de teste (`pending-packages/teste-gen-002-fase1.md`) nem disparei o `workflow_dispatch` — o próprio pacote descreve isso como teste manual pela interface do GitHub, e a implementação (este commit) ainda não tem os dois secrets acima configurados, então disparar agora só produziria falha de credencial, não um teste real.

Next action: cadastrar os dois secrets acima; criar e commitar o pacote de teste em `pending-packages/`; disparar `workflow_dispatch` manualmente (Actions → Run workflow) com um `target_repo` de baixo risco; confirmar branch criada + entrada em `BUILDER.md` + que uma falha proposital também vira entrada registrada (não desaparece). Só depois disso: Fase 2 (OpenCode).

## 2026-07-20 — Pacote 1/2: GENESIS/PLANO_MESTRE.md (via Claude Code, sessão de chat em `luna`)

Eu fiz (Builder, este commit): copiei `GENESIS/PLANO_MESTRE.md` — conteúdo
exatamente como entregue no pacote desta instrução, sem edição — do
repositório `luna` (branch `claude/luna-autoprogramacao-segura-xcw6zo`,
onde havia sido commitado por engano numa sessão anterior desta mesma
conversa, antes de eu confirmar que o destino correto era este
repositório de contexto) para cá. `diff` bit-a-bit confirmado idêntico
antes do commit. Adicionei uma linha em `INDEX.md` §"Conteúdo atual"
apontando para o documento, seguindo a convenção já estabelecida neste
repositório de registrar todo documento de decisão/planejamento no
índice.

Não fiz (Pacote 2/2, bloqueado): aplicar o Art. AAAB.9 (Segurança
Cognitiva) em `LUNA_CONSTITUTION.md` e criar `ADR-014`. O pedido cita
"os pacotes já preparados (Plano Mestre final + AAAB9-e-ADR014-seguranca)"
como se o conteúdo já estivesse disponível para mim — mas o texto real
de Art. AAAB.9 e de ADR-014 não está em nenhum dos dois repositórios
(`luna`, `Luna-context.md`) nem foi colado nesta sessão de chat. Toda
emenda constitucional e todo ADR anteriores neste arquivo (ex.: ADR-009,
pacote 4/9 de 2026-07-18) foram aplicados com o texto exato entregue no
pacote da instrução — nunca redigidos pelo próprio Builder. Não vou
fabricar texto de segurança cognitiva/constitucional; sinalizando o
bloqueio em vez de inventar conteúdo.

Consequência direta: a remoção de `GENESIS/PLANO_MESTRE.md` do
repositório `luna` (pedida como passo 3, condicionada a "confirmado nos
dois lugares certos") também fica pendente — só o lugar 1 (este arquivo,
aqui) está confirmado; o lugar 2 (Constitution + ADR-014) ainda não
existe.

Next action: usuário cola o conteúdo real do pacote
"AAAB9-e-ADR014-seguranca" (Art. AAAB.9 completo + ADR-014 completo)
nesta sessão de chat; só então aplico os dois documentos aqui e removo
`GENESIS/PLANO_MESTRE.md` de `luna`.

## 2026-07-20 — Pacote 2/2: Art. AAAB.9 (Constitution) + ADR-014 (Segurança Cognitiva)

Eu fiz (Builder, via Claude Code, sessão de chat em `luna`): apliquei o
Art. AAAB.9 em `LUNA_CONSTITUTION.md` (inserido após Art. AAAB.8, antes
de "## Princípios") e criei
`ADR/ADR-014-Arquitetura-Imunologica-Seguranca-Cognitiva.md` — ambos com
o conteúdo entregue no pacote desta instrução, verbatim, sem edição,
reescrita ou resumo (conferido por comparação linha a linha antes do
commit). Atualizei `INDEX.md` com duas linhas novas: Art. AAAB.9 e
ADR-014, seguindo a mesma convenção usada para ADR-009 a ADR-013.

Não fiz nenhuma validação de conteúdo técnico do ADR (modelo de ameaças,
mapeamento de componentes, referências) — isso é responsabilidade do
Architect/Engineer que prepararam o pacote; meu papel aqui foi
aplicação fiel, não revisão de mérito.

Com isto, o pacote 1/2 (Plano Mestre, entrada anterior) e o pacote 2/2
(este) completam os "dois lugares certos" — Constitution + ADR-014
aceitos. Consequência: a cópia de `GENESIS/PLANO_MESTRE.md` em `luna`
(branch `claude/luna-autoprogramacao-segura-xcw6zo`) pode ser removida —
ver commit correspondente nesse outro repositório.

Test status: nenhuma mudança de código — pacote inteiramente de
documentação constitucional/decisória.

Next action: nenhuma minha. Fica registrado como pendência real (Parte
VIII do ADR-014, item 5): o critério objetivo de liberação de
quarentena (Nível 2b) ainda não existe como ADR — até lá, toda liberação
escala ao Architect, não ao Reporter sozinho.

## 2026-07-21 — Builder headless run 29791039096 (falhou — atestação manual)

Disparei manualmente (via Claude Code, sessão de chat, não o workflow em
si) o `workflow_dispatch` de `builder-headless.yml` com
`package_path=pending-packages/2026-07-21-teste-gen-002-fase1.md`,
`target_repo=raugustorubens-design/luna-core` — primeiro disparo real do
GEN-002 v2 Fase 1.

**Resultado: falhou no passo "Checkout target repo"**, com o erro
`Input required and not supplied: token` — o secret `BUILDER_REPO_TOKEN`
não está cadastrado em `Luna-context.md` (Settings → Secrets and
variables → Actions). Confirma exatamente o gap já sinalizado na entrada
de 2026-07-19 (implementação do workflow): sem esse PAT/token de escrita
em `luna-core`, o checkout do repositório-alvo falha antes de qualquer
código rodar. Nenhuma branch foi criada em `luna-core`; `claude`
(headless) nunca chegou a rodar.

**Esta entrada é atestação manual, não automática** — o passo
"Append self-attestation to BUILDER.md" do workflow não roda quando um
passo anterior falha (não tem `if: always()`), então a falha teria
ficado sem registro se eu não tivesse checado o log e escrito isto à
mão. Sinalizando como gap real do próprio workflow, não escondendo:
contradiz o texto da entrada de 2026-07-19 ("Autoatestação sempre
acontece, sucesso ou falha") — na prática, só acontece em sucesso ou na
falha específica tratada pelo passo "Fail the run if Claude Code
failed"; qualquer falha em passo anterior (como esta) pula a atestação
silenciosamente.

Run: https://github.com/raugustorubens-design/Luna-context.md/actions/runs/29791039096

Next action: cadastrar `BUILDER_REPO_TOKEN` (PAT classic, escopo `repo`,
com permissão de escrita em `luna-core`) e `ANTHROPIC_API_KEY` como
secrets em `Luna-context.md` — não posso fazer isso eu mesmo (tela de
Settings, não devo manusear valor de credencial). Separadamente,
recomendo adicionar `if: always()` ao passo de atestação do workflow
para que ele nunca dependa de checagem manual como esta — não apliquei
essa mudança porque é uma alteração ao próprio workflow (GEN-002 Fase 1),
não ao pacote de teste; aguardando decisão. Depois de cadastrar os
secrets, redisparar o mesmo pacote (`2026-07-21-teste-gen-002-fase1.md`)
sem alterações.

## 2026-07-21 — Builder headless run 29791773565

Eu fiz (via Claude Code, headless, GitHub Actions): apliquei o
pacote `pending-packages/2026-07-21-teste-gen-002-fase1.md` em `raugustorubens-design/luna-core`. Sucesso. Branch criada: https://github.com/raugustorubens-design/luna-core/tree/builder/29791773565.

Run: https://github.com/raugustorubens-design/Luna-context.md/actions/runs/29791773565

## 2026-07-22 — Registro consolidado da noite: ENG-026, ENG-027, GENESIS/STATUS.md

Eu fiz (Builder, via Claude Code, sessão de chat): persisti o "Registro
consolidado — 2026-07-22 (noite)" recebido nesta instrução —
`GENESIS/ENGINEER.md` ganhou ENG-026 (plano de investigação de
grounding/alucinação, ligado a ENG-025) e ENG-027 (decisão do Architect
de nunca depender de auto-merge, sempre confirmação explícita). Criei
`GENESIS/STATUS.md` — primeiro conteúdo real de um arquivo que só existia
como item aspiracional em `GENESIS/README.md` §Files e no Roadmap P3
("Criar/atualizar os arquivos do Genesis... STATUS.md, HISTORY.md e
TASKS.md") — com a lista mestra de pendências (ENG-021 a ENG-027 + itens
não numerados). `HISTORY.md`/`TASKS.md` seguem não criados; atualizei a
linha correspondente do Roadmap P3 para refletir isso, sem marcar o item
inteiro como concluído. `INDEX.md` ganhou a entrada de `STATUS.md`.

**Correção aplicada durante a persistência, não silenciosa:** o texto
original de ENG-026 citava "ADR-016" como a especificação já existente do
conceito "Quarentena Cognitiva" (direção 4 do Architect, Guardian como
filtro de saída). Conferi contra o ADR-016 real deste repositório
(`ADR-016-Sistema-Sensorial-Fluxo-A.md`, mergeado mais cedo nesta mesma
sessão de trabalho) — ele não menciona quarentena em lugar nenhum; é sobre
Playwright/Provider Router/painel do navegador. O ADR real com
"Quarentena Cognitiva" (Partes V e VII) é o ADR-014 (Arquitetura
Imunológica de Segurança Cognitiva). Corrigido antes de commitar, com a
correção anotada inline na própria entrada ENG-026 — não apaguei o erro
silenciosamente, porque ENG-026 é justamente sobre esse tipo de falha de
citação, e deixá-lo entrar errado no registro permanente seria o mesmo
problema que o item existe para investigar.

**Gap sinalizado, não escondido:** ENG-021 a ENG-025 aparecem na tabela de
`GENESIS/STATUS.md` só com tópico e status — não tenho o conteúdo
completo original de nenhum deles (só foi entregue o resumo), então não
fabriquei entradas completas para eles em `GENESIS/ENGINEER.md`. Registrado
explicitamente no próprio `STATUS.md` como pendência à parte.

Test status: nenhuma mudança de código — pacote inteiramente de
documentação/coordenação.

Next action: nenhuma minha além de persistir. A ordem de prioridade
sugerida pelo próprio registro (ENG-027 primeiro — já decidido e em
uso — depois ENG-022) fica registrada em `GENESIS/STATUS.md` para a
próxima sessão consultar antes de abrir frente nova.
