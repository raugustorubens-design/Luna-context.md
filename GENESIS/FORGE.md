# FORGE

Owner: sessão multiagente, coordenada por projeto

## Definição de trabalho

Luna Forge é a interface operacional da LUNA — permite observar, operar,
evoluir e administrar todos os órgãos do organismo cognitivo. O Workspace
é um desses órgãos e deve oferecer, no mínimo, capacidades equivalentes às
melhores IDEs do mercado.

## Modelo de órgãos (Theory — não promovida à Constituição ainda)

Forge não é a IDE — é o cockpit da LUNA. A IDE é um órgão dentro dele.

```
FORGE
├── Workspace (Editor, Terminal, Git, Debug, AI Coding)
├── Memory
├── Reporter
├── Guardian
├── Runtime
├── Projects
├── Observability
└── Constitution
```

## Forge v0.1 — especificação técnica (Design Decision, não ADR)

Decisões de contrato do MVP. Registradas aqui, não em `ADR/`, porque ainda
são especificação de MVP — promover para ADR quando multiagente, Guardian
e Context Loader amadurecerem além do v0.1.

### Chat
Um agente ativo por vez (seletor GPT/Claude/Groq). Toda mensagem carrega
metadado de atribuição (agent, model, timestamp, project_id) mesmo com um
único agente ativo — prepara v0.2 (multiagente concorrente) sem retrabalho.

### Workspace v0.1
Integração fina com Claude Code (IDE-grade já existente), não
reimplementação de editor/LSP/terminal. Workspace nativo equivalente a
Cursor + VS Code é meta de longo prazo, item de roadmap separado
(FORGE-WORKSPACE-001), fora do escopo do v0.1.

Nota (2026-07-17): Editor (Monaco) e Terminal (xterm) já existiam em
luna-frontend antes desta implementação (confirmado no audit do
FORGE-MVP-01) — não são entrega do v0.1. O que o v0.1 endereça é apenas o
nó "AI Coding": FORGE-MVP-08A (Claude Activity Panel), visibilidade de
atividade do Builder via github.read_file, sem sessão embutida (sem PTY
real). Workspace com AI Coding em paridade com Cursor segue em
FORGE-WORKSPACE-001, sem prazo.

### Execution Metadata
Não é Operational Memory Layer (MEM-001, congelado). Todo item salvo carrega:

```yaml
id: <identificador estável>
content: <texto>
execution_metadata: { repository, branch, path, commit, owner }
project: <LUNA | RENASCER | SMX | ...>
saved_at: <timestamp>
```

### Storage Contract
Guardian nunca conhece Supabase diretamente — só o Storage Contract
(`retrieveMemory`, `persistMemory`). Troca de banco futura não muda chamador.

### GitHub
Botões commit/push/pull/branch sempre executam sob credencial única de
serviço (Builder), independente do agente ativo no chat.

### Reporter (manual)
Botão "Analisar Projeto" — gera pendências/concluído/roadmap/drift. Mesmo
escopo de ENG-007: verifica por evidência, nunca cria ou reprioriza item.

## ID: FORGE-001
Data: 2026-07-16
Tópico: Multiagente simultâneo — decidido, implementação adiada pro v0.2

Decisão: arquitetura de multiagente com prompt próprio por agente permanece
decidida (ver ENG-010 para requisitos técnicos), mas implementação é v0.2 —
v0.1 usa chat sequencial de agente único.
Status: decidido; implementação não iniciada, sem prazo definido.

## Backlog — Operational Intelligence
Ver GENESIS/RESEARCH/meta-cognitive-memory.md (já registrado, Research
Hypothesis, congelado por ARCH-001). Não duplicar como novo item.
