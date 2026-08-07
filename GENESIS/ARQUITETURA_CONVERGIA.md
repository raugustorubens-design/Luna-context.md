# Arquitetura do Convergia — Mapa de Entrada, Processamento, Persistência e Saída

Registrado em 2026-08-07, a partir de sessão de mapeamento com o
Architect. Não é proposta — é o estado real confirmado no código nesta
data. Se o código mudar depois, este documento pode ficar desatualizado
e precisa ser revisado, não tratado como verdade permanente.

## Visão geral (grafo mestre)

```
Entrada
   ↓
Processamento (luna-core / Convergia)
   ↓
Persistência (Guardian)
   ↓
Saída
```

Fluxo único, sem ramificação neste nível — cada estágio alimenta o
próximo.

## Entrada — 4 caminhos

| Caminho | O que é | Rota real |
|---|---|---|
| Wizard de ronda | Foto + achado, fila offline | `/ronda` (`luna-frontend`), `POST /convergia/ronda` (`luna-core`) |
| Upload de dado | Planilha/arquivo de origem | Catálogo & Upload, Convergia — aceita xlsx, csv, json, pdf |
| Template visual | Imagem de fundo pra posicionar campo | Aba Template Visual, Convergia — PNG/JPG |
| Treinamento | Texto que vira conhecimento | Aba Conhecimento, Convergia |

## Processamento — `luna-core`

Pipeline do Convergia: parser → validação → transformação → renderer.
Consulta a base de conhecimento (ver Persistência) quando a operação
precisa de contexto de risco real, não só transformar dado bruto.

## Persistência — Guardian (Princípio 4 da Constitution: único ponto de
persistência)

4 grupos de coleção, todas via Guardian, nunca acesso direto ao banco:

| Grupo | Coleções reais | Propósito |
|---|---|---|
| Templates e posições | `convergia_visual_templates`, `convergia_template_positions` | CONV-001/002 — imagem de fundo + campo posicionado |
| Rondas | `convergia_rondas` (ver nota abaixo) | Fase 1 do ADR-021 — coleta de campo |
| Base de conhecimento | `biblioteca_risco`, `biblioteca_atividade`, `biblioteca_protocolo`, `controle_risco`, `atividade_risco`, `risco_protocolo`, `risco_relacionado` | Planilha real de riscos + caderno de treinamento, cruzados por cargo/risco/treinamento |
| Memória de longo prazo | `memoria_luna` | Signal Engine (ADR-019) decide consolidar ou descartar |

**Nota (2026-08-07, mesmo dia deste documento, sessão posterior) —
`convergia_rondas` não existia como tabela física quando este mapeamento
foi registrado:** a coleção estava correta como *destino de código*
(`RondaStore`, `src/convergia/ronda/ronda-store.ts`, já gravava nela
desde o PR #35), mas a tabela física no Supabase nunca tinha sido
criada — mesmo padrão de lacuna já visto com `convergia_template_positions`
antes de CONV-002. Confirmado direto via `information_schema.tables`
(não suposição) numa sessão de correção urgente, depois deste documento
já estar escrito: o Wizard PWA (já em produção) teria falhado com
400/500 na primeira ronda real enviada. Tabela criada nessa mesma
correção (`luna-core`, `supabase/migrations/20260807_convergia_rondas.sql`,
aplicada ao vivo e testada ponta a ponta contra produção real — ver
`luna-core/BUILDER.md`, entrada "Fix urgente: tabela `convergia_rondas`
nunca existia no Supabase"). Este documento não estava errado sobre o
código; estava otimista sobre a infraestrutura por trás dele — registro
mantido aqui para não sugerir que a tabela já existia desde o
mapeamento original.

**Achado não resolvido, registrado aqui de propósito:** existe uma
estrutura paralela (`risco`, `atividade`, `treinamento`, sem prefixo
`biblioteca_`/`convergia_`) com integridade referencial real (FK) mas
conteúdo quase vazio/com linha de teste duplicada — mesmo padrão do
achado do `hipocampo-temp` (código órfão, nunca reconciliado com o
resto). Não tratar como parte funcional do sistema até isso ser
resolvido — decisão de qual schema é o correto fica para quando a Fase
4 do ADR-021 (`CONV-016`) virar código de verdade.

## Saída — 3 destinos, só 1 implementado hoje

| Destino | Estado |
|---|---|
| Documento gerado (download) | ✅ Implementado — pipeline Convergia completo, testado em produção |
| Painel de gestão (achados ao longo do tempo, filtrável) | ❌ Não implementado — decisão tomada em 2026-08-07 (sessão de mapeamento), inspirada em comparação real com Checklist Fácil (RZ2), ainda sem ID de roadmap formal (`CONV-0XX` a definir) |
| Aprendizado de longo prazo (`memoria_luna`, sensível/lógica separadas) | ❌ Não implementado — Fase 3 do ADR-021 |

## Decisões de estética registradas junto (rota `/ronda`, não o Forge)

- Tema escuro por padrão, claro por alternância manual (botão, não
  automático) — mesmo par de cores invertido: `#1E2761` (Midnight,
  reaproveitado do protótipo real do relatório) / `#F4F6FB` (branco
  gelo).
- Cores de classificação (Positivo/Atenção/Não Conformidade) idênticas
  entre wizard de coleta e relatório final: `#2E7D32` / `#E8A33D` /
  `#C62828`, extraídas do arquivo real do protótipo, não aproximadas.
- Forge mantém o tema dele como está — nenhuma mudança de estética
  cruza pro Forge nesta rodada.
