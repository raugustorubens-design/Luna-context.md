# GENESIS

Genesis is the collaborative workspace for Architects, Engineer, Builder, and Reporter.

It is operational memory, not permanent memory.

## Purpose

- Track what was proposed.
- Track what was executed.
- Track status and completion.
- Track open questions.
- Track workplans generated from the Frameworks.

## Rules

1. Write short, factual entries.
2. Each participant updates only their own file.
3. Permanent knowledge must still pass through Guardian.
4. Genesis can generate status and work plans, but it is not the source of truth.
5. When an item is consolidated, it can be promoted to Framework, Inferência, ADR, or Context.
6. Nenhuma decisão é considerada persistida até existir como commit real no
   GitHub. Engineer (Claude, chat) e Architect (GPT) não têm acesso de
   escrita — apenas decidem e especificam. Builder é o único canal de
   persistência real, mesmo em sessões simultâneas com os outros papéis
   presentes. Builder não é mais definido como uma ferramenta única: é o
   agente de codificação designado no momento da execução — Claude Code
   como titular, com reserva automática (ver GEN-002 v2,
   `GENESIS/ENGINEER.md`) para outras ferramentas quando o titular não
   estiver disponível. Toda execução de Builder, seja qual for a
   ferramenta, se autoatesta em `BUILDER.md` identificando explicitamente
   qual agente executou — nunca uma entrada genérica sem essa
   informação.

## Files

- ARCHITECTS.md
- ENGINEER.md
- BUILDER.md
- REPORTER.md
- FORGE.md
- STATUS.md
- ROADMAP.md
- HISTORY.md
- RESEARCH/ (Research Hypotheses — ver ARCH-001)

## Current usage

Use Genesis to coordinate work in near real time and reduce noise before consolidation into permanent knowledge.