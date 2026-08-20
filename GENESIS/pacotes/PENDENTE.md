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

### Colunas de EXIF em `convergia_ronda_fotos` — `luna-core#55`, mergeado 20/08

`GENESIS/pacotes/2026-08-20-exif-colunas.md`, continuação do `#54`. `luna-core#52` (lado
servidor do EXIF, mergeado antes) estava gravando em colunas que não existiam — corrigido
com uma migração aditiva (`ALTER TABLE ... ADD COLUMN`, seis colunas nuláveis, nenhuma
existente tocada). Verificado nesta sessão: as 51 fotos anteriores continuam íntegras, e um
upload sintético de teste (imagem 1×1px + EXIF preenchido) confirmou gravação ponta a ponta
contra produção real — linha de teste removida depois.

**Portão do Arquiteto:** tirar uma foto pelo `/ronda`, com GPS ligado, e conferir no
Supabase que **data e hora reais da captura** chegaram (`exif_captured_at`,
`exif_gps_lat`/`exif_gps_lng`). Depois, uma foto vinda da galeria — que costuma vir sem
EXIF nenhum — e confirmar que ela anexa normalmente, com as seis colunas de EXIF nulas.

### Hero do `/v2` — LUNA no espaço — `luna-frontend#48`, mergeado 20/08

`GENESIS/pacotes/2026-08-20-hero-luna-espaco.md`, `referencia_hero-luna-espaco.html`
(aprovado pelo Arquiteto) reproduzido: LUNA centralizada e inteira, máscara elíptica,
sem quadriculado, estrelas com densidade crescente pra baixo, sinapses no crânio + disco
pulsante nos valores "50% mais forte". `LunaCore` do `#45` não usado mais no hero (segue
no repositório).

**Duas decisões tomadas sem perguntar, conforme as próprias condições de parada do
pacote — registradas aqui, não escondidas:**

- **Tema claro:** a cena ficou **sempre escura**, nos dois temas (hex literais, ignora
  `[data-theme="light"]`). O pacote listava duas opções e mandava, na ausência de
  decisão do Arquiteto, "reportar e seguir com o escuro" — foi o que aconteceu.
  **Se a decisão for a outra opção** (imagem em duotone azul sobre fundo claro), é
  pacote novo.
- **Quebra do título em telas largas:** o `h1` quebra uma palavra por linha em desktop
  (`max-width:24ch` em `.copy` resolve contra o font-size herdado do corpo, não o do
  `h1`). **Confirmado que não é erro de portagem** — o próprio
  `referencia_hero-luna-espaco.html`, renderizado localmente no mesmo viewport, faz
  exatamente a mesma coisa. O pacote só definia portão no celular; desktop não tinha
  critério explícito.

**Terceira divergência, menor:** o parágrafo abaixo do título ficou com o texto **já em
produção** (nomeia as três frentes de trabalho), não o texto mais curto do protótipo —
o pacote descreve estrutura da seção "4 · A frase, abaixo", não pediu trocar as
palavras.

**Portão do Arquiteto** — no celular, que é onde o próprio pacote diz que o defeito
original aparecia:

1. A LUNA aparece **inteira e centralizada** na primeira tela, sem cortar a cabeça
2. A frase abaixo dela, legível sem rolar
3. Sem quadriculado; estrelas adensando pra baixo; sinapses e disco animando
4. Sem cursor (é o caso do celular), ela deriva sozinha

E as duas decisões acima: confirmar se a cena sempre escura serve, ou se entra pacote
próprio para o duotone; e se a quebra do título em desktop precisa de correção (fora do
escopo original, mas visível caso o Arquiteto abra em tela larga).

### Roxo do `body` e inversão de paleta no Forge v1 — `luna-frontend#47`, mergeado 20/08

`GENESIS/pacotes/2026-08-19-paleta-em-tudo.md`. Etapa 1: os três degradês do `body`
(`#7C3AED`/`#A78BFA`, atrás de toda superfície exceto `/ronda`) trocados por azul/dourado
dentro do portão de matiz. Etapa 2: `--background`/`--muted`/`--secondary`/`--border`/
`--foreground`/`--primary`/`--ring`/`--luna-cyan` do shadcn (lidos pelo Forge v1, que nunca
tinha recebido o segundo estágio da inversão do ADR-022) religados para os mesmos valores
que `/v2`/Forge v2 já usam. Etapa 3: `--luna-violet` marcado como legado.

**Achado, não corrigido:** o portão de matiz (`constitution-check.mjs` + `hue-gate.mjs`)
nunca varre `app/globals.css` (só `components/site/**` e os `*-v2` do Forge) e só reconhece
hex literal, não `rgba()` — o roxo do `body` nunca teria sido pego pelo teste automático.
Detalhe completo no `BUILDER.md` de `luna-frontend`.

**Portão do Arquiteto**, no aparelho real, nos dois temas onde fizer sentido:

- `/forge` e `/forge?tab=convergia` — fundo quase preto, painéis destacando dele, sem
  mancha violeta
- `/` — sem mancha violeta atrás do conteúdo
- **`/ronda` sem nenhuma mudança de aparência** — é a trava do pacote; se algo lá mudou de
  cor, a inversão passou do escopo

### Portão do ADR-022 — nunca foi feito

O `#28` foi mergeado em 18/08 sem o portão de produção. Continua em aberto:

- `/forge?layout=v2` — redimensionar a coluna do chat, abrir e fechar a gaveta do terminal
  sem derrubar a sessão
- `/forge` e `/` continuam com o arranjo de painéis de sempre, ainda que a cor tenha mudado

---

## Verificado

*(vazio — o Arquiteto move para cá o que confirmar, com a data)*
