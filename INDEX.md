# INDEX — Mapa mestre da documentação da LUNA

Este documento aponta onde cada tipo de informação deve viver.

## Documentos principais

- `LUNA_CONSTITUTION.md` — regras permanentes do organismo.
- `LUNA_COGNITIVE_LEXICON.md` — vocabulário da arquitetura cognitiva (ECP, CIL, L-Cell, etc.), cruzado com o que já existe em ADR/código.
- `LUNA_CONTEXT.md` — contexto global, visão e estado atual.
- `ECOSYSTEM_ARCHITECTURE.md` — arquitetura de alto nível do ecossistema.
- `GENESIS/ARCHITECTURE_INVENTORY.md` — inventário canônico dos 7 repositórios (responsabilidades, dependências, conexões externas, ambientes, Railway/Vercel/Supabase), com evidência citada e status "Não confirmado" onde aplicável. Documento vivo — atualizar, não recriar.
- `GENESIS/ARQUITETURA_CONVERGIA.md` — mapa de entrada/processamento/persistência/saída do Convergia (4 caminhos de entrada, pipeline `luna-core`, 4 grupos de coleção via Guardian, 3 destinos de saída), registrado em 2026-08-07 a partir do estado real do código. Documento vivo — atualizar, não recriar.
- `CHANGELOG.md` — histórico de mudanças relevantes.

## Diretórios

- `ADR/` — decisões arquiteturais.
- `ORGANS/` — definição dos órgãos e suas responsabilidades.
- `CHECKPOINTS/` — marcos de evolução do organismo.
- `GENESIS/padroes/` — normas de design e cor da SMX (`PADRAO-SMX-DESIGN.md`, `PADRAO-SMX-CORES.md`).
- `GENESIS/pacotes/` — fila de pacotes de instrução para o Builder, commitados em vez de anexados por chat (ver `GENESIS/pacotes/README.md`).
- `GENESIS/achados-campo/` — defeitos descobertos em campo, com a medição que levou ao diagnóstico. Registro histórico — não reescrever para "atualizar".
- `GENESIS/decisoes/` — decisões operacionais tomadas em campo ou fora do ciclo formal de ADR, com a motivação registrada.
- `GENESIS/pendencias/` — o que ficou pendente ao fim de uma sessão/etapa, para a próxima retomar sem perder contexto.
- `GENESIS/patches/` — diffs aplicados, preservados como histórico de como uma correção de campo foi implementada.

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
| Art. AAAB.9 — Segurança Cognitiva como Sistema Imunológico (extensão do Atrator Cognitivo) | `LUNA_CONSTITUTION.md` |
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
| ADR-012 Consolidação do backend em `luna-core` + Interface de Convergia (Aceito) | `ADR/ADR-012-Consolidacao-Backend-luna-core-Interface-Convergia.md` |
| ADR-013 Índice Semântico do GENESIS (**RASCUNHO — não aplicado**, voto 2-1) | `ADR/ADR-013-Indice-Semantico-GENESIS.md` |
| Plano Mestre — Autoprogramação Aderente e Segura da LUNA (tronco, raiz, galhos 1-8, ordem de prioridade) | `GENESIS/PLANO_MESTRE.md` |
| ADR-014 Arquitetura Imunológica de Segurança Cognitiva (Aceito, ancorado em Art. AAAB.9) | `ADR/ADR-014-Arquitetura-Imunologica-Seguranca-Cognitiva.md` |
| ADR-015 Gestão de Segredos — nome no código, valor nunca no GitHub (Proposto) | `ADR/ADR-015-Gestao-de-Segredos-Env-Vars.md` |
| ADR-016 Sistema Sensorial, Fluxo A — navegador controlado pelo servidor, painel lateral no Forge, gate de aprovação (Aceito) | `ADR/ADR-016-Sistema-Sensorial-Fluxo-A.md` |
| ADR-017 Emenda ao Atrator AAAA — Verdade, Respeito à Decisão e Proibição de Engenharia Social (AAAA.1-5) (**Proposto — aguardando ratificação do Architect**) | `ADR/ADR-017-Emenda-Atrator-AAAA-Verdade-Respeito-Engenharia-Social.md` |
| ADR-018 Autoaperfeiçoamento via Ensino Ativo — índice de confiabilidade, AAAB como corroboração computável, `architect_teaching`, loop socrático via `trace` (**Proposto — aguardando ratificação do Architect**) | `ADR/ADR-018-Autoaperfeicoamento-Ensino-Ativo.md` |
| ADR-019 Fechamento Trilhas 1/2 (Memória e Decision Engine) — Memory Signals, Signal Engine, Consolidation Engine v1, Decision Engine v1 escopado (**Proposto** — documenta código já mergeado em `luna-core` PR #19) | `ADR/ADR-019-Signal-Engine-Decision-Engine-Fechamento.md` |
| Inferências registradas (auditoria de código, maturidade real de órgãos) | `INFERENCIAS.md` |
| Lista mestra de pendências (ENG-021 a ENG-028 e itens não numerados, entre sessões) | `GENESIS/STATUS.md` |
| Treinamento Adaptativo com Captura de Conhecimento Tácito (Research Hypothesis pronta para promoção a Theory, resultado de campo real fora da arquitetura LUNA) | `GENESIS/RESEARCH/luna-treinamento-adaptativo.md` |
| Relatório Fotográfico de Auditoria via Convergia (Theory — especificação completa, sem execução de campo; une CONV-001/003/005/007/009 num único fluxo) | `GENESIS/RESEARCH/luna-relatorio-fotografico-auditoria-convergia.md` |
| Editor de Layout do Convergia — Carteirinha/Certificado em Lote (Theory — especificação completa de CONV-002, 4 tipos de campo, faces por template, decisão de processar-sem-armazenar dado sensível) | `GENESIS/RESEARCH/luna-editor-layout-carteirinha-certificado.md` |
| Léxico da Arquitetura Cognitiva — vocabulário ECP/CIL/L-Cell/etc., cruzado com ADR/código existentes, termos de reconciliação em aberto marcados | `LUNA_COGNITIVE_LEXICON.md` |
| Convergia — Especificação Técnica Consolidada (arquitetura unindo os 3 documentos de Theory num modelo único: 6 tipos de trabalho, modelo de Sujeito de 3 chaves, NRs como banco de perguntas, formatos de saída; pronta para virar ADR) | `GENESIS/RESEARCH/convergia-spec-tecnica-consolidada.md` |
| Tabela de Gerenciamento de Riscos da LUNA Auto-Aplicada — **domínio Hipocampo/Signal Engine, não Convergia** (Theory — primeira operacionalização real de V(s)/outcome, nomenclatura ISO/IEC 23894+42001, formalização de A(t)/A_politica(t)/Crescimento(t)) | `GENESIS/RESEARCH/luna-tabela-risco-iso-outcome.md` |
| Arquitetura do Convergia — mapa de entrada (4 caminhos), processamento (`luna-core`), persistência (Guardian, 4 grupos de coleção) e saída (3 destinos, 1 implementado), registrado a partir do código real em 2026-08-07, inclui achado não resolvido sobre schema paralelo (`risco`/`atividade`/`treinamento`) | `GENESIS/ARQUITETURA_CONVERGIA.md` |
| ADR-021 Extensão — Questionário por modelo (3 modelos extensíveis: Riscos Críticos, Procedimentos, 5S), painel de gestão (novo, sem código ainda), templates multi-página enviados pela empresa para a Fase 2 (`CONV-014`) (**Pendências P1-P3 resolvidas — escopo técnico de Decisão 1/2 ainda por detalhar antes de instrução de Builder**); inclui o feedback do primeiro teste real em campo (2026-08-10/11): toda edição de TST vira memória (**sem escopo técnico ainda**), contagem de padrão já coberta pelo painel de gestão, e dois princípios permanentes (usuário final nunca vê nome de provedor de IA; relato escrito do TST é a fonte principal, não a leitura de imagem) | `ADR/ADR-021-Extensao-Questionario-Painel-Gestao.md` |
| Revisão de Arquitetura — Wizard de Ronda: Achado Dinâmico, Flags de Sugestão, Foto em Duas Resoluções (Research — **3 pendências reais em aberto** (catálogo de flags, mecanismo de "não se aplica", armazenamento de foto original); **muda arquitetura já implementada e em produção hoje** nos módulos de ronda de `luna-core`/`luna-frontend`, não é feature nova sobre base vazia) | `GENESIS/RESEARCH/revisao-arquitetura-achado-dinamico-flags-foto.md` |
| Padrão SMX de Design — método de extração/criação de sistema de design (banco de referências, dois modos, estrutura de `design-system.html`), norma para toda superfície visual de todo projeto SMX (Aceito) | `GENESIS/padroes/PADRAO-SMX-DESIGN.md` (adotado por `ADR/ADR-023-Padrao-SMX-Design.md`) |
| Padrão SMX de Cores — valores extraídos por medição da logo SMX e de três imagens de referência (quatro faixas, portão de matiz, orçamento de luz), norma para toda superfície visual de todo projeto SMX (Aceito, emenda parcial de ADR-022) | `GENESIS/padroes/PADRAO-SMX-CORES.md` (adotado por `ADR/ADR-024-Padrao-SMX-Cores.md`) |
| ADR-022 Padronização de Paleta e Redesenho (registro retroativo — Aceito, mergeado em 18/08 via PR `#37`) — paleta do Safety Walk promovida a paleta do produto; `/v2` e `/forge?layout=v2` ao lado das superfícies atuais; hierarquia de superfície emendada pelo ADR-024 | `ADR/ADR-022-paleta-e-redesenho.md` |
| ADR-025 (proposta) Leitura de foto acumulativa, com pergunta ao técnico — contexto por achado acumulado no cliente sem reenviar imagem já lida, pergunta opcional (nunca bloqueia) da LUNA ao técnico, par pergunta-resposta como dado de aprendizado (**Proposto — aguardando ratificação do Arquiteto**; emenda ADR-021 Decisões 6 e 9) | `ADR/ADR-025-Leitura-Acumulativa-de-Foto.md` |
| ADR-026 (proposta) LUNA Sense — órgão de observabilidade dentro do `Luna-reporter`: contrato de sinal único, núcleo determinístico com IA só na borda, observa mudança (não estado), propõe mas nunca grava direto, canal por urgência (painel/e-mail/WhatsApp conforme faixa de prazo, ratificada em 19/08); escopo inicial de um sinal só (prazo normativo vencendo) (**Proposto — aguardando ratificação do Arquiteto**) | `ADR/ADR-026-LUNA-Sense.md` |
| Canais e a idade da fonte — os três canais do LUNA Sense (e-mail formaliza, WhatsApp agiliza, painel divulga), por que idade absoluta de fonte é sinal fraco (só 3 casos legítimos: prazo normativo, idade relativa entre docs acoplados, divergência contra observação), e as faixas de prazo por tempo-de-ação (ratificado em 19/08) | `GENESIS/RESEARCH/canais-e-idade-da-fonte.md` |

**Nota:** `CHANGELOG.md`, `ORGANS/` e `CHECKPOINTS/` estão listados abaixo (seção "Diretórios") mas não existem neste repositório — divergência identificada e registrada em `LUNA_CONTEXT.md` ("Divergência estrutural adicional — Luna-context.md"), não corrigida aqui (decisão de produto: criar as pastas ou remover as referências).
