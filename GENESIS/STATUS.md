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
| ENG-021 | Gap do Convergia MVP (CONV-001 a CONV-006) | Pacote entregue, aplicação não confirmada |
| ENG-022 | Chat sem histórico de conversas | Causa raiz confirmada, correção não implementada |
| ENG-023 | Ajuste de janelas do Workspace (painéis expansíveis) | Pedido reforçado, implementação não confirmada |
| ENG-024 | Terminal desconecta imediatamente | Diagnosticado (sem PTY real), sem correção |
| ENG-025 | Suspeita de alucinação por falta de contexto (FORGE.md) | Hipótese registrada |
| ENG-026 | Plano de investigação de grounding/alucinação | Avaliado, investigação a iniciar — ver `GENESIS/ENGINEER.md` |
| ENG-027 | Merge sempre com confirmação explícita, sem auto-merge | Decidido, prática já em uso — ver `GENESIS/ENGINEER.md` |
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
