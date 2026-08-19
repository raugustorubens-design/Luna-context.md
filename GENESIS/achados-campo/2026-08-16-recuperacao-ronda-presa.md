# Recuperação da ronda presa em "enviando…" — sem esperar deploy

**Data:** 16/08/2026
**Contexto:** ver `GENESIS/achados-campo/2026-08-16-safety-walk-viewport-celular.md`, Defeito 3.

## Estado verificado do servidor

`GET https://uvicorn-main-production-92f8.up.railway.app/api/convergia/ronda` devolve **uma única ronda**:

```json
{ "id": "ronda_8dd1c77d-7adb-4479-bddf-d4908a36c94e",
  "titulo": "Luna Safety Walk - Turno B",
  "data": "2026-08-11", "local": "UT SYLVAMO -LOGISTICA",
  "achadosCount": 0 }
```

Duas conclusões:

1. **A ronda de 16/08 não chegou ao servidor.** Ela existe só no IndexedDB do aparelho, presa em `status: "syncing"`. Logo, destravá-la **não gera duplicata** — a troca descrita no Defeito 3 não se aplica a este caso concreto.
2. **A ronda de 11/08 está no servidor com zero achados.** A tela de edição mostrar só "Observações gerais" é consequência disso, não bug de UI (`RondaEditor` renderiza `FindingCard` por achado; sem achados, não há card). **Vale investigar** se achados foram registrados nesse dia e não persistiram.

## Por que nenhuma autorização dá acesso remoto ao dado

O IndexedDB é isolado pelo próprio navegador, por origem. Nada fora do Chrome lê aquilo — não é questão de permissão concedida ou negada. E a ponte de dispositivo do Cowork alcança um **computador** rodando o app de desktop do Claude, não um celular, e mesmo lá enxerga arquivos, não armazenamento de navegador.

Restam três caminhos: o próprio app (após o deploy), DevTools por USB (`chrome://inspect`), ou executar JS na origem — abaixo.

## Bookmarklet de recuperação (testado)

Vira `syncing` → `pending`, devolvendo o item ao filtro de reenvio que **o código atualmente publicado já aplica**. Não depende do deploy da correção.

```js
javascript:(function(){var r=indexedDB.open('luna-ronda');r.onsuccess=function(){var db=r.result;var tx=db.transaction('queue','readwrite');var s=tx.objectStore('queue');var g=s.getAll();g.onsuccess=function(){var n=0;g.result.forEach(function(i){if(i.status==='syncing'){i.status='pending';s.put(i);n++;}});tx.oncomplete=function(){alert(n+' ronda(s) destravada(s). Recarregue a pagina.');};};};})();
```

Verificado com `fake-indexeddb` contra um banco montado igual ao do app (`luna-ronda` / store `queue`, keyPath `localId`): item `syncing` vira `pending`, item `synced` fica intacto, `submission` preservada.

**No Chrome Android:** o navegador remove `javascript:` colado na barra de endereços, então tem que ser por favorito — salvar um favorito qualquer, editar nome (ex. "destravar ronda") e URL (o código acima), abrir a página do Safety Walk **no Chrome normal** (o PWA instalado não tem barra de endereços) e digitar o nome do favorito na barra, escolhendo a sugestão. Mesma origem = mesmo IndexedDB do app instalado.

## Nota de método

Isto só foi possível porque o servidor foi **consultado**, em vez de se assumir que "1 enviando…" significava envio em andamento. A barra de status descreve o banco local, não o servidor — as duas coisas divergiram e ninguém tinha como saber sem perguntar ao servidor. Reforça a nota do documento principal: **unificar fila local e histórico numa visão só**, para que a tela pare de contar uma história que o servidor não confirma.
