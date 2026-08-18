# ROADMAP

Sequência de prioridades consolidada em 2026-07-13, agora incluindo a evolução do Genesis, o Framework Curator, o Sistema Metabólico e o Research Pipeline.

## P00 — Forge v0.1: ferramenta de uso diário (prioridade máxima)

- [x] FORGE-MVP-01 — Validated Existing Capability (auditado, não implementado — ver GENESIS/BUILDER.md)
- [x] FORGE-MVP-02 — Chat sequencial com seleção de agente + metadado de atribuição (ver GENESIS/FORGE.md) — `luna-frontend` PR #7 (commit `f358752`), mergeada em `main` em 2026-07-17.
- [x] FORGE-MVP-03 — Projetos com contexto próprio (LUNA, RENASCER, SMX, CURSO EMPILHADEIRA) — `luna-frontend` PR #7 (commit `d7fddb5`), mergeada em `main` em 2026-07-17.
- [x] FORGE-MVP-04 — Storage Contract: Forge → Guardian → Storage Contract → Supabase Adapter — `luna-frontend` PR #7 (commit `322bba0`), mergeada em `main` em 2026-07-17.
- [x] FORGE-MVP-05 — Execution Metadata em toda memória salva (ver GENESIS/FORGE.md) — `luna-frontend` PR #7 (commit `5e0c57a`), mergeada em `main` em 2026-07-17.
- [x] FORGE-MVP-06 — Botões GitHub (commit/push/pull/branch) sob credencial de Builder — `luna-frontend` PR #7 (commit `1df218d`), mergeada em `main` em 2026-07-17.
- [x] FORGE-MVP-07 — Reporter manual: botão "Analisar Projeto" — `luna-frontend` PR #7 (commit `03dddc4`), mergeada em `main` em 2026-07-17. **Completo de ponta a ponta em 2026-07-19** (correção, ver `GENESIS/BUILDER.md`): esse `[x]` cobria só o botão/cliente — a capability `reporter.analyze_project` nunca existiu no Gateway (confirmado por payload real de `/api/gateway/capabilities`, 19 capabilities, zero `reporter.*`), então clicar no botão em produção sempre retornava `CAPABILITY_NOT_FOUND`. Implementada em `luna-core` (`claude/reporter-analyze-project`, PR aberto para `main`): lê `GENESIS/ROADMAP.md` real, classifica `[x]`/`[ ]`, compara com a análise anterior (drift) e commita em `GENESIS/ARCHITECTURE_INVENTORY.md` §11 + autoatestação em `GENESIS/BUILDER.md`. Testado de ponta a ponta com conteúdo real (commit `8cae4b1` em `Luna-context.md`), não só com fixture.
- [x] FORGE-MVP-08A — Claude Activity Panel (nó "AI Coding" do Workspace, integração honesta sem PTY — ver GENESIS/FORGE.md) — já satisfeito pelo commit `04d84fe` (mesma PR #7, mergeada em 2026-07-17); `components/forge/claude-code-panel.tsx` lê `GENESIS/BUILDER.md` via `github.read_file`, sem sessão embutida, e está de fato ligado como aba no `forge-layout.tsx`, não órfão. Confirmado 2026-07-19: nenhuma implementação nova foi necessária, a renomeação de "08" para "08A" no Roadmap (2026-07-17) já tinha sido só reclassificação do item, não indicava código faltante.

## FORGE-WORKSPACE-001 — Workspace nativo equivalente a Cursor + VS Code (pós-v0.1, sem prazo)

Nota (2026-08-06, ver `GENESIS/ENGINEER.md` ENG-038): este item é a
dependência real de destravamento do gate de alinhamento `A(t)` (Frente
2 do Signal Engine) — `A(t)` fica pausado no gate real até
`FORGE-WORKSPACE-001` (ou qualquer forma de tool-calling no pipeline de
chat) existir. Quando este item virar tarefa de Builder, o gate `A(t)`
(Fase 1, modo sombra) precisa entrar na mesma leva — ver ENG-038 para o
detalhe completo.

## P0 — Continuidade Cognitiva Distribuída (DESCONGELADO em 2026-07-22, ver ARCH-001)

Condição de descongelamento cumprida: Forge v0.1 em uso diário real,
confirmado em 2026-07-22 (chat funcionando de ponta a ponta com Groq).
Retomado precisamente porque o Forge esbarrou na lacuna da fórmula de
memória que o congelamento adiava — ver ADR-019 e o trabalho de Signal
Engine já mergeado em luna-core (PRs #19/#20).

- [ ] MEM-001 — Especificar a Operational Memory Layer — **especificação
  decidida via ADR-010 (2026-07-18)**; implementação liberada — Signal
  Engine (parte de MEM-001) já implementado, ver ADR-019.
- [ ] STOR-001 — Redesenhar storage.query/storage.insert do Gateway mediado
  pelo Hipocampo — **especificação decidida via ADR-010 (2026-07-18)**;
  implementação liberada — Signal Engine (parte de MEM-001) já
  implementado, ver ADR-019. Atualização (2026-07-22, ver ENG-011): código
  de referência para as 7 operações do Supabase (`query`/`insert`/`update`/
  `delete`/`rpc`/`uploadFile`/`downloadFile`, porte de `luna` PR #15) já
  existe em `luna-core` (`SupabaseHubConnector`), sem consumidor no Gateway
  — não é implementação do redesenho, só disponibiliza o que o redesenho
  vai precisar quando destravado.
- [ ] MEM-002 — LUNA compacta o próprio contexto de conversa usando a
  mesma fórmula de consolidação de memória (Memory Signals/Signal
  Engine, ver ADR-019), preservando um arquivo temporário completo (não
  compactado) para consulta/auditoria sob demanda — mesmo padrão
  observado no mecanismo de compactação do próprio Claude (resumo
  estruturado + transcript de backup acessível). Depende de o Signal
  Engine calcular sinais reais sobre um objeto genérico
  (`ConversationObject` em vez de `MemoryObject`) — não implementado
  ainda (registrado, ADR-019 Parte 0/3).
- [ ] GEN-001 — Adotar IDs estáveis por domínio em todo item de Roadmap/Framework
- [ ] REP-001 — Redefinir escopo do Reporter (propagação por evidência)
- [x] ~~INFRA-001 — Corrigir permissão do GitHub App~~ — correção (2026-07-18, ver BLD-003): confirmado resolvido (ver item correspondente em P1); registrado aqui só por consistência com o ID, não é trabalho novo sob o congelamento do P0.

## P1 — Pronto para concluir (Builder, sem decisão de Architects pendente)
- [x] ~~Configurar GROQ_API_KEY... — ativa model routing do PR #9~~ — correção (2026-07-13, ver ENG-005/BLD-001): o PR #9 só trazia infraestrutura sem consumidor; não havia capability para as env vars "ativarem" ainda. Implementadas agora: `model.chat`, `model.chat_deep`, `storage.query`, `storage.insert`.
- [x] ~~Aplicar o patch de `model.chat`/`model.chat_deep`/`storage.query`/`storage.insert` no luna-core (bloqueado: GitHub App conectado com "Contents"/"Pull requests" somente leitura nesta sessão — ver ENG-005)~~ — correção (2026-07-18, ver BLD-003): aplicado apenas `model.chat`/`model.chat_deep`, via `luna-core` PR #10 (mergeada em 2026-07-15). `storage.query`/`storage.insert` foram deliberadamente deixadas de fora — violam o Princípio 4 da Constitution (persistência deve rotear por Guardian/Hipocampo, nunca Gateway→Supabase direto); permanecem bloqueadas até o Architect decidir o redesenho (ver STOR-001, ENG-011). Configurar GROQ_API_KEY, DEEPSEEK_API_KEY, OPENROUTER_API_KEY, ANTHROPIC_API_KEY em luna-core/honest-joy (Railway) segue como pendência separada, fora do escopo desta sessão (ação de infraestrutura, sem acesso ao Railway) — sem essas credenciais `model.chat`/`model.chat_deep` continuam ausentes de `/api/gateway/capabilities` (design condicional, não bug).
- [x] ~~Ajustar permissão do GitHub App (Contents + Pull requests: Read and write) para viabilizar commits e fechamento de PR direto em sessões futuras~~ — correção (2026-07-18, ver BLD-003): confirmado resolvido — esta sessão comentou com sucesso em `luna-core` PR #3/#4/#5 (sem 403), ver evidência abaixo.
- [x] ~~Fechar PRs #3, #4 e #5 no luna-core (obsoletas, versão Python pré-ADR-004) — bloqueado pelo mesmo motivo de permissão~~ — correção (2026-07-18, ver BLD-003): as 3 PRs já estavam fechadas por Rubens diretamente em 2026-07-14 (comentário "arquivo obsoleto" em cada uma); esta sessão adicionou comentário de rastreabilidade referenciando ADR-004 em cada uma (2026-07-18).
- [x] ~~Corrigir tabela de classificação de sistemas em ECOSYSTEM_ARCHITECTURE.md e LUNA_CONTEXT.md (luna-core sai de "Legado/Experimental")~~ — correção (2026-07-18, ver BLD-003): já corrigido em 2026-07-12 (ver nota "Reclassificação" em ambos os documentos) — luna-core já aparece como "Infraestrutura, Órgão" na tabela de classificação atual de LUNA_CONTEXT.md §Sistemas, não mais em "Legado/Experimental"; a linha antiga é preservada explicitamente como snapshot histórico, não apagada.
- [ ] GEN-002 — Workflow de aplicação automática de ADRs via GitHub Actions, acionável pelo Forge (ver ADR-008). Movido de P2 para P1 em 2026-07-18: a decisão de caminho já foi tomada (ADR-008), o que resta é implementação, sem decisão de Architect pendente.
- [ ] GEN-006 — Painel lateral de navegador controlado (Playwright + Provider Router) na tela Workspace do Forge, com gate de aprovação para ações de risco óbvio (ver ADR-016, 2026-07-19). A decisão de caminho já foi tomada e ratificada pelo Architect — o que resta é implementação (Builder), sem decisão pendente.

## P2 — Requer decisão de Architects antes de execução
- [x] ~~Escolher caminho de delegação API+GitHub (GitHub Action com @claude / Claude Code headless em cron / Gateway próprio via API)~~ — resolvido por ADR-008 (2026-07-18, ver `ADR/ADR-008-GitHub-Genoma-Delegacao-Automatica-Forge.md`): caminho escolhido é GitHub Actions, acionável sob demanda pelo Forge. Implementação passa a ser GEN-002 em P1.
- [x] ~~Decidir futuro de luna-guardian /chat e /context (deprecar vs. redefinir)~~ — resolvido por ADR-012 (2026-07-19, ver `ADR/ADR-012-Consolidacao-Backend-luna-core-Interface-Convergia.md`): deprecadas e removidas de `luna-guardian` (commit `28c1c6e`) — o backend único de chat/contexto passa a ser `luna-core`, portado do monorepo `luna`.
- [ ] Escolher 1 dos 4 candidatos a Skill (auditoria de compliance, geração de ADR/checkpoint, assistente Reporter, scaffolding de capability)
- [ ] Formalizar a fronteira entre repo-interface e MVP acoplável: cada repositório é uma interface evolutiva, não o órgão em si
- [x] ~~Consolidar a decisão arquitetural sobre Convergia: portar a implementação real do monorepo luna para luna-convergia ou manter a arquitetura atual~~ — resolvido por ADR-012 (2026-07-19): nem um nem outro exatamente — o Convergia completo foi portado para `luna-core` (não para `luna-convergia`, que segue como esqueleto de 1 endpoint, órfão), com interface de usuário em `luna-frontend`. Decisão formal registrada no ADR, não a mesma alternativa binária que este item original enumerava.

## P3 — Genesis e coordenação do organismo
- [ ] Criar/atualizar os arquivos do Genesis para coordenação em tempo real: STATUS.md, HISTORY.md e TASKS.md — `STATUS.md` criado em 2026-07-22 (lista mestra de pendências, ver `GENESIS/STATUS.md`); `HISTORY.md`/`TASKS.md` seguem não criados, item continua aberto até os três existirem.
- [ ] Manter COORDINATION.md como barramento de memória de trabalho, sem virar memória permanente
- [ ] Fazer o Reporter atuar como gestor operacional: comparar proposto × executado e calcular percentual de conclusão
- [ ] Criar um Framework Curator para transformar aprendizados consolidados em Frameworks reutilizáveis
- [ ] ARCH-INV-001 — Reauditar e atualizar `GENESIS/ARCHITECTURE_INVENTORY.md`
  — documento de 2026-07-19, nunca atualizado desde então, apesar de
  mudanças reais confirmadas (ADR-012 no mesmo dia já resolveu o P1
  crítico que o inventário registra como aberto; toda a sessão de
  2026-07-22/23 não está refletida).
- [x] ~~DRIFT-001 — Reconciliar o histórico de migrations do Supabase
  (`jdbzhrtovpoaafpytgza`) com o que está versionado em
  `luna-core/supabase/migrations/`~~ — decisão do Architect (2026-08-05):
  **disciplina daqui pra frente, não reconciliação do passado.** Achado
  em 2026-08-02 (ver `luna-core` `BUILDER.md`, entrada CONV-002): o
  projeto já tinha 4 migrations aplicadas diretamente
  (`enable_rls_on_exposed_tables`,
  `enable_pgvector_and_add_embedding_column`,
  `create_hnsw_index_memoria_luna_embedding`,
  `create_semantic_search_function`) contra só 1 arquivo versionado no
  repo antes da migration de `convergia_template_positions` (a 2ª a
  virar arquivo). O Architect decidiu não reconstruir retroativamente
  esses 4 arquivos `.sql` — o banco funciona, a reconstrução histórica
  não vale o esforço agora; as 4 migrations anteriores a 2026-08-05
  permanecem sem arquivo correspondente, aceito como está, não pendência
  esquecida. Regra concreta para todo commit daqui pra frente registrada
  em `GENESIS/ENGINEER.md` ENG-036.

## P4 — Atividades de framework
- [ ] Confirmar com GPT/LUNA o paradeiro do frontend de mapeamento de campo ("bolhas") — não encontrado em nenhum repositório auditado
- [x] ~~Decisão de Architects: portar convergia/ do monorepo luna para luna-convergia (padrão ADR-004), ou manter arquitetura atual~~ — resolvido por ADR-012 (2026-07-19): portado para `luna-core`, não `luna-convergia` — ver nota equivalente em P2.
- [x] ~~Escrever ADR de migração do Convergia (Engineer), análogo ao ADR-004~~ — é o próprio ADR-012 (2026-07-19).
- [x] ~~CONV-001 — Upload de template visual (imagem/arquivo como plano de
  fundo do documento)~~ — concluído (2026-08-04): `luna-core` PR #29
  (commit de merge `8ebbcf2`) e `luna-frontend` PR #11 (commit de merge
  `736249b`), ambos mergeados em `main`. Decisão de escopo já
  ratificada antes da implementação: template visual é uma imagem
  (PNG/JPG) de fundo com campos posicionados por cima (reaproveitando
  `pptx-renderer.ts`/CONV-010), não upload de `.pptx`; persistência via a
  mesma coleção genérica do `GuardianContract` que CONV-002 já usa
  (nova coleção `convergia_visual_templates`, migration própria aplicada
  em `jdbzhrtovpoaafpytgza`). Verificado ponta a ponta — upload de
  imagem → catálogo unificado → editor abrindo sobre a imagem real →
  posições com fonte/tamanho salvas → `transform` → `.pptx` real aberto
  como zip, XML conferido campo a campo — contra o Guardian real de
  produção (`strong-celebration`) e via browser real (Playwright), a
  partir de um `luna-core`/`luna-frontend` locais rodando o código das
  duas branches; dados de teste removidos do Guardian depois. Ver
  `luna-core` `BUILDER.md`, entrada "2026-08-04 — CONV-001", para o
  relato completo — inclui um achado corrigido na própria sessão
  (`listAllTemplates()` derrubava o catálogo inteiro se o Guardian
  estivesse inalcançável, corrigido pra degradar) e a ressalva de que a
  verificação foi feita antes do deploy (o PR não estava em produção no
  momento do teste — `POST /convergia/templates/visual` contra
  `uvicorn-main-production` ainda respondia 404 então).
- [x] ~~CONV-002 (backend + editor) — Persistência de layout (posições
  de campo por template) e editor de arrastar/redimensionar~~ —
  concluído dos dois lados (2026-07-31, ver ENG-032 e correção de
  `luna-frontend` como "não verificado" abaixo): backend em `luna-core`
  PR #25, commit `60aa158` (`GET`/`PUT
  /convergia/templates/:id/positions`, `TemplatePositionStore`, coleção
  genérica do Guardian já citada acima). O front-end consumidor
  (`luna-frontend` PR #9, `components/forge/convergia-position-editor.tsx`)
  — que ENG-031 tinha marcado como "não verificado nesta sessão" por
  `luna-frontend` estar fora do escopo daquela sessão — foi verificado
  e mergeado em `main` numa sessão seguinte com os três repositórios
  anexados: `npm run typecheck` limpo, `npm run test:constitution`
  aprovado (46 arquivos), `npm test` 24/24, commit `7e5c230`. Nenhuma
  mudança de código foi necessária no front-end — o contrato já batia
  com a rota nova. Ambos os PRs mergeados em `main` nos respectivos
  repositórios. Ainda vale a ressalva já registrada: o editor só
  posiciona campos sobre templates pré-codificados do catálogo, não
  sobre um template visual enviado pelo usuário — isso dependia de
  CONV-001, que estava em aberto quando este parágrafo foi escrito.
  **Correção 2026-08-04:** CONV-001 está concluído (ver acima) — essa
  ressalva não vale mais, o editor já abre sobre imagem de fundo real.
  **Correção 2026-08-02 (ver `luna-core` `BUILDER.md`):** o `[x]` acima
  cobria só código mergeado dos dois lados — o recurso nunca tinha
  funcionado em produção, porque a tabela `convergia_template_positions`
  nunca tinha sido criada no Supabase (`GET`/`PUT
  /api/convergia/templates/:id/positions` retornava `400` real em
  produção, confirmado por logs do Railway). Fechado agora de fato:
  migration criada e aplicada (`20260802_convergia_template_positions.sql`,
  projeto `jdbzhrtovpoaafpytgza`), testado nesta ordem — Guardian direto
  contra `strong-celebration` (save/search/update/delete), API do
  Convergia contra `uvicorn-main` (`GET`/`PUT` → `200`, dado real
  persistido para `documento_tabular_generico_csv`), e a UI real do
  Forge (Rubens, clique real em "Salvar posições", mensagem "Posições
  salvas." confirmada por inspeção de DOM). CONV-002 está, agora sim,
  testado em produção via UI real — não só backend + frontend
  mergeados.
- [x] ~~CONV-010 — Leitura e posicionamento de imagem em PPTX (posição/
  dimensão/bytes)~~ — as duas metades concluídas: leitura (2026-07-30,
  `luna-core` PR #24, mergeado, commit `0f26320`) e escrita
  (2026-07-30, PR #25, mergeado, commit `60aa158`) — `pptx-parser.ts`
  extrai imagens por slide (`<p:pic>`, resolução via `.rels`),
  `pptx-renderer.ts` posiciona de volta (EMU→polegada,
  `sizing: contain` — nunca corta, sempre encolhe pra caber, regra do
  Architect aplicada na primitiva de renderização). `CanonicalRecord.
  images?` novo no Canonical Model, aditivo. Ver ENG-029/ENG-030 em
  `GENESIS/ENGINEER.md`. **Não confundir com CONV-009** (interpretação
  semântica de foto via LLM) — capacidades diferentes.
- [x] ~~CONV-011 — Normalização de identificador (RE) + motor de
  correspondência arquivo↔linha~~ — concluído (2026-07-30, `luna-core`
  PR #25, mergeado, commit `60aa158`, ver ENG-030):
  `src/convergia/matching/identifier.ts` (zero-pad a 6 dígitos, sempre)
  e `record-file-matcher.ts` (chave sem arquivo → `"missing"`, nunca
  trava o lote; chave com mais de um arquivo → `"ambiguous"`, nunca
  decide sozinho). Utilitário de apoio, ainda sem rota HTTP.
  **Correção 2026-08-04:** o texto original dizia "CONV-001/002/004
  continuam bloqueados por decisões abaixo" — CONV-001 e CONV-002 estão
  concluídos hoje; só CONV-004 segue não implementado, e não por
  decisão pendente, ver correção no próprio item CONV-004 abaixo.
- [x] ~~CONV-003 — Motor de preview — visualização prévia fiel ao
  documento final, antes de gerar/baixar~~ — **só escopo A**, decidido
  explicitamente como redução de escopo (Architect + Engineer), não a
  especificação original completa: preview instantâneo 100% client-side
  em CSS, só para templates visuais (imagem de fundo real, CONV-001) —
  sem chamar `/transform`, sem gerar `.pptx` real a cada ajuste.
  Concluído (2026-08-04, `luna-frontend` PR #12, commit de merge
  `ae56c2f`): cada campo
  ganha um "valor de exemplo" opcional; preenchido, a caixa no canvas
  passa a renderizar esse texto com `fontSize`/`fontFamily` reais do
  campo via CSS (conversão pt→`cqw`, baseada nos 720pt de largura do
  slide padrão do `pptxgenjs`, mesmo default de `pptx-renderer.ts`),
  sobreposto na imagem de fundo real — sem valor preenchido, continua
  mostrando o nome do campo. Verificado contra um template visual real
  (upload no Guardian real, dados removidos depois) e via browser real:
  dois campos com fonte/tamanho distintos (26pt Georgia, 14pt Verdana)
  renderizados visivelmente diferentes na tela.
  **Escopo B — preview gerando o `.pptx` real (ex. via LibreOffice) —
  não foi decidido nem implementado.** Não tratar este item como
  fechado no sentido mais amplo que a especificação original sugeria;
  "pixel-perfect" segue em aberto, sem decisão de quando/se será feito.
- [ ] CONV-004 — Motor de lote (batch) — geração explícita de múltiplos
  documentos a partir de múltiplos registros, com indicação de progresso.
  **Atualização 2026-08-04:** CONV-001 e CONV-003 (escopo A) estão
  concluídos — este item não está mais bloqueado por eles nem por
  decisão de arquitetura pendente. Continua simplesmente não
  implementado, sem especificação de interface própria ainda
  (reconstruir essa especificação não é escopo desta atualização).
- [ ] CONV-005 — Renderizador de PDF — hoje só existem CSV/HTML/JSON/
  Markdown/PPTX/XLSX
- [x] ~~CONV-006 — Decisão do Architect: a aba "Conhecimento" (treinamento
  do Guardian/Hipocampo) permanece dentro do painel Convergia, ou migra
  para painel próprio~~ — decisão tomada (2026-08-05): **separa.**
  "Conhecimento" deixa de ser aba dentro do painel Convergia e vira
  painel próprio no Forge. Decisão registrada aqui, implementação (código
  em `luna-frontend`) ainda não feita — vira tarefa de Builder separada,
  não parte desta entrada.
- [ ] CONV-007 — Gerar relatório/checklist de auditoria a partir de
  documentos enviados via Convergia. **Atualização 2026-08-04:** CONV-001
  e CONV-003 (escopo A) concluídos, CONV-002 já estava concluído desde
  2026-08-02 — não está mais bloqueado por eles nem por decisão de
  arquitetura pendente. Segue não implementado; a única dependência real
  restante é CONV-004 (lote), que também está só "não implementado
  ainda", não bloqueado.
- [ ] CONV-008 — Acompanhamento de auditoria ao vivo, item por item,
  com evidência por item. Capacidade nova, sem especificação de
  interface ainda.
- [ ] Implementar templates reais dos 13 tipos de documento corporativo — deixa de ser "bloqueado por revisão de especialista": ADR-012 define que o conteúdo passa a ser alimentado via `/api/convergia/training` pelo especialista diretamente (mecanismo já portado), não mais uma revisão externa a esperar. **Nota 2026-08-04:** a exibição desses 13 tipos na aba Catálogo & Upload do Forge foi reorganizada por legibilidade (`luna-frontend` PR #12, commit de merge `ae56c2f`, mesma sessão de CONV-003) — agrupamento por categoria com cabeçalho de grupo em vez de duas colunas soltas com tag desalinhada, ordem alfabética, nota deixando claro que são tipos planejados, não clicáveis. Mudança só de apresentação — `CORPORATE_DOCUMENT_CATALOG` (`luna-core`) e o contrato de `/convergia/catalog` continuam intactos, este item de pendência (templates reais) não avançou.
- [x] ~~Convergia: renderer PPTX marcado como "parcialmente feito" em ECOSYSTEM_ARCHITECTURE.md~~ — correção (2026-07-19): a doc estava desatualizada, não o código. O renderer já era completo (título + tabela paginada, 18 linhas/slide) antes desta entrada; faltava rigor de teste (só buffer não-vazio). Endurecido em `luna-core` commit `fe5b354` (branch `claude/pptx-renderer-test-rigor`, PR aberto para `main`): teste abre o `.pptx` como zip real, lê XML dos slides, confere título/cabeçalho/valores com dados SSMA/ASO, mais teste de paginação. Ver ECOSYSTEM_ARCHITECTURE.md §Convergia para o texto completo. Templates reais dos 13 tipos de documento (item acima) seguem como pendência separada, não afetada por esta correção.
- [x] ~~ADR-012 Decisão 2: Interface de Convergia em `luna-frontend`~~ — concluído (2026-07-19, ver `GENESIS/BUILDER.md`): nova área "Convergia" no Forge (`components/forge/convergia-panel.tsx`), mesmo padrão visual/estrutural de `components/forge/` (Tabs, ScrollArea, Button), com o fluxo Catálogo & Upload → Transformação → Conhecimento consumindo `/api/convergia/{catalog,templates,parse,transform,training}` em `luna-core` — `luna-frontend` commit `673b29c` (`main`). Correção adicional no mesmo commit: `sendChatMessage`/`fetchOrganismContext` ainda apontavam para a base antiga de `luna-guardian` (rotas removidas pelo porte da Decisão 1) — atualizados para `LUNA_GATEWAY_BASE_URL` (`luna-core`), junto de `.env.example`/`DEPLOY.md`.
- [ ] luna-convergia: acoplar frontend (uma vez localizado) ao pipeline real
- [x] ~~Engineer: especificar Fluxo A do Sistema Sensorial (Playwright vs. Computer Use API)~~ — resolvido por ADR-016 (2026-07-19, ratificado pelo Architect no mesmo dia): Playwright (mãos) + Provider Router (decisor, papel de "Computer Use"), transporte via captura de tela periódica por WebSocket, gate de aprovação para ações de risco óbvio. Autenticação da sessão do Playwright em Railway/GitHub também resolvida na mesma conversa: login manual do Originador, sessão mantida via cookies, nenhuma credencial de terceiros armazenada. Implementação passa a ser GEN-006 em P1 (movido para `luna-core`/`luna-frontend`, decisão original mergeada em `luna` PR #20 e corrigida de lugar — ver ENG-020).
- [ ] Builder: implementar Fluxo A — acompanhamento de vídeos de curso organizados por tópico
- [ ] Builder: implementar Fluxo B — aplicação do conhecimento em sessões de projeto frontend
- [ ] Fluxo C (interrupção em tempo real): pendência sem prazo, fora deste ciclo
- [ ] CONV-009 — Interpretação de fotos (visão computacional via LLM).
  Nenhum adaptador do luna-core processa imagem hoje — nem Groq, nem o
  AnthropicHubConnector real (que só manda texto, embora a API da
  Anthropic suporte imagem nativamente). Interpretação de
  foto nasce com `provenance_state: "unverified"` (a leitura da IA
  sobre a imagem pode errar, mesmo a foto em si sendo evidência real) —
  mesma disciplina do ADR-014 Emenda 1, só que aplicada a imagem, não
  só texto. Promove a `corroborated` só depois de confirmação do
  Originador. Depende de: endpoint de upload de imagem (não existe
  hoje), decisão de armazenamento (base64 direto vs. objeto em
  storage), e escopo de uso real (fotos de auditoria: equipamento,
  ambiente, documento fotografado). `CONV-007`/`CONV-008`
  (relatório/checklist de auditoria e acompanhamento ao vivo) — quando
  esta nota foi escrita ainda não existiam como IDs rastreados neste
  roadmap; agora registrados, ver os dois itens logo acima. Ver
  `GENESIS/ENGINEER.md` ENG-028 para a ordem de prioridade sugerida
  entre estes itens.
  **Correção 2026-08-05 (ADR-021, reconciliação com
  `GENESIS/RESEARCH/convergia-spec-tecnica-consolidada.md`):** o
  caminho técnico original acima ("estender `AnthropicHubConnector`")
  está **superado** — a especificação consolidada recomenda **Qwen-VL
  via Groq**, provider já configurado em `luna-core`, evitando
  dependência de imagem via Anthropic. Não estender
  `AnthropicHubConnector`; usar o provider Groq já existente, com
  modelo da família Qwen-VL. Caso de uso real que finalmente justifica
  implementar esta capacidade: ADR-021 (ronda fotográfica), Fase 4 —
  ver `CONV-016` abaixo.
- [ ] CONV-012 — Pipeline assíncrono de ingestão de documento grande no
  Hipocampo (ex. cartilhas de treinamento, procedimento completo em
  PDF) — hoje só documento pequeno é ingerido via `/api/convergia/
  training`. Sem isto, não há como carregar procedimento real (NR, PGR)
  para a busca semântica que a Decisão 3/Fase 4 do ADR-021 depende.
  Existe pelo menos um arquivo real já disponível para quando este item
  for implementado: cartilha de treinamento de operador de empilhadeira
  (Manserv), hoje só acessível como arquivo enviado ao Engineer, não
  ingerida no organismo. Bloqueia `CONV-016` (ADR-021 Fase 4).
  **Nota 2026-08-10:** investigação iniciada nesta sessão (não
  implementação) — achado real: zero buckets de Supabase Storage
  existem no projeto hoje. Decisão do Architect: o worker deste pipeline
  roda como serviço separado no Railway, não dentro de `luna-core`.
  Continua `[ ]`, sem código novo.
- [x] ~~CONV-013 — ADR-021 Fase 1: Wizard PWA de coleta de ronda
  fotográfica (foto + campo + voz nativa + fila offline via IndexedDB
  com reenvio automático ao detectar rede — evento `online`, não
  Background Sync API), gravidade escolhida manualmente nesta fase. Não
  depende de infraestrutura nova de backend — service worker + fila
  offline são só front (`luna-frontend`). Ver ADR-021 Decisão 1.~~ —
  **concluído (2026-08-09/10), cobrindo a linha evolutiva inteira, não
  só a versão original:** Fase 1 (`POST /convergia/ronda`, wizard PWA)
  em produção, seguida da extensão de edição pós-envio
  (`PATCH /convergia/ronda/:id`, `luna-core`/`luna-frontend`), também em
  produção. **O desenho original de achado — uma entrada fixa por
  categoria de risco — foi depois superado, no mesmo período, por uma
  revisão de arquitetura completa** (achado vira lista dinâmica, sem
  categoria fixa como chave) — ver `CONV-018` logo abaixo, já mergeada e
  em produção nos dois repositórios. Este `[x]` reconhece que o wizard
  de coleta em si está entregue; o modelo de achado que ele usa hoje é o
  de `CONV-018`, não mais o de categoria fixa descrito no texto original
  acima.
- [x] ~~CONV-018 — Revisão de arquitetura de achado dinâmico (Luna-context.md,
  `GENESIS/RESEARCH/revisao-arquitetura-achado-dinamico-flags-foto.md`)~~
  — **concluído e em produção (2026-08-09/10), duas rodadas, mergeadas
  em `luna-core` e `luna-frontend`:**
  - **Rodada 1:** achado deixa de ser uma entrada fixa por categoria de
    risco e vira lista livre, endereçada por `id` próprio (não mais
    `categoria`); catálogo real de 8 flags individuais
    (`convergia_ronda_flags`, tabela nova, sem agrupamento em "Riscos
    Críticos"); sugestão gerada por consulta determinística a
    `controle_risco` real, no nível do controle específico, não da
    categoria de risco inteira; três formas de "+" (a partir de
    sugestão, repetir dentro do mesmo flag, duplicar achado já
    preenchido); foto original (não comprimida) preservada localmente
    em IndexedDB, sem envio ao servidor nesta rodada.
  - **Rodada 2:** leitura de risco na foto via `qwen/qwen3.6-27b`
    (Groq) como segunda fonte de sugestão (Fase 4 do ADR-021 original,
    integrada aqui em vez de fluxo separado — confirmado com chamada
    real contra produção antes da implementação, não assumido); correção
    humana sobre sugestão (de flag ou de foto) alimenta o Hipocampo
    (`memoria_luna`, `tipo: "convergia_correcao_sugestao"`).
  - **Não é a mesma coisa que `CONV-016`** (ver nota em `CONV-016`
    abaixo) — cobre só a leitura de foto como sugestão pontual, não a
    separação sensível/lógica nem a tokenização de cliente/local que
    `CONV-016` exige.
- [ ] CONV-014 — ADR-021 Fase 2: Geração do relatório a partir do
  coletado na Fase 1 (`CONV-013`), usando a segunda forma de entrada do
  Convergia (metadata + achados[] + encerramento, ADR-021 Decisão 2) —
  formato PPT no curto prazo, docx (`CONV-015` abaixo) como upgrade
  quando disponível. Depende de `CONV-013`.
  **Nota 2026-08-10:** a extensão do ADR-021 (`ADR/
  ADR-021-Extensao-Questionario-Painel-Gestao.md`, Decisão 3) redefine o
  escopo deste item — não é mais um formato único de relatório, são
  **dois modelos de saída coexistentes** (Detalhado, baseado em
  relatório real de auditoria SSMA; Visual, foto-primeiro, baseado em
  `.pptx` real de ronda 5S), mais densificação automática por IA ao
  trocar de modelo. Quando `CONV-014` for retomado, especificar contra
  essa versão da Decisão 3, não a especulação anterior (caixa de texto
  única) que ela substituiu.
- [ ] CONV-015 — Infraestrutura compartilhada: parser de PDF
  (`pdf-parse`, plano B `pdfjs-dist`) e renderer docx (lib `docx`, npm)
  — desbloqueia caso de uso ASO e o formato de saída editável
  prioritário do ADR-021 Decisão 4 (docx rebaixa PDF de prioridade).
  Infraestrutura pura, sem caso de uso específico embutido; não depende
  de nenhum outro item desta lista.
- [ ] CONV-016 — ADR-021 Fase 3+4 combinadas (Decisão 6 já incorpora
  Decisão 3 — gravidade nasce da mesma leitura diagnóstica da foto,
  fundamentada em procedimento, não de um passo separado): separação
  sensível/lógica alimentando `memoria_luna` com tokenização de
  cliente/local (nome de pessoa nunca entra, ADR-021 Decisão 5) +
  leitura de risco na imagem via Qwen-VL/Groq (`CONV-009`, caminho
  técnico corrigido acima) + embedding (`pgvector`/HNSW já em produção)
  + comparação com achados anteriores. `provenance_state: "unverified"`
  até confirmação do responsável pela ronda. Depende de `CONV-014` e de
  `CONV-012` (pipeline assíncrono — sem ele não há procedimento real
  ingerido no Hipocampo para a busca semântica fundamentar a leitura).
  **Nota 2026-08-05 (ver ENG-037):** a base de conhecimento de apoio
  (`biblioteca_risco`/`biblioteca_atividade`/`biblioteca_protocolo`/
  `controle_risco`/`risco_relacionado`) já está populada com dado real
  e cruzada (cargo↔risco↔treinamento) — não é mais dependência em
  aberto desta fase. Pendência de schema duplicado (`biblioteca_*` vs.
  a estrutura paralela `risco`/`atividade`/`treinamento`) segue em
  aberto, ver ENG-037.
  **Nota 2026-08-10 — não marcar como concluído:** `CONV-018` (achado
  dinâmico, Rodada 2) entregou uma fração pequena deste item — leitura
  de risco na foto como sugestão pontual, via `qwen/qwen3.6-27b`/Groq
  (não mais "Qwen-VL", nome real confirmado com chamada de teste contra
  produção), e correção humana persistida em `memoria_luna`. Isso **não**
  é a separação sensível/lógica completa nem a tokenização de
  cliente/local que este item exige — a leitura de foto de `CONV-018`
  vira só uma sugestão pré-preenchendo o formulário, confirmada e salva
  pelo humano como texto claro, sem nenhuma etapa de tokenização por
  trás. `CONV-016` continua em aberto, com as mesmas dependências de
  antes (`CONV-014`, `CONV-012`).
- [ ] CONV-017 — ADR-021 Fase 5: renderizador de PDF (`CONV-005`) e,
  depois, exportação BI real (hoje "BI" é só o estilo visual
  dashboard já validado — KPI cards + gráfico nativo, não exportação
  para Power BI). Fica por último de propósito — sem prazo, entra só
  quando fizer sentido de negócio.
- [ ] Extensão do ADR-021 — questionário por modelo (3 modelos
  extensíveis: Riscos Críticos, Procedimentos, 5S, catálogo em tabela
  não fixo no código) + painel de gestão (dashboard, lista filtrável,
  achados como Plano de Ação). Decisões registradas e as 3 pendências
  originais (P1-P3) resolvidas — ver `ADR/
  ADR-021-Extensao-Questionario-Painel-Gestao.md` — mas **sem ID de
  roadmap formal ainda**, deliberadamente: o painel de gestão não tem
  escopo técnico detalhado (Decisão 2 do documento é só desenho, nenhum
  código), e o questionário por modelo se sobrepõe parcialmente com
  `CONV-018` (achado dinâmico, já entregue) sem uma linha clara ainda
  de onde um termina e o outro começa. Nota cruzada aqui em vez de
  forçar um `CONV-0XX` prematuro — ID formal fica para quando o escopo
  técnico do painel de gestão for detalhado.

## P5 — Sistema de crescimento e sustentabilidade
- [ ] Definir Atrator AAAC — Sustentabilidade (renomeado de AAAB em 2026-07-19: AAAB já é o Atrator Cognitivo, ver ADR-009/LUNA_CONSTITUTION.md)
- [ ] Definir indicadores econômicos por MVP
- [ ] Definir telemetria econômica para o Reporter
- [ ] Conectar valor econômico ao Atrator Evolução
- [ ] Modelar o Sistema Metabólico da LUNA
- [ ] MEM-003 — Workflow de autoaperfeiçoamento via n8n: pesquisa
  contínua na web, infere e testa respostas alternativas contra o
  índice de confiabilidade (ADR-019), propõe correção — nunca aplica
  sozinho, sujeito ao Gate de Aprovação (Plano Mestre Galho 3, ainda
  não implementado). Depende de: Fatia 4/índice de confiabilidade em
  produção (já mergeado), Gate de Aprovação generalizado (não
  implementado ainda).
- [ ] Padronizar fontes contínuas de pesquisa e classificação automática de conteúdo
- [ ] Enviar conhecimento validado ao Guardian apenas após revisão do Reporter
- [ ] Garantir que cada MVP gere valor mensurável sempre que possível

## P6 — Arquitetura maior, sem prazo definido
- [ ] Connector Hub: adapters além do Supabase
- [ ] Extrair Hipocampo do Guardian para módulo próprio
- [ ] Implementar Sistema Imunológico Cognitivo (CIS)
- [ ] Tornar o Reporter funcional além do scanner básico
