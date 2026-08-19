# Fila local visível e editável — a correção estrutural (16/08/2026)

**Pedido do Rubens, depois de uma ronda sumir de vista:** *"quero poder editar rondas anteriores clicando em ver rondas anteriores… eu necessariamente não preciso dessa ronda que ainda não subiu, eu preciso debugar e evitar que essa situação recorra."*

Este é o terceiro commit do dia e o único que não corrige um defeito pontual — corrige a condição que fez os outros dois serem tão difíceis de enxergar.

**Commit:** `1c8da09`, em cima de `25f78a9` e `b975735`.
**Patch completo dos três:** `GENESIS/patches/2026-08-16-safety-walk-fixes.patch`.

## O diagnóstico

O problema não era a ronda específica. Era a **cegueira**.

"Ver rondas anteriores" listava só o que o servidor havia confirmado. A fila local existia apenas como *contagem* na barra de status — "1 enviando…". Uma ronda pendente, travada ou rejeitada não dava para abrir, nem para ver o que tinha dentro, nem para saber por que não subiu. O único registro do erro (`lastError`) só era exibido para itens `invalid`.

Ou seja: **não existia tela capaz de responder "cadê minha ronda"**. Foi por isso que hoje foi preciso consultar o servidor por fora, pela API, para descobrir que a ronda simplesmente não tinha chegado lá.

## O que mudou

### Lista unificada (`lib/ronda/list-view.ts`, novo)

Funde servidor + fila numa lista só, ordenada por data da ronda, com etiqueta de estado por item: *no servidor / aguardando envio / enviando / falhou / rejeitada*. Função pura — testável sem IndexedDB nem rede.

Uma distinção que carrega comportamento: `server === null` (inalcançável) é tratado diferente de `[]` (respondeu vazio). Sem servidor, itens já sincronizados continuam listados, para a tela não ficar vazia justamente em campo; com servidor, são omitidos porque o registro dele é o canônico.

`countIdentified` espelha a contagem do backend (só achado `identificado`) — número que muda sozinho ao sincronizar é exatamente o tipo de coisa que faz a pessoa desconfiar de perda de dado.

### A tela deixa de sumir quando o servidor cai

Falha do servidor virava tela vazia. Agora vira um aviso com "tentar de novo" **acima** dos itens locais, que continuam lá. Em campo, sem rede, essa era a tela que aparecia vazia bem quando mais importava.

### Editor para ronda que ainda não subiu (`/ronda/fila/[localId]`)

Mesmos `FindingCard` do wizard, fotos inclusive. Salvar grava no IndexedDB, devolve o item para `pending` e dispara o envio. É o que fecha o ciclo para uma ronda rejeitada por formato: **corrigir e reenviar, em vez de refazer do zero**.

Rota própria, e não o mesmo `/ronda/historico/[id]`: os ids vêm de espaços diferentes (`ronda_<uuid>` do servidor, `localId` da fila) e decidir qual é qual por formato do id seria adivinhação silenciosa.

### Uma assimetria proposital: remover achado

Só existe no modo `queue`. `PATCH /convergia/ronda/:id` faz **upsert por `id`** e não tem como dizer "este achado saiu" — um "×" no modo servidor removeria o card, salvaria com sucesso, e o achado voltaria no próximo carregamento. Falha silenciosa. Local, o registro é substituído inteiro e a remoção é real.

Habilitar remoção no servidor depende de o contrato do `luna-core` ganhar semântica de remoção. **Pendência de arquitetura**, junto com a chave de idempotência.

### Viewport estendido

A correção de `b975735` valia só para o wizard. Lista e editor também usavam `min-h-dvh` + `flex-1 overflow-y-auto` — mesmo defeito, mesmas telas rolando o documento inteiro. Corrigidos.

## Verificação

Pixel 7 emulado, **com o backend fora do ar de propósito** (o cenário de campo):

| Verificação | Resultado |
|---|---|
| Ronda concluída aparece na lista | ✅ com estado "Falhou — vai tentar de novo" e o erro real |
| Abre com os achados e a observação | ✅ 2 achados + encerramento |
| Edição persiste após reload | ✅ |
| Remoção de achado persiste | ✅ |
| Descartar esvazia a lista | ✅ |
| Documento não rola em nenhuma tela | ✅ rodapé sempre em `bottom == innerHeight` |

7 testes novos (**49 no total**), `pnpm typecheck` e `pnpm build` ok.

## Pendências de arquitetura que sobraram (`luna-core`)

1. **Chave de idempotência** em `POST /convergia/ronda`, usando o `localId` do cliente. Elimina o risco de duplicata em qualquer reenvio — hoje assumido conscientemente em `reclaimStaleSyncing`.
2. **Semântica de remoção** em `PATCH /convergia/ronda/:id`. Sem ela, remover achado continua impossível em ronda já enviada.

## Lição

A correção mais valiosa do dia não foi nenhum dos dois bugs — foi tornar o estado do sistema **legível pela pessoa que está em campo**. Os dois defeitos existiam há tempo; o que os tornou caros foi não haver onde olhar. Vale como critério para o resto do LUNA: *quando algo puder ficar parado num estado intermediário, tem que existir uma tela que mostre esse estado, o motivo dele, e um caminho de saída.*
