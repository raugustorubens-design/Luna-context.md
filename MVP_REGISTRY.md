# MVP Registry — LUNA Forge

Formato: 5 Porquês, por MVP (não por sistema). Complementa `ECOSYSTEM_ARCHITECTURE.md`
(Entregável 1, por sistema) e `GENESIS/ROADMAP.md` (P1–P6, por prioridade de execução).
Este documento não substitui nenhum dos dois — cruza a informação por MVP para
decisões pontuais como a do Chat abaixo.

## Princípio consolidado — LUNA é multi-interface desde já

**Decisão (2026-07-16, Rubens, decisão solo como proprietário/responsável legal de
LUNA, GitHub, Railway e conexões — não requer ratificação do sócio arquiteto):**
LUNA roda em múltiplas interfaces (web, mobile, CLI, IDE, etc.) desde já, não como
visão de longo prazo. `luna-frontend` é **um cliente de referência**, não **o**
frontend oficial exclusivo.

Consistente com Constituição (Princípio 1 — órgãos, não tecnologias; Princípio 6 —
infraestrutura é substituível; Princípio 7 — órgãos têm identidade conceitual
permanente), então registrado aqui como consolidação, não como ADR.

**Implicação prática para os MVPs abaixo:** cada MVP separa **Capability**
(interface-agnóstica, vive no Gateway/Cognitive Engine, é o que deve ser testado e
versionado) de **Cliente de referência** (a primeira UI a consumir a capability —
hoje `luna-frontend`, mas não a única prevista). Specs para o Builder devem
implementar a capability de forma que qualquer cliente possa chamá-la, com o
cliente de referência como a primeira prova de uso, não como o destino definitivo.

---

## MVP: Git

**Função:** operações Git (branches, commits, PRs) expostas como capability do organismo.
**Capability:** `luna-core` (Gateway, capabilities GitHub já portadas em ADR-004) — interface-agnóstica.
**Cliente de referência:** `luna-frontend` (UI do Forge) — primeiro consumidor, não o único previsto.

**Cadeia de Porquês:**
1. Por que este MVP não está pronto? → Falta a UI que consome as capabilities de GitHub do Gateway.
2. Por que a UI não foi construída? → Porque o Forge como um todo nunca fechou nenhum MVP.
3. Por que o Forge nunca fechou um MVP? → Porque os ciclos anteriores priorizaram consolidar o backend (Gateway, Connector Hub, ADR-004).
4. Por que o backend foi priorizado antes? → Porque sem Gateway estável não havia API real para uma UI consumir.
5. Por que isso deixou de ser verdade agora? → Porque as 17 capabilities do Gateway já estão confirmadas em produção, incluindo o pacote GitHub — a dependência técnica já foi resolvida.

**O que falta:** construir a UI. Nenhuma dependência de backend pendente.
**Status:** liberado para o Builder — sem bloqueio.

---

## MVP: Editor

**Função:** edição de arquivos, exposta como capability do organismo.
**Capability:** `luna-core` (Filesystem capability do Gateway) — interface-agnóstica.
**Cliente de referência:** `luna-frontend` (UI do Forge) — primeiro consumidor, não o único previsto.

**Cadeia de Porquês:**
1. Por que não está pronto? → Falta o componente de edição em si.
2. Por que só falta o componente? → Porque a capability de Filesystem já existe no Gateway desde antes do ADR-004.
3. Por que a capability existe mas nada foi construído em cima? → Porque foi implementada como parte do pacote geral do Gateway, não como resposta a uma demanda específica do Forge.
4. Por que não houve demanda específica? → Porque o Forge nunca teve um dono de produto cobrando esse MVP.
5. Por que isso importa agora? → Porque, diferente do Git e do Chat, aqui não há nem decisão pendente nem bloqueio técnico — só falta alguém pegar a tarefa.

**O que falta:** implementação direta, sem pré-requisito de decisão.
**Status:** liberado para o Builder — sem bloqueio.

---

## MVP: Chat

**Função:** conversa ligada ao Cognitive Engine (Hipocampo/Memory Engine), exposta como capability do organismo.
**Capability atual:** serviço hospedado no ambiente Railway anteriormente referido como
"luna-guardian" (nome em transição — ver nota abaixo) — ainda não migrada para `/api/chat`
do Cognitive Engine.
**Cliente de referência:** `luna-frontend` (UI do Forge) — primeiro consumidor, não o único previsto.

**Distinção importante antes da cadeia de Porquês:**
Esse serviço hospeda duas coisas diferentes, e é fácil confundi-las:
- **O órgão Guardian** (Princípio 4 da Constituição, DA-001) — ativo, sólido, capability `guardian.memory_index_search` confirmada via `GuardianOrganAdapter`. **Não é candidato a nada.**
- **Os endpoints `/chat` e `/context`** — parte experimental do mesmo serviço, com contrato incompatível (`/chat`) ou ausente (`/context`), já confirmada pelo dono do produto como candidata à descontinuação.

O Forge, hoje, depende especificamente da segunda parte, não do órgão Guardian em si.

**Cadeia de Porquês:**
1. Por que este MVP não está pronto? → O Forge chama um endpoint de chat com contrato incompatível.
2. Por que ainda chama esse endpoint? → Porque `lib/forge/api-client.ts` nunca foi redirecionado para o `/api/chat` do Cognitive Engine — só as chamadas de Gateway foram migradas no ADR-004.
3. Por que chat/contexto ficaram fora do escopo do ADR-004? → Porque o ADR-004 tratou explicitamente da migração Gateway/runtime; chat foi citado como fora de escopo.
4. Por que continua apontando para a parte experimental? → Porque a decisão de redirecionamento ficou registrada como "próximo passo em aberto" e não voltou à mesa até esta sessão.
5. Por que isso é relevante agora? → Porque a causa raiz não é técnica (o destino correto já existe e já funciona: `/api/chat` já atravessa Hipocampo/Memory Engine v1) — é puramente uma decisão de roteamento pendente.

**Decisão registrada (2026-07-16, Rubens, execução, sem ratificação do sócio):**
manter o Forge apontando para o serviço atual (a parte `/chat`, não o órgão Guardian)
por enquanto. Redirecionamento para `/api/chat` do Cognitive Engine fica em espera.

**O que falta:** nada tecnicamente — decisão tomada. Revisitar quando fizer sentido.
**Status:** adiado por decisão (não é mais pendência esquecida).

---

## MVP: Python / Terminal

**Função:** execução de código, exposta como capability do organismo.
**Capability:** ambiente `outstanding-learning` — interface-agnóstica em teoria, mas hoje
só acessível via WebSocket do `/forge`.
**Cliente de referência:** `luna-frontend` (`/forge`) — primeiro consumidor, não o único previsto.

**Cadeia de Porquês:**
1. Por que não está pronto? → O terminal está bloqueado em produção.
2. Por que está bloqueado? → Falta configurar `FORGE_TERMINAL_TOKEN` / `NEXT_PUBLIC_FORGE_TERMINAL_TOKEN`.
3. Por que a variável não foi configurada? → Porque o gate foi implementado deliberadamente após revisão de segurança — rejeitar WebSocket sem token é comportamento intencional, não bug.
4. Por que a revisão de segurança não avançou para liberar o token? → Porque execução arbitrária de código é a operação mais sensível do Forge, e não há política de autorização real no Gateway (`AllowGatewayAuthorizationPolicy` é allow-all hoje).
5. Por que isso é o item certo para ficar por último? → Porque a causa raiz é a lacuna de Auth do ecossistema inteiro (já registrada em `ECOSYSTEM_ARCHITECTURE.md` e como item P2 do ROADMAP) — é o único dos 4 MVPs cuja causa raiz não é local ao Forge.

**O que falta:** decisão de Architects sobre política de Auth, antes de configurar o token.
**Status:** bloqueado — fora do escopo de decisão solo.

---

## Resumo de prioridade resultante

| MVP | Causa raiz | Status | Próxima ação |
|---|---|---|---|
| Git | Resolvida (backend já pronto) | Liberado | Handoff ao Builder |
| Editor | Resolvida (backend já pronto) | Liberado | Handoff ao Builder |
| Chat | Decisão de roteamento | Adiado por decisão | Nenhuma — revisitar quando fizer sentido |
| Python/Terminal | Lacuna de Auth do ecossistema | Bloqueado | Decisão de Architects (P2) |
