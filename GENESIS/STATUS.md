# STATUS — Lista mestra de pendências

Consolidação de tudo que já foi identificado/especificado mas ainda não
confirmado como aplicado, para não se perder o fio entre sessões.
Arquivo anteriormente só anticipado em `GENESIS/README.md` §Files e no
Roadmap P3 ("Criar/atualizar os arquivos do Genesis para coordenação em
tempo real: STATUS.md, HISTORY.md e TASKS.md") — este é o primeiro
conteúdo real dele. `HISTORY.md` e `TASKS.md` seguem não criados.

Este é documento de coordenação (mesma natureza de `COORDINATION.md` —
memória de trabalho, não permanente): lista o que está pendente e seu
status atual; não substitui a especificação completa de cada item, que
mora em `GENESIS/ENGINEER.md`, nos ADRs ou no Roadmap quando existir.

**Gap identificado ao criar este arquivo:** ENG-021 a ENG-025 aparecem
nesta lista com tópico e status, mas nenhum deles tem uma entrada
completa em `GENESIS/ENGINEER.md` ainda — só ENG-026 e ENG-027 (adicionadas
junto com este arquivo) têm o registro completo. Não fabriquei o conteúdo
integral de ENG-021 a ENG-025 aqui porque só recebi o resumo (tópico +
status), não a especificação original — registrar isso é mais honesto do
que inventar detalhe que não foi de fato entregue.

## Tabela

| ID | Tópico | Status |
|---|---|---|
| ENG-021 | Gap do Convergia MVP (CONV-001 a CONV-006) | Pacote entregue, aplicação não confirmada. **Atualização 2026-07-31**: CONV-010/011 (imagem em PPTX, normalização/correspondência RE) concluídos; CONV-002 concluído dos dois lados (backend `luna-core` PR #25 + editor `luna-frontend` PR #9, ambos mergeados em `main`), mas só sobre templates pré-codificados — a experiência completa segue bloqueada por CONV-001 (upload real), que continua sem implementação, assim como CONV-003/004/006. **Atualização 2026-07-31 (2)**: bug de produção na validação de PPTX corrigido, `.ppt` suportado via conversão LibreOffice (pendência de infraestrutura no Railway antes de funcionar em produção), roteamento síncrono/assíncrono >20MB implementado (primeira peça da Capacidade 2, `luna-core` PR #26) — ver ENG-041 (numeração real no momento do merge deste PR, 18 dias depois de aberto — ver nota em `GENESIS/ENGINEER.md`). Ver `GENESIS/ROADMAP.md` P4 e `GENESIS/ENGINEER.md` ENG-029 a ENG-032 e ENG-041. **Atualização 2026-08-04**: CONV-001 concluído (`luna-core` PR #29 + `luna-frontend` PR #11, mergeados) — template visual (imagem de fundo real + campos posicionados, com fonte/tamanho configuráveis) funcionando, verificado contra Guardian real e browser real. CONV-002 (já concluído desde 2026-08-02, tabela criada em produção) segue válido. CONV-003 concluído só no escopo A (preview instantâneo em CSS, `luna-frontend` PR #12, mergeado) — escopo B (preview via `.pptx` real) não decidido nem implementado. Restam: CONV-004 (lote), CONV-005 (renderizador PDF), CONV-006 (decisão sobre aba Conhecimento), CONV-007 (relatório de auditoria — depende de CONV-004), CONV-008 (acompanhamento ao vivo) — nenhum bloqueado por decisão de arquitetura pendente ou por CONV-001, só não implementados ainda. `luna-core` PR #23 (mergeado na mesma sessão) também corrigiu 3 bugs reais de produção do Convergia (zeragem de memória, PPTX/PPTM na validação, planilha mesclada) — ver `GENESIS/ENGINEER.md` ENG-034. Ver `GENESIS/ROADMAP.md` P4 para o detalhe completo item a item. **Atualização 2026-08-05:** CONV-006 não é mais pendência de decisão — o Architect decidiu (separa: "Conhecimento" vira painel próprio no Forge, sai da aba dentro do painel Convergia). Decisão registrada, implementação ainda não feita (tarefa de Builder separada, `luna-frontend`). CONV-004/005/007/008 seguem como listado acima, não afetados por esta atualização. |
| ENG-022 | Chat sem histórico de conversas | Causa raiz confirmada, correção não implementada |
| ENG-023 | Ajuste de janelas do Workspace (painéis expansíveis) | Pedido reforçado, implementação não confirmada |
| ENG-024 | Terminal desconecta imediatamente | Diagnosticado (sem PTY real), sem correção |
| ENG-025 | Suspeita de alucinação por falta de contexto (FORGE.md) | Hipótese registrada |
| ENG-026 | Plano de investigação de grounding/alucinação | Avaliado, investigação a iniciar — ver `GENESIS/ENGINEER.md` |
| ENG-027 | Merge sempre com confirmação explícita, sem auto-merge | Decidido, prática já em uso — ver `GENESIS/ENGINEER.md`. **Atualização 2026-08-04**: `luna-core`/`luna-frontend` ganharam CI (`.github/workflows/ci.yml`) + branch protection em `main`; a decisão de merge manual em si não mudou, ver nota na própria entrada. |
| ENG-028 | Capacidade de visão registrada (CONV-009, interpretação de fotos) | Registrado no Roadmap P4, não especificado em detalhe, não iniciado — ver `GENESIS/ENGINEER.md` |
| — | Extensão do ADR-021 — Questionário gerado por modelo + Painel de gestão (Convergia) | Consolidação de sessão 2026-08-07/08 registrada; comparação com Checklist Fácil (RZ2) usada só como referência de estrutura de mercado, não de conteúdo (conteúdo vem da experiência/pesquisa própria do Architect) nem de estética (Forge mantém tema Midnight). **Decisão 1 — questionário por modelo, não fluxo fixo nem construção livre**: descartado fluxo fixo por categoria de risco (rígido demais) e construção 100% livre no chat da Luna (bloqueada por limitação técnica real — `runCognitiveEngine` não tem tool-calling, mesmo achado que já pausou `A(t)`/modo sombra, ligado a `FORGE-WORKSPACE-001`/ENG-038). Decidido: três modelos prontos e extensíveis como ponto de partida (não lista fechada em código) — Riscos Críticos (`controle_risco`/`atividade_risco`), Procedimentos (`biblioteca_protocolo`), 5S (checklist próprio); Luna sugere estrutura com dado real da categoria, pessoa revisa e sempre confirma antes de salvar (IA nunca grava sozinha, mesmo princípio de cautela do `A(t)` e da separação sensível/lógica do ADR-021 Decisão 5); catálogo de modelos deve ser tabela editável, não enum fixo. Estrutura de campo de referência (padrão "alerta preventivo" já elaborado pelo Architect) identificou 2 campos que faltam no wizard hoje — "desvio identificado foi tratado?" (status/ciclo de vida) e "responsável pela aprovação" (hierarquia) — ambos pertencem ao painel de gestão (Decisão 2), não à captura de campo. **Decisão 2 — painel de gestão (novo, sem código ainda)**: dashboard com contagem agregada de status ao longo do tempo (em andamento/atrasado/aguardando solução), lista filtrável (status/período/unidade) reaproveitada em telas diferentes, achados viram itens rastreáveis tipo Plano de Ação (aberto → em andamento → resolvido/atrasado). Ainda sem ID de roadmap formal (`CONV-0XX` a definir) nem escopo técnico detalhado. **Pendências — bloqueiam qualquer instrução de Builder para esta extensão até serem respondidas:** P1 (PT — Permissão de Trabalho: sistema só sinaliza "esta categoria exige PT", ou emite/aprova/arquiva a PT de verdade? muda o tamanho do trabalho em uma ordem de grandeza); P2 (passivo trabalhista: (a) repositório de documento por pessoa/cargo com alerta de vencimento, (b) base de referência de direito trabalhista consultável, ou (c) rastreamento de passivo jurídico real — processo, valor, prazo?); P3 (sequenciamento: esta extensão entra depois da fila já aprovada — Ctrl+V no Template Visual, cores de classificação, tema claro/escuro — ou prioridade diferente?). As três instruções já aprovadas antes desta sessão (Ctrl+V, cores de classificação, tema claro/escuro) não são afetadas e continuam valendo. Ver também `GENESIS/ARQUITETURA_CONVERGIA.md` para o mapa de entrada/processamento/persistência/saída que esta extensão amplia. |
| — | Recomendações da pesquisa Cursor/Antigravity (Trust Package, política do Connector Hub, etc.) | Só como pesquisa registrada, nunca formalizada em Roadmap — ver `GENESIS/RESEARCH/cursor-vs-antigravity-forge-sintese.md` |
| — | Honeypot (`luna-security-lab`) | Decidido, repositório nunca criado |
| — | Chave SSH/GPG do Atrator AAAA | Nunca gerada |
| — | Limpeza de repositórios (Front-View, projeto-renascer-backup, luna-convergia) | Decidido, aplicação não confirmada |
| — | ClaudeAdapter ainda stub (nunca ligado ao Connector Hub real) | Instrução entregue duas vezes, nunca aplicada |
| — | Sentidos Acoplados / GEN-006 (painel de navegador completo) | Especificado (ADR-016), implementação não iniciada |

## Next action (registrado em 2026-07-22)

Antes de abrir qualquer frente nova, revisar esta lista — prioridade
sugerida: ENG-027 primeiro (afeta a confiabilidade de todo o resto do
processo — já decidido, ver acima), depois ENG-022 (mais barato, resolve
algo visivelmente quebrado).
