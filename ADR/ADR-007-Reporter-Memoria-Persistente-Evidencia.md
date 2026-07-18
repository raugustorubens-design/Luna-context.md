# ADR-007 — Reporter como Memória Arquitetural Persistente + Evidência antes de Intervenção

Status: Aceito (redigido em sessão anterior; redraft aplicado em 2026-07-18)

## Contexto

O Reporter precisa acumular conhecimento arquitetural ao longo do tempo sem
virar fonte de verdade paralela ao GENESIS, e sem disparar intervenções por
inferência não verificada.

## Decisão

- O Reporter mantém memória persistente de observações.
- Toda intervenção arquitetural proposta pelo Reporter exige evidência
  objetiva (commit / PR / deploy / teste) antes de ser aceita.
- Autoria de Framework/Pendências/Plano de trabalho continua humana +
  Engineer + Architect; o Reporter apenas confirma o que já existe
  ("eu confirmei", nunca autoria própria).
