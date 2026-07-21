# ADR-012 — Consolidação do backend em `luna-core` + Interface de Convergia

Status: Aceito
Data: 2026-07-19
Decisor: Architect (Rubens)
Contexto: ENG-014 (`GENESIS/ENGINEER.md`) — Convergia completo, Cognitive Engine
e as rotas reais de `/chat`/`/context` existem testados dentro do monorepo
`luna` (`apps/frontend/artifacts/api-server`), nunca portados. `luna-guardian`
hospeda hoje uma versão legada e incompatível de `/chat`/`/context`,
coexistindo com seu papel oficial de Guardian (armazenamento).

## Decisão 1 — Porte para `luna-core`

Portar (não reescrever a lógica) para `luna-core`, mesmo padrão do ADR-004:

- Cognitive Engine (`src/luna/*`: Memory Engine, Context Hub, Índice
  Cognitivo, Provider Router/Engine, Budget Manager, Hipocampo, Reporter
  interno, contratos)
- Convergia completo (`src/convergia/*`: parsers, renderers, templates,
  validação, transformação, catálogo, knowledge gate, training)
- Rotas `chat.ts` / `context.ts`

`luna-core` passa a ser o backend único de execução (Gateway + Cognitive
Engine + Convergia). `luna-guardian` mantém seu papel de Guardian oficial
(Princípio 4 da Constituição — toda persistência passa por ele), mas suas
rotas `/chat`/`/context` legadas são descontinuadas após o porte.

### Refinamento 1a — Persistência de `chat.ts` via Guardian, não Postgres direto

Auditoria pré-implementação (Builder, 2026-07-19) encontrou que `chat.ts`,
no código-fonte a ser portado, persiste `conversations`/`messages`
diretamente via Drizzle/Postgres (`@workspace/db`), sem passar pelo
Hipocampo/Memory Engine/Guardian — uma violação do Princípio 4 idêntica à
que já foi recusada nesta mesma sessão para `storage.query`/`storage.insert`
do Gateway (BLD-003/ENG-011). Portar isso como está recriaria a violação
dentro do próprio backend que a Constitution proíbe explicitamente de falar
com Supabase/Postgres direto.

**Decisão do Architect (2026-07-19):** portar tudo, substituindo os
inserts/selects diretos de `conversations`/`messages` por chamadas ao
Guardian, reaproveitando o padrão de `guardian.memory_index_search` já em
uso no Gateway (`luna-core/src/gateway/organs/guardian-adapter.ts`). O
Guardian já expõe um contrato genérico de armazenamento
(`save`/`update`/`delete`/`get`/`search`, coleção arbitrária) — usado para
armazenar `conversations`/`messages` como duas coleções desse contrato
genérico, sem endpoint bespoke para conversa. Uma única extensão pontual é
necessária: uma operação `count` (contagem eficiente via `SELECT count(*)`
do Supabase, não fetch-all) para viabilizar `/stats`, já que o contrato
genérico não tinha operação de contagem. Essa extensão é um ponto isolado
do contrato genérico do Guardian, não o redesenho completo de STOR-001
(que continua bloqueado por ARCH-001/P0).

Concretamente: `luna-core/src/luna/guardian-local-adapter.ts` (a
implementação local/transitória do `GuardianContract`, que o próprio
comentário do arquivo original já previa trocar por um cliente HTTP quando
o Guardian real estivesse alcançável) é substituído por um cliente HTTP
real, mesmo padrão de `gateway/organs/guardian-adapter.ts` (recursos de
resiliência do Connector Hub, `GUARDIAN_BASE_URL`, tolerância a ausência de
configuração).

### Refinamento 1b — Contexto via GitHub, não filesystem local

Auditoria também encontrou que `context-hub.ts`/`indice-cognitivo.ts` leem
arquivos locais do monorepo (`luna_context/*.md`, `forge/ROADMAP.md`,
`docs/architecture/adr-004-*.md`) que não existem em `luna-core` — portados
como estão, degradariam graciosamente (sem crash) mas retornariam contexto
vazio, silenciosamente.

**Decisão do Architect (2026-07-19):** trocar as leituras de arquivo local
por leituras via `GithubConnector.readFile` (mesma interface já usada pelo
Gateway, mesmo padrão maduro e testado do Claude Activity Panel/FORGE-MVP-08A)
apontando para `raugustorubens-design/Luna-context.md` — `LUNA_CONTEXT.md`,
`GENESIS/ROADMAP.md`, `ADR/ADR-004-*.md` — em vez de cópias locais
desatualizadas. Isso também está alinhado ao Princípio 8 da Constitution
(documentação centralizada no repositório oficial de contexto).

### Nota de escopo — `@workspace/api-zod` / `@workspace/db`

`@workspace/api-zod` é código gerado por `orval` a partir de uma spec
OpenAPI (mais um módulo `renascer/contracts.ts` não relacionado a este
porte) — não é lógica de negócio para portar verbatim. As ~10 schemas Zod
que `chat.ts` de fato usa (`SendMessageBody`, `SendMessageResponse`, etc.)
são copiadas manualmente como arquivo local em `luna-core`, preservando a
validação exata, sem trazer o pipeline de codegen inteiro. `@workspace/db`
não é portado — sua função é substituída inteiramente pelo cliente HTTP do
Guardian (Refinamento 1a).

## Decisão 2 — Interface de Convergia em `luna-frontend`

Nova área no `luna-frontend` (mesmo padrão de `components/forge/`) para:

- Upload de arquivo (hoje: XLSX) → `/api/convergia/parse`
- Visualização do catálogo → `/api/convergia/catalog`
- Upload de modelo/conhecimento pelo especialista → `/api/convergia/training`
  (mecanismo já existente na API para o especialista alimentar o sistema —
  precisa de UI, não de endpoint novo)
- Execução de transformação → `/api/convergia/transform`

Depende da Decisão 1 estar aplicada e confirmada funcionando em `luna-core`
antes da UI apontar para lá.

## Fora de escopo (pendências separadas, não bloqueiam isto)

- Parsers de DOCX/PDF — ainda não existem.
- Conteúdo real dos 13 tipos de documento SSMA — passam a ser alimentados
  via `training` pelo especialista, não mais "bloqueado por revisão
  externa".
- Autorização real do Gateway (hoje allow-all) — prioridade paralela
  recomendada, já que esta interface expõe upload de dado potencialmente
  sensível através dela.
- `training-to-memory.ts` chama `checkpoint()` (que já é Guardian-mediado
  via `persistMemory`) sem passar pela decisão do Hipocampo — divergência
  já registrada em `LUNA_CONTEXT.md` antes deste ADR, não resolvida aqui
  (não é uma violação do Princípio 4, é uma lacuna de filtro do Hipocampo;
  portado como está, mesmo tratamento do restante do código-fonte).

## Consequência

`apps/{core,api,frontend}` do monorepo `luna` ficam definitivamente órfãos
após o porte — candidatos a arquivamento numa etapa futura.
