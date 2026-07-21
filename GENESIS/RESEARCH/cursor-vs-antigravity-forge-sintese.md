# Cursor vs. Google Antigravity — Síntese Final Aplicada ao LUNA Forge

Status: Pesquisa registrada (pipeline Hypothesis → Research → Theory →
ADR, ver `GENESIS/RESEARCH/README.md`)
Data: 2026-07-21
Proveniência: pesquisa em três passadas — ChatGPT Deep Research (duas
rodadas independentes), Gemini 3.1 Pro (correção/refinamento), Claude
(síntese final no hub de IAs) — consolidada e verificada contra o código
real do ecossistema LUNA pelo Engineer (chat).

---

## 1. Resumo executivo

A pesquisa em múltiplas passadas convergiu no mesmo diagnóstico: o LUNA
Forge não precisa importar arquitetura do Cursor ou do Antigravity,
porque já resolveu, em produção ou em ADR aprovado, os problemas mais
difíceis que ambos os produtos tentam resolver comercialmente (separação
de autoridade, governança de execução, percepção segura e memória
mediada). O trabalho real não é "adicionar features de agente", mas
**tornar observável, auditável e formalmente contratual** o que já
existe — GEN-002 precisa de estados explícitos e política tipada no
Connector Hub; ADR-014 precisa de artefatos visuais assináveis;
Guardian/Hipocampo precisam de objetos de memória estruturados. As únicas
capacidades genuinamente novas e não descritas em nenhum ADR existente
são o pacote de confiança de ponta a ponta (unificado como **Trust
Package**) e a supervisão operacional multiagente. O risco de depender de
uma plataforma-preview (Antigravity) reforça que o Forge deve extrair
padrões, não dependências.

**Verificação adicional contra o código real (Engineer, 2026-07-21):**
boa parte do que a pesquisa classificou como "esforço Alto" ou
"capacidade nova" já tem fundação real no `luna-core`, só não
completada — o que muda a estimativa de esforço de três itens da tabela
(ver seção 4).

---

## 2. Tabela final de recomendações (com correções de esforço/classificação)

| # | Recomendação | Classificação | Componente responsável | Esforço |
|---|---|---|---|---|
| 1 | Formalizar o **Trust Package** (objetivo → plano → contrato → pacote → diff → testes → autoatestação → evidências ADR-014 → aprovação → commit) | Capacidade nova | GENESIS + GEN-002 + Guardian | ~~Alto~~ **Alto/Médio** — já existe `GatewayAuditor`/`AuditSink` capturando eventos de capability com contexto e metadado; falta persistir (`InMemoryAuditSink` → Guardian), não criar do zero |
| 2 | Manter Builder como única autoridade de commit; converter `BUILDER.md` em contrato verificável | Já resolvido (reforço de contrato) | GEN-002 | Médio |
| 3 | Máquina de estados explícita do GEN-002 (`PROPOSTO → PLANEJADO → APROVADO → EM_EXECUÇÃO → AUTOATESTADO → AGUARDANDO_REVISÃO → APROVADO_PARA_COMMIT → COMMITADO`) | Extensão do GEN-002 | GEN-002 | Médio |
| 4 | Connector Hub como *policy enforcement point* | Extensão do Connector Hub | Connector Hub | ~~Médio~~ **Baixo/Médio** — a interface `GatewayAuthorizationPolicy` já existe em `src/gateway/auth/auth.ts`; hoje só tem uma implementação no-op (`AllowGatewayAuthorizationPolicy`, autoriza tudo). Falta preencher a lógica real, o ponto de encaixe já foi desenhado |
| 5 | Fallback OpenCode/Aider sob o mesmo contrato de execução | Extensão do GEN-002 | GEN-002 | Médio |
| 6 | Paralelismo com ownership e dependências explícitas | Extensão do GEN-002/GENESIS | GEN-002 + GENESIS | Alto |
| 7 | Artefatos visuais assináveis (ADR-014) | Extensão do ADR-014 | ADR-014 | Médio |
| 8 | Granularidade extra de origem do dado suspeito na quarentena | Extensão do ADR-014 (única contribuição genuína) | Guardian | Baixo |
| 9 | Reasoning Integrity operacionalizado (Reporter vs. precedentes) | Já resolvido em teoria (ADR-014 Parte III) — falta implementar | Reporter | Baixo |
| 10 | Memória causal reconstruível + detecção de contradição | Extensão da Parte V do ADR-014 | Guardian + Hipocampo | Alto |
| 11 | Painel operacional (Manager View próprio) | Capacidade nova | GENESIS + GEN-002 | Alto |
| 12 | Scheduler restrito a pacotes pré-aprovados | Capacidade nova — **requer decisão explícita do Architect**: ADR-008 já escolheu disparo "sob demanda", não agendado; um Scheduler muda essa premissa | GEN-002 + Connector Hub | Baixo |
| 13 | Política formal de reversibilidade/compensação por classe de ação | Extensão das Classes de Ação do ADR-014 | Connector Hub + Guardian | Médio |
| 14 | Orçamento por tarefa/agente/provedor | ~~Capacidade nova~~ **Extensão** — `src/luna/budget-manager.ts` já existe, controla volume de chamadas por provider hoje; falta granularidade por tarefa e dado de custo em $ (hoje só controla volume, não $) | GEN-002 + Connector Hub | Baixo |
| 15 | Arquitetura agnóstica de vendor (extrair padrões do Antigravity sem depender de preview) | Decisão estratégica | Governança do Forge | Baixo |

---

## 3. Plano de implementação em fases (dependência real)

**Fase 1 — Fundações de confiança:** Trust Package (agora com fundação
real via `GatewayAuditor`, falta persistência) + Builder como autoridade
única + `BUILDER.md` como contrato verificável.

**Fase 2 — Governança de execução e fronteira:** Estados do GEN-002 +
Connector Hub como policy enforcement point (agora com interface já
pronta, `GatewayAuthorizationPolicy`) + fallback OpenCode/Aider.

**Fase 3 — Percepção e segurança cognitiva:** Artefatos visuais do
ADR-014 + granularidade de origem na quarentena + Reasoning Integrity
operacional.

**Fase 4 — Memória causal e rastreabilidade:** Guardian + Hipocampo
reconstruindo decisão/invariante/evidência/falha/proveniência.

**Fase 5 — Supervisão e paralelismo:** Painel operacional + execução
paralela com ownership/dependências.

**Fase 6 — Autonomia estendida:** Scheduler (pendente de ratificação —
ver nota na tabela, item 12) + política de reversibilidade + orçamento
por tarefa (agora extensão do Budget Manager já existente, não capacidade
nova).

---

## 4. O que foi descartado por duplicar arquitetura já existente

- **"Quarentena cognitiva" / "Saúde cognitiva do projeto"** — o ADR-014
  já define os 8 estados do Guardian e a resposta em 4 níveis com
  de-escalonamento 2b. Mantida só a granularidade de origem como extensão
  legítima.
- **"Risk-aware execution graph"** — reformulação das Classes de Ação já
  especificadas no ADR-014.
- **"Memória causal reconstruível"** — extensão direta da Parte V do
  ADR-014, não mecanismo novo.
- **Nomenclatura duplicada** — "Trust Artifacts" e "Forge Trust Package"
  unificados sob **Trust Package**.
- **(Verificação de código, Engineer) "Connector Hub como policy
  enforcement point"** — a interface já existe (`GatewayAuthorizationPolicy`),
  não é conceito a introduzir, é implementação a completar.
- **(Verificação de código, Engineer) "Orçamento por tarefa/agente/provedor"**
  — `budget-manager.ts` já existe; reclassificado de capacidade nova para
  extensão.
- **(Verificação de código, Engineer) Trust Package como "capacidade
  nova" em esforço Alto puro** — o esqueleto de auditoria
  (`GatewayAuditor`) já existe; o esforço real é de persistência e
  composição, não de criação de mecanismo de zero.

## 5. Nota de governança (Engineer)

O item 12 (Scheduler) não deve avançar para implementação sem
ratificação explícita do Architect — o ADR-008 já decidiu que a execução
do Builder é acionada sob demanda pelo Forge, não agendada. Um Scheduler
muda essa premissa arquitetural; não é só um item de esforço baixo a
implementar, é uma decisão a tomar primeiro.
