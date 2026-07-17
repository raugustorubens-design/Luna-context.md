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
Nenhum push ainda — branch local, PR não solicitado.