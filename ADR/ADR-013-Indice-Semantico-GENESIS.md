# ADR-013 — Índice Semântico do GENESIS (RASCUNHO — não aplicado)

Status: Proposto, aguardando formalização (não é trabalho ativo agora)
Data: 2026-07-19
Decisor: voto 2-1 (Arquiteta e Engineer; Engineer concordou com a direção,
discordou do sequenciamento e da separação de sistema)
Contexto: Arquiteta propôs um grafo de conhecimento (camadas física/lógica/
semântica) substituindo o inventário plano hoje mantido manualmente
(`ECOSYSTEM_ARCHITECTURE.md`, `GENESIS/ARCHITECTURE_INVENTORY.md`). Esta
mesma sessão de auditoria encontrou, duas vezes, documentação não
revalidada divergindo silenciosamente da realidade — mais recentemente o
renderer PPTX marcado "parcial" em `ECOSYSTEM_ARCHITECTURE.md` quando já
estava completo (ver `GENESIS/BUILDER.md`, entrada 2026-07-19).

## Decisão (quando formalizado)

1. O índice semântico não é um sistema novo — é o Hipocampo/Memory Engine
   (ADR-010/ADR-011) aplicado reflexivamente aos próprios repositórios da
   LUNA, em vez de um mecanismo paralelo. Reutilizar antes de criar
   (Princípio 3).
2. Estrutura em três camadas (física/lógica/semântica), conforme proposto
   pela Arquiteta, como **formato de saída do Reporter** — não como
   substituição do Reporter.
3. Atualização incremental como padrão, com re-scan completo periódico como
   rede de segurança — o inventário desta sessão já provou 2 vezes que
   documentação não revalidada diverge silenciosamente da realidade (PPTX
   marcado "parcial" quando já estava completo).
4. Sequenciamento: não substitui nem atrasa a v1 do Reporter
   (`FORGE-MVP-07`, inventário simples, prova o loop
   botão→executa→atualiza doc). O formato de três camadas é a v2 da saída
   do Reporter, depois da v1 estar rodando de verdade.

## Não fazer antes disso

Nenhuma implementação do índice semântico antes do Reporter v1 (inventário
simples) estar funcionando ponta a ponta pelo menos uma vez.

## Status de aplicação

Nenhuma. Este ADR é um registro do rascunho da decisão, não uma decisão
formalizada — nenhum código, roadmap ou builder log foi alterado em função
dele. Ver "Não fazer antes disso" acima.
