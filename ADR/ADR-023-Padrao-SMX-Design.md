# ADR-023 — Padrão SMX de Design

Status: Aceito
Data: 2026-08-17
Decisor: Architect (Rubens)
Contexto: Engineer — a partir do padrão descrito em
`GENESIS/padroes/PADRAO-SMX-DESIGN.md`

## Contexto

Interfaces vinham sendo desenhadas sem referência extraída, e o resultado
divergia entre superfícies. O caso concreto que expôs o problema, em 17/08:
o trabalho de redesenho do produto (ver ADR-022,
`ADR/ADR-022-paleta-e-redesenho.md`) propôs Archivo em largura
expandida, peso 800, sem consultar o banco de referências já capturado —
nenhuma das 26 referências do banco usa display acima de peso 600, e todas
usam entreletra apertada. Era invenção, não extração. Corrigida no mesmo dia
para Manrope 500/600.

Faltavam também, no material produzido antes desta norma existir: seção de
layout e espaçamento, seção de ícones, navegação com âncoras e um `STACK.md`
ao lado do `design-system.html` — todos corrigidos em 17/08, e o detalhe
completo do que faltou fica registrado na seção 6 do próprio padrão, como
exemplo de uso.

## Decisão

Adotar `GENESIS/padroes/PADRAO-SMX-DESIGN.md` como norma. Nenhuma interface é
desenhada do zero; toda interface parte de referência escolhida, cujo sistema
foi extraído antes de qualquer pixel.

Dois modos: **Extração**, quando existe uma referência (HTML de entrada,
`design-system.html` de saída, sem modificar a entrada); **Criação**, quando
não existe (produtos da SMX) — nesse caso, 2 a 4 referências do banco são
escolhidas pelo problema que resolvem, não pela aparência, o que se toma
emprestado e o que se recusa é nomeado com motivo, e só então se compõe.

## Papéis

| Papel | Faz |
|---|---|
| Arquiteto | Escolhe as referências — decisão de produto, não de engenharia |
| Engenheiro | Extrai, documenta, produz `design-system.html` + `STACK.md`, nomeia o que foi recusado |
| Builder | Porta para o código e commita — único canal de escrita no GitHub |

## Consequências

- Nenhum PR de interface abre sem `design-system.html` correspondente.
- Nenhum `design-system.html` é aceito sem `STACK.md` ao lado.
- "Feito" continua exigindo verificação em produção — documento de design
  bonito não é entrega.
- O banco de referências passa a viver sob `GENESIS/padroes/referencias/`,
  alimentado pelo Site Downloader quando uma referência nova entra.

## Alternativas descartadas

- **Deixar cada sessão escolher referência informalmente, sem registro.**
  Descartado: foi exatamente esse vazio que permitiu a tipografia inventada
  de 17/08 passar sem ninguém questionar.

## Fontes

**A Asimov Academy aparece apenas nesta seção**, nunca no título ou na
decisão desta ADR — ela é fonte do método, do mesmo modo que a FM Global
DS 8-21 é fonte dos controles de proteção contra incêndio usados na ronda:
citada, creditada e seguida, sem dar nome à norma.

| Fonte | O que forneceu |
|---|---|
| Asimov Academy — curso "Fundamentos de Vibe Design" | Método de extração em seis passos, estrutura de sete seções do `design-system.html`, banco inicial de 26 referências e 21 sistemas extraídos, e a ferramenta Site Downloader |
| Aura.build | Origem da maior parte das referências do banco |
| Mobbin | Padrões de aplicativo |
| Webflow · Dribbble | Exploração visual |

## Relação com outros documentos

- `GENESIS/padroes/PADRAO-SMX-DESIGN.md` — texto integral da norma adotada
  por esta ADR.
- `ADR-024` — Padrão SMX de Cores, companheiro: aquele decide **com que
  cor**, este decide **como se desenha**.
