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
Pendente — o texto desta seção foi cortado pela interrupção da mensagem que
o especificou (2026-07-17). Não preenchido para evitar Builder especificando
no lugar do Architect/Engineer (ver Regra 6). Reenviar o conteúdo completo
para persistir.
