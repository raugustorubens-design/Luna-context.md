# Research Hypothesis — Meta-Cognitive Memory

Status: Research Hypothesis. Não é implementação, não entra em Roadmap.
Registrado por ARCH-001 (`GENESIS/ARCHITECTS.md`, 2026-07-16).

## Hipótese

Uma camada de memória sobre qual agente/estratégia funciona melhor por tipo
de problema — não memória sobre conteúdo (o que já é escopo da Operational
Memory Layer, MEM-001, também congelada), mas memória sobre desempenho e
seleção de agente/estratégia ao longo do tempo.

## Por que não é implementação agora

ARCH-001 congela toda proposta de arquitetura nova até o Forge v0.1 estar em
uso diário (ver `GENESIS/ARCHITECTS.md`). Meta-Cognitive Memory depende de
volume real de execução do Forge para ter dados a aprender — não pode ser
especificada com rigor antes disso.

## Próxima ação

Nenhuma até o critério de congelamento de ARCH-001 ser levantado. Quando
levantado, promover para especificação técnica (padrão MEM-001) antes de
qualquer código.
