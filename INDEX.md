# INDEX — Mapa mestre da documentação da LUNA

Este documento aponta onde cada tipo de informação deve viver.

## Documentos principais

- `LUNA_CONSTITUTION.md` — regras permanentes do organismo.
- `LUNA_CONTEXT.md` — contexto global, visão e estado atual.
- `ECOSYSTEM_ARCHITECTURE.md` — arquitetura de alto nível do ecossistema.
- `GENESIS/ARCHITECTURE_INVENTORY.md` — inventário canônico dos 7 repositórios (responsabilidades, dependências, conexões externas, ambientes, Railway/Vercel/Supabase), com evidência citada e status "Não confirmado" onde aplicável. Documento vivo — atualizar, não recriar.
- `CHANGELOG.md` — histórico de mudanças relevantes.

## Diretórios

- `ADR/` — decisões arquiteturais.
- `ORGANS/` — definição dos órgãos e suas responsabilidades.
- `CHECKPOINTS/` — marcos de evolução do organismo.

## Regra de uso

1. Sempre consultar este índice primeiro.
2. Nunca duplicar conteúdo entre documentos.
3. Cada assunto deve ter uma única fonte de verdade.
4. Referenciar outros documentos em vez de repetir conteúdo.

## Conteúdo atual

| Assunto | Local |
|---|---|
| Atrator AAAA — maior relevância da LUNA | `LUNA_CONSTITUTION.md` |
| Atrator AAAB — Atrator Cognitivo (peso inferior a AAAA) | `LUNA_CONSTITUTION.md` |
| Checkpoint GENESIS-ATTRACTOR-001 | `CHECKPOINTS/GENESIS-ATTRACTOR-001.md` |
| ADR Gateway + Connector Hub (Aceito, emendado por DA-001 — Guardian é órgão interno) | `ADR/ADR-002-Gateway-ConnectorHub.md` |
| ADR Porte do Gateway + migração de runtime do `luna-core` (Aceito) | `ADR/ADR-004-Portar-Gateway-Migrar-Runtime-luna-core.md` |
| ADR-005 Reporter via GitHub Actions + metacognição (Aceito) | `ADR/ADR-005-Reporter-GitHub-Actions-Metacognicao.md` |
| ADR-006 Hierarquia biológica — "Sistema Funcional" (Aceito) | `ADR/ADR-006-Hierarquia-Biologica-Sistema-Funcional.md` |
| ADR-007 Reporter memória persistente + evidência (Aceito) | `ADR/ADR-007-Reporter-Memoria-Persistente-Evidencia.md` |
| ADR-008 GitHub Actions como caminho de delegação, via Forge (Aceito) | `ADR/ADR-008-GitHub-Genoma-Delegacao-Automatica-Forge.md` |
| ADR-009 Emenda constitucional — Atrator AAAB (Aceito) | `ADR/ADR-009-Emenda-Constitucional-Atrator-AAAB.md` |
| ADR-010 Arquitetura canônica de memória, resolução MEM-001/STOR-001 (Aceito, emendado por ADR-011 — símbolos M/X, A/γ) | `ADR/ADR-010-Arquitetura-Canonica-Memoria-MEM-001-STOR-001.md` |
| ADR-011 Emenda de símbolos — M(t)/X(t), A(t)/γ(t) (Aceito) | `ADR/ADR-011-Emenda-Simbolos-M-X-A-Gamma.md` |
