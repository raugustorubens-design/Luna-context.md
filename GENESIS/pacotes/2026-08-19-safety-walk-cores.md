# Pacote do Engenheiro — Safety Walk para o Padrão de Cores (17/08/2026)

> ## REPOSITÓRIO-ALVO
>
> **`raugustorubens-design/luna-frontend`** — exclusivamente.
> Escopo: `app/ronda/`, `components/ronda/`, `public/ronda-manifest.json`,
> `public/ronda-sw.js`.
>
> `luna-core` não muda. **O relatório gerado não muda** — ele sai do Convergia, no
> backend, e não lê nada da tela.
>
> Verifique `GENESIS/ARCHITECTURE_INVENTORY.md` antes de caracterizar qualquer repo.

**Decisão do Arquiteto (17/08):** migrar o LUNA Safety Walk para
`GENESIS/padroes/PADRAO-CORES.md`. Este pacote implementa; o padrão em si já registra
que `/ronda` estava preservado, então **o padrão precisa ser emendado junto** — ver
etapa 6.

**Regra:** nenhuma lógica muda. Fila offline, IndexedDB, service worker, compressão de
foto, gate de conclusão, `PATCH`, correção de sugestão — **nada disso é tocado**. Esta
é uma troca de valores de cor e nada além.

---

## O que a medição diz — leia antes de aplicar

### Melhora, e não é pouco

Selos compostos por alfa (`bg-COR-400/15` sobre o fundo da página), que foram
corrigidos em campo em 09/08 e medidos naquela ocasião contra `#1E2761`:

| Elemento | Sobre `#1E2761` | Sobre `#001428` | Delta |
|---|---|---|---|
| Chip "Risco identificado" | 5,99:1 | **8,16:1** | +36% |
| Badge "pendente" / "Não avaliado" | 7,13:1 | **9,69:1** | +36% |
| Chip "Considerado inexistente" | 6,80:1 | **9,13:1** | +34% |
| Texto de corpo `slate-100` | 12,63:1 | **16,95:1** | +34% |

**Nenhuma regressão de legibilidade.** O trabalho de contraste de 09/08 continua
válido e fica com folga maior. Não desfaça nada dele.

### Piora — e precisa de correção junto

As bordas do wizard usam branco translúcido (`border-white/10`, `/15`, `/25`).
Compostas sobre um fundo mais escuro, elas **somem**:

| Borda | Sobre `#1E2761` | Sobre `#000206` |
|---|---|---|
| `white/10` | 1,35:1 | **1,21:1** |
| `white/15` | 1,58:1 | **1,40:1** |

**Correção obrigatória:** as linhas passam a derivar de `glow-3` (`#7088A0`) em
opacidade, como o padrão define — `rgba(112,136,160,.16 / .28 / .46)`. Isso as devolve
à visibilidade **e** as tira do branco, que é o que mantinha um cinza dentro de um
sistema que não deveria ter nenhum.

Sem esta correção, a tela de campo fica com cartões sem contorno definido. É o único
ponto em que a migração piora alguma coisa, e tem conserto no mesmo PR.

---

## Etapa 1 — Tokens do `/ronda`

**Não unifique o mecanismo de tema.** `/ronda` continua com a classe `dark` em
`#ronda-theme-root` e a chave `luna-ronda-theme`. O provider do site usa
`data-theme` e chave própria. Os dois seguem separados — é a dívida já registrada, e
resolvê-la aqui misturaria duas mudanças de risco diferente.

O que muda são os valores, dentro do mecanismo que já existe:

| Papel | Antes | Depois |
|---|---|---|
| Fundo escuro sólido | `#1E2761` | `#000206` |
| Degradê escuro | `#05060B → #1E2761` | `#000206 → #001428` |
| Superfície de cartão | `bg-white/[0.03]` | `#001428` |
| Superfície elevada | — | `#001E3C` |
| Linhas | `white/10 · /15 · /25` | `rgba(112,136,160,.16 · .28 · .46)` |
| Texto | `slate-100 / 200 / 300 / 400` | `#DCE6F2 · #A8BBD4 · #7E92AE · #5A6E8A` |
| Fundo claro | `#F4F6FB` | **inalterado** |
| Texto claro | `#1E2761` | `#0A1B3D · #1E3A61 · #41557A` |

**O degradê mantém a lógica original.** Ele nasceu escuro no topo porque
`app/ronda/layout.tsx` declara `statusBarStyle: "black-translucent"` — no iOS a barra
de status do sistema se sobrepõe ao topo da página. `#000206` no topo serve a esse
propósito melhor do que `#05060B` servia.

**O tema claro quase não muda.** O fundo continua `#F4F6FB`, então os selos claros
corrigidos em 09/08 (`bg-COR-400/40` com `text-COR-900`, medidos entre 6,35:1 e
7,01:1) **compõem sobre o mesmo fundo e mantêm os mesmos números**. Não os toque.

---

## Etapa 2 — `themeColor` do PWA

`app/ronda/layout.tsx`: `viewport.themeColor` de `#1E2761` para `#000206`.

Isso corrige uma incoerência que já existia: o valor apontava para o **fim** do
degradê, enquanto a barra de status do iOS fica sobre o **começo** dele.

`public/ronda-manifest.json`: `theme_color` e `background_color` para `#000206`,
mantendo `start_url`, `display`, `name` e os ícones exatamente como estão.

---

## Etapa 3 — Invalidação do cache do service worker

**Sem isto, você vai fazer o deploy e não ver mudança nenhuma no celular.**

`public/ronda-sw.js` faz cache do app shell com estratégia cache-first para assets. O
CSS novo não chega ao aparelho que já tem o PWA instalado até o cache expirar ou ser
invalidado.

Bump da constante de versão do cache, e limpeza dos caches antigos no evento
`activate`, se ainda não houver.

**Duas travas obrigatórias:**

1. **Nunca limpar o object store `queue` nem o `originalPhotos`.** São IndexedDB, não
   Cache API — não deveriam ser alcançados por nada disto, e é exatamente por isso que
   o risco precisa estar escrito. Ronda pendente e foto original vivem ali.
2. **O `POST` continua nunca sendo interceptado.** Regra da Fase 1, mantida.

Se este item for esquecido, o sintoma no aparelho é "nada mudou" — e a conclusão
errada seria que a migração falhou.

---

## Etapa 4 — Verificação de campo antes de virar padrão

**A preocupação real desta migração não é contraste, é luz ambiente.**

Os números melhoram em tela calibrada, no escuro. Em pátio industrial ao meio-dia, o
reflexo da tela soma uma luminância constante que comprime o contraste — e comprime
**proporcionalmente mais** um fundo quase preto do que um azul médio. É plausível que
`#000206` fique pior que `#1E2761` sob sol direto, exatamente onde a ronda acontece.

Não tenho como medir isso daqui, e não vou afirmar o que não medi.

**Portanto:** o escuro continua sendo o padrão do produto, mas a validação é
presencial. O Arquiteto abre o Safety Walk num pátio, em luz de trabalho real, nos
dois temas, e decide. Se o escuro não servir em campo aberto, a resposta não é
reverter a paleta — é o tema claro virar o padrão de `/ronda`, que já está pronto e
não mudou nesta migração.

---

## Etapa 5 — O que não muda, e por quê

**As três cores de classificação.** `#2E7D32`, `#E8A33D`, `#C62828`, com
`#1E2761` sobre o âmbar. São sólidas, não compõem com o fundo, e por isso os 5,13:1 /
6,41:1 / 5,62:1 seguem idênticos. Elas vêm do relatório impresso e são a exceção
permanente do padrão.

**Midnight não desaparece do sistema.** Ele continua sendo o texto sobre o âmbar de
"Atenção" — a medição de 2,16:1 do branco naquele fundo continua valendo e continua
registrada em `finding-card.tsx`.

**O `[color-scheme:dark] dark:[color-scheme:light]` do seletor de Gravidade.** Foi
invertido de propósito em 15/08 para o popup nativo contrastar com a página. Com uma
página mais escura, o raciocínio se mantém. Não mexer.

**Nenhuma lógica.** Fila, reenvio, compressão de foto, gate, `PATCH`, `×` de remover,
`+ Duplicar`, correção de sugestão. Se qualquer arquivo de `lib/ronda/` aparecer no
diff com mudança que não seja de cor, o PR está errado.

---

## Etapa 6 — Emendar o padrão

`GENESIS/padroes/PADRAO-CORES.md`, seção 7, hoje diz que `/ronda` preserva os valores
próprios. Isso deixa de ser verdade.

**Não reescreva a seção apagando o histórico.** Acrescente a decisão com data,
registrando: o Arquiteto decidiu migrar em 17/08; os contrastes compostos melhoraram
entre 34% e 36%; as bordas exigiram derivação nova; e a validação em luz de campo
ficou pendente. Se a validação reprovar, isso também entra ali — decisão registrada
com o resultado, não só com a intenção.

Vai em PR próprio no `Luna-context.md`, junto do pacote
`GENESIS_2026-08-17_commit-padrao-cores.md`.

---

## Verificação

Automático: `pnpm typecheck`, `pnpm run test:constitution`, `pnpm test`
(**39/39 — não pode cair, e nenhum teste existente pode ser alterado**), `pnpm build`.

Nenhum teste novo: isto é CSS, sem lógica testável. A verificação real é visual e por
medição.

**Medir, não olhar.** No padrão que o `BUILDER.md` já usa nas entradas de 09/08: via
`getComputedStyle` no navegador real, compondo o alfa sobre a cor de fundo efetiva —
não a cor nominal do token. Confirmar os cinco valores da tabela de melhora e os três
de borda. Captura de tela dos dois temas nas três etapas do wizard, mais a tela de
edição e o histórico.

**Portão real, o único que conta:**

1. O Arquiteto abre `/ronda` **no celular onde o PWA está instalado** e vê a cor nova
   — se não mudou, é a etapa 3
2. Preenche uma ronda de ponta a ponta, nos dois temas
3. Confirma que a fila pendente que já estava no aparelho **continua lá**
4. Abre em pátio, em luz de trabalho, e decide qual tema serve em campo

Autoatestar em `BUILDER.md`: verificado neste ambiente **versus** reportado sem
confirmação.

---

## Ordem — e um aviso de colisão

**Este pacote não é o primeiro da fila.**

`GENESIS_2026-08-17_URGENTE_gate-ronda-divergente.md` toca os mesmos arquivos e
desbloqueia uma ronda real do Sylvamo, coletada em campo em 17/08, com duas fotos que
só existem naquele aparelho. Cor não desbloqueia nada.

Ordem:

1. Correção do gate da ronda
2. Merge dela, e confirmação de que a ronda do Sylvamo subiu
3. **Este pacote**
4. Emenda do padrão no `Luna-context.md`

**Colisão:** o `BUILDER.md` mostra sessões do Claude Code em `/ronda` até 15/08. Os
dois pacotes e qualquer sessão paralela disputam `finding-card.tsx`, `ronda-wizard.tsx`
e `theme-provider.tsx`. Rodar em série, não em paralelo — e o segundo rebasear no
primeiro, não mergear.
