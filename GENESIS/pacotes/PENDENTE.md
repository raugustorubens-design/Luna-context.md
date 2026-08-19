# Verificações pendentes

**Caminho:** `GENESIS/pacotes/PENDENTE.md`
**Acrescentado por:** o Builder, ao concluir pacote com portão de campo
**Limpo por:** o Arquiteto, ao verificar

---

## Por que este arquivo existe

Trabalho rodando sozinho **acumula mudança não verificada**. O código sobe, os testes
passam, o PR fecha — e ninguém confirmou no aparelho que a coisa funciona onde importa.

Aconteceu em 18/08: as cores do `/ronda` foram para produção com o portão de campo em
aberto, e ficou assim porque não havia onde registrar.

Sem este arquivo, o estoque de não verificado fica invisível — que é exatamente o gargalo
de observabilidade que o `ADR-026` nomeia, aparecendo no processo em vez de no produto.

**Regra:** pacote com portão de campo pode mergear sem esperar o Arquiteto, **desde que a
verificação entre aqui.**

---

## Em aberto

### `/ronda` mudou de cor — PR `#38`, mergeado 19/08

O Safety Walk passou para a paleta nova. É o único item recente que tocou a ferramenta
usada em planta.

Conferir no celular:

- Fundo quase preto, não azul
- **Bordas dos cartões visíveis** — eram branco translúcido e sumiriam sobre fundo escuro;
  o pacote trocou por azul da rampa. Cartão sem contorno significa que essa parte não entrou
- **Os três selos de classificação idênticos** — Positivo, Atenção e Não Conformidade são
  sólidos e não compõem com o fundo. Se algum mudou de tom, algo passou do escopo
- Fila sem ronda presa

### `/v2` com o fundo novo — PR `#36`, mergeado 19/08

Conferir nos dois temas. No claro, os feixes de luz não aparecem — é o comportamento
correto: luz sobre papel não existe.

### Portão do ADR-022 — nunca foi feito

O `#28` foi mergeado em 18/08 sem o portão de produção. Continua em aberto:

- `/forge?layout=v2` — redimensionar a coluna do chat, abrir e fechar a gaveta do terminal
  sem derrubar a sessão
- `/forge` e `/` continuam com o arranjo de painéis de sempre, ainda que a cor tenha mudado

---

## Verificado

*(vazio — o Arquiteto move para cá o que confirmar, com a data)*
