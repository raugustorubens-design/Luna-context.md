# Achado de campo — LUNA Safety Walk no celular (16/08/2026)

**Data:** 16/08/2026 (durante ronda real, Rubens em campo)
**Aparelho:** Android, Chrome. Começou por link no navegador; instalado na tela inicial no meio da sessão.
**Superfície:** `luna-frontend` → `/ronda`
**Base:** `main` em `6bfb600` (o rename + botão do modal, PRs #20/#21, já está mergeado — estas correções são em cima disso)
**Commits prontos:** `b975735` (viewport + rascunho) e `25f78a9` (fila presa em "enviando…")

> ## ⚠️ HANDOFF ENTRE SESSÕES — leia isto primeiro
>
> A sessão que produziu estas correções **não tem escrita** em `raugustorubens-design/luna-frontend`. Outra sessão tem (branch `claude/luna-frontend-access-b7mcnt`).
>
> **Não reimplemente do zero.** O diff completo dos dois commits está neste projeto:
>
> ### `GENESIS/patches/2026-08-16-safety-walk-fixes.patch`
>
> Leia com `project_read` nesse caminho — a ferramenta grava o conteúdo num arquivo local e devolve o caminho. Depois, dentro do repo:
>
> ```
> git am <caminho-devolvido-pelo-project_read>
> # se o am reclamar do cabeçalho de e-mail:
> #   git apply <caminho> && commit manual com as mensagens abaixo
> pnpm typecheck && pnpm test && pnpm build   # esperado: 42 testes passando
> ```
>
> Os dois commits aplicam limpos sobre `6bfb600`. Os textos de commit já estão escritos no patch — preserve-os, eles carregam o diagnóstico medido.
>
> O deploy só dispara quando o PR for mergeado na `main` (o Railway publica de `main`, serviço `luna-frontend`, projeto `outstanding-learning`).

Três defeitos distintos apareceram nesta ronda. Os dois primeiros vieram do relato inicial; o terceiro só apareceu porque Rubens mandou print da barra de status.

---

## Defeito 1 — a tela fugia (relato original)

> "o relatório está saindo da página ou subindo sozinho e eu tenho que reiniciar a todo momento"

### Correção de rota no diagnóstico

O primeiro diagnóstico desta sessão apontou o **zoom automático do iOS** como causa principal. Estava errado: o aparelho é Android, e o Chrome não amplia a página ao focar campo pequeno — isso é comportamento do WebKit. A hipótese foi levantada antes de confirmar o aparelho. A causa real foi então **medida**, não deduzida. O ajuste de 16px continua no commit, mas como correção preventiva para iPhone, não como a causa deste relato.

### Causa, medida

Emulação de Pixel 7 (412×805), etapa B com 5 achados:

| | antes | depois |
|---|---|---|
| documento rola | **sim** | não |
| `<main>` rola | **não** | sim |
| `footer.bottom` | **4066px** (tela: 805px) | 839px = fim da tela |
| `header.top` após rolar 400px | **−367px** (fora da tela) | 33px, fixo |

Os botões Voltar/Avançar ficavam **3,2 mil pixels abaixo do fim da tela** e o cabeçalho saía por cima ao rolar.

**Raiz:** `min-h-dvh` no shell. Altura **mínima** não impõe limite ao filho `flex-1 overflow-y-auto`, e o `min-height: auto` que o flex dá de padrão deixa a `<main>` crescer junto com o conteúdo — o `overflow-y-auto` nunca chega a valer. Quem rolava era o documento.

**Correção:** `100svh` fixo no shell + `min-h-0` na `<main>` + `overflow: hidden` no html/body enquanto em `/ronda`.

### O "sobe sozinho" — duas fontes, ambas de Android

1. `dvh` acompanha a barra de endereços do Chrome recolhendo durante a rolagem — o shell mudava de altura no meio do gesto. Por isso `svh` (altura com a barra visível, constante).
2. O padrão `interactive-widget=resizes-visual` faz o Chrome **arrastar o documento inteiro** pra trazer o campo focado à vista quando o teclado abre. Com o documento sendo o scroller, isso movia a tela toda. Corrigido com `interactive-widget=resizes-content`.

### Preventivo para iPhone (mesma superfície, outro aparelho)

- `env(safe-area-inset-*)` no topo e no rodapé: o layout declara `viewportFit: cover` + status bar translúcida e nada compensava o recorte.
- Fonte mínima de 16px em `input`/`select`/`textarea`: o WebKit amplia a página sozinho abaixo disso.
- `maximumScale: 1` removido: não impedia esse zoom, só impedia desfazê-lo com a pinça — e quebrava a acessibilidade de quem precisa ampliar pra ler.

---

## Defeito 2 — a ronda em andamento se perdia

O "tenho que reiniciar" custava **a ronda inteira**. O wizard mantinha tudo em memória React e só gravava em IndexedDB na conclusão. Qualquer recarga da aba apagava tudo — e recarga não é hipótese remota em campo: o Chrome descarta abas em segundo plano sob pressão de memória, e abrir a câmera é justamente o pico de pressão. O próprio ato de fotografar um achado podia apagar a ronda.

**Correção:** novo store `draft` no IndexedDB (`DB_VERSION` 2 → 3), gravado a cada 600ms com debounce (IndexedDB e não localStorage porque as fotos são base64 e estouram a cota de ~5MB), recuperado na montagem com aviso na tela e opção de "começar do zero", apagado na conclusão.

---

## Defeito 3 — ronda presa em "enviando…" para sempre

Descoberto pelo print da barra de status: `0 pendentes / 1 enviando… / 1 confirmada no servidor`, com o "1 enviando…" imóvel.

`trySyncPendingRondas` grava `status: "syncing"` no IndexedDB **antes** de disparar a requisição, e o filtro de reenvio só considerava `"pending"`/`"error"`. Se a aba morre entre uma coisa e outra, o item fica gravado como `"syncing"` permanentemente:

- nenhum gatilho de retry o alcança — evento `online`, reabertura do app e o "Sincronizar agora" da barra chamam todos a mesma função;
- `discardInvalidQueueItem` só atende status `"invalid"`, então nem descartar pela interface dava;
- a ronda continua íntegra em IndexedDB, mas inalcançável sem DevTools.

**Correção:** `reclaimStaleSyncing` roda no início de `trySyncPendingRondas`, logo depois do guarda `if (syncing) return` — nesse ponto sabidamente não há envio em curso nesta aba, então todo `"syncing"` no banco é herança de uma sessão morta e volta pra `"pending"`.

**Troca assumida:** se a requisição completou no servidor e só o registro local do sucesso se perdeu, o reenvio gera uma ronda duplicada. Duplicata é visível no histórico e descartável; ronda perdida em campo não volta.

**Pendência para `luna-core`:** aceitar `localId` como **chave de idempotência** em `POST /convergia/ronda`. É o que elimina a troca acima de vez — o servidor reconhece o reenvio como o mesmo registro em vez de criar outro.

**Impacto imediato em campo:** há uma ronda do Rubens presa nesse estado, no aparelho dele. Ela sobe sozinha assim que este código estiver publicado. **Até lá, não limpar os dados do site nem desinstalar o app** — é onde ela está.

---

## Arquivos tocados

| Arquivo | Mudança |
|---|---|
| `app/globals.css` | `.ronda-locked` / `.ronda-shell` / safe-area / 16px |
| `app/ronda/layout.tsx` | viewport: remove `maximumScale`, adiciona `interactiveWidget` |
| `components/ronda/viewport-lock.tsx` | **novo** — marca `<html class="ronda-locked">` |
| `components/ronda/ronda-wizard.tsx` | shell `100svh`, `min-h-0`, safe-area, rascunho automático |
| `lib/ronda/db.ts` | store `draft` + `saveDraft`/`loadDraft`/`clearDraft` |
| `lib/ronda/queue.ts` | `reclaimStaleSyncing` / `reclaimStaleSyncingItems` |
| `lib/ronda/__tests__/queue.test.ts` | 3 testes sobre a recuperação de item preso |

Verificação: emulação de Pixel 7 e iPhone 13; `pnpm typecheck`, `pnpm build` e **42 testes** passando.

---

## Onde ficam as rondas (mapa de estados, pra referência)

| Estado | Onde vive | Sobrevive a recarga? | Visível onde |
|---|---|---|---|
| Em andamento, não concluída | memória React → **agora também store `draft`** | antes não, **agora sim** | a própria tela |
| Concluída, aguardando rede | IndexedDB, store `queue` | sim | barra de status ("X pendentes") |
| Enviada e confirmada | servidor | sim | "Ver rondas anteriores" (`GET /convergia/ronda`) |

Nota: "Ver rondas anteriores" lista **só o que o servidor confirmou**. A fila local não aparece lá — só na barra de status. Isso já confundiu em campo; vale considerar unificar as duas visões.

---

## Lições para o sistema

1. **Confirmar o aparelho antes de diagnosticar.** O primeiro diagnóstico partiu de "celular" e assumiu iPhone. Aparelho e navegador são a primeira pergunta de qualquer bug de campo.
2. **Medir antes de afirmar.** A causa real saiu de três números num viewport emulado. Leitura de código gera hipótese; medição gera diagnóstico.
3. **Todo estado gravado antes de uma operação de rede precisa de caminho de volta.** O `"syncing"` era um estado sem saída — escrito antes da requisição, sem nada que o recupere se a requisição nunca terminar. Vale auditar se há outros assim no sistema.
4. **Toda superfície de campo do LUNA precisa de um passe em viewport móvel real antes de ir pra ronda** — nenhuma dessas causas aparece em desktop, e build verde não diz nada sobre elas.
5. **Sessões do Cowork não compartilham repositório nem disco — só o projeto.** Duas sessões deste mesmo dia divergiram sobre "quem tem acesso ao quê" e uma quase reimplementou do zero um trabalho que já existia. O projeto é o único canal de handoff confiável: código pronto vai pra `GENESIS/patches/`, contexto vai pra `GENESIS/achados-campo/`.
