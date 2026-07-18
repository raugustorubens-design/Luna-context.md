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