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

### Relatório da ronda em três formatos, página configurável — `luna-core` PR `#53`, `luna-frontend` PR `#44`, mergeados 20/08

`GENESIS/pacotes/2026-08-19-saida-formato-e-pagina.md`. `#53` mergeou já com os três
ajustes da revisão (`GENESIS/pacotes/ARQUIVO/2026-08-20-revisao-pr53.md`): quebra por
palavra dentro de um campo sozinho que estoura o slide, texto que termina onde a foto
começa em vez de sobrepor, e largura real de coluna na estimativa de altura do xlsx.
`#44` mergeou depois, na ordem certa. Gerar a mesma ronda nos três formatos (PPTX, XLSX,
DOCX) e conferir em cada um:

- Nenhum texto cortado — inclusive o achado de descrição mais longa
- Editável sem pedir senha
- Tamanho de página nas propriedades do arquivo bate com o escolhido
- Rodapé traz ronda, data e versão do template
- **Novo, por causa do ajuste 1:** gerar com um achado de descrição bem longa e conferir
  que nenhum slide do PPTX corta texto nem escreve por cima da foto — era exatamente o
  caso que a revisão bloqueou antes do merge

**Portão do Arquiteto:** imprimir um em Ofício e conferir que nada foi cortado na margem —
é onde o erro de milímetro aparece. Limitação conhecida: XLSX não tem código de papel exato
para Ofício (`exceljs` só aceita tamanhos enumerados); a geração reporta isso como aviso
não-fatal em vez de mentir um tamanho errado — DOCX e PPTX suportam Ofício com exatidão.

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

### Constituição chegando ao prompt — mergeado em `luna-core`, sem PR numerado

Item 3 da fila (`FILA.md`). O adaptador do Groq passou a montar o contexto com
`LUNA_CONSTITUTION.md` de verdade, em vez de descartá-lo. Verificação de produção:

- Perguntar à LUNA algo que só está na Constituição — ex.: por que foto nunca é
  obrigatória no Safety Walk
- Ela precisa responder certo, citando ou parafraseando a regra real, não inventando

### Relatório da ronda (backend) — `luna-core#50`, mergeado 19/08

Item 2 da fila, parte `luna-core`. Adaptador, XLSX e curadoria (editar/excluir) prontos,
verificados só com Guardian falso + geração real fora da suíte (script descartável). Não
testado contra o Guardian de produção real nem clicado em produção — e a peça de
`luna-frontend` (botão + tela de curadoria) ainda não existe, então este portão só fecha
depois dela. Registrado aqui agora para não se perder — mover pra "Verificado" só depois
do portão completo (ver `FILA.md` item 2, "Pronto quando").

### Portão do ADR-022 — nunca foi feito

O `#28` foi mergeado em 18/08 sem o portão de produção. Continua em aberto:

- `/forge?layout=v2` — redimensionar a coluna do chat, abrir e fechar a gaveta do terminal
  sem derrubar a sessão
- `/forge` e `/` continuam com o arranjo de painéis de sempre, ainda que a cor tenha mudado

---

## Verificado

*(vazio — o Arquiteto move para cá o que confirmar, com a data)*
