# Armazenamento no aparelho e upload incremental — decisão de 16/08/2026

**Origem:** Rubens, em campo: *"e se o relatório fosse subindo automaticamente durante a ronda e até a finalização pudesse ser salvo com atualizações, a gente evitaria latência e reduziria espaço no dispositivo, que acho que é o problema aqui… podendo ser recuperado a partir do último upload realizado."*

**Veredito:** a intuição sobre espaço estava certa; a causa não. **Camada 1 implementada** (commit `3d9e97e`). **Camada 2 aprovada, pendente.**

---

## A medição que mudou o diagnóstico

Uma foto de 12MP passando pela mesma cadeia de `compressPhoto` (1280px, JPEG q0.7):

| | tamanho | em base64 |
|---|---|---|
| original da câmera | 6,95 MB | **9,27 MB** |
| comprimida (a que o relatório usa) | 0,10 MB | **0,13 MB** |

**98,6% do que o app gravava por foto era dado que nenhuma linha de código lia.**

Três acúmulos, nenhum com política de descarte:

1. `saveOriginalPhoto` gravava a original em base64 a cada clique — e `getOriginalPhotosForFinding` **não tinha um único chamador**. Write-only, para uma Fase 2 que não existe.
2. Nada apagava essas originais, nunca.
3. O item da fila **não era removido depois de confirmado no servidor** (`deleteQueueItem` só era chamado por `discardInvalidQueueItem`). A ronda inteira, com as fotos comprimidas, ficava para sempre.

Vinte fotos numa ronda passavam de 180 MB permanentes. É a explicação mais provável para o Chrome descartar a aba em campo — **não é a ronda que é pesada, é o rastro que ela deixa.**

### Por que isso reordena a proposta

Upload incremental resolve latência e recuperação, mas **sem política de descarte o aparelho enche igual**. Tratar o momento do upload antes de tratar o descarte seria corrigir o sintoma.

---

## Camada 1 — implementada (`3d9e97e`)

- Original guardada como **`Blob`**, não base64 (IndexedDB guarda binário nativamente; base64 só é necessário no fio). −27% sobre o maior arquivo do sistema, sem o custo de FileReader por foto.
- `saveOriginalPhoto` **deixa de lançar**: guardar a original é um "seria bom ter", e cota cheia nela não pode interromper o preenchimento em campo.
- `discardRondaLocalCopies`: ao confirmar no servidor, apaga o item da fila **e** as originais daquela ronda.
- Novo store `history` (`DB_VERSION` 3 → 4), resumo de ~1 KB por ronda. Sem ele, economizar espaço custaria o histórico offline.
- Migração v4 limpa o store de originais — seguro porque nunca teve leitor. Na prática, devolve de uma vez os MB já acumulados no aparelho.

**Verificação:** Pixel 7 emulado, `POST` interceptado para exercitar o caminho de sucesso real no navegador, foto de 5,6 MB. Durante a ronda `originalPhotos=1`; após a confirmação `queue=0, originalPhotos=0, draft=0, history=1`. Lista mostra "No servidor" e continua mostrando com o servidor fora.

---

## Por que a original só chega ao servidor via upload por foto

Duas restrições duras do backend, verificadas em `luna-core`:

1. **`POST /convergia/ronda` tem limite de 25 MB** (`RONDA_JSON_BODY_LIMIT`), dimensionado para ~69 fotos *comprimidas* — e já houve um 413 em produção em 15/08. Uma única original em base64 pesa 5–9 MB. Três ou quatro e a ronda inteira para de subir.
2. **O schema Zod não é `.strict()`** — campo desconhecido é **descartado em silêncio**. Pendurar `originalBase64` no payload faria o app reportar sucesso com a original jamais tendo existido no servidor. Falha silenciosa, o pior desfecho.

Portanto **"subir a original" e "só mexer no frontend" são mutuamente exclusivos.** A original só cabe se a foto subir sozinha, no momento em que é tirada.

---

## Camada 2 — aprovada, a fazer

**Forma:** cada foto sobe assim que é tirada (comprimida + original), o servidor devolve um id, o aparelho guarda só o id. No fim, o relatório é texto puro — sobe em um segundo em qualquer rede.

**O que isso entrega:**

- a original **preservada no servidor**, que é o que a Decisão 4 sempre quis e o aparelho não tem como bancar;
- latência distribuída ao longo da caminhada, em vez de concentrada no "Concluir";
- **retomada a partir do último upload** — cada foto que subiu está a salvo mesmo se o aparelho morrer em seguida;
- o aparelho para de guardar bytes de foto por completo.

**Escopo em `luna-core`:**

- `POST /convergia/ronda/foto` — multipart (`multer` já é usado em `convergia.ts` para templates visuais), campos `comprimida` e `original`, devolve `{ fotoId }`. Multipart e não base64: evita a inflação de 33% no fio, que é exatamente o que torna a original inviável hoje.
- `RondaFinding.fotoIds?: string[]` no contrato e na validação, convivendo com `fotos?` (que continua sendo o caminho offline).
- `GET /convergia/ronda/foto/:id` para exibição.

**Escopo em `luna-frontend`:**

- `uploadFoto()` no api-client, com fila e retry próprios.
- `FindingCard`: após comprimir, tenta subir. Sucesso → guarda `fotoId` e descarta os bytes locais. Sem rede → mantém em `fotos[]` como hoje e sobe depois. **A fila offline continua sendo a rede de segurança — sem sinal a pessoa não pode parar de trabalhar.**

**Riscos a tratar no desenho:** dois caminhos de foto convivendo no wizard (id e bytes) é complexidade real; e foto órfã no servidor quando a ronda é abandonada precisa de política de expiração.

---

## Camada 3 — avaliada e não escolhida (por ora)

Relatório criado no servidor no início e atualizado a cada achado. Daria recuperação total, inclusive perda do aparelho. Custa: estado de rascunho no servidor, validação em dois níveis, ciclo de vida de ronda abandonada — e **ainda assim precisaria da fila offline**. Fica registrada como opção, não como pendência.

---

## Pendências acumuladas de `luna-core`

1. `POST /convergia/ronda/foto` + `fotoIds` no contrato (Camada 2).
2. **Chave de idempotência** com o `localId` do cliente — elimina o risco de duplicata em qualquer reenvio.
3. **Semântica de remoção** em `PATCH /convergia/ronda/:id` — sem ela, remover achado continua impossível em ronda já enviada.
