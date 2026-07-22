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

## ID: ENG-014
Data: 2026-07-19
Tópico: `/api/chat` e `/api/context` já implementados no monorepo `luna` — nunca portados para `luna-core` (ADR-004 portou só o Gateway)

Observação: `LUNA_CONTEXT.md`/`DEPLOY.md` (luna-frontend) registram como
lacuna aberta que o backend de chat/contexto hoje em produção
(`luna-guardian`, projeto Railway "strong-celebration") tem contrato
incompatível para `/chat` e não implementa `/context`. Auditoria de
arquitetura (2026-07-19, ver `GENESIS/ARCHITECTURE_INVENTORY.md`) encontrou
que o contrato correto **já está implementado e montado** dentro do
monorepo `luna`, em
`apps/frontend/artifacts/api-server/src/routes/{chat,context}.ts` (325 +
16 linhas, `runCognitiveEngine`/`buildOrganismContext`, schemas
`@workspace/api-zod`, montado em `/api` via `app.ts:32`) — nunca portado
para fora do monorepo. O ADR-004 portou explicitamente só o Gateway e o
Connector Hub; o restante do `api-server` (Cognitive Engine, Memory
Engine, Convergia real, chat/context) ficou para trás, sem deploy próprio
conhecido.

Risco: a lacuna de chat/contexto vem sendo tratada implicitamente como
"falta implementar", quando na verdade é "falta portar" — um trabalho de
escopo muito menor (mesmo padrão mecânico do ADR-004) do que reimplementar
do zero.

Ação sugerida: Architect decidir se autoriza um ADR análogo ao ADR-004
para portar `src/luna/*` (Cognitive Engine) e `src/routes/{chat,context}.ts`
de `apps/frontend/artifacts/api-server` para `luna-core` — resolveria a
lacuna registrada em `LUNA_CONTEXT.md` (MVP Chat) sem nova implementação.
Fora do escopo desta observação: decidir se `src/convergia/` (também não
portado) segue o mesmo caminho ou aguarda ENG-004.
Status: **resolvido por ADR-012 (2026-07-19)** — Cognitive Engine +
Convergia + rotas chat/context portados para `luna-core` (commit `ac38aee`),
`/chat`/`/context` legados descontinuados em `luna-guardian` (commit
`28c1c6e`). Ver ADR-012 para os dois refinamentos que a auditoria
pré-implementação exigiu (persistência via Guardian, contexto via GitHub)
antes do porte ser executado. Decisão 2 (interface de Convergia em
`luna-frontend`, mais a correção de `sendChatMessage`/
`fetchOrganismContext` para a nova base do Gateway) concluída no mesmo dia,
commit `673b29c`.

## ID: ENG-015
Data: 2026-07-19
Tópico: CPF removido de LUNA_CONSTITUTION.md — dado sensível exposto em repositório versionado

Observação: o Art. AAAA da Constituição citava o CPF do Originador
Constitucional em texto plano. Repositório aparentemente público — CPF é
dado sensível (documento de identidade nacional brasileiro), exposição
é risco real de fraude/doxxing, não teórico. Removido nesta sessão
(ver commit correspondente), mantendo o nome completo do Originador —
suficiente para a função de identificação do Artigo, sem o dado sensível.

Risco residual: histórico de commits do Git é praticamente permanente —
quem já clonou o repositório antes desta remoção ainda tem o CPF na
história local. Remover do arquivo atual não apaga isso; só uma reescrita
de histórico (`git filter-repo` ou equivalente) resolveria de fato, e isso
tem custo próprio (invalida hashes de commit existentes, exige
force-push). Não executado nesta sessão — decisão de Architect, não
urgência técnica adicional além da já resolvida (arquivo atual limpo).

Ação sugerida: Architect decidir se vale reescrever o histórico do
repositório para remover o CPF de commits antigos também, ou se a remoção
do arquivo atual é suficiente dado o risco residual descrito acima.
Pendência relacionada, já em andamento: substituir a identificação do
Originador por verificação criptográfica (fingerprint de chave pública),
uma vez que a chave SSH/GPG de assinatura de commit seja gerada — ver
próximo pacote Engineer sobre o Artigo de Autonomia Limitada.
Status: CPF removido do arquivo atual; reescrita de histórico e
verificação criptográfica seguem pendentes de decisão/execução.

## ID: INFRA-002
Data: 2026-07-19
Tópico: GitHub App instalado não tem acesso a 4 repositórios (luna, luna-frontend, luna-guardian, Luna-reporter)

Observação: verificado por tentativa direta de leitura via API — o GitHub
App usado pelas sessões de chat/Engineer retorna 404 (não 403) para:
`luna` (monorepo), `luna-frontend`, `luna-guardian`, `Luna-reporter`.
Acesso confirmado, no mesmo teste, para: `Luna-context.md`, `luna-core`,
`Front-View`, `projeto-renascer`, `projeto-renascer-backup`.

Diferente do INFRA-001 (permissão de escrita, já resolvido) — aqui o App
nem lista os repositórios, sugerindo instalação configurada como "Only
select repositories" sem esses 4 incluídos.

Risco: qualquer sessão de Engineer (chat) que precise auditar esses 4
repositórios opera sem evidência direta, dependendo inteiramente do que
`BUILDER.md` relata. Essa lacuna atrasou o diagnóstico do incidente
registrado em ENG-019 (abaixo) — o Guardian, especificamente, é um dos 4
bloqueados, e é onde a causa raiz real do bug de chat provavelmente está.

Ação sugerida: Originador ajusta a instalação do GitHub App — GitHub →
Settings → Applications → Installed GitHub Apps → Configure → adicionar
`luna`, `luna-frontend`, `luna-guardian`, `Luna-reporter` à lista de
repositórios autorizados.
Status: aguardando ação do Originador. Não bloqueia o Builder (usa
credencial própria), mas bloqueia diagnóstico independente do Engineer —
ver ENG-019, onde isso já atrasou a investigação.

## ID: ENG-019
Data: 2026-07-19
Tópico: Incidente em produção no Forge (chat 500, GitHub 404, terminal cai) — diagnóstico completo até a causa raiz de código

Observação: Originador reportou Forge em produção com múltiplas falhas
simultâneas: chat retorna 500 (todos os 3 agentes: GPT/Claude/Groq),
painel Git retorna "GitHub request failed with status 404", terminal
conecta e desconecta imediatamente, painel de Contexto inicialmente
retornava "Failed to fetch". Diagnóstico conduzido em conjunto
(Originador operando o Railway/Forge, Engineer lendo código-fonte e
propondo hipóteses testáveis) ao longo desta sessão.

Mapeamento de infraestrutura real (não documentado antes em lugar
nenhum):

| Serviço Railway | Repositório | Papel |
|---|---|---|
| `uvicorn main` | `luna-core` | Gateway + Cognitive Engine + Convergia (nome do serviço é resquício do Python pré-ADR-004; `railway.json` confirmado correto, Node) |
| `strong-celebration` | `luna-guardian` | Guardian/memória — tem `OPENAI_API_KEY` residual de rota já descontinuada por ADR-012, não urgente remover |
| `luna-frontend` | `luna-frontend` | O próprio Forge |

**Causas identificadas, em ordem cronológica de descoberta:**

1. **`GITHUB_TOKEN` ausente do `luna-frontend`** — confirmado ausente por
   inspeção da lista de variáveis. Corrigido pelo Originador: token
   pessoal (classic, escopo `repo`) criado e cadastrado. Redeploy
   disparado automaticamente pelo Railway. **Resolvido** — porém o painel
   Git continuou retornando 404 mesmo depois, então não era (ou não era só
   isso) a causa do erro do GitHub — ver item 4.

2. **Variável de URL do Gateway desatualizada** — `NEXT_PUBLIC_LUNA_API_BASE_URL`
   (nome antigo, pré-ADR-012) estava presente; a variável nova esperada
   pelo código pós-ADR-012 não foi confirmada por nome exato (Engineer não
   tem acesso a `luna-frontend` para grep — ver INFRA-002). Como variáveis
   `NEXT_PUBLIC_*` do Next.js são fixadas no build, um redeploy foi
   necessário para qualquer correção de variável ter efeito.

3. **Painel de Contexto voltou a funcionar** após a correção do item 1 +
   redeploy — confirmado visualmente ("Sistema atual: LUNA", "Missão
   atual" com conteúdo real carregando). Prova que a ligação
   `luna-frontend` → `luna-core` está request funcionando para essa rota.

4. **Chat continuou falhando (500) mesmo com credenciais de IA
   confirmadas** — painel do Forge mostra "2/5 provedores configurados:
   groq ✓, claude ✓" — ou seja, Groq e Claude estão corretamente
   configurados, e mesmo assim as três tentativas de chat (GPT/Claude/Groq)
   falharam identicamente. Isso descarta credencial ausente como causa.

5. **Causa raiz de código confirmada por leitura direta de
   `luna-core/src/routes/chat.ts`** (commit `ac38aee`, `main`): no handler
   `POST /chat`, as duas primeiras chamadas ao Guardian (`guardian.save`
   para criar conversa e salvar mensagem do usuário) estão protegidas por
   `try/catch`, devolvendo 500 com mensagem legível em caso de falha. A
   terceira chamada — `const lunaResponse = await runCognitiveEngine(content);`,
   a que de fato invoca a IA — **não tem nenhum `try/catch`**. Qualquer
   erro dentro dela sobe sem tratamento, vira 500 genérico do Express sem
   corpo de erro útil — exatamente o comportamento observado (Response
   vazio no DevTools do navegador).

6. **Hipótese sobre o gatilho do erro dentro de `runCognitiveEngine`**
   (não confirmada — falta acesso ao código do `luna-guardian`, ver
   INFRA-002): `runCognitiveEngine` consulta memória via Guardian
   internamente (logs do `luna-core` já mostram eventos
   `memory.retrieval.started`/`completed`). O painel de Contexto do Forge
   mostra, separadamente, "Guardian Memory Index search failed with
   status 400". Se essa consulta interna falhar sem tratamento, o efeito
   é exatamente o 500 opaco observado — para os três agentes, porque a
   falha ocorre antes de qualquer provider de IA específico ser chamado.

7. **Painel Git (404) e Terminal (desconecta na hora) permanecem sem
   causa raiz confirmada** — não investigados a fundo ainda; GITHUB_TOKEN
   sozinho não resolveu o Git, então a causa é outra (rota do código, ou
   nome de repositório incorreto na configuração do painel).

Risco: sem tratamento de erro em `runCognitiveEngine`, qualquer falha
futura nessa função (não só esta) continuará produzindo 500 opacos,
difíceis de diagnosticar sem leitura direta de código-fonte a cada
incidente — como esta própria investigação demonstrou (múltiplas hipóteses
descartadas por falta de mensagem de erro legível).

Ação sugerida, em ordem:
1. Envolver `runCognitiveEngine(content)` em `try/catch` em `chat.ts`,
   devolvendo 500 com a mensagem de erro real — baixo risco, alta
   utilidade para diagnóstico futuro. Aplicar primeiro.
2. Com o erro real visível, investigar `luna-guardian` (Builder tem
   acesso, Engineer não) para achar o parâmetro malformado na consulta de
   memória que retorna 400.
3. Investigar separadamente a causa do painel Git (404) e do Terminal
   (desconexão imediata) — nenhuma hipótese forte ainda, tratar como
   pendências independentes, não assumir mesma causa do chat.
4. Retestar os 3 sintomas restantes (chat, Git, Terminal) depois de cada
   correção — não marcar como resolvido sem reteste real (Regra 6 —
   evidência antes de intervenção).

Status: causa raiz do chat parcialmente confirmada (ponto exato no código
identificado); causa raiz final (por que o Guardian retorna 400) e as
causas do Git/Terminal seguem não confirmadas. Painel de Contexto e
GITHUB_TOKEN — resolvidos e confirmados por reteste real.

## ID: ENG-020
Data: 2026-07-22
Tópico: Sessões repetidamente aplicando correções no repositório errado quando um ADR já portou o código — regra permanente de confirmação

Observação: numa única sessão, duas tarefas separadas (fix de `git-panel`/
Forge, fix de `POST /chat` nunca vazar erro cru de provider) foram
inicialmente direcionadas ao monorepo `luna`, que ainda contém as cópias
pré-porte de ambos (`forge/`, `apps/frontend/artifacts/api-server/`) —
código que compila, tem teste passando e estrutura de pasta idêntica ao
destino real, então não tem nenhum sinal automático de que é código morto.
`forge/README.md` já registrava o porte (ADR de Forge → `luna-frontend`,
"não desenvolva aqui"); o backend não tinha aviso equivalente antes desta
sessão — só o comentário de cabeçalho `// Porte de ... — ADR-012` no
arquivo de destino (`luna-core/src/routes/chat.ts`), nunca uma nota na
origem. Mesma classe de risco já registrada em ENG-004 (Convergia) e
ENG-014 (chat/context) — não é acidente isolado, é padrão recorrente
sempre que um ADR de porte deixa a cópia de origem sem remoção nem aviso.

Risco: qualquer sessão futura que receba uma tarefa descrevendo só um
caminho de arquivo, sem repositório explícito, tende a bater no monorepo
`luna` primeiro (mais antigo, mais familiar, estrutura idêntica ao
destino) e aplicar/testar a correção lá — trabalho real, PR real, tempo
gasto — antes de descobrir que o alvo vivo é outro repositório. Cada
ocorrência é individualmente barata de corrigir (fechar PR, redirecionar),
mas o padrão em si não estava registrado como risco conhecido a checar
antes de começar.

Ação sugerida: antes de escrever código num caminho específico, se o
repositório tiver histórico de porte/consolidação documentado em ADR
(ADR-004, ADR-012, ou futuro equivalente), a sessão deve confirmar o
repositório de destino real antes de prosseguir — mesmo se o caminho
existir e compilar onde já está. Sinal prático: procurar por comentário
"Porte de ..." no topo de arquivos candidatos nos repositórios de destino
conhecidos (`luna-core`, `luna-frontend`) antes de assumir que o monorepo
`luna` é o alvo. Mitigação estrutural complementar (não substitui esta
regra): aviso explícito no `README.md` raiz do monorepo `luna` (aplicado
nesta sessão) e avaliação, pelo Architect, de remover fisicamente as
cópias pré-porte em vez de só sinalizá-las.
Status: regra ativa a partir de 2026-07-22.

## ID: GEN-002
Data: 2026-07-19
Tópico: Workflow multi-agente de Builder (Claude Code → OpenCode → Aider), via GitHub Actions — v2

Status: Proposto — aguardando ratificação do Architect.

Substitui: a especificação original de GEN-002 (entregue mais cedo nesta
sessão) — mesma base (ADR-008: GitHub Actions, acionável sob demanda pelo
Forge, autoatestação com run ID), agora ampliada para múltiplos agentes
de Builder com fallback e atribuição visível, conforme pedido do
Originador.

Contexto: Builder hoje só existe como sessão manual do Claude Code —
Rubens abre aba, cola pacote, acompanha, cola resultado de volta no chat.
Pedido: automatizar essa execução via GitHub Actions (ADR-008 já decidiu
esse caminho), com Claude Code como titular e OpenCode e Aider como
reservas, nessa ordem — se um falhar, tenta o próximo sozinho. Em Modo
Dev, deve existir seleção manual também. Toda execução, automática ou
manual, deve informar visualmente qual ferramenta/modelo respondeu —
logotipo do fornecedor + nome do modelo, mesmo padrão de transparência já
decidido no ADR-016 para o chat.

Decisão de governança (resolve o ponto em aberto antes de especificar o
resto): o `task` executado pelo Action nunca é texto livre. O gatilho do
workflow (via botão no Forge) só pode referenciar um pacote já existente
e commitado (ex.: um arquivo em `pending-packages/` no próprio
repositório, ou um commit/branch específico já revisado) — nunca uma
string arbitrária digitada na hora. Isso preserva a fronteira
Engineer-propõe/Architect-decide/Builder-executa mesmo em modo
automático — sem essa trava, qualquer acesso ao botão do Forge
equivaleria a acesso de escrita irrestrito ao código.

Decisão técnica: cadeia de fallback, em ordem: Claude Code (headless,
`claude -p`, sintaxe exata a confirmar na documentação vigente da
ferramenta no momento da implementação — não travar num flag específico
que pode já ter mudado) → OpenCode → Aider. Cada tentativa roda no mesmo
runner, mesmo `GITHUB_TOKEN` do Action (escopo próprio, independente do
GitHub App instalado — mesma observação já registrada em ADR-008). Se
uma ferramenta falhar (erro de autenticação, rate limit, exit code
não-zero, timeout), o workflow segue para a próxima automaticamente —
sem intervenção humana no meio.

Seleção manual (Modo Dev): o `workflow_dispatch` aceita um input opcional
`agent` (`claude-code` | `opencode` | `aider`). Se vazio, roda a cadeia
de fallback completa; se preenchido, tenta só a ferramenta escolhida
(sem cair pras outras) — é o modo de depuração/teste que o Originador
pediu para preservar, mesmo padrão do campo `provider` já decidido no
ADR-016 para o chat.

Cada ferramenta precisa da própria credencial — `ANTHROPIC_API_KEY`
(Claude Code, já existe), e novas: credencial do OpenCode (modelo a
definir — ele suporta 75+ providers, decisão de qual usar é separada,
sugestão: reaproveitar `GROQ_API_KEY` já configurada, já que Groq é o
único provider realmente testado no ecossistema hoje) e do Aider (mesma
lógica). Não há credencial "genérica" — cada tentativa de fallback só
roda se a credencial dela existir; se faltar, pula direto pra próxima,
mesmo padrão de tolerância a ausência já usado em todo o `luna-core`.

Atualização em `GENESIS/BUILDER.md`: a autoatestação passa a incluir
explicitamente qual ferramenta executou (não mais só "Builder"
genérico) — ex.: `Eu fiz (via OpenCode, Claude Code indisponível — ver
log do run): ...`. Isso alimenta o próximo item.

Atribuição visível no Forge: o painel "Claude Code" existente
(FORGE-MVP-08A, já lê as últimas 5 entradas de `BUILDER.md`) passa a
mostrar, por entrada: logotipo do fornecedor + nome do modelo/ferramenta
que executou — reaproveita o painel que já existe, só adiciona o dado (já
vai estar no texto da autoatestação, é só parsear). Renomear a aba de
"Claude Code" pra algo mais genérico (ex. "Builder") já que agora pode
não ser sempre o Claude Code.

Fora de escopo desta decisão:
- Sintaxe exata de invocação headless de cada ferramenta (Builder
  confirma na documentação vigente de cada uma no momento de
  implementar — este documento não trava versão/flag específico, que
  muda com frequência).
- Qual provider de modelo o OpenCode/Aider usam por padrão — decisão
  separada, mais barata de adiar (pode nascer só com Claude Code + 1
  reserva, adicionar a segunda depois).
- Onde exatamente vive `pending-packages/` e o mecanismo de aprovação
  antes do commit desse pacote — reaproveita o mesmo fluxo Engineer→
  Architect que já existe (colar aqui no chat, eu preparo, você aprova),
  só muda o que acontece depois da aprovação.

Next action: Ratificação do Architect antes de qualquer implementação —
esta é uma decisão de arquitetura real (governança de execução
automática), não só UI. Depois de ratificado, Builder implementa em
fases: (1) Claude Code sozinho, headless, sem fallback ainda — prova o
caminho básico; (2) adiciona OpenCode como reserva; (3) adiciona Aider;
(4) atualiza o painel do Forge pra mostrar atribuição visual.
