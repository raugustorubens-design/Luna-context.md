# Arquitetura do Ecossistema LUNA — Documento Oficial

Status: Consolidado
Data: 2026-07-09
Este documento é a fonte de verdade da arquitetura do Ecossistema LUNA. Substitui qualquer entendimento de "monorepo único" como identidade padrão dos sistemas. Produzido inteiramente a partir de auditorias já realizadas nesta mesma linha de trabalho — nenhum repositório foi re-clonado ou re-lido do zero para este documento; onde a informação já existia, foi reaproveitada.

Este é o último prompt macro da arquitetura. Toda evolução futura ocorre por MVPs independentes (ver Entregável 7).

---

## Entregável 1 — Mapa Oficial do Ecossistema

### Sistemas com repositório próprio

| Sistema | Objetivo | Responsabilidade principal | Estado atual | Maturidade | Relação com o organismo |
|---|---|---|---|---|---|
| **luna** (monorepo) | Núcleo cognitivo executável da LUNA | Hospedar o Cognitive Engine e os órgãos fortemente acoplados a ele; superfície de integração via Gateway | Ativo, único runtime real testado ponta a ponta | Alta (dentro do seu escopo) | É o organismo em si — cérebro + sistema de integração, não um órgão isolado |
| **Luna-context.md** | Continuidade e memória de longo prazo do ecossistema | Fonte de verdade da estratégia, decisões e princípios entre repositórios | Ativo, atualizado no mesmo dia desta consolidação | Alta (como documento) | Infraestrutura de continuidade — não é código, é o "córtex de longo prazo" compartilhado |
| **Luna-reporter** | Consciência situacional do organismo | Observar GitHub/Supabase/Railway, diagnosticar bloqueadores, recomendar próxima ação de maior impacto | Ativo — scanner de GitHub real e funcional; Supabase/Railway ainda não implementados | Média (MVP funcional, escopo parcial) | Órgão oficial "Reporter" — independente por desenho, não por acidente |
| **luna-convergia** | Origem do órgão de transformação de documentos | Parsing de XLSX + regra de negócio ASO (SSMA) | Absorvido fisicamente dentro de `luna` (`src/convergia/`); repositório original preservado, não deletado | Baixa como repo próprio hoje (código evoluiu no monorepo) | Órgão com identidade própria pré-existente; candidato prioritário a voltar a ser independente quando houver contrato de API |
| **luna-frontend** | Protótipo visual do "rosto" da LUNA | UI de dashboard cognitivo, terminal de chat, painel de observabilidade | Protótipo estático (Next.js, ~130 linhas de componentes, majoritariamente mockado) | Baixa/experimental | Candidato a frontend oficial, não confirmado nem integrado a nenhum backend real |
| **Luna-API** | Protótipo antigo de backend HTTP | Chat com memória (`memoria_eventos`) + leitura de arquivo do GitHub | Estagnado (último commit "Add debug logging"); tem bug real (`const pool` redeclarado — não executa) | Legado, não funcional no estado atual | Duplicata histórica de `apps/api` no monorepo; nenhum dos dois tem consumidor confirmado |
| **luna-core** | Protótipo antigo de backend Python | FastAPI + Supabase, endpoint `training_modules` | Ativo — último commit "force deploy" sugere instância real em produção | Média (funcional, mas sem uso confirmado) | Duplicata quase idêntica de `apps/core` no monorepo (Procfile/requirements idênticos) |
| **Front-View** | Frontend histórico pré-monorepo | UI original da LUNA, hospedada no Replit | Superado — absorvido manualmente no `luna` monorepo (`luna_checkpoint.json`: "integração manual do frontend Front-View") | Legado | Historicamente relevante, funcionalmente substituído; não reauditado nesta etapa (informação reaproveitada, não reverificada) |
| **projeto-renascer** | Pretendia ser o frontend oficial da LUNA | — | Artefato de geração automática falho: commit único, payload `[object Object]`, página de erro estática | Quebrado / não é um produto | Evidência de uma capacidade de geração de repositórios ("Luna Dev") cujo código-fonte não foi localizado em nenhum repositório auditado |
| **projeto-renascer-backup** | Backup do projeto acima | — | Idêntico em natureza ao original | Quebrado / não é um produto | Mesmo status |

> **Atualização — 2026-07-12 (ADR-004, execução concluída):** a linha de `luna-core` acima é o snapshot da auditoria de 2026-07-09 e é preservada como histórico, não apagada. Desde então, ADR-004 foi aceito e executado (`luna-core` PR #6 e PR #7, ambos mergeados): `luna-core` deixou de ser o protótipo Python/FastAPI descrito acima e passou a hospedar o Gateway (portado do monorepo `luna`, 17 capabilities) e o Connector Hub (Supabase, GitHub, Groq, DeepSeek, OpenRouter) como órgãos coabitando o mesmo runtime Node/TypeScript. Não é mais "duplicata quase idêntica de `apps/core`" nem "sem uso confirmado" — é o destino de deploy real do Gateway, confirmado ao vivo em produção (`/api/gateway/capabilities` responde com as 17 capabilities). Ver a nota de fechamento em `LUNA_CONTEXT.md` para a execução completa.

### Órgãos internos do monorepo `luna` (sem repositório próprio)

| Órgão | Objetivo | Responsabilidade principal | Estado atual | Maturidade |
|---|---|---|---|---|
| Gateway | Superfície de execução de capacidades do organismo | Registro, autorização, auditoria e execução de capacidades (GitHub, Filesystem; Railway e n8n preparados e desabilitados) | Ativo, 19 capacidades registradas, testado | Alta |
| Cognitive Engine | Orquestração da cognição | Coordena retrieveMemory → Context Hub → Provider Router → Hipocampo, sem persistir ou chamar provider diretamente | Ativo | Alta (fronteiras verificadas por teste automatizado) |
| Hipocampo | Decisão de consolidação de memória (inclui Filtro Cognitivo) | Filtra conteúdo vazio/duplicado, delega persistência ao Memory Engine | Ativo, v1 determinística | Média (fórmula completa referenciada como ADR-003 — **Missing Reference**, ADR-003 não existe na pasta ADR/; ver ADR-010 §6. Fonte de verdade vigente para a fórmula é ADR-010.) |
| Memory Engine | Persistência e recuperação de memória | Único módulo autorizado a tocar Supabase (`memoria_luna`) | Ativo | Média (retrieval é só recência, sem semântica) |
| Provider Engine | Registro de modelos de IA | 5 adapters registrados (Groq real; ChatGPT/Claude/Grok/Manus honestamente "não configurado") | Ativo | Baixa (só 1 de 5 providers funcional) |
| Provider Router | Seleção e fallback entre providers | Itera providers configurados, checa orçamento, faz fallback real em falha | Ativo | Média (critério de seleção é só disponibilidade, não custo/qualidade/latência real) |
| Budget Manager | Controle de volume de chamadas por provider | Limite diário configurável via env, sem dados de custo em $ | Ativo | Baixa (v1 mínima, sem preço real) |
| Índice Cognitivo | Reconstrução do contexto evolutivo do projeto | Leitura determinística de `luna_context/*.md` | Ativo | Baixa (reconstrução lógica only; semântica ausente) |
| Context Hub | Contexto único compartilhado por todo provider | Monta identidade + estado do projeto + memórias + roadmap | Ativo | Média |
| "Reporter" interno (`src/luna/reporter.ts`) | Log de auditoria do pipeline cognitivo | Buffer de 200 eventos em processo | Ativo | Baixa como órgão — **não é o Reporter oficial** (ver Conflito abaixo) |
| Filtro Cognitivo | Regra de filtro antes de consolidar conhecimento | Vive dentro do Hipocampo (decisão ADR-003) | Ativo (v1) | Baixa |
| Planner | — | Sem responsabilidade definida em nenhum documento, monorepo ou externo | Não existe | N/A — bloqueado |
| LUNA Forge | IDE cognitiva tipo Cursor ("Modo Dev") | Editor, chat, Git, execução Python, observabilidade — per `Luna-context.md` | Não existe (nem código, nem repositório) | N/A — planejado |
| Convergia (dentro do monorepo) | Transformação de informação em documentos/conhecimento | Pipeline de 8 estágios: Entrada→Parser→Modelo Canônico→Validação→Transformação→Template→Renderer→Resultado | Ativo, testado, verificado em produção real | Média-alta (3/5 parsers, 6/7 renderers, 1 template de conteúdo real) |
| apps/core (dentro do monorepo) | — | Cópia estática de `luna-core` | Sem consumidor confirmado | Órfão |
| apps/api (dentro do monorepo) | — | Cópia estática de `luna-api`, com os mesmos bugs | Sem consumidor confirmado | Órfão |

### Conflito de identidade — dois "Reporters" (reafirmado do ADR-004)

O Reporter oficial do organismo é `Luna-reporter` (repositório próprio). `src/luna/reporter.ts` é um log de auditoria interno ao pipeline cognitivo do monorepo — nome coincidente, responsabilidade diferente. Não renomeado ainda (ação registrada no roadmap, Entregável 7).

---

## Entregável 2 — Classificação

Um sistema pode ter mais de uma classificação simultânea.

| Sistema/Órgão | Classificações | Justificativa |
|---|---|---|
| luna (monorepo) | Sistema, Infraestrutura | Hospeda o núcleo cognitivo E a superfície de integração entre órgãos internos |
| Luna-context.md | Shared Kernel, Infraestrutura | Não é código executável; é o contrato de continuidade que todo sistema deve consumir |
| Luna-reporter | Sistema, Órgão, MVP, Produto (candidato) | Responsabilidade única e real; escopo ainda parcial (só GitHub); tem potencial comercial próprio |
| luna-convergia (repo) | Órgão, Legado (como repo), MVP (como código no monorepo) | Repositório original preservado mas não é onde o código evolui hoje |
| Convergia (no monorepo) | Órgão, MVP, Produto (candidato) | Responsabilidade única (transformação de documentos); testado; falta só contrato de API para virar produto independente de novo |
| luna-frontend | Experimental | Protótipo visual sem integração backend confirmada |
| Luna-API | Legado, Experimental | Não executa no estado atual (bug de redeclaração); sem consumidor confirmado |
| luna-core | Infraestrutura, Órgão (hospeda Gateway + Connector Hub) — *classificação anterior até 2026-07-09: "Legado, Infraestrutura (possível)", preservada como histórico* | Atualizado 2026-07-12: pós-ADR-004, `luna-core` hospeda o Gateway (portado, 17 capabilities) e o Connector Hub (Supabase/GitHub/Groq/DeepSeek/OpenRouter), confirmado ao vivo em produção. A justificativa de 2026-07-09 ("função `training_modules` não ligada a nenhum órgão oficial") não se aplica mais — esse endpoint foi removido junto com o runtime Python que o hospedava |
| Front-View | Legado | Superado, funcionalmente substituído |
| projeto-renascer / backup | Experimental, Legado | Artefato quebrado, sem valor de produto |
| Gateway | Órgão, Shared Kernel (padrão), Infraestrutura | Único órgão cujo *padrão* (Capability/Manifest/Registry) já é reconhecidamente reutilizável por design |
| Cognitive Engine, Hipocampo, Memory Engine, Provider Engine/Router, Budget Manager, Índice Cognitivo, Context Hub, Filtro Cognitivo | Órgão | Fortemente acoplados entre si; sem valor de produto isolado; nenhuma classificação de "Produto" se aplica hoje |
| "Reporter" interno | Biblioteca | Utilitário interno de log, não um sistema com responsabilidade própria no organismo |
| Planner, LUNA Forge | — (ainda não classificável) | Não existem; qualquer classificação seria especulação |
| apps/core, apps/api (monorepo) | Legado, Órfão | Cópias sem consumidor confirmado; candidatos a remoção pendente de decisão de produto |

---

## Entregável 3 — Mapa de Dependências

### Matriz (quem consome / de quem depende / quem nunca deve acessar diretamente)

| Sistema | Quem pode consumi-lo | De quem depende | Quem nunca deve acessá-lo diretamente |
|---|---|---|---|
| Memory Engine | Hipocampo (escrita), Cognitive Engine (leitura) | Supabase (`memoria_luna`) | Qualquer sistema que não seja Hipocampo, para **escrita** — Cognitive Engine e Convergia só podem escrever através do Hipocampo |
| Hipocampo | Cognitive Engine, Convergia (via knowledge-gate) | Memory Engine | Nenhum sistema deve persistir contornando o Hipocampo |
| Provider Router | Cognitive Engine | Provider Engine, Budget Manager | Convergia (por desenho — hoje 100% determinística), Gateway |
| Provider Engine | Provider Router apenas | Adapters de provider (Groq real; demais não configurados) | Qualquer chamada direta a um adapter de provider, fora do Router |
| Budget Manager | Provider Router apenas | Nenhuma dependência externa | Qualquer sistema que decida "rotear" sem consultar o orçamento primeiro |
| Context Hub | Cognitive Engine | Índice Cognitivo | Provider adapters (não devem montar contexto sozinhos) |
| Índice Cognitivo | Context Hub, Convergia (inferência de treinamento) | Sistema de arquivos local (`luna_context/*.md`) | — |
| Gateway | Clientes HTTP externos (GPT Action, futuro Forge) | GitHub API, filesystem local; Railway/n8n (desabilitados) | Nenhum órgão interno hoje o consome programaticamente (zero import cruzado confirmado) |
| Convergia | Clientes HTTP (`/api/convergia/*`) | Hipocampo, Memory Engine (**ver inconsistência abaixo**), Índice Cognitivo | Provider Engine/Router (nenhuma chamada de IA no MVP atual, por desenho) |
| "Reporter" interno | Cognitive Engine, Hipocampo, Provider Router, Convergia (todos emitem eventos) | Nenhuma dependência externa | — |
| Luna-reporter (externo) | Nenhum consumidor confirmado hoje | GitHub API (real); Supabase, Railway (planejados) | — |
| Luna-context.md | Toda sessão/agente que trabalha em qualquer repositório LUNA | Nenhuma dependência | Não deve ser tratado como opcional por nenhum sistema |

### Inconsistência encontrada ao montar esta matriz (registrada, não corrigida)

`src/convergia/training/training-to-memory.ts` chama `checkpoint()` do Memory Engine **diretamente**, sem passar pelo Hipocampo. `checkpoint()` internamente executa `persistMemory()` — ou seja, é uma operação de persistência real. A verificação automatizada existente (`architecture-check.mjs`) não capturou isso porque só procura os tokens `supabase|drizzle` no código do Convergia; `checkpoint()` não contém esses tokens, então passou despercebido.

Isso é uma violação sutil da regra "Convergia nunca pode persistir diretamente" estabelecida no Prompt 3. Não corrigida nesta etapa (restrição explícita: não implementar, não mover código). Registrada como ação prioritária no roadmap (Entregável 7) e como regra futura de teste na Constituição Executável.

---

## Entregável 4 — Contratos Oficiais (especificação, não implementação)

| Contrato | O que define | Estado de implementação | Quem deveria consumi-lo |
|---|---|---|---|
| **Context Hub Contract** | Shape do contexto compartilhado: identidade, missão, estado do projeto, contexto evolutivo, tarefas abertas, roadmap, memórias, atratores cognitivos, refs de sincronização | Implementado dentro do monorepo (`LunaContext`); nunca publicado como contrato externo | Todo provider, todo órgão que gera resposta — e, no futuro, Forge e Convergia-como-serviço |
| **Canonical Model** | Shape de dado formato-agnóstico para transformação de informação: título, colunas, registros, metadados | Implementado dentro do Convergia (`CanonicalDocument`); escopo hoje é só Convergia | Qualquer sistema futuro que transforme dados estruturados (não só Convergia) |
| **Eventos / Observations** | Formato padrão de evento observável do organismo | **Dois formatos incompatíveis existem hoje**: `AuditEvent` interno (`{name, at, evidence}`) e `observations.json` do Luna-reporter (`{source, system, type, timestamp, payload}`) | Todo sistema que precise reportar estado observável — recomenda-se adotar o formato do Luna-reporter como oficial, por já cobrir múltiplas fontes |
| **Provider Contract** | Interface `ProviderAdapter`: id, isConfigured(), execute() | Implementado, testado, com 5 adapters registrados | Qualquer sistema que precise de IA — nunca deve chamar um provider fora deste contrato |
| **Memory Contract** | persistMemory / retrieveMemory / checkpoint + shape `LunaMemoryRecord` | Implementado, com injeção de dependência para teste | Hipocampo (escrita); qualquer órgão (leitura) |
| **Identity** | `LunaIdentity {name, mission}` | Implementado de forma mínima | Hoje só o Context Hub; precisa expandir para cobrir voz/marca consistente entre Convergia, Forge, luna-reporter |
| **Auth** | — | **Não especificado em lugar nenhum do ecossistema.** Gateway tem uma política de autorização allow-all (`AllowGatewayAuthorizationPolicy`) | Lacuna real — nenhuma identidade de serviço, nenhum token entre sistemas está definido |
| **APIs compartilhadas** | OpenAPI 3.1 (`apps/frontend/lib/api-spec/openapi.yaml`) | Existe, mas escopo é só o monorepo | Precisa se tornar um padrão que cada sistema independente publique a própria spec, descobrível centralmente |

---

## Entregável 5 — Shared Kernel

**O que pertence:**

- As *interfaces* dos contratos do Entregável 4 (não as implementações) — `LunaContext`, `ProviderAdapter`, `ConsolidationCandidate`/`ConsolidationDecision`, `CanonicalDocument`, `AuditEvent`/Observation, `CapabilityManifest`/`Capability`.
- O padrão Capability/Manifest/Registry do Gateway — já reutilizado 1x fora do Gateway original (GitHub+Filesystem) e preparado para Railway/n8n; é o único padrão do ecossistema com reuso comprovado.
- O padrão de "constituição executável" (script de verificação de fronteira por varredura recursiva de diretório + regras de proibição de token) — já reutilizado 3x (Cognitive Engine/Hipocampo, Convergia, e aplicável ao Gateway).
- `LUNA_CONTEXT.md` (o oficial, neste repositório) — toda continuidade do ecossistema depende dele.

**O que NÃO pertence (justificativa: evitar crescimento desnecessário):**

- Implementações concretas de adapter (GroqAdapter, GithubRestAdapter, parsers/renderers do Convergia) — são substituíveis, organ-specific, e colocá-las no kernel criaria acoplamento desnecessário.
- Qualquer lógica de negócio (regra SSMA do Convergia, filtro do Hipocampo) — pertence ao órgão dono, não ao núcleo.
- `luna_context/LUNA_CONTEXT.md` (a cópia dentro do monorepo) — é um registro derivado, não fonte de verdade; não deve ganhar status de kernel para não competir com o repositório oficial.

---

## Entregável 6 — APIs Públicas por Sistema (especificação)

| Sistema | APIs públicas | Eventos publicados | Eventos consumidos | Contratos utilizados |
|---|---|---|---|---|
| Gateway | `GET /api/gateway/capabilities`, `POST /api/gateway/execute` | `capability.requested/executed/failed/dryrun` (auditoria interna, não exposta externamente) | nenhum | Capability/Manifest |
| Cognitive Engine (via HTTP) | `POST /api/chat`, `GET/POST/DELETE /api/conversations*`, `GET /api/stats` | eventos internos do Reporter (`cognitive_engine.*`, `memory.*`, `provider_router.*`, `hipocampo.*`) — não expostos externamente | nenhum | Context Hub, Memory, Provider |
| Convergia | `GET /api/convergia/catalog`, `GET /api/convergia/templates`, `POST /api/convergia/parse`, `POST /api/convergia/transform`, `POST /api/convergia/training` | nenhum evento externo hoje | nenhum | Canonical Model, Memory (via Hipocampo) |
| Luna-reporter | nenhuma API HTTP — execução via script (`src/main.py`), saída em `reports/*.json` | `observations.json` (formato candidato a contrato oficial de Eventos) | GitHub API | nenhum contrato formal do ecossistema ainda — é o produtor original do formato de evento |
| luna-frontend | N/A (é o consumidor, não o provedor) | — | — | nenhum confirmado (não há chamada de API real identificada na leitura feita) |
| luna-core | `GET /`, `GET /health`, `GET /api/gateway/capabilities`, `POST /api/gateway/execute` — atualizado 2026-07-12 (ADR-004); até então (histórico): `GET /`, `GET /health`, `GET /modules` (`/modules` removido junto com o runtime Python) | — | — | Capability/Manifest (mesmo contrato da linha "Gateway" acima — o Gateway daquela linha, descrito em 2026-07-09 como interno ao monorepo sem deploy próprio, agora responde a partir daqui) |
| Luna-API | `GET /`, `GET /api/github/file`, `POST /chat` | — | — | nenhum |

---

## Entregável 7 — Roadmap Oficial (cada item é um MVP independente)

### Forge (não iniciado)
- [ ] MVP: Editor — capacidades básicas de edição de código, integração com Filesystem capability do Gateway
- [ ] MVP: Chat — interface de conversa ligada ao Cognitive Engine via API já existente
- [ ] MVP: Git — capacidades já existem no Gateway (11 capabilities GitHub); Forge precisa só de UI
- [ ] MVP: Python — execução de bibliotecas Python, escopo ainda não definido

### Convergia
- [x] MVP: Parser XLSX — feito (evoluído do `luna-convergia` original)
- [x] MVP: SSMA (transformação/normalização ASO) — feito
- [x] MVP: Memória (integração com Hipocampo/Memory Engine) — feito, com a inconsistência do `checkpoint()` direto registrada acima
- [ ] MVP: DOCX (parser + renderer) — não iniciado, precisa de modelo de documento em árvore/seções
- [ ] MVP: PPTX — correção de documentação (2026-07-19): esta linha estava desatualizada. O renderer (`luna-core/src/convergia/renderers/pptx-renderer.ts`) já estava completo antes desta correção — título + tabela paginada (18 linhas/slide), registrado em `renderers/registry.ts` — não "parcialmente feito" como descrito. O que era real e faltava era rigor de teste: a suíte só checava buffer não-vazio, sem abrir o arquivo. Corrigido (`luna-core` commit `fe5b354`, branch `claude/pptx-renderer-test-rigor`, PR aberto para `main`): teste agora abre o `.pptx` como zip real (`jszip`), lê o XML dos slides e confere conteúdo (título, cabeçalho, valores), com dados no padrão SSMA/ASO — mais um teste de paginação (25 registros → 3 slides). Segue incompleto **apenas** quanto a templates de conteúdo reais para os 13 tipos de documento corporativo — mesma pendência que já existia, não específica do PPTX (ver item de templates abaixo e `GENESIS/ROADMAP.md` P4).
- [ ] MVP: PDF (parser + renderer) — não iniciado
- [ ] MVP: cada um dos 13 tipos de documento corporativo catalogados (APR, PGR, DDS, etc.) — catalogados, nenhum com conteúdo real; cada um é seu próprio MVP futuro, dependente de validação de especialista SSMA

### Hipocampo
- [x] MVP: Consolidação (filtro de conteúdo vazio/duplicado) — feito, v1 determinística
- [ ] MVP: Compactação semântica (não apenas concatenação/truncamento) — não iniciado
- [ ] MVP: Reconstrução semântica (embeddings) — não iniciado, depende de decisão de infraestrutura (pgvector ou equivalente)
- [ ] MVP: corrigir a chamada direta de `checkpoint()` pelo Convergia, passando a rotear pelo Hipocampo — prioritário, baixo esforço

### Provider Engine
- [x] Groq — único provider real e funcional hoje
- [ ] MVP: OpenAI (ChatGPT) — adapter existe como stub "não configurado"
- [ ] MVP: Claude (Anthropic) — idem
- [ ] MVP: Grok — idem
- [ ] MVP: Qwen — não iniciado, requer decisão de infraestrutura open-source
- [ ] MVP: DeepSeek — não iniciado, idem
- [ ] MVP: Whisper — não iniciado, idem (voz/áudio)
- [ ] MVP: Gemma — não iniciado, idem
- [ ] MVP: Manus — adapter existe como stub "não configurado" (não citado no exemplo do prompt, mas já presente no organismo)

### Reporter
- [x] MVP: scanner de GitHub — feito, em `Luna-reporter`
- [ ] MVP: adapter Supabase — planejado na própria constituição do `Luna-reporter`, não iniciado
- [ ] MVP: adapter Railway — idem
- [ ] MVP: Diagnostics Engine, Recommendation Engine, Report Engine completos — arquitetura especificada na constituição, implementação parcial (scanner + relatório JSON/Markdown existem; diagnóstico/recomendação automatizados não confirmados)
- [ ] MVP: renomear/desambiguar `src/luna/reporter.ts` do monorepo, para não colidir de identidade

### Gateway
- [x] MVP: capability pack GitHub — feito
- [x] MVP: capability pack Filesystem — feito
- [ ] MVP: capability pack Railway — contrato preparado (`status: disabled`), implementação real não iniciada
- [ ] MVP: capability pack n8n — idem
- [ ] MVP: autorização real (substituir `AllowGatewayAuthorizationPolicy`) — prioritário para qualquer capability destrutiva ir a produção real

### Memory Engine / Índice Cognitivo / Context Hub
- [ ] MVP: persistência durável do log de auditoria (Reporter interno) — hoje é só em memória
- [ ] MVP: reconstrução semântica do Índice Cognitivo — mesma dependência de infraestrutura do Hipocampo
- [ ] MVP: expandir Identity contract além de `{name, mission}`

---

## Entregável 8 — Estratégia Comercial

| Pergunta | Resposta |
|---|---|
| Quais sistemas podem tornar-se produtos independentes? | **Convergia** (geração de documentos SSMA/compliance — mercado real, já validado pelo caso de uso original de ASO); **Luna-reporter** (inteligência de repositório/observabilidade — mercado adjacente a ferramentas de engenharia); **LUNA Forge** (IDE cognitiva — maior potencial, mas também maior concorrência: Cursor, Windsurf, etc.) |
| Quais dependem do organismo? | Cognitive Engine, Hipocampo, Memory Engine, Provider Engine/Router, Budget Manager, Context Hub, Índice Cognitivo, Filtro Cognitivo — nenhum tem valor comercial isolado; só existem como o "cérebro" da LUNA |
| Quais podem gerar receita individualmente? | Convergia (preço por documento gerado, ou assinatura por equipe SSMA); Luna-reporter (assinatura por repositório/organização monitorada); Forge (assinatura por usuário, modelo Cursor-like) |
| Quais devem permanecer internos? | Gateway, Budget Manager, Provider Router — são infraestrutura de controle de custo/integração, não algo que um cliente compra separadamente. Exceção especulativa de longo prazo: o *padrão* do Gateway (Capability/Manifest) poderia um dia virar uma plataforma de integração própria, mas isso é além do horizonte deste roadmap |

---

## Entregável 9 — Arquitetura de Longo Prazo

**Como o organismo evolui durante anos sem perder identidade:**
1. Contratos (Entregável 4) são a única superfície de acoplamento permitida entre sistemas com repositório próprio — nunca import direto entre repos.
2. Cada sistema mantém seu próprio README/constituição/testes — identidade não pode ser reconstruída de fora.
3. `Luna-context.md` (este repositório) é a fonte de verdade única; cópias locais (como `luna_context/LUNA_CONTEXT.md` no monorepo) existem para conveniência operacional, mas divergência é sempre resolvida a favor do oficial e sempre registrada, nunca ocultada.
4. Descobrir → Integrar → Criar aplicado a cada prompt futuro, sem exceção — a lição concreta desta própria consolidação é que pular a etapa de descoberta (5 repositórios encontrados tarde) gera retrabalho real, não apenas risco teórico.

**Princípios que impedem crescimento caótico:**
1. Todo novo trabalho nasce como um MVP do tamanho listado no Entregável 7 — nunca como um "prompt macro" (este é o último).
2. Nenhum órgão é criado sem antes provar ausência real da capacidade (regra já em vigor desde o Prompt 2).
3. Toda regra arquitetural relevante nova vira teste (ver Constituição Executável abaixo) — arquitetura que não é testável tende a ser violada sem ninguém perceber, como a inconsistência do `checkpoint()` encontrada nesta própria etapa.
4. Auditorias de ecossistema completo (não só do monorepo) devem ter cadência — a alternativa é descobrir repositórios relevantes por acidente, como ocorreu aqui.

**Princípios que preservam compatibilidade entre sistemas:**
1. Contratos versionados quando virarem pacotes publicáveis — mudança incompatível exige nova versão, não edição silenciosa.
2. O padrão Capability/Manifest do Gateway é o modelo de referência para qualquer integração heterogênea futura (Railway, n8n, e eventualmente entre sistemas com repositório próprio).
3. Nenhuma fusão física de sistemas por conveniência de implementação — esta é a lição central que motivou o ADR-004 e este documento.

---

## Constituição Executável — regras futuras (não implementadas nesta etapa)

| Princípio consolidado | Teste futuro necessário |
|---|---|
| Convergia nunca persiste diretamente, nem via `checkpoint()` | Estender `architecture-check.mjs` para proibir qualquer chamada a `memory-engine.ts` que não seja através de `hipocampo.ts` — hoje só a leitura de tokens `supabase\|drizzle` é verificada, não a topologia de chamadas |
| Contratos compartilhados não quebram silenciosamente | Contract tests: cada sistema consumidor de um contrato publicado deve rodar, em CI, uma verificação de compatibilidade contra a versão vigente do contrato |
| Nenhuma capability do Gateway executa sem autorização real | Teste de fronteira que falhe caso `AllowGatewayAuthorizationPolicy` (ou equivalente allow-all) ainda esteja em uso quando uma capability tiver `requiresApproval: true` |
| Eventos do ecossistema seguem um formato único | Validação de schema (JSON Schema) garantindo que todo evento publicado por qualquer sistema seja compatível com `{source, system, type, timestamp, payload}` |
| `src/luna/reporter.ts` não deve ser confundido com o Reporter oficial | Teste/lint que impeça o nome "Reporter" de aparecer como label de órgão oficial em documentação gerada automaticamente a partir do monorepo, até a desambiguação (renomeação) ocorrer |
| Nenhum órgão novo nasce sem MVP explícito no roadmap | Checklist obrigatório (não testável por CI, mas por processo): todo novo item de código no monorepo deve corresponder a uma linha do Entregável 7 antes de ser aceito |

---

## Registro de divergência entre os dois LUNA_CONTEXT.md

Nenhuma divergência de conteúdo foi encontrada entre `luna_context/LUNA_CONTEXT.md` (monorepo) e `LUNA_CONTEXT.md` (este repositório) até a data deste documento — o monorepo já registrava, em sua seção 10, a mesma reclassificação de órgãos consolidada aqui. Este documento (`ECOSYSTEM_ARCHITECTURE.md`) é o primeiro artefato que existe **somente** no repositório oficial, por desenho — evita duplicar um documento extenso em dois lugares e criar risco de divergência futura. O monorepo mantém apenas um ponteiro resumido.
