# ADR-004 — Portar o Gateway para o `luna-core` e migrar seu runtime de Python para Node/TypeScript

**Status:** Aceito

**Data:** 2026-07-11 (proposto e aceito na mesma data)

**Relacionado a:**
- LUNA_CONSTITUTION.md — Princípio 3 ("Reutilizar antes de implementar.")
- LUNA_CONSTITUTION.md — Princípio 6 ("Infraestrutura é substituível.")
- LUNA_CONSTITUTION.md — Princípio 7 ("Órgãos possuem identidade conceitual permanente.")
- ADR-002 — Gateway e Connector Hub como órgãos distintos, coabitando o `luna-core`
- ECOSYSTEM_ARCHITECTURE.md — Entregável 9 ("Nenhuma fusão física de sistemas por conveniência de implementação")

**Nota de numeração:** um prompt anterior desta mesma linha de trabalho citou esta decisão como "ADR-003". Esse número já pertence a outra decisão registrada (a fórmula de consolidação do Hipocampo/Filtro Cognitivo, referenciada em `ECOSYSTEM_ARCHITECTURE.md`). Este documento corrige a numeração para ADR-004, e é a primeira vez que esta decisão específica (porte do Gateway + migração de runtime) é escrita como ADR.

---

# Contexto

O ADR-002 estabeleceu que o Gateway e o Connector Hub são órgãos distintos que, durante a fase de migração, coabitarão fisicamente o `luna-core`. O ADR-002 não especificou, no entanto, **como** o Gateway chega até o `luna-core` — se seria reescrito ali, ou se a implementação já existente seria movida.

Essa implementação já existe e está em produção de teste: o Gateway do monorepo `luna` (`apps/frontend/artifacts/api-server/src/gateway`), com Registry, Capability/Manifest, auditoria, política de autorização e dois capability packs completos e testados — GitHub (11 capabilities: read_file, write_file, create_branch, commit, create_pull_request, list_branches, list_pull_requests, list_commits, compare_commits, create_issue, comment_pull_request) e Filesystem (6 capabilities: read, write, list, search, diff, exists), totalizando 17 capabilities registradas e cobertas por teste automatizado (`gateway.test.ts`, `filesystem-adapter.test.ts`) e por um script de verificação de fronteira (`architecture-check.mjs`). Está escrito em TypeScript, roda em Node via Express, e é hoje o único runtime do ecossistema com um Gateway real, testado e ponta a ponta.

*(Nota: `ECOSYSTEM_ARCHITECTURE.md` registra "19 capabilities". A contagem direta no código-fonte, feita para este ADR, confirma 17 — 11 GitHub + 6 Filesystem, sem capability packs de Railway ou n8n presentes no diretório atual apesar de mencionados alhures como "preparados e desabilitados". Divergência registrada aqui, não corrigida no documento de origem por não ser escopo deste ADR.)*

O `luna-core`, por outro lado, é hoje um serviço Python/FastAPI mínimo (`main.py`, ~60 linhas): dois endpoints triviais (`/`, `/health`) e um terceiro (`/modules`) que lê uma tabela do Supabase sem relação com o Gateway. `ECOSYSTEM_ARCHITECTURE.md` (2026-07-09) classificou esse serviço como Legado — duplicata quase idêntica de `apps/core` no monorepo — e não como o destino planejado de um órgão executivo.

Isso cria a pergunta que este ADR resolve:

> Para que o `luna-core` hospede o Gateway (conforme ADR-002), o Gateway existente deve ser reescrito em Python, ou a implementação TypeScript já testada deve ser portada — e, se portada, o que isso implica para o runtime do `luna-core`?

Essa pergunta importa em particular porque `ECOSYSTEM_ARCHITECTURE.md` também registrou, no mesmo documento que classificou `luna-core` como legado, o princípio "nenhuma fusão física de sistemas por conveniência de implementação" como lição central do ADR-004 [sic — à época sem numeração própria] daquela consolidação. Uma decisão que force `luna-core` a mudar de runtime precisa deixar explícito por que isso não é a mesma coisa que a fusão por conveniência que aquele princípio proíbe.

---

# Decisão

1. **O Gateway não será reescrito.** A implementação TypeScript existente em `apps/frontend/artifacts/api-server/src/gateway` (Registry, Capability/Manifest, auditoria, política de autorização, capability packs GitHub e Filesystem, testes) será **portada** para dentro do `luna-core`, ajustando apenas imports, caminhos e o ponto de montagem HTTP — sem reescrever a lógica de nenhuma capability, adapter ou do Registry.

2. **O `luna-core` muda de runtime: de Python/FastAPI para Node/TypeScript.** `main.py`, `requirements.txt`, `runtime.txt`, `Procfile` e o `Dockerfile` baseado em `python:3.11` deixam de ser a implementação física do serviço. Em seu lugar: `package.json`, `tsconfig.json`, e configuração de deploy Node equivalente (Railway detecta e builda Node/Nixpacks ou um `Dockerfile` Node, a definir na execução, não neste ADR).

3. **O Connector Hub (definido no ADR-002) nasce também em TypeScript, no mesmo runtime**, como módulo irmão do Gateway dentro do `luna-core` — não em Python, e não em um processo separado. Isso preserva a coabitação física decidida no ADR-002 sem introduzir um segundo runtime dentro do mesmo serviço.

4. **A separação de contratos do ADR-002 (`gateway/contracts/` e `connector_hub/contracts/`) permanece integral.** Portar o Gateway para dentro do `luna-core` não significa que o Connector Hub herda acesso a `gateway/contracts/` nem vice-versa; a fronteira lógica entre os dois órgãos definida no ADR-002 é preservada dentro do novo runtime físico, incluindo a regra de dependência (Frontend → Gateway → Connector Hub → Adapters → Sistemas Externos) e as proibições explícitas (nenhum órgão fora do Connector Hub cria clientes HTTP/SDKs diretamente).

---

# Justificativa

### 1. Reutilizar antes de implementar (Princípio 3 da Constitution)

O Gateway já existe, já está testado (`gateway.test.ts`, `filesystem-adapter.test.ts`), já tem um script de verificação de fronteira (`architecture-check.mjs`) e já processa 17 capabilities reais. Reescrevê-lo em Python duplicaria esse trabalho inteiro só para satisfazer o runtime atual do `luna-core` — o oposto do que a Constitution pede.

### 2. Infraestrutura é substituível (Princípio 6 da Constitution); o runtime do `luna-core` é infraestrutura, não identidade

O `luna-core` como serviço Python/FastAPI nunca foi, ele mesmo, um órgão com identidade — `ECOSYSTEM_ARCHITECTURE.md` o classifica como Legado/duplicata. O único órgão com identidade permanente em jogo aqui é o Gateway, e o Gateway já é TypeScript. Trocar o runtime do container que o hospeda é trocar infraestrutura substituível; não é alterar a identidade de nenhum órgão.

### 3. Por que isto não é a "fusão física por conveniência" que `ECOSYSTEM_ARCHITECTURE.md` proíbe

O princípio registrado naquele documento nasceu para impedir que sistemas com identidade própria e código já divergente fossem fisicamente empilhados só para simplificar deploy — o exemplo concreto era não repetir, com outros órgãos, o que já havia acontecido de forma não intencional antes daquela consolidação. Este ADR é o caso oposto:

- Não há dois códigos divergentes sendo empilhados — há **um único Gateway**, já testado, sendo movido do lugar onde não tem deploy próprio (`luna`, monorepo sem serviço Railway dedicado ao Gateway) para o lugar que o ADR-002 já havia designado para ele (`luna-core`).
- A fronteira conceitual Gateway/Connector Hub estabelecida no ADR-002 não é tocada — ela é preservada dentro do novo runtime físico, com contratos separados, exatamente como já decidido.
- A decisão é deliberada e documentada (este ADR), não uma conveniência silenciosa de implementação — que era precisamente o que faltava nos casos que motivaram o princípio original.

Em suma: fusão por conveniência é empilhar identidades diferentes sem decisão registrada. Isto é o oposto — uma única identidade (o Gateway) sendo movida para seu destino já decidido, com a decisão registrada antes da execução.

### 4. Evolução gradual, sem reescritas desnecessárias

Segue o mesmo padrão que o ADR-002 já cita para o `luna-api` → Guardian: preservar o que funciona, redefinir responsabilidades, documentar a decisão antes de agir.

---

# Consequências

## Curto prazo

- `luna-core` deixa de ser Python/FastAPI; `main.py`, `requirements.txt`, `runtime.txt`, `Procfile` e o `Dockerfile` atual são removidos.
- O Gateway (Registry, contracts, capability packs GitHub e Filesystem, testes) passa a viver dentro do `luna-core`, com imports/caminhos ajustados, sem alteração de lógica.
- `GET /api/gateway/capabilities` e `POST /api/gateway/execute` passam a responder a partir do `luna-core`, não mais apenas dentro do monorepo `luna` sem deploy próprio.
- Nasce `connector_hub/` dentro do `luna-core`, com seu primeiro adapter (Supabase), seguindo a separação de contratos do ADR-002.
- `luna-frontend` (`lib/forge/api-client.ts`, `NEXT_PUBLIC_LUNA_API_BASE_URL`) passa a apontar para o `luna-core`, não mais para `luna-guardian` — resolvendo a causa raiz identificada na auditoria de Fase 1 (o Forge chamava `/gateway/execute` e `/api/context` em um serviço, `luna-guardian`, cujo contrato HTTP nunca implementou essas rotas).

## Médio prazo

- O monorepo `luna` deixa de ser o único lugar onde o Gateway roda; passa a ser tratado como a fonte de desenvolvimento/teste do Gateway, com `luna-core` como seu destino de deploy. A relação entre os dois repositórios (o Gateway continua evoluindo em qual dos dois?) fica registrada aqui como uma decisão pendente de execução, a resolver quando o porte for implementado — não especulada neste ADR.
- Novos conectores externos (GitHub, Supabase, Railway, OpenAI, etc., listados no ADR-002) nascem dentro do Connector Hub do `luna-core`, não do Gateway nem de nenhum outro órgão.

## Longo prazo

- Caso Gateway e Connector Hub precisem se tornar serviços independentes (já previsto no ADR-002), a migração exigirá apenas trocar a implementação dos contratos (chamada local → chamada remota) — este ADR não compromete essa reversibilidade.
- Caso o monorepo `luna` continue evoluindo o Gateway em paralelo ao `luna-core`, será necessário decidir uma fonte única de verdade para o código do Gateway (provavelmente `luna-core`, pós-porte) — risco registrado, não resolvido aqui.

---

# Restrições Arquiteturais

- O porte não deve alterar a lógica de nenhuma capability, adapter, do Registry, da auditoria ou da política de autorização — apenas caminhos de import e o ponto de montagem HTTP.
- O Connector Hub nascente não deve importar nada de dentro de `gateway/contracts/`, nem o Gateway importar de `connector_hub/contracts/` — a separação de contratos do ADR-002 é uma fronteira testável, não apenas uma convenção documental.
- Nenhuma das restrições do ADR-002 (proibição de `fetch()`/SDKs/clientes HTTP fora do Connector Hub, regra de dependência Frontend→Gateway→Connector Hub→Adapters) é revogada ou enfraquecida por este ADR.

---

# Inferência Registrada

## Inferência 024

> **Portar não é reescrever, e mudar o runtime do container não é o mesmo que mudar a identidade do órgão que ele hospeda.**

O princípio "nenhuma fusão física por conveniência" protege identidades divergentes de serem empilhadas sem decisão. Ele não proíbe mover uma identidade única (um órgão já testado) para o destino físico que uma decisão anterior (ADR-002) já havia designado para ela. Confundir os dois casos levaria a reescrever software testado por respeito excessivo à forma, não ao princípio que a forma deveria proteger.
