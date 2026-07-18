# LUNA Architecture Inventory

Data da auditoria: 2026-07-19
Autor: Claude Code (Builder), a partir de `git clone` + GitHub API dos 7 repositórios de `raugustorubens-design`
Owner: GENESIS (documento vivo — atualizar em vez de recriar; ver §Evidências para o critério de reaproveitamento)

**Escopo de acesso desta auditoria:** GitHub completo (API + clone). **Nenhum acesso ao Railway, Vercel ou Supabase** (sem CLI, sem token, sem conector MCP — confirmado antes de iniciar, não é suposição). Toda afirmação sobre esses três serviços vem de **evidência documental** (arquivos versionados: `README.md`, `DEPLOY.md`, `LUNA_CONTEXT.md`) ou de **atividade de bot no GitHub** (comentários/PRs automáticos), nunca de consulta ao vivo — cada uma está marcada como tal. Onde nenhuma das duas existir, o documento registra `Status: Não confirmado`, conforme instruído.

---

## Visão Geral

O achado mais importante desta auditoria não é sobre Railway — é sobre onde o organismo LUNA realmente mora hoje:

> **O monorepo `luna` (`apps/frontend/artifacts/api-server`) ainda hospeda a única implementação real e testada do Cognitive Engine, do Convergia completo, e das rotas `/api/chat`/`/api/context` — nenhum dos três foi portado para fora do monorepo.** O ADR-004 portou *só* o Gateway e o Connector Hub para `luna-core`; o resto do api-server ficou para trás, ativo mas sem deploy próprio conhecido. Isso significa que a lacuna registrada em `LUNA_CONTEXT.md` ("`luna-guardian` tem contrato de `/chat` incompatível e não implementa `/context`") já tem solução pronta em código — só não foi portada (ver §Problemas, P1).

Isso muda a resposta a "qual é o núcleo da arquitetura": não é um repositório único, é uma migração **parcial**. `luna-core` é o destino oficial (ADR-004), mas só recebeu uma fatia do que o monorepo ainda executa de fato.

---

## 1. Repositórios

| Repositório | Descrição / Finalidade | Status | Linguagens / Frameworks | Branch principal | Última atividade (push) | Estrutura principal |
|---|---|---|---|---|---|---|
| `luna` | Monorepo original — Runtime, Cognitive Engine, Convergia, Gateway (pré-porte) | **Ativo (parcial)** — ver Visão Geral | TypeScript/Node (pnpm workspace), Python (`apps/core`), React/Vite (`apps/frontend`) | `main` | 2026-07-17 | `apps/{api,core,frontend}`, `apps/frontend/artifacts/{api-server,frontend,mockup-sandbox}` |
| `luna-core` | Gateway + Connector Hub oficiais pós-ADR-004 | **Ativo** | Node/TypeScript (Express) | `main` | 2026-07-15 | `src/{gateway,connector_hub}` |
| `luna-frontend` | Frontend oficial (User Mode + Forge/Dev Mode) | **Ativo** | Node/TypeScript (Next.js, custom server + WebSocket) | `main` | 2026-07-17 | `app/`, `components/forge/`, `lib/forge/`, `server.ts` |
| `luna-guardian` | Guardian (storage) oficial + rotas `/chat`/`/context` legadas (pacote interno chamado `luna-api`) | **Ativo (misto)** — órgão oficial + dívida experimental no mesmo processo | Node/Express | `main` | 2026-07-12 | `src/guardian/{contracts,audit,adapters,routes}.js`, `index.js` |
| `luna-convergia` | Repo-interface para o pipeline Convergia | **Experimental / esqueleto** | Node/Express | `main` | 2026-06-06 | `src/index.js` (1 arquivo) |
| `Luna-reporter` | Observador do organismo — "ler os repositórios e passar status de cada repo" (README) | **Ativo (MVP parcial)** | Python (scanner) + TypeScript (`src/index.ts`, `src/reporter.ts`, sem integração confirmada entre os dois) | `main` | 2026-07-11 | `src/{github,ai,reports}`, `.github/workflows/reporter-discovery.yml` |
| `Luna-context.md` | Fonte de verdade documental — Constituição, ADRs, Roadmap, GENESIS | **Ativo** | Markdown + 1 script Python utilitário (`generate_index.py`) | `main` | 2026-07-19 (esta sessão) | `GENESIS/`, `ADR/`, `CHECKPOINTS/` |

Responsável funcional de cada repositório: `Status: Não confirmado` — não há campo de "owner"/CODEOWNERS em nenhum dos 7 repositórios (confirmado por ausência de arquivo `CODEOWNERS` e por todos os commits/PRs relevantes serem do mesmo usuário, `raugustorubens-design`, sem outros colaboradores humanos visíveis no histórico consultado).

---

## 2. Responsabilidades

| Repositório | Backend | Frontend | Biblioteca | Documentação | Infraestrutura | Pesquisa | Protótipo | Legado |
|---|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|
| `luna` | ✅ (×3: api-server, `apps/api`, `apps/core`) | ✅ (`apps/frontend`, Vite/React) | — | — | ✅ (`railway.json` raiz) | — | — | parcial (`apps/core`, `apps/api`, `apps/frontend` já superados; `api-server` ainda ativo) |
| `luna-core` | ✅ | — | — | — | — | — | — | — |
| `luna-frontend` | — (só rotas locais `/api/forge/*`) | ✅ | — | — | — | — | — | — |
| `luna-guardian` | ✅ | — | — | — | — | — | — | parcial (rotas `/chat`,`/context`,`/api/github/file` legadas, coexistindo com o Guardian ativo) |
| `luna-convergia` | ✅ (mínimo) | — | — | — | — | — | ✅ | — |
| `Luna-reporter` | — (não é serviço persistente) | — | — | — | — | ✅ (`src/ai/repository_analyzer.py`) | — | — |
| `Luna-context.md` | — | — | — | ✅ | — | — | — | — |

---

## 3. Dependências internas

Mapeado por import/config real, não por suposição de nomes parecidos:

```
luna-frontend
  ├─→ luna-core         (Gateway: /api/gateway/{capabilities,execute} — lib/forge/api-client.ts)
  └─→ luna-guardian      (chat/contexto: NEXT_PUBLIC_LUNA_API_BASE_URL — DEPLOY.md:19; contrato incompatível)

luna-core
  └─→ luna-guardian      (guardian.memory_index_search, via src/gateway/organs/guardian-adapter.ts — HTTP direto, não Connector Hub, por DA-001)

luna-guardian
  └─→ Supabase           (@supabase/supabase-js — package.json:12; único adapter de storage autorizado)

luna (monorepo) — apps/frontend/artifacts/api-server
  ├─→ Supabase           (src/lib/supabase.ts, drizzle-orm/pg no package.json raiz)
  └─→ (nenhum consumidor externo confirmado — chat.ts/context.ts existem mas não há evidência de que algo os chame em produção)

luna-convergia
  └─→ nenhuma dependência externa real (esqueleto de 1 endpoint, sem cliente conhecido)

Luna-reporter
  └─→ GitHub API (src/github/{client,repository_scanner,activity_analyzer}.py)
  └─→ Groq (requirements.txt:26 — "groq==1.4.0"; uso real no código não confirmado nesta auditoria — Status: Não confirmado)

Luna-context.md
  └─→ consumido por luna-frontend (Claude Activity Panel lê GENESIS/BUILDER.md via capability github.read_file — components/forge/claude-code-panel.tsx)
```

**Packages compartilhados (pnpm workspace, dentro do monorepo `luna`):** `@workspace/api-zod`, `@workspace/db`, `@workspace/api-client-react` (usados por `apps/frontend/artifacts/api-server/src/routes/chat.ts` e pelo restante do api-server) — nenhum desses é publicado ou consumido fora do monorepo; são internos ao workspace pnpm, não pacotes npm reais.

**Submodules git:** nenhum encontrado em nenhum dos 7 repositórios.

**Workflows compartilhados:** nenhum — o único repositório com `.github/workflows` é `Luna-reporter` (`reporter-discovery.yml`), e não é reutilizado por nenhum outro repo.

---

## 4. Conexões externas

| Serviço | Finalidade | Repositório responsável | Ambiente | Evidência |
|---|---|---|---|---|
| **Railway** | Hospedagem do Gateway | `luna-core` | Produção (citado) | `LUNA_CONTEXT.md:121` — projeto "honest-joy", serviço "uvicorn-main" |
| **Railway** | Hospedagem do Guardian + chat/context legado | `luna-guardian` | Produção (citado) | `LUNA_CONTEXT.md:124` — projeto "strong-celebration" |
| **Railway** | Hospedagem do frontend | `luna-frontend` | Produção (citado) | `DEPLOY.md:24` — URL `luna-frontend-production-ffcc.up.railway.app` |
| **Railway** | Config de deploy presente, conexão ativa não confirmada | `luna` (raiz), `apps/core` | Não confirmado | `railway.json` (raiz), `apps/core/{Procfile,Dockerfile,runtime.txt}` — arquivos existem, conexão real: **Status: Não confirmado** |
| **Vercel** | Hospedagem do frontend (preview/produção) | `luna-frontend` | **Confirmado** — não é doc, é atividade real de bot | PR #2 ("Fix React Server Components CVE...", aberta por `vercel[bot]`) e comentário de deploy do `vercel[bot]` na PR #7 citando `vercel.com/raugustorubens-designs-projects/luna-frontend` e uma URL de preview `.vercel.app` |
| **Supabase** | Armazenamento (Guardian) | `luna-guardian` | Produção (dependência declarada) | `package.json:12` |
| **Supabase** | Armazenamento (Cognitive Engine, `drizzle-orm`) | `luna` (monorepo, api-server) | Não confirmado em produção | `src/lib/supabase.ts`, `drizzle-orm`/`pg` no `package.json` raiz |
| **Supabase** | Conector existe, sem consumidor | `luna-core` (Connector Hub) | Dormente | `README.md` — "conector Supabase existe mas não tem consumidor no Gateway" |
| **GitHub Actions** | Discovery/observação do Reporter | `Luna-reporter` | CI (push/PR) | `.github/workflows/reporter-discovery.yml` |
| **GitHub API** | 11 capabilities (read/write/branch/PR) | `luna-core` (Gateway) | Produção | `README.md` (ADR-004) |
| **GitHub API** | Scanner de repositórios | `Luna-reporter` | CI | `src/github/{client,repository_scanner}.py` |
| **Groq / DeepSeek / OpenRouter / Anthropic** | Model routing (code-reasoning) | `luna-core` (Connector Hub) | Dormente — credenciais ausentes em produção hoje | `README.md` §"Capabilities condicionais"; confirmado no BUILDER.md desta mesma sessão |
| **Groq** | Provider de IA declarado | `Luna-reporter` | Não confirmado (dependência presente, uso real não verificado) | `requirements.txt:26` |
| **Google OAuth (via Auth.js/next-auth)** | Login restrito a 1 e-mail (`FORGE_ALLOWED_EMAIL`) | `luna-frontend` | Produção (citado) | `DEPLOY.md`, `auth.ts` |
| **Docker** | Único repositório com Dockerfile | `luna` (`apps/core`) | Não confirmado se usado | `apps/core/Dockerfile` |
| **MCP** | — | — | — | **Não confirmado.** Nenhuma referência a MCP encontrada em nenhum dos 7 repositórios (a única ocorrência do termo é em `ADR-008` deste próprio repositório, que descreve GitHub Actions como caminho de delegação — não é um uso de MCP pela LUNA em si) |
| **Webhooks** | — | — | — | Não confirmado — nenhum endpoint de webhook encontrado no código auditado |
| **OpenAI** | — | — | — | Não confirmado — nenhuma referência em nenhum repositório |

---

## 5. Ambientes

- **Desenvolvimento:** local, todos os repositórios com servidor de dev via `pnpm`/`npm` (`dev`/`start`) — sem evidência de um ambiente de dev compartilhado/hospedado.
- **Homologação/staging:** **Status: Não confirmado.** Nenhum dos 7 repositórios tem configuração (`railway.json`, env var, branch) sugerindo um ambiente de staging dedicado. A única aproximação é o preview automático do Vercel em `luna-frontend` (por PR, efêmero — não um staging persistente).
- **Produção:** ver matriz da §Railway abaixo — `luna-core`, `luna-guardian`, `luna-frontend` (Railway, citado) e `luna-frontend` (Vercel, confirmado). Deploy é acionado por push a `main` em todos os casos documentados (nenhum dos `railway.json` encontrados especifica branch diferente).
- **Serviços órfãos (candidatos):** `luna` (raiz do monorepo) e `apps/core` — configuração de deploy presente, sem confirmação de uso. Ver §Problemas, P1/P2.
- **Serviços duplicados (candidatos):** `luna-frontend` em dois ambientes de produção simultâneos (Railway citado + Vercel confirmado) — ver §Problemas, P2.

---

## 6. Railway — detalhe da auditoria original

*(Consolidado aqui para não duplicar um documento separado — este é o resultado completo do pedido de auditoria Railway × GitHub.)*

### Matriz Railway × GitHub

| Repositório | Railway conectado? | Serviço (citado) | Produção? | Backend | Frontend | Evidência |
|---|---|---|---|---|---|---|
| `luna-core` | Provável (doc.) | uvicorn-main / honest-joy | Provável (doc.) | Sim | Não | `LUNA_CONTEXT.md:121` |
| `luna-guardian` | Provável (doc.) | strong-celebration | Provável (doc.) | Sim | Não | `LUNA_CONTEXT.md:124` |
| `luna-frontend` | Provável (doc.) + **Vercel confirmado** | — | Provável (doc.) | Não | Sim | `DEPLOY.md:24`; PRs `vercel[bot]` |
| `luna` (monorepo) | Não confirmado | Não confirmado | Não confirmado | Sim (×3) | Sim | `railway.json` presente na raiz |
| `luna-convergia` | Não confirmado | Não confirmado | Não confirmado | Sim (mínimo) | Não | sem arquivo de deploy |
| `Luna-reporter` | Não confirmado | Não confirmado | N/A (não é serviço) | Não | Não | `.github/workflows/reporter-discovery.yml` |
| `Luna-context.md` | Não confirmado | N/A | N/A | Não | Não | repositório de documentação |

### Respostas objetivas

**A. Qual repositório é a fonte oficial do backend em produção?**
`luna-core` para o Gateway (autodeclarado, ADR-004) — evidência documental, não confirmada ao vivo. Ressalva: não existe hoje um único backend oficial de fato — chat/contexto continuam em `luna-guardian`, com um contrato incompatível, enquanto a implementação correta já existe (não portada) em `luna`/`apps/frontend/artifacts/api-server` (ver §Problemas, P1).

**B. Qual repositório é a fonte oficial do frontend em produção?**
`luna-frontend` — autodeclarado, sem repositório concorrente.

**C. Existem repositórios conectados ao Railway que não deveriam estar?**
Sem evidência suficiente para confirmar conexões ativas. Por evidência de código: se `luna` (raiz) ou `apps/core` ainda estiverem conectados, nenhum dos dois deveria estar — são versões pré-porte/órfãs do que hoje vive em `luna-core`.

**D. Existem repositórios que deveriam estar conectados e não estão?**
Sem evidência suficiente sobre o estado atual. Os três candidatos legítimos por desenho são `luna-core`, `luna-frontend`, `luna-guardian`. `luna-convergia` só deveria conectar após a decisão de arquitetura pendente em ENG-004.

**E. Existe duplicação entre ambientes?**
Sim, duas, com níveis de confiança diferentes:
1. **Confirmada:** `luna-frontend` em Vercel (bot ativo no GitHub) *e* documentado para Railway (`DEPLOY.md`) — dois ambientes de produção para o mesmo frontend.
2. **Não confirmada, mas de risco real:** o Gateway existe em código simultaneamente em `luna` (pré-porte) e `luna-core` (oficial), cada um com sua própria config de deploy — se o serviço antigo ainda estiver ativo, é duplicação real de backend.

---

## 7. Inventário arquitetural

```
LUNA
│
├── luna (monorepo) — parcialmente superado, parcialmente ÚNICA FONTE ainda ativa
│   ├── apps/frontend/artifacts/api-server
│   │   ├── src/gateway/          → Gateway (PRÉ-PORTE — duplicado em luna-core, ADR-004)
│   │   ├── src/luna/             → Cognitive Engine, Memory Engine, Context Hub, Provider Router,
│   │   │                           Budget Manager, Hipocampo, Reporter interno — NÃO PORTADO, ativo aqui
│   │   ├── src/convergia/        → pipeline real (parsers, renderers, templates, validação) — NÃO PORTADO
│   │   └── src/routes/{chat,context}.ts → implementação REAL do contrato que luna-guardian não cumpre
│   ├── apps/core (Python/FastAPI) → órfão, duplicata de luna-core pré-ADR-004
│   ├── apps/api (Node/Express, pacote "luna-api") → legado, mesmo nome interno de luna-guardian
│   └── apps/frontend (Vite/React) → superado por luna-frontend
│
├── luna-core → Gateway + Connector Hub oficiais (ADR-002/004) — produção (honest-joy, citado)
├── luna-frontend → Interface oficial, User Mode + Forge — produção (Railway citado + Vercel confirmado)
├── luna-guardian ("luna-api") → Guardian oficial (armazenamento) + /chat /context legados incompatíveis
├── luna-convergia → repo-interface esqueleto (1 endpoint) — sem produção, aguardando ENG-004
├── Luna-reporter → observador via GitHub Actions, sem serviço persistente
└── Luna-context.md → fonte de verdade documental (Constituição, ADRs, Roadmap, GENESIS)
```

Por que cada peça existe / quem depende dela / situação atual — ver §§2–4 acima para cada item; não duplicado aqui.

---

## 8. Problemas encontrados (por prioridade)

**P1 — Crítico: a correção para o gap de chat/contexto já existe em código, não portada.**
`luna`/`apps/frontend/artifacts/api-server/src/routes/{chat,context}.ts` implementam exatamente o contrato que `luna-frontend` espera (`SendMessageBody`/`SendMessageResponse` via `@workspace/api-zod`, `runCognitiveEngine`, `buildOrganismContext`) — 325 + 16 linhas, montados em `/api` no `app.ts` real. Isso não é um protótipo: é uma implementação completa, testada dentro do monorepo. `luna-guardian` (o que está de fato em produção para chat/contexto, per `DEPLOY.md`/`LUNA_CONTEXT.md`) não implementa esse contrato. **A causa raiz do problema documentado desde o ADR-004 não é "falta implementar" — é "falta portar".**
Evidência: `apps/frontend/artifacts/api-server/src/routes/chat.ts:1-30`, `context.ts` (arquivo inteiro), `app.ts:32`.

**P1 — Crítico (não confirmado ao vivo): possível Gateway duplicado em produção.**
`luna` (raiz do monorepo) mantém `railway.json` apontando para o mesmo `api-server` que `luna-core` já recebeu portado. Se ainda conectado, é uma segunda cópia do mesmo órgão rodando em paralelo.
Evidência: `luna/railway.json`; conexão ativa — Status: Não confirmado.

**P2 — Alto: `luna-frontend` em dois ambientes de produção.**
Vercel (confirmado por atividade de bot) e Railway (documentado em `DEPLOY.md`) — risco de dessincronia entre as duas instâncias (env vars, versão de código, qual é a "real").
Evidência: PRs `vercel[bot]` (#2, comentário na #7); `DEPLOY.md:24`.

**P2 — Alto: `apps/core` é um backend órfão, tecnicamente deployável.**
Dockerfile + Procfile + runtime.txt próprios, já classificado como "sem consumidor confirmado" em `ECOSYSTEM_ARCHITECTURE.md`.
Evidência: `apps/core/{Dockerfile,Procfile,runtime.txt}`; `Luna-context.md/ECOSYSTEM_ARCHITECTURE.md:48`.

**P3 — Médio: colisão de nome `"luna-api"`.**
`apps/api` (monorepo, legado) e `luna-guardian` (repo separado, oficial) declaram o mesmo `"name"` no `package.json`. Risco de confusão operacional, não uma falha funcional confirmada.
Evidência: `luna/apps/api/package.json`; `luna-guardian/package.json`.

**P3 — Médio: `luna-guardian` sem config de deploy explícita.**
Único dos três serviços "de produção" sem `railway.json`/`Procfile`/`Dockerfile` — dependeria de autodetecção Nixpacks.
Evidência: ausência confirmada por listagem completa da raiz.

**P4 — Baixo: segredos reais versionados no monorepo.**
`.env` (não `.env.example`) na raiz de `luna` com `PORT`, `DATABASE_URL`, `SUPABASE_URL`, `SUPABASE_KEY` — nomes confirmados, valores não expostos neste documento.
Evidência: `luna/.env` (nomes de chave).

**P4 — Baixo: identidade do Reporter parcialmente resolvida, não fechada.**
`Luna-reporter` é o órgão oficial; `luna`/`src/luna/reporter.ts` é um log de auditoria interno diferente, ainda não renomeado/isolado — já registrado como ação em aberto pelo próprio `LUNA_CONTEXT.md`.
Evidência: `LUNA_CONTEXT.md:71`.

---

## 9. Recomendações

1. **Portar Cognitive Engine + Convergia + rotas `chat`/`context`** de `apps/frontend/artifacts/api-server` para `luna-core`, no mesmo padrão do ADR-004 (porte sem alteração de lógica, validado por typecheck/testes antes do merge). Resolve o P1 mais crítico com trabalho que já existe e já funciona — não é uma reimplementação.
2. **Confirmar manualmente** no dashboard do Railway e da Vercel se `luna` (raiz) e `apps/core` ainda têm serviço conectado; desconectar/arquivar se sim.
3. **Escolher um único ambiente de produção para `luna-frontend`** (Railway ou Vercel, não os dois) — decisão do Architect, não uma correção técnica unilateral.
4. **Resolver ENG-004** (portar Convergia real para `luna-convergia` ou manter a arquitetura atual) antes de conectar esse repositório a qualquer ambiente.
5. **Renomear** `apps/api` ou o pacote interno de `luna-guardian` para eliminar a colisão `"luna-api"`.
6. **Adicionar `railway.json` explícito** a `luna-guardian`, alinhando com os outros dois serviços de produção.
7. **Remover segredos reais do `.env` versionado** no monorepo e rotacionar as credenciais expostas (ação de segurança, não arquitetural).

---

## 10. Roadmap de consolidação

- **Curto prazo:** confirmar ao vivo as conexões Railway/Vercel (ação humana, fora do alcance desta sessão); abrir ADR formal para o porte do Cognitive Engine/Convergia/chat/context (item 1 das recomendações).
- **Médio prazo:** executar o porte (uma vez decidido); descontinuar as rotas `/chat`/`/context` de `luna-guardian`, mantendo-o só como Guardian de armazenamento.
- **Longo prazo:** decidir e executar o destino de `luna-convergia` (ENG-004); arquivar/remover `apps/{core,api,frontend}` do monorepo `luna` uma vez que o porte completo estiver confirmado em produção.

---

## Evidências utilizadas

Todas as citações ao longo deste documento apontam para arquivo(s) e, quando aplicável, linha(s) específica(s), lidos diretamente via `git clone` (shallow, branch `main` de cada repositório) ou GitHub API nesta sessão (2026-07-19). Nenhuma conclusão sobre Railway, Vercel ou Supabase se apoia em consulta ao vivo a essas plataformas — ver aviso de escopo no topo do documento. Reaproveitamento: este documento parte da auditoria de PRs/ADRs já registrada em `GENESIS/BUILDER.md` (pacotes anteriores desta mesma sessão) e do relatório de auditoria Railway pedido na mesma sequência de trabalho — não foi re-descoberto do zero.
