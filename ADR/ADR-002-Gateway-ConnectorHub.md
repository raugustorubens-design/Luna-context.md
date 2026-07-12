# ADR-002 — Gateway e Connector Hub como órgãos distintos, coabitando o `luna-core`

**Status:** Aceito

**Data:** 2026-07-11

**Relacionado a:**
- LUNA_CONSTITUTION.md — Princípio 1 ("A arquitetura da LUNA é orientada por órgãos, não por tecnologias.") e Princípio 7 ("Órgãos possuem identidade conceitual permanente.")
- LUNA_CONSTITUTION.md — Princípio 2 ("Descobrir → Integrar → Criar.")
- LUNA_CONSTITUTION.md — Princípio 8 (documentação arquitetural e decisória centralizada no repositório oficial de contexto da LUNA)
- ADR-001 — Guardian (MVP-01)
- ADR-004 — Portar o Gateway para o `luna-core` e migrar seu runtime de Python para Node/TypeScript (especifica *como* o Gateway chega ao `luna-core` decidido aqui)
- **DA-001 — Guardian como Órgão Interno (2026-07-12)** — emenda este ADR (ver seção "Emenda 001" abaixo e "Restrições Arquiteturais")

**Nota de correção (2026-07-11):** a versão original deste documento citava "Article I/II/IV" da Constitution da LUNA. `LUNA_CONSTITUTION.md` não tem artigos numerados — são 8 princípios em bullet. A tabela acima substitui essas referências por citação direta do princípio correspondente, por conteúdo.

---

# Emenda 001 (DA-001, 2026-07-12)

**O que motivou a emenda:** a implementação da capability `guardian.memory_index_search` (Gateway, `luna-core`) expôs uma tensão não resolvida neste documento: a seção "Arquitetura" abaixo sempre desenhou o Guardian como filho direto do Gateway, irmão do Connector Hub — mas a seção "Restrições Arquiteturais" proibia qualquer HTTP direto fora do Connector Hub, sem exceção explícita para o Guardian. A primeira implementação seguiu o texto (mais restritivo) e tratou o Guardian como mais um sistema externo, roteado pelo Connector Hub — e o próprio engenheiro sinalizou a tensão diagrama-vs-texto em vez de resolvê-la silenciosamente.

**Decisão dos arquitetos:** o Guardian não é um sistema externo. O erro foi aplicar uma regra geral (destinada a sistemas externos ao organismo) a um caso que é, na verdade, fisiologia interna. A seção "Arquitetura" estava certa; a seção "Restrições Arquiteturais" precisava desta exceção explícita.

**Regra geral (mantida, sem alteração):** o Connector Hub centraliza toda comunicação com sistemas externos ao organismo. Exemplos: GitHub, Supabase (como infraestrutura de Storage), OpenAI, Claude, Groq, DeepSeek, OpenRouter, Railway, Gmail, Calendar.

**Exceção arquitetural (nova, formalizada por esta emenda):** órgãos do próprio organismo — Gateway, Guardian, Hipocampo, Reporter, e futuros órgãos — não se comunicam entre si como integração externa. Comunicação entre órgãos internos é fisiologia interna, não roteada pelo Connector Hub.

**Texto de emenda à seção "Restrições Arquiteturais":**

> O Connector Hub centraliza toda comunicação com sistemas externos ao organismo. A comunicação entre órgãos internos (Gateway, Guardian, Hipocampo, Reporter e futuros órgãos) não é considerada integração externa e não deve ser roteada pelo Connector Hub. Esses órgãos comunicam-se através de contratos internos do organismo.

**Consequência prática já implementada:** `luna-core` (`src/gateway/organs/`) — comunicação Gateway→Guardian é direta (HTTP, sem Connector Hub, sem credenciais de terceiros), reservada para órgãos internos; `connector_hub/` permanece exclusivo para sistemas verdadeiramente externos.

---

# Contexto

A evolução arquitetural da LUNA estabeleceu que **órgãos possuem identidade permanente**, enquanto repositórios, linguagens, frameworks e serviços representam apenas suas implementações físicas.

Durante a auditoria do organismo foi identificado que:

- o repositório `luna-core` representa atualmente um serviço estável, porém com implementação mínima;
- o Forge já possui interface preparada para consumir um Gateway de capacidades (`/gateway/execute`, `/gateway/capabilities`, `/api/context`);
- a lógica de orquestração existe parcialmente no monorepo `luna`, porém ainda não constitui um órgão oficialmente implantado;
- as integrações externas (GitHub, Supabase, OpenAI, Railway, Claude, Groq, Gmail, etc.) necessitam de um ponto único de acesso e governança.

Surgiu então a necessidade de responder uma questão arquitetural fundamental:

> O Gateway e o Connector Hub representam o mesmo órgão ou possuem responsabilidades distintas?

---

# Decisão

O **Gateway** e o **Connector Hub** passam a ser oficialmente reconhecidos como **órgãos distintos do organismo LUNA**, com responsabilidades independentes e fronteiras arquiteturais explícitas.

Durante a fase de migração, ambos serão implementados fisicamente dentro do repositório `luna-core`, compartilhando a mesma infraestrutura de execução, porém permanecendo logicamente independentes.

A coabitação física não altera sua identidade arquitetural.

---

# Responsabilidades

## Gateway

**Natureza**

Órgão executivo.

**Responsabilidades**

- receber intenções provenientes da Interface;
- descobrir capacidades disponíveis;
- decidir quais órgãos participarão da execução;
- orquestrar fluxos;
- consolidar respostas;
- controlar pipelines de execução;
- expor endpoints públicos do organismo.

O Gateway **não implementa comunicação externa**.

Ele depende exclusivamente de contratos públicos oferecidos por outros órgãos.

---

## Connector Hub

**Natureza**

Órgão circulatório.

**Responsabilidades**

- centralizar comunicação com sistemas externos;
- gerenciar autenticação;
- administrar credenciais;
- encapsular clientes de API;
- implementar adapters;
- controlar retries;
- controlar rate limiting;
- padronizar contratos externos.

O Connector Hub **não toma decisões cognitivas nem de orquestração**.

Seu papel é exclusivamente fornecer acesso aos recursos externos.

---

# Arquitetura

```text
                 Frontend
                     │
                     ▼
                Gateway
                     │
        ┌────────────┴────────────┐
        ▼                         ▼
 Connector Hub              Guardian
        │
 ┌──────┼──────────────┐
 ▼      ▼              ▼
GitHub Supabase      OpenAI
```

---

# Regra de Dependência

Fluxo permitido:

```text
Frontend
    ↓
Gateway
    ↓
Connector Hub
    ↓
Adapters
    ↓
Sistemas Externos
```

Fluxos proibidos:

```text
Connector Hub
      ↓
Gateway
```

```text
Frontend
      ↓
Connector Hub
```

```text
Gateway
      ↓
Adapters
```

```text
Qualquer órgão
      ↓
API externa
```

Toda comunicação externa deverá ocorrer exclusivamente através do Connector Hub.

---

# Contratos

O Gateway consumirá apenas contratos públicos fornecidos pelo Connector Hub.

A implementação interna do Hub será considerada um detalhe de infraestrutura.

Consequentemente:

- adapters poderão ser substituídos;
- bibliotecas poderão mudar;
- provedores poderão ser trocados;
- infraestrutura poderá evoluir;

sem necessidade de alterar a lógica do Gateway.

---

# Justificativa

A decisão baseia-se nos seguintes princípios arquiteturais:

### 1. Separação de responsabilidades

O Gateway coordena.

O Connector Hub conecta.

Misturar ambas as responsabilidades criaria alto acoplamento entre lógica de negócio e infraestrutura.

---

### 2. Reaproveitamento de infraestrutura existente

O `luna-core` já possui pipeline de deploy e infraestrutura operacional.

Utilizá-lo como implementação inicial reduz complexidade operacional sem comprometer a arquitetura conceitual.

---

### 3. Princípio da Constituição

> Órgãos são permanentes.

> Implementações são temporárias.

A decisão preserva esse princípio.

Caso seja necessário separar Gateway e Connector Hub em serviços distintos no futuro, nenhuma alteração arquitetural será necessária.

Apenas a implementação física será modificada.

---

### 4. Evolução gradual

A estratégia segue o mesmo padrão adotado anteriormente na evolução do `luna-api` para o órgão Guardian:

- preservar infraestrutura;
- redefinir responsabilidades;
- documentar a decisão;
- evoluir sem reescritas desnecessárias.

---

# Consequências

## Curto prazo

- o `luna-core` deixa de representar um "Core Cognitivo";
- passa a implementar explicitamente dois órgãos;
- o Forge poderá consumir um Gateway oficialmente definido;
- as integrações externas deixam de estar distribuídas pela aplicação.

---

## Médio prazo

Novos conectores passam a ser adicionados apenas ao Connector Hub.

Exemplos:

- GitHub
- Supabase
- Railway
- OpenAI
- Claude
- Gemini
- Groq
- Ollama
- PostgreSQL
- Slack
- Gmail
- Google Calendar
- Filesystem
- futuros conectores

Nenhum outro órgão poderá acessar esses sistemas diretamente.

---

## Longo prazo

Caso haja necessidade de escalabilidade independente, Gateway e Connector Hub poderão tornar-se serviços separados.

Essa migração deverá exigir apenas a substituição da implementação dos contratos (chamada local → chamada remota), preservando integralmente a lógica interna dos órgãos.

---

# Restrições Arquiteturais

**Emendado por DA-001 (2026-07-12) — ver "Emenda 001" acima.** O texto original abaixo não distinguia sistemas externos de órgãos internos do organismo; essa distinção agora é explícita.

O Connector Hub centraliza toda comunicação com sistemas externos ao organismo. A comunicação entre órgãos internos (Gateway, Guardian, Hipocampo, Reporter e futuros órgãos) não é considerada integração externa e não deve ser roteada pelo Connector Hub. Esses órgãos comunicam-se através de contratos internos do organismo (ex.: `src/gateway/organs/` no `luna-core`).

Para sistemas **externos**, continua proibido, fora do Connector Hub:

- criação direta de clientes HTTP;
- chamadas REST arbitrárias;
- instâncias de SDKs externos;
- gerenciamento de API Keys;
- autenticação direta;
- criação manual de conexões com provedores.

Exemplos:

- `fetch()`
- `axios()`
- `OpenAI()`
- `Octokit()`
- `Anthropic()`
- `Groq()`
- `create_client()`
- qualquer SDK externo equivalente.

Todo acesso a sistemas **externos** deverá ocorrer mediante contratos do Connector Hub.

> **Texto original (histórico, pré-DA-001), preservado por não descartar decisões superadas:**
>
> É proibido, fora do Connector Hub:
>
> - criação direta de clientes HTTP;
> - chamadas REST arbitrárias;
> - instâncias de SDKs externos;
> - gerenciamento de API Keys;
> - autenticação direta;
> - criação manual de conexões com provedores.
>
> Exemplos: `fetch()`, `axios()`, `OpenAI()`, `Octokit()`, `Anthropic()`, `Groq()`, `create_client()`, qualquer SDK externo equivalente.
>
> Todo acesso deverá ocorrer mediante contratos do Connector Hub.
>
> *(Esta redação não excepcionava órgãos internos do organismo — corrigido pela Emenda 001/DA-001.)*

---

# Observação

Nem o Gateway nem o Connector Hub pertencem à camada cognitiva do organismo.

Ambos constituem **órgãos de infraestrutura**, responsáveis por fornecer os mecanismos necessários para que os órgãos cognitivos possam perceber, planejar, inferir e agir.

---

# Inferência Registrada

## Inferência 023

> **Coabitação física não implica identidade arquitetural.**

Dois órgãos podem compartilhar o mesmo processo, contêiner, repositório ou serviço sem perder sua identidade.

A arquitetura é definida por responsabilidades, contratos e dependências, e não pelos limites físicos da implementação.

Essa inferência torna possível a evolução incremental do organismo, permitindo reorganizar sua infraestrutura sem alterar sua arquitetura conceitual.
