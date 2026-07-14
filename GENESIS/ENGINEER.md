# ENGINEER

Owner: Claude

Use this file for technical review, inconsistencies, risks, and specification notes.

## What goes here
- Technical divergences
- Risks
- Constraints
- Dependency notes
- Specification refinements
- Implementation impact

## What does not go here
- Final architecture decisions
- Code
- Permanent knowledge

## Entry format
- ID
- Date
- Topic
- Observation
- Risk
- Suggested action
- Status

## Current workplan
- Verify Guardian implementation boundaries.
- Keep the Memory Index as a structured map, not raw memory.
- Keep the Conversation Coordination flow small and low-noise.
- Flag any architecture/document mismatches before implementation.

## ID: ENG-004
Data: 2026-07-13
Tópico: Convergia — divergência entre repo-interface e implementação real

Observação: o repositório luna-convergia (a interface que deveria ser o MVP
separado do organismo) contém apenas um esqueleto de 1 endpoint em ambas as
branches (main e codex/create-post-route-for-excel-upload). A implementação
real e madura — pipeline completo Entrada→Parser→Modelo Canônico→Validação→
Transformação→Template→Renderer→Resultado, 3 parsers, 6 renderers, catálogo
de 13 documentos corporativos, e o Guardian-passthrough já correto via
knowledge-gate.ts — vive dentro do monorepo luna, em
apps/frontend/artifacts/api-server/src/convergia/.

Risco: essa divergência é estruturalmente idêntica à que motivou o ADR-004
(Gateway nasceu no monorepo luna, foi portado pro luna-core). Sem uma decisão
equivalente para o Convergia, o repo-interface luna-convergia continua
desalinhado com o princípio "cada repo é um MVP separado preparado para
acoplamento".

Frontend com mapeamento de campo ("bolhas") não localizado em nenhum dos
repositórios auditados (luna-convergia, luna-frontend, luna/apps/frontend/
artifacts/frontend) — hipótese do usuário é que existe do lado do GPT/LUNA,
ainda não commitado.

Ação sugerida: decisão de Architects sobre portar convergia/ do monorepo para
luna-convergia (mesmo padrão do ADR-004), e confirmação com GPT/LUNA sobre o
paradeiro do frontend.
Status: aguardando decisão de Architects

## ID: ENG-005
Data: 2026-07-13
Tópico: model.chat / model.chat_deep / storage.query / storage.insert — primeiras capabilities a consumir o Model Router (PR #9) e o SupabaseHubConnector

Observação: o PR #9 (mergeado em 2026-07-12) entregou a infraestrutura de
roteamento de modelo (Groq/DeepSeek/OpenRouter/Anthropic) e o conector
Anthropic de propósito sem nenhuma capability consumidora ("infraestrutura
pura, sem consumidor ainda", conforme a própria PR documenta). O
SupabaseHubConnector também já existia, sem consumidor. Verificado antes de
implementar: nenhuma capability do Gateway chamava IA ou Supabase até esta
sessão.

Risco identificado e mitigado: chamar createGroqConnector()/
createDeepseekConnector()/createOpenrouterConnector()/
createAnthropicConnector()/createSupabaseConnector() no boot sem guarda
derrubaria o processo inteiro — resolve*Credentials() lança quando a env var
falta, e nenhuma das 5 credenciais está configurada em produção hoje (Railway).
Mitigação: construção de cada grupo de conectores isolada em try/catch em
app.ts; a capability correspondente simplesmente não é registrada
(CAPABILITY_NOT_FOUND ao chamar, ausente de /api/gateway/capabilities) se a
credencial faltar — mesma tolerância a ausência já usada para GITHUB_TOKEN.

Risco não resolvido, fora do meu controle nesta sessão: o GitHub App do
conector usado por mim está com "Contents" e "Pull requests" em somente
leitura (403 Resource not accessible by integration em toda tentativa de
escrita, em luna-core e neste próprio repo). Não consegui commitar o código
nem fechar as PRs #3/#4/#5 (obsoletas, versão Python pré-ADR-004) diretamente.
Entreguei como patch para aplicação manual/push local.

Ação sugerida: usuário ajustar a permissão do GitHub App (Settings →
Applications → Installed GitHub Apps → Configure → Contents: Read and write,
Pull requests: Read and write) para viabilizar commits e fechamento de PR
diretos em sessões futuras.
Status: implementação pronta e validada localmente (typecheck, test:architecture,
94/94 testes, boot smoke-tested com e sem credenciais); aguardando push manual
do patch ou ajuste de permissão do GitHub App.
