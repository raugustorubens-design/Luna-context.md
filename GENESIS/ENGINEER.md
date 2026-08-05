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

Atualização (2026-07-22): ao portar `luna` PR #15 (capability packs
Supabase/Railway/Reporter do Gateway) para `luna-core`, o `SupabaseRestAdapter`
original (`query`/`insert`/`update`/`delete`/`rpc`/`uploadFile`/`downloadFile`)
foi portado como código de referência para dentro do `SupabaseHubConnector`
já existente no Connector Hub (`luna-core`
`src/connector_hub/adapters/supabase-connector.ts`) — não como capability do
Gateway. As 7 operações continuam sem consumidor no Gateway, no mesmo
status "bloqueado" que `query`/`insert` já tinham; nenhuma linha de código
nova viola o Princípio 4. `uploadFile`/`downloadFile` foram avaliadas
especificamente (são Supabase Storage, não linha de tabela relacional) e
mantidas bloqueadas também: o Princípio 4 diz "toda persistência", sem
qualificar como só-relacional, então persistência de arquivo em object
storage cai na mesma regra. Isto não é o redesenho de STOR-001 — é só
código de referência pronto, esperando a decisão do Architect. Ver PR
correspondente em `luna-core` para o diff completo.

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

Atualização (2026-07-22): mais uma ocorrência do mesmo padrão encontrada e
corrigida — `luna` PR #20 mergeou um documento de GENESIS (ADR-014,
Sistema Sensorial Fluxo A) direto em `docs/architecture/` do monorepo,
violando o Princípio 8 da Constitution (documentação de GENESIS centralizada
em `Luna-context.md`) e colidindo de número com o ADR-014 já existente aqui
(Arquitetura Imunológica de Segurança Cognitiva, Aceito 2026-07-20). Corrigido:
conteúdo movido para `Luna-context.md` como `ADR-016-Sistema-Sensorial-Fluxo-A.md`
(Status atualizado para Aceito, ratificado pelo Architect em 2026-07-19), e a
cópia em `luna` removida fisicamente (não só marcada como superada) — mesmo
raciocínio já aplicado a `forge/`/`apps/frontend/artifacts/api-server`.

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

## ID: ENG-026
Data: 2026-07-22
Tópico: Plano de investigação — continuidade de contexto entre agentes e alucinação (ligado a ENG-025)

Observação: proposta do Architect, quatro direções possíveis para reduzir
alucinação de agentes sobre o próprio estado do projeto: (1) regra
constitucional de grounding obrigatório (citar fonte ou admitir
desconhecimento); (2) separar fato/inferência também na saída
conversacional, não só na gravação de memória; (3) checkpoint de
reconsulta ao Reporter/GitHub antes de decisão de peso; (4) Guardian como
filtro de saída, não só de entrada.

Avaliação do Engineer: não desenhar regra ainda — testar primeiro onde a
falha real está, ligado ao caso concreto do ENG-025 (Claude/GPT
alucinando sobre "o que é o Forge"). Duas causas possíveis, que pedem
correção diferente: (a) `GENESIS/FORGE.md` nunca foi consolidado na
memória do Guardian — problema de retrieval, nenhuma regra de citação
resolve; (b) o documento existe na memória, mas o agente não usou —
nesse caso as direções 2 e 3 se aplicam.

Nota: a direção 4 (Guardian como filtro de saída) já tem equivalente
especificado — é o "Reasoning Integrity" do ADR-014, Parte III (Reporter
compara resposta nova a precedentes, sinaliza divergência sem bloquear).
Não é capacidade nova, é extensão de algo já decidido — mesmo padrão de
duplicação já visto antes (ver ADR-014, não ADR-016 — correção aplicada
nesta persistência: o registro original recebido citava "ADR-016" para o
conteúdo de "Quarentena Cognitiva", mas ADR-016 real neste repositório é
Sistema Sensorial/Fluxo A e não menciona quarentena em lugar nenhum;
"Quarentena Cognitiva" é ADR-014, Parte V/VII. Sinalizando a correção
explicitamente em vez de persistir a citação errada — é exatamente o
tipo de erro de referência que este próprio item, ENG-026, existe para
investigar).

Ação sugerida: primeiro passo é investigação (não implementação) — checar
se `GENESIS/FORGE.md` e documentos GENESIS equivalentes já foram
consolidados no Guardian alguma vez, ou se o Hipocampo nunca teve esse
conteúdo pra reconstruir. Resultado dessa investigação decide qual das 4
direções (ou combinação) faz sentido especificar formalmente depois.
Status: avaliado, investigação ainda não iniciada.

## ID: ENG-027
Data: 2026-07-22
Tópico: Merge de PR sempre exige confirmação explícita — decisão do Architect, não depender de auto-merge

Observação: investigada a causa da inconsistência observada (algumas PRs
mergeadas sem instrução explícita, outras esperando "tira de draft e
mergeia"). Confirmado, via documentação oficial do Claude Code: o
auto-merge só age "assim que todas as verificações (CI) passarem" — e
praticamente nenhum repositório do ecossistema LUNA tem CI configurado
hoje, o que torna esse comportamento ambíguo na prática. Também
confirmado: existe caso documentado publicamente de Claude Code
mergeando PR em produção sem aprovação humana, tratado pela própria
Anthropic como risco de segurança.

Decisão do Architect: **não perseguir auto-merge agora.** Mantém-se o
padrão manual já usado com sucesso a noite toda — toda PR fica em draft,
Engineer confirma o conteúdo real (contra o GitHub, não só o relato da
sessão), e só depois disso alguém (Architect ou instrução explícita do
Engineer) manda mergear. Nenhuma configuração de CI é necessária para
viabilizar isso — é justamente o oposto: evitar depender de um mecanismo
automático que já provou side-effects reais e documentados.
Status: decidido — merge sempre com confirmação explícita, sem
auto-merge. Não é mais pendência aberta.

Atualização (2026-08-04, correção não silenciosa — mesmo padrão já
usado em ENG-031): a premissa "praticamente nenhum repositório do
ecossistema LUNA tem CI configurado hoje" estava certa para a data em
que foi escrita, não é mais verdade agora. `luna-core` e
`luna-frontend` ganharam `.github/workflows/ci.yml` (typecheck +
testes + check específico de cada repo — `test:architecture` em
`luna-core`, `test:constitution` em `luna-frontend`), com branch
protection ativa em `main` nos dois repositórios (status check `test`
obrigatório, PR obrigatório, branch atualizada obrigatória antes de
merge). A decisão em si não muda: merge continua sempre com
confirmação explícita, sem auto-merge — CI configurado não altera quem
aperta o botão de merge, só adiciona um gate técnico obrigatório antes
disso ser possível. Não é o mesmo mecanismo que o texto original
descartou (auto-merge do Claude Code por CI verde); branch protection
com status check obrigatório é pré-condição pro merge manual continuar
seguro, não substituição dele.

## ID: ENG-028
Data: 2026-07-23
Tópico: Capacidade de visão registrada (CONV-009) — nada implementado ainda

*Nota de numeração:* pedido original desta entrada citava `ENG-033`; o
último ID real usado em `GENESIS/*.md` é `ENG-027` — segue como
`ENG-028`, sequência real, não a assumida.

Observação: Architect precisa de interpretação de fotos para a
auditoria real que vai conduzir, junto de `CONV-007`
(relatório/checklist) e `CONV-008` (acompanhamento ao vivo) —
**nenhum dos dois existe como ID rastreado em `GENESIS/ROADMAP.md` hoje**
(só `CONV-001` a `CONV-006`, ver `GENESIS/STATUS.md` ENG-021); citados
aqui como contexto de intenção do Architect, não como itens já
registrados. Investigação confirmou: nenhum adaptador do luna-core
processa imagem hoje — nem Groq, nem o AnthropicHubConnector (só texto,
apesar da API real da Anthropic suportar imagem). Não é ligação de algo
existente, é capacidade nova.

Decisão de escopo: leitura de foto pela IA nasce `unverified`, não
`corroborated` — a foto é evidência real, mas a interpretação da IA
sobre ela ainda pode alucinar, mesma disciplina já aplicada a texto no
ADR-014 Emenda 1. Só o Originador confirmando promove a leitura pra
confiança alta.
Status: registrado (`CONV-009`, `GENESIS/ROADMAP.md` P4), não
especificado em detalhe, não iniciado.

### Ordem de prioridade sugerida (dado o contexto da auditoria real)

1. `CONV-001` a `CONV-004` (template/editor/preview/lote) — destrava um
   eventual `CONV-007`, se e quando for registrado como ID real
2. `CONV-007` (relatório/checklist de auditoria) — ainda não registrado
   como ID neste roadmap, ver nota acima
3. `CONV-009` (interpretação de fotos) — pode já ser útil mesmo antes
   de um eventual `CONV-008` estar pronto (fotos soltas anexadas a um
   relatório já ajudam, sem precisar do acompanhamento ao vivo completo)
4. `CONV-008` (acompanhamento ao vivo) — ainda não registrado como ID
   neste roadmap; o mais complexo dos quatro, precisa de especificação
   própria de interface

Nenhuma implementação nesta rodada — registro apenas. Architect decide
quando priorizar `CONV-001`/`CONV-009` dado o prazo real da auditoria,
e se `CONV-007`/`CONV-008` devem virar IDs rastreados formalmente.

## ID: ENG-029
Data: 2026-07-30
Tópico: Dependência compartilhada "leitura e posicionamento de imagem em PPTX" — distinta de CONV-009

Achado, antes de qualquer implementação: o pacote "Convergia — Capacidades
de Geração e Ingestão" (Capacidade 1, mala direta/relatório agregado;
Capacidade 2, ingestão pra memória da Luna) cita como dependência
compartilhada das duas "leitura e posicionamento de imagem — não existe
hoje em nenhum parser/renderer do Convergia" — confirmado por auditoria
direta do código antes de aceitar a premissa: `pptx-parser.ts` só lia
`<a:t>` (texto), `pptx-renderer.ts` só escreve tabela, nenhum dos dois
tocava imagem.

**Distinção que o pacote original não fazia e que precisa ficar registrada:**
essa dependência **não é `CONV-009`**. `CONV-009` (acima, nesta mesma
seção) é interpretação semântica de foto via LLM — o modelo olha a imagem
e descreve o que vê (equipamento, ambiente, NC), com proveniência
`unverified`→`corroborated`. A dependência compartilhada da Capacidade
1/2 é mecânica: extrair posição/dimensão/bytes de uma imagem já presente
num `.pptx` (parser) e escrever imagem posicionada num template
renderizado (renderer) — geometria, não semântica. `CONV-009` não
desbloqueia nenhuma das duas capacidades; são capacidades independentes
que só coincidem em usar "imagem" como palavra.

O que mudou no Canonical Model (`luna-core`, `src/convergia/contracts.ts`):
`CanonicalRecord` ganhou um campo opcional `images?: CanonicalImage[]`
(nome, mimeType, bytes brutos, posição em EMU — mesma unidade que o XML
do PPTX já usa em `<a:off>`/`<a:ext>`, sem conversão pra polegada/pixel
aqui, decisão de renderer). Aditivo: `CanonicalField.value` continua
escalar (string/number/boolean/null), então validação/transforms/
renderers existentes (xlsx/csv/json/html) não precisaram mudar.

O que foi implementado (só a metade de leitura): `pptx-parser.ts` agora
extrai imagens por slide — lê blocos `<p:pic>`, resolve `r:embed` via
`ppt/slides/_rels/slideN.xml.rels`, lê os bytes reais de `ppt/media/`.
Testado com fixture PNG real (assinatura de bytes conferida, não só
tamanho > 0) e com EMU de posição/tamanho calculados a partir de valores
conhecidos em polegadas.

O que NÃO foi implementado, deliberadamente fora desta rodada: escrever/
posicionar imagem em `pptx-renderer.ts` (metade de saída da mesma
dependência — necessária pra Capacidade 1 gerar o documento final com
foto/assinatura no lugar certo do template) e qualquer trabalho de
Capacidade 1 (CONV-001 a CONV-004, editor de posicionamento no Forge) ou
Capacidade 2 (fila assíncrona, quarentena no Supabase Storage, escolha de
retenção). Isso é a peça mínima que desbloqueia as duas, não as duas
capacidades em si.

Status: parser implementado e testado (`luna-core`, PR #24, branch
`claude/convergia-generation-ingestion-250w1z`); renderer e as duas
capacidades completas seguem não iniciados.

## ID: ENG-030
Data: 2026-07-30
Tópico: Metade de escrita da dependência de imagem (ENG-029) + motor de normalização/correspondência — três bloqueios reais registrados, não contornados

Eu fiz (código já mergeado antes desta entrada, `luna-core` PR #25,
commit `60aa158` em `main`): completei a metade de escrita da
dependência compartilhada registrada em ENG-029 —
`pptx-renderer.ts` agora posiciona qualquer `CanonicalImage` presente
num registro, na posição EMU original convertida pra polegada, usando
`sizing: { type: "contain" }` do `pptxgenjs` — nunca corta, sempre
encolhe pra caber na caixa. Essa é a regra de negócio que o Architect
definiu para campo do tipo imagem no editor de posicionamento (CONV-002)
— apliquei na primitiva de renderização em si, não só na UI que ainda
não existe, porque a primitiva é reutilizável por qualquer capacidade
que precise posicionar imagem (Capacidade 1 e 2 ambas).

Também implementei `src/convergia/matching/`: `identifier.ts`
(`normalizeIdentifier` — zero-pad a 6 dígitos, sempre, sem exceção por
quantidade de dígitos faltando, exatamente como especificado) e
`record-file-matcher.ts` (`matchFilesToRecords`), que aplica as duas
regras de negócio do Architect para o lote de arquivos soltos: chave
sem arquivo correspondente → `status: "missing"`, nunca trava o resto
do lote; chave com mais de um arquivo → `status: "ambiguous"`, nunca
decide sozinho, exige resolução explícita do usuário. Nenhuma rota
HTTP chama isso ainda — é utilitário de apoio, testado isoladamente
(12 testes novos, 270/270 no total).

**Três bloqueios reais, sinalizados em vez de contornados (Regra 6):**

1. **CONV-001 (upload de template) não é falta de parsing.** O parser
   já devolve texto + posição/bytes de imagem via `/convergia/parse`
   — tecnicamente já é "leitura de template". O que falta é decisão de
   arquitetura: um template enviado persiste em algum lugar entre a
   inspeção (usuário vê os campos) e a geração em lote (dias depois,
   talvez), ou o cliente reenvia os bytes do template a cada chamada
   (stateless, mesmo padrão que o resto do Convergia já usa,
   sem introduzir camada de persistência nova)? Não decidi sozinho —
   é exatamente o tipo de escolha que muda o formato de storage/sessão
   do resto da Capacidade 1.

2. **CONV-002 (editor de "bolha" no Forge) é frontend, fora do
   repositório desta sessão.** Vive em `luna-frontend`, não anexado
   nesta sessão de trabalho (só `luna-core` e `Luna-context.md`
   estavam no escopo). Não implementei nem posso implementar sem esse
   repositório ser anexado explicitamente.

3. **CONV-003 (preview) depende dos dois itens acima existirem** — não
   é bloqueio próprio, é bloqueio derivado.

Também não avancei a Matriz de Treinamento (formato de armazenamento
segue "não decidido", pergunta em aberto do pacote original, não
resolvida em nenhuma instrução recebida até agora) nem a Capacidade 2
(fila assíncrona Supabase vs. Railway e a mudança de forma
síncrono→streaming, ambos riscos já sinalizados em rodada anterior,
seguem sem decisão).

Test status: `luna-core` — `npm run typecheck` limpo, `npm run
test:architecture` aprovado, `npm test` 270/270 (258 pré-existentes +
12 novos: posicionamento de imagem no renderer, normalização de
identificador, correspondência arquivo↔linha incluindo os casos
`missing`/`ambiguous`/nome de arquivo sem dígito).

O que está bloqueado: os três itens acima — decisão de persistência de
template (CONV-001), anexação de `luna-frontend` a uma sessão futura
(CONV-002), formato de storage da Matriz de Treinamento, decisão de
infra de fila para Capacidade 2.

Next action: Architect decide persistência de template (CONV-001) e
formato da Matriz de Treinamento antes de qualquer código novo nessas
frentes; anexar `luna-frontend` numa sessão futura para CONV-002;
decidir fila (Supabase table vs. serviço Railway) antes de iniciar
Capacidade 2.

## ID: ENG-031
Data: 2026-07-30
Tópico: Correção de ENG-030 — bloqueio de persistência de template já resolvido, em paralelo, mesma branch

Achado, ao sincronizar a branch local após o merge do PR #25: o commit
mergeado (`60aa158`) tem 3 commits, não 2 — os 2 que eu escrevi nesta
sessão (renderer + matching, ver ENG-030) mais um terceiro, de uma
**sessão diferente do Claude Code** (`Claude-Session:
.../session_014gEcpV5efitgXmZKXuACAx`, não a desta entrada), empurrado
pra mesma branch antes do Rubens marcar o PR como pronto e mergear.
Esse terceiro commit implementa `GET`/`PUT
/convergia/templates/:id/positions` (`routes/convergia.ts`) e
`TemplatePositionStore` (`convergia/templates/position-store.ts`) —
exatamente o primeiro dos três bloqueios que ENG-030 (minutos antes)
tinha registrado como "decisão de arquitetura não tomada".

**Correção, não silenciosa (Princípio 8):** ENG-030 estava certo sobre
o estado do código no momento em que foi escrito — não fabriquei o
bloqueio, era real até aquele commit acontecer. A questão em si já
tinha resposta conhecida no próprio repositório: o padrão de coleção
genérica do `GuardianContract` (mesmo caminho já usado por
`luna/memory-engine.ts`) — persistência de posição de template não
precisava de decisão de arquitetura nova, só de aplicar um padrão já
existente. A outra sessão aplicou; eu não tinha visto essa saída antes
de escrever ENG-030, porque a sessão paralela ainda não tinha
empurrado o commit quando registrei.

Conferido nesta sessão, código real (não só a mensagem do commit):
`position-store.ts` usa `HttpGuardianClient`/`GuardianContract`,
coleção `convergia_template_positions`, validação de shape antes de
salvar (`TemplatePositionValidationError`, capturado no error handler
de `routes/convergia.ts`, 404 se o template não existe). `npm run
typecheck` limpo, `npm run test:architecture` aprovado, `npm test`
278/278 (270 anteriores + 8 novos da própria sessão paralela).

**O que não verifiquei, e não devo apresentar como confirmado:** a
mensagem do commit cita `luna-frontend` PR #9
(`convergia-position-editor.tsx`) como o consumidor desse endpoint —
`luna-frontend` não está no escopo desta sessão, não anexei o
repositório, não li o PR #9 diretamente. Trato essa parte como não
verificada, não como fato.

Escopo que continua real, não resolvido por este achado: CONV-001 em
si (upload do arquivo de template, não só a posição dos campos que já
tem endpoint) segue sem implementação; CONV-003/CONV-004 continuam
bloqueados por isso; Matriz de Treinamento e Capacidade 2 (fila,
streaming) seguem exatamente como ENG-030 registrou, nenhuma novidade
sobre eles.

Status: `ROADMAP.md` corrigido nesta mesma rodada (CONV-002 backend
marcado `[x]`, nota de correção em CONV-001, CONV-003/004 com bloqueio
atualizado).

## ID: ENG-032
Data: 2026-07-31
Tópico: Verificação e merge de `luna-frontend` PR #9 — fecha a ressalva "não verificado" de ENG-031

Eu fiz (sessão com os três repositórios anexados —
`luna-core`/`luna-frontend`/`Luna-context.md`, o que ENG-030/ENG-031
não tinham): li o PR #9 (`luna-frontend`) inteiro — descrição, diff
completo — e o código real de `lib/forge/api-client.ts` e
`components/forge/convergia-position-editor.tsx` antes de mexer em
qualquer coisa. Confirmei que `fetchConvergiaTemplatePositions`/
`saveConvergiaTemplatePositions` já apontavam para o contrato exato
que a rota nova de `luna-core` (PR #25) devolve (`{ positions: [...] }`
em GET e PUT) — nenhuma mudança de código foi necessária no
front-end. Rodei `npm run typecheck` (limpo), `npm run
test:constitution` (46 arquivos, aprovado) e `npm test` (24/24) antes
de considerar o PR pronto.

Também identifiquei, comparando os dois repositórios lado a lado, que
o editor de posicionamento não depende de CONV-001 (upload) para
funcionar — ele opera sobre `TemplateDescriptor.variables` de
qualquer template já registrado no catálogo (`GET
/convergia/templates`), não sobre um arquivo enviado. Isso não muda o
que falta (CONV-001 continua sem implementação), mas corrige uma
suposição implícita que eu tinha antes de ler o código: CONV-002 não
estava "bloqueado" por CONV-001 no sentido de não poder rodar sem ele
— só a experiência completa (posicionar sobre um template visual real)
é que depende disso.

Mergeei os dois PRs em `main`, nesta ordem: `luna-core` PR #25
primeiro (`60aa158`), `luna-frontend` PR #9 depois (`7e5c230`) — ordem
lógica, já que o front-end depende do endpoint existir. Depois de
confirmar os dois merges, sincronizei esta branch de documentação com
o que uma sessão paralela já tinha empurrado direto pra `main`
(ENG-030/ENG-031, mesmo achado de bloqueio) para não duplicar
conteúdo — esta entrada só acrescenta o que aquela sessão não tinha
(acesso a `luna-frontend`), não repete o que já está registrado lá.

Test status: `luna-frontend` — `npm run typecheck` limpo, `npm run
test:constitution` aprovado (46 arquivos), `npm test` 24/24. `luna-core`
— reconferido nesta sessão também, mesmo resultado de ENG-031 (278/278,
typecheck e `test:architecture` limpos). `npm run lint` não rodou em
nenhum dos dois repositórios (setup interativo do ESLint, mesmo motivo
já registrado no PR #9 original). Nenhum CI configurado em `luna-core`
para PRs (`get_check_runs` vazio); Vercel do `luna-frontend` passou
antes do merge.

O que está bloqueado: CONV-001 (upload de template visual) segue sem
implementação — nada nesta rodada avançou isso. Sem visibilidade sobre
`luna-api` (fora do escopo desta sessão) para confirmar se a coleção
`convergia_template_positions` já existe do lado do Guardian real em
produção — a chamada via `HttpGuardianClient` está correta e testada
com fake da interface, mas o comportamento contra o Guardian real não
foi verificado. Teste manual no browser (arrastar/redimensionar bolha)
não foi executado.

Next action: nenhuma minha até o Originador revisar os merges e esta
documentação. Se o Guardian real não tiver a coleção provisionada, o
próximo passo é abrir isso em `luna-api`, fora do escopo dos três
repositórios desta sessão.

## ID: ENG-033
Data: 2026-08-02
Tópico: React error #418 (hidratação) — achado ao vivo no Forge, `luna-frontend`

Observação: durante o teste manual de UI de CONV-002 (posicionamento
de campos, template `documento_tabular_generico_csv`, 2026-08-02), o
Originador abriu o DevTools do navegador em
`https://luna-frontend-production-ffcc.up.railway.app/forge` e
capturou o seguinte no Console (texto verbatim, não editado):

```
Unchecked runtime.lastError: The message port closed before
a response was received.
    forge:1
```

```
Uncaught Error: Minified React error #418; visit
https://react.dev/errors/418?args[]=HTML&args[]= for the
full message or use the non-minified dev environment for full errors
and additional helpful warnings.
    at rD (8e74727f-4e3abe8ce9d63ec1.js:1:35060)
    at oq (8e74727f-4e3abe8ce9d63ec1.js:1:85082)
    at ik (8e74727f-4e3abe8ce9d63ec1.js:1:114680)
    at 8e74727f-4e3abe8ce9d63ec1.js:1:110728
    at iu (8e74727f-4e3abe8ce9d63ec1.js:1:110829)
    at iX (8e74727f-4e3abe8ce9d63ec1.js:1:132932)
    at MessagePort.w (675-a9a39ee12f945b7d.js:1:61400)
```

```
Failed to load resource: the server responded with a status of 400 ()
    uvicorn-main-production...(truncado na captura)/api/gateway/execute:1
```

DevTools reportava "8 Issues" no total nessa sessão de página — só os
3 acima foram capturados na tela, os demais não estão documentados.

Classificação, já feita:
- `runtime.lastError` → artefato de extensão do Chrome, não é bug do
  projeto, só citado para registro completo do que apareceu.
- `/api/gateway/execute → 400` → não é achado novo, é o bug já
  conhecido do Guardian Memory Index (`searchGuardianMemoryIndex`,
  painel de Contexto do Forge) — não usa o mesmo caminho do `PUT` de
  posições, que é `fetch` direto. Não misturar com CONV-002.
- React error #418 é o único item realmente novo desta observação.

Risco: desconhecido — erro de hidratação pode ser cosmético (React
recupera sozinho) ou sintoma de um problema real de SSR/CSR mismatch
em `luna-frontend`. Sem investigação ainda, não dá pra dizer qual.

Ação sugerida: sessão futura, com `luna-frontend` anexado, para
localizar o componente que causa o mismatch de hidratação e decidir
severidade.

Status: observado, não investigado, não corrigido.

## ID: ENG-034
Data: 2026-08-04
Tópico: `luna-core` PR #23 mergeado — 3 bugs reais de produção corrigidos (zeragem de memória, PPTX/PPTM rejeitado na validação, planilha mesclada corrompendo dado)

Observação: PR #23, aberto em 2026-07-27 e retomado/rebaseado em
2026-08-04 (ver `luna-core` `BUILDER.md`, entradas "2026-07-27 —
Pacote de 5 consertos do Convergia" e "2026-08-04 — Rebase do PR #23
sobre `main`..."), mergeado em `main` (commit de merge `ee57fb6`).
Corrige três bugs reais de produção, não hipotéticos:

1. **Zeragem de memória (incidente de produção, 2026-07-26)** — 10
   registros de memória virando 0 mantidos quando um único registro
   não cabia no orçamento de caracteres restante do payload.
   `shrinkMemoryToFit` (`src/luna/adapters/memory-payload.ts`) agora
   encolhe o `conteudo` do registro que não cabe, em vez de descartar
   o registro inteiro (e o loop, via `break` antes de qualquer `push`)
   quando isso acontece.
2. **PPTX/PPTM rejeitado na etapa de Validação, mesmo com parsing
   perfeito** — `validateCanonicalDocument` rejeitava
   `sourceFormat: "pptx"`/`"pptm"` por essas strings não estarem no
   `z.enum` de `validation.ts` — bug de drift entre parser e
   validador, não do parser em si.
3. **Planilha XLSX com célula mesclada corrompendo dado
   silenciosamente** — antes, uma planilha com células mescladas
   virava um documento com colunas erradas ou vazias, sem nenhum
   erro visível. `xlsx-parser.ts` agora checa
   `worksheet.model.merges` logo após abrir a planilha e lança um
   erro claro em vez de seguir.

Testado, não só implementado — resumo (ver `luna-core` `BUILDER.md`
para o relato sessão a sessão completo, incluindo o rebase sobre
`main` que essa branch precisou por ter ficado parada enquanto CONV-002
e o CI avançavam): `npm run typecheck` limpo, `npm run test:architecture`
passou, `npm test` **286/286** (285 pass + 1 skip pré-existente,
LibreOffice, não relacionado a este PR). Verificação com arquivo real
— pendência da versão original do PR, fechada nesta rodada: `.pptm`
sintético e planilha com célula mesclada sintética, gerados por
script (não documentos reais de produção, mas exercitam os formatos
de verdade). Contra produção (`uvicorn-main-production`), antes do
merge: os dois bugs ainda ativos, confirmando que a correção era de
fato necessária. Contra um `luna-core` local rodando o código já
rebaseado: `.pptm` parseado corretamente, planilha mesclada rejeitada
com erro claro — exatamente o comportamento que o PR promete.

Achado colateral, registrado mas não corrigido (fora do escopo desta
entrega): um `.pptm` parseado localmente reporta
`metadata.sourceFormat: "pptx"`, não `"pptm"` — `PptxParser.parse()`
grava esse valor de forma hardcoded, independente de qual chave do
registry levou até ele. Consequência direta do desenho "mesmo OOXML,
reaproveita a mesma instância" que o próprio PR já documenta, não um
problema introduzido pelo rebase.

Status: mergeado em `main`, testado (typecheck limpo,
`test:architecture` passou, 286/286 testes, verificação com arquivo
sintético real contra servidor local). Não verificado diretamente
contra produção pós-deploy nesta sessão — ver `BUILDER.md` para a
distinção exata entre o que foi confirmado contra produção (bug ainda
ativo, antes do merge) e o que foi confirmado só localmente (a
correção em si).

## ID: ENG-035
Data: 2026-08-05
Tópico: ADR-021 registrado (Convergia Mobile — Ronda Fotográfica), reconciliado com `convergia-spec-tecnica-consolidada.md`, `luna-tabela-risco-iso-outcome.md` e o relatório real da Manserv

Decisão: coleta de ronda fotográfica ganha superfície própria, mobile,
fora do Forge — PWA (não app nativo), service worker + fila offline em
IndexedDB, reenvio automático ao detectar rede. Foto nunca é obrigatória
para avançar — cada categoria de risco tem um seletor de estado explícito
(não avaliado / risco identificado / risco considerado e inexistente),
crítica de usabilidade sobre a ferramenta real da Manserv, que trava o
usuário pedindo imagem mesmo quando não há nada a fotografar. Gravidade de não
conformidade deixa de ser um número solto: passa a usar o mesmo motor de
Probabilidade+Gravidade=Resultado (nomenclatura ISO/IEC 42001/23894) já
desenhado para o `outcome` (`O`) do Signal Engine (ADR-019),
parametrizado por domínio em vez de duplicado. A leitura de foto (Decisão
6) é diagnóstica, não descritiva — interpreta a implicação de risco da
cena à luz do procedimento já ingerido no Hipocampo, não descreve o que
aparece. Correção de caminho técnico relevante: CONV-009 (interpretação
de foto) deixa de propor estender `AnthropicHubConnector` — usa **Qwen-VL
via Groq**, provider já configurado, evitando dependência de imagem via
Anthropic.

Aprendizado de longo prazo (`memoria_luna`) nunca guarda nome de pessoa,
em nenhuma forma; guarda departamento/local/cliente tokenizados (código
estável, ex. `CLI-042`), com tabela de mapeamento código→nome cujo acesso
começa restrito só ao Architect. Achado do tipo EPI/comportamental
(envolve pessoa) segue disciplina de dado sensível mais estrita que
achado Estrutural (sem pessoa na cena) — nunca entra com identificação de
pessoa, mesmo tokenizado. Referência de dado real encontrada nesta
sessão: relatório de campo real da Manserv (SSMA, NR-16, Sylvamo/Mogi
Guaçu) — usado só como fonte de taxonomia de risco (7 categorias) e
estilo de texto diagnóstico para a leitura de imagem; o layout visual do
relatório final continua sendo o já validado no protótipo do ADR-020, não
o da Manserv.

Fases do ADR-021 registradas como itens próprios em `GENESIS/ROADMAP.md`
P4 (`CONV-013` a `CONV-017`), depois de confirmar que `CONV-009` a
`CONV-011` eram os últimos IDs realmente em uso — nenhum ID assumido sem
checar. `CONV-012` (pipeline assíncrono de ingestão de documento grande
no Hipocampo) registrado como item próprio também, por já ser referenciado
como bloqueio explícito da Fase 4 (`CONV-016`) dentro do próprio ADR.

Ver ADR-021 completo (`ADR/ADR-021-convergia-mobile-ronda-fotografica.md`)
para as 8 decisões e a tabela de fases.

Status: registrado, aguardando ratificação final do Architect — nenhuma
implementação de código nesta entrada (ver Etapa 2 do plano de ação,
tratada em `luna-core` separadamente, PR próprio).
