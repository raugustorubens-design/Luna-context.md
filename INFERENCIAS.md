# Inferências da LUNA

Este arquivo registra inferências, hipóteses, padrões observados e recomendações arquiteturais da LUNA.

## Regras
- Não usar este arquivo para documentação operacional de repositórios específicos.
- Registrar inferências com evidências, contexto e nível de confiança quando possível.
- A migração futura para o Supabase deve preservar a estrutura e o histórico deste arquivo.

## Estrutura sugerida
- Data
- Tópico
- Inferência
- Evidências
- Confiança
- Implicações
- Próximas ações

---

## Entrada — 2026-07-11

**Data:** 2026-07-11

**Tópico:** Maturidade real do órgão Reporter (`Luna-reporter`) vs. descrição em `ECOSYSTEM_ARCHITECTURE.md`

**Inferência:** O `ECOSYSTEM_ARCHITECTURE.md` classifica o `Luna-reporter` como "Média (MVP funcional, escopo parcial)" e descreve um "scanner de GitHub real e funcional" com saída em `observations.json` no formato `{source, system, type, timestamp, payload}`. A leitura direta do código-fonte mostra maturidade menor: apenas a cadeia `main.py → client.py → repository_scanner.py` está de fato implementada e executando, produzindo `reports/repositories.json` com metadados básicos (`name`, `description`, `language`, `updated_at`, `private`, `default_branch`). O Observation Engine especificado na Constitution do próprio repositório (`docs/constitution/luna_constitution_v1.md`), responsável pelo formato `observations.json` citado na documentação do ecossistema, **não possui nenhuma implementação no código** — é especificação, não realidade.

**Evidências:**
- `src/github/activity_analyzer.py` — arquivo vazio (0 bytes)
- `src/ai/repository_analyzer.py` — arquivo vazio (0 bytes)
- `src/reports/json_report.py` — arquivo vazio (0 bytes)
- `src/reports/markdown_report.py` — arquivo vazio (0 bytes)
- Nenhum arquivo no repositório gera ou referencia `observations.json` — busca por `observations` e pelo formato `{source, system, type, timestamp, payload}` só retorna ocorrências dentro de `docs/constitution/luna_constitution_v1.md` (especificação), nunca em código
- `src/index.ts` + `src/reporter.ts` constituem um segundo pipeline, em TypeScript, desconectado do pipeline Python real: `buildHeuristicFindings()` retorna um achado fixo e hardcoded sobre o próprio `Luna-reporter`, sem ler repositórios de verdade
- `.github/workflows/reporter-discovery.yml` não invoca `main.py` — gera um markdown genérico e estático ("Discovery only", "No AI inference", "No persistence", "Next step: Add repository introspection"), desconectado do scanner funcional

**Confiança:** Alta — baseada em leitura direta do código-fonte completo do repositório (ZIP oficial), não em inferência sobre documentação.

**Implicações:**
- O Reporter não é, hoje, consumidor nem dependência do Gateway, do futuro Connector Hub, ou de qualquer outro órgão — não há contrato formal implementado em nenhuma direção.
- O formato de evento `{source, system, type, timestamp, payload}` permanece válido como **proposta** de contrato oficial de Eventos do ecossistema (conforme Entregável 4 do `ECOSYSTEM_ARCHITECTURE.md`), mas deve ser tratado como não implementado em lugar nenhum até prova em contrário — nem no Reporter, nem no monorepo `luna` (`AuditEvent` interno segue em formato próprio, incompatível).
- Documentação otimista sobre maturidade de um órgão pode levar a decisões arquiteturais equivocadas (ex.: assumir que um contrato existe e construir algo que depende dele) — reforça a regra "Descobrir → Integrar → Criar" também para leitura de documentação, não só de código.

**Próximas ações:**
- Ao planejar o Connector Hub, não assumir nenhuma integração pronta com o Reporter.
- Se o Observation Engine for priorizado no futuro, ele nasce como MVP próprio no roadmap (`Entregável 7` do `ECOSYSTEM_ARCHITECTURE.md`), não como pressuposto de algo já pronto.
- Revisar periodicamente se documentação e código convergem, aplicando o mesmo tipo de auditoria feita aqui a outros órgãos classificados como "funcionais" na documentação.
