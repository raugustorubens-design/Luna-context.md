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

## ID: ENG-006
Data: 2026-07-16
Tópico: Auto-atualização do BUILDER.md a cada etapa concluída

Observação: Rubens (Architect) determinou que toda etapa de implementação
concluída deve incluir, no mesmo commit, a atualização do BUILDER.md —
sem depender de pedido manual separado. Autoatestação em primeira pessoa
("eu fiz"), no arquivo que já é do Builder por Regra 2.
Status: regra ativa.

## ID: ENG-007
Data: 2026-07-16
Tópico: Escopo do Reporter — verificação por evidência, não autoria; IDs estáveis no Roadmap

Observação: Reporter não cria, reprioriza nem remove itens do Roadmap —
apenas marca como concluído o que já existe, com evidência objetiva
(commit/PR/deploy/teste). Autoria de Framework/Pendências/Plano de trabalho
continua humana + Engineer + Architect. Para viabilizar essa verificação sem
ambiguidade, todo item do Roadmap passa a levar um ID estável e permanente,
com prefixo por domínio (MEM-, STOR-, REP-, BLD-, HIP-, FORGE-, INFRA-, GEN-).
Builder diz "eu fiz" (BUILDER.md); Reporter diz "eu confirmei" (propagação
por evidência, nunca por fala do Builder).
Status: regra ativa; aguarda maturidade do Reporter além do scanner básico
para execução de fato.

## ID: ENG-008
Data: 2026-07-16
Tópico: Roteamento de persistência — Engineer/Architect decidem, Builder persiste

Observação: Engineer e Architect seguem sem acesso de escrita ao GitHub
(403 confirmado nesta sessão). Toda decisão é entregue como pacote de
aplicação pronto (conteúdo exato + caminho + mensagem de commit) para o
Builder executar — só se considera oficial após esse commit existir.
Status: regra ativa a partir de 2026-07-16.

## ID: ENG-009
Data: 2026-07-16
Tópico: Proposta — sessão simultânea de múltiplas IAs no luna-forge (Architectural Transition, não decidida ainda)

Observação: proposta do Architect e Rubens de operar Engineer + Builder
(+ Architect, opcional) simultaneamente na mesma interface do luna-forge,
eliminando a ponte manual atual (decisão em chat → cópia manual → execução
→ relato). Nota: GENESIS/FORGE.md, referenciado em sessão anterior como
papel formal do Forge, ainda não existe no repositório (mesmo bloqueio de
permissão) — esta proposta parte de um documento que ainda não foi aplicado.

Risco identificado: presença simultânea, sem guardrail, recria o mesmo tipo
de violação de fronteira já registrada anteriormente (Engineer escrevendo
código atribuído ao Builder). Guardrail proposto: mesmo em modo simultâneo,
apenas o Builder commita; Engineer/Architect produzem diff sugerido, nunca
commit próprio.

Ação sugerida: Architect decide formalmente antes de implementar (não é
correção de bug, é mudança de arquitetura operacional do Forge).
Status: Research Hypothesis / Architectural Transition — não implementar
até decisão explícita do Architect sobre o guardrail de escrita.

## ID: ENG-010
Data: 2026-07-16
Tópico: Requisitos técnicos mínimos para sessão multiagente no luna-forge (v0.2, ver FORGE-001)

Observação: para viabilizar FORGE-001 sem recriar violação de fronteira já
registrada neste projeto: (1) isolamento de contexto por agente; (2)
atribuição explícita por mensagem/ação; (3) escrita restrita ao Builder
mesmo com múltiplos agentes ativos; (4) sincronização de prompt com GENESIS
quando o arquivo de origem mudar.
Status: especificação pronta; implementação adiada pro v0.2 (ver ARCH-001,
congelamento).

## ID: ENG-011
Data: 2026-07-18
Tópico: `storage.query`/`storage.insert` bloqueadas — não aplicadas ao Gateway (ver STOR-001)

Observação: `luna-core` PR #10 (mergeada em 2026-07-15) aplicou apenas
`model.chat`/`model.chat_deep` ao Gateway. As capabilities
`storage.query`/`storage.insert`, especificadas originalmente junto com as
duas anteriores (ver ENG-005/BLD-001), foram deliberadamente excluídas
dessa PR: dariam ao Gateway acesso direto ao Supabase
(`Gateway → Supabase`), violação do Princípio 4 da Constitution
("toda persistência passa pelo Guardian"). O desenho correto é
`Gateway → Guardian → Hipocampo → Supabase`, ainda não especificado.

Risco: implementar uma versão "provisória" de `storage.query`/
`storage.insert` direto no Gateway para destravar o P1 recriaria a mesma
violação de fronteira já identificada — não é uma correção incremental,
é o redesenho que STOR-001 (P0, congelado por ARCH-001) existe para
resolver.

Ação sugerida: não implementar `storage.query`/`storage.insert` no
Gateway até o Architect decidir o redesenho via Guardian/Hipocampo
(STOR-001). `SUPABASE_URL`/`SUPABASE_KEY` seguem dormentes, sem consumidor
no Gateway.
Status: bloqueado por decisão de Architect pendente (STOR-001); não é
tarefa de Builder sozinho.

Atualização (2026-07-18, ver ADR-010): o "ainda não especificado" acima
não é mais verdade — ADR-010 fecha a especificação canônica de memória
(MEM-001/STOR-001). O que muda: a decisão de *especificação* está tomada;
a decisão de *liberar a implementação* continua sob o congelamento de
ARCH-001 (retomar após Forge v0.1 em uso diário). Status revisado:
bloqueado por congelamento de implementação (ARCH-001), não mais por
decisão de especificação pendente.

## ID: ENG-012
Data: 2026-07-18
Tópico: ENG-006/ENG-008 passam de regra rígida a boa prática ajustável pelo fundador

Observação: decisão do fundador (Rubens), 2026-07-18 — a disciplina de
"cada etapa concluída inclui, no mesmo commit, a atualização do
BUILDER.md" (ENG-006) e "só o Builder commita, demais papéis produzem
diff sugerido" (ENG-008) deixam de ser regras rígidas e passam a ser boa
prática, ajustável pelo fundador conforme conveniência de produção. Na
prática: a preferência por commit separado por arquivo + autoatestação
correspondente continua sendo o padrão default; agrupar múltiplos
arquivos num commit só é permitido quando autorizado explicitamente,
desde que essa decisão seja registrada no BUILDER.md.
Status: regra ativa como boa prática, não mais como obrigação rígida.

## ID: ENG-013
Data: 2026-07-18
Tópico: `context.txt` § Cognitive Model — `Decision(t) = H(t) + M(t)` vs. `H(t) + A(t)` assumido por ADR-010

Observação: ADR-010 §9 e a nota adicionada a `context.txt` § Memory Update
(ver BLD, pacote 2/6 de 2026-07-18) afirmam "Action lives in Decision(t) =
H(t) + A(t), in the Cognitive Model section above". O texto real da seção
`🧠 COGNITIVE MODEL` de `context.txt` (linha 29) diz `Decision(t) = H(t) +
M(t))` — nunca usa o símbolo `A(t)`. Nenhum dos dois documentos (o pacote
de instrução que gerou ADR-010, nem o próprio ADR) conferiu essa frase
contra o arquivo real antes de assumi-la.

Risco: a nota inserida em `context.txt` agora descreve incorretamente o
conteúdo da própria seção que ela cita ("acima"), criando uma nova
inconsistência interna no mesmo documento que o ADR-010 pretendia corrigir.

Ação sugerida: decisão do Architect/Engineer sobre qual lado corrigir —
(a) atualizar `Decision(t) = H(t) + M(t)` para `H(t) + A(t)` em
`context.txt` § Cognitive Model (parece a leitura mais provável, dado que
`M(t)` já é usado para "machine state" ali e para "long-term memory" na
seção seguinte — colisão de símbolo semelhante à que motivou ADR-010 §3),
ou (b) reescrever a nota da Memory Update para não pressupor um texto que
não existe.
Status: divergência técnica sinalizada; não resolvida por conta própria
do Builder (Regra 6).
