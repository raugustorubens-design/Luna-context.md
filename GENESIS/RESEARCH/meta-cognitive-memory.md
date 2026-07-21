# Meta-Cognitive Memory — Research Hypothesis

Status: Research Hypothesis. Não implementar — depende de ENG-007 (Reporter
em modo evidência) já estar funcionando com dados reais antes de fazer
sentido implementar. Registrado por ARCH-001 (`GENESIS/ARCHITECTS.md`,
2026-07-16).

## A ideia

A resposta de um agente de IA não é o produto final — é matéria-prima. A
LUNA extrai padrão (problema → solução → evidência → resultado) em vez de
só guardar a resposta.

## Quarta camada de memória proposta

```
Memory
├── Semantic
├── Episodic
├── Operational
└── Meta-Cognitive (novo)
```

Meta-Cognitive registra: qual agente foi usado, qual estratégia, qualidade
da resposta, tempo, correções necessárias, aceitação do usuário, impacto.

## Posicionamento estratégico

Os provedores de IA evoluem em inteligência geral; a LUNA evolveria em
inteligência operacional sobre o uso desses modelos — complementar, não
concorrente aos provedores.

## Por que está congelada

Motivada por ARCH-001 (congelamento). Também depende tecnicamente de
Reporter maduro (ENG-007) para ter dado real de "qual agente resolveu
melhor" — não há como implementar antes disso.
