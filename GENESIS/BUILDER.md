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