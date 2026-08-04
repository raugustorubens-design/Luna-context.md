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
| ENG-021 | Gap do Convergia MVP (CONV-001 a CONV-006) | Pacote entregue, aplicação não confirmada. **Atualização 2026-07-31**: CONV-010/011 (imagem em PPTX, normalização/correspondência RE) concluídos; CONV-002 concluído dos dois lados (backend `luna-core` PR #25 + editor `luna-frontend` PR #9, ambos mergeados em `main`), mas só sobre templates pré-codificados — a experiência completa segue bloqueada por CONV-001 (upload real), que continua sem implementação, assim como CONV-003/004/006. Ver `GENESIS/ROADMAP.md` P4 e `GENESIS/ENGINEER.md` ENG-029 a ENG-032. **Atualização 2026-08-04**: CONV-001 concluído (`luna-core` PR #29 + `luna-frontend` PR #11, mergeados) — template visual (imagem de fundo real + campos posicionados, com fonte/tamanho configuráveis) funcionando, verificado contra Guardian real e browser real. CONV-002 (já concluído desde 2026-08-02, tabela criada em produção) segue válido. CONV-003 concluído só no escopo A (preview instantâneo em CSS, `luna-frontend` PR #12, mergeado) — escopo B (preview via `.pptx` real) não decidido nem implementado. Restam: CONV-004 (lote), CONV-005 (renderizador PDF), CONV-006 (decisão sobre aba Conhecimento), CONV-007 (relatório de auditoria — depende de CONV-004), CONV-008 (acompanhamento ao vivo) — nenhum bloqueado por decisão de arquitetura pendente ou por CONV-001, só não implementados ainda. `luna-core` PR #23 (mergeado na mesma sessão) também corrigiu 3 bugs reais de produção do Convergia (zeragem de memória, PPTX/PPTM na validação, planilha mesclada) — ver `GENESIS/ENGINEER.md` ENG-034. Ver `GENESIS/ROADMAP.md` P4 para o detalhe completo item a item. |
| ENG-022 | Chat sem histórico de conversas | Causa raiz confirmada, correção não implementada |
| ENG-023 | Ajuste de janelas do Workspace (painéis expansíveis) | Pedido reforçado, implementação não confirmada |
| ENG-024 | Terminal desconecta imediatamente | Diagnosticado (sem PTY real), sem correção |
| ENG-025 | Suspeita de alucinação por falta de contexto (FORGE.md) | Hipótese registrada |
| ENG-026 | Plano de investigação de grounding/alucinação | Avaliado, investigação a iniciar — ver `GENESIS/ENGINEER.md` |
| ENG-027 | Merge sempre com confirmação explícita, sem auto-merge | Decidido, prática já em uso — ver `GENESIS/ENGINEER.md`. **Atualização 2026-08-04**: `luna-core`/`luna-frontend` ganharam CI (`.github/workflows/ci.yml`) + branch protection em `main`; a decisão de merge manual em si não mudou, ver nota na própria entrada. |
| ENG-028 | Capacidade de visão registrada (CONV-009, interpretação de fotos) | Registrado no Roadmap P4, não especificado em detalhe, não iniciado — ver `GENESIS/ENGINEER.md` |
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
