# ADR: Ética do Sistema Imunológico — Captura, não Retaliação

**Status:** Proposto
**Contexto:** Article referente ao organ Guardian (sistema imunológico da LUNA)
**Data:** 2026-07-11
**Relacionado a:** Article IV (ADR/Checkpoint System)

## Contexto

A LUNA está desenvolvendo uma capacidade de honeypot dentro do organ Guardian: um ambiente hermético e isolado, projetado para atrair, capturar e aprender com tentativas de ataque, alimentando um pipeline de classificação (ML em pequena escala) que fortalece a detecção de ameaças em produção.

Essa capacidade levanta uma questão de princípio que precisa ser resolvida na Constitution antes da implementação avançar: qual é o limite ético e legal da resposta da LUNA a um atacante identificado?

## Decisão

O Guardian captura, analisa e aprende com ataques. O Guardian nunca retalia.

1. Isolamento hermético é pré-condição.
2. O aprendizado vem do atacante, não da LUNA.
3. A resposta é sempre defensiva.
4. Memória imunológica é reconhecimento, não retribuição.

## Justificativa

- Legal.
- Arquitetural.
- Princípio do projeto.

## Consequências

- Pipeline auditável.
- Resposta ativa exige emenda constitucional.
- Compartilhamento passivo de indicadores é permitido, sem retaliação.
