# Pacote do Engenheiro — bloquear o envio e levar até o campo que falta

> ## REPOSITÓRIO-ALVO
>
> **`raugustorubens-design/luna-frontend`** — exclusivamente.
> Escopo: `lib/ronda/`, `components/ronda/`.
> **`luna-core` não muda.** A regra do servidor está certa; o cliente é que precisa
> alcançá-la antes e apontar onde.
>
> Verifique `GENESIS/ARCHITECTURE_INVENTORY.md` antes de caracterizar qualquer repo.

**Pedido do Arquiteto, 17/08:** *"na hora de subir, não subir até os campos
obrigatórios estarem preenchidos e informar o campo que está faltando, tipo um link
até o campo."*

**Base:** o commit `9c6c709` já espelhou a regra do servidor no cliente
(`missingRequiredWhenIdentified`) e já bloqueia "Concluir". Este pacote fecha as três
lacunas que sobraram: **onde ainda não bloqueia**, **como avisar** e **como chegar
lá**.

**Regra:** só acréscimo. Nenhuma lógica de fila, IndexedDB, upload de foto ou
compressão é tocada.

---

## 1. Onde ainda não bloqueia — a tela de edição

O gate vive em `ronda-wizard.tsx` (`canConclude`). **`ronda-editor.tsx` não tem gate
nenhum.**

Isso significa que uma ronda recusada por campo faltando abre para correção, você
preenche parte, salva — e ela volta para a fila, sobe, e o servidor recusa **de novo**,
pelo campo que continua vazio. O mesmo ciclo que o fix urgente eliminou no wizard segue
inteiro na tela onde ele é mais provável de acontecer, porque é justamente ali que a
pessoa chega já vindo de uma recusa.

**"Salvar e enviar" precisa do mesmo gate**, com a mesma função — não uma cópia.
`missingRequiredWhenIdentified` já é pura e já está testada; importe-a.

### E antes de entrar na fila, não só antes de subir

Hoje a checagem é uma só, no botão de concluir. Torne-a uma invariante da fila:
`enqueueRonda` (`lib/ronda/queue.ts`) recusa item com campo obrigatório faltando, e
quem chama trata.

Não é redundância defensiva por defensividade — é o padrão que o documento de gargalos
nomeia: **o portão vem antes do custo.** Um item que não pode passar não deve ocupar
fila, não deve gastar upload, não deve gerar 422 e não deve virar registro `invalid`
que depois alguém precisa entender. Se algum caminho futuro enfileirar sem passar pelo
wizard, o gate continua valendo.

---

## 2. Como avisar — um link por campo, não um aviso por ronda

Hoje o aviso nomeia achado e campos em texto. Vira lista navegável:

```
Faltam 3 campos para concluir

Achado manual · Risco identificado
  → Departamento
  → Descrição

Movimentação de cargas · Risco identificado
  → Descrição
```

Regras:

- **Um link por campo.** "Faltam 2 campos neste achado" obriga a procurar; o pedido
  foi chegar no campo
- **Nunca uma contagem sozinha.** Foi exatamente disso que a tela do servidor sofria:
  *"6 problema(s)"* sem dizer quais
- **Nome do achado como cabeçalho**, para orientar quando há vários — use o rótulo do
  flag, ou "Achado manual" quando `flagId` for nulo
- **Rótulos em PT-BR do usuário.** `MISSING_FIELD_LABELS` já existe em
  `lib/ronda/types.ts` e é a fonte — não escreva os nomes de novo em outro lugar

O mesmo componente serve às duas origens: campos que **o cliente** detectou como
vazios, e `issues` que **o servidor** devolveu. Já existe `parseIssuePath` traduzindo
`achados.{id}.{campo}` — os dois desembocam no mesmo par `{ findingId, field }`.

---

## 3. Como chegar lá — o âncora, e a armadilha

### Um único gerador de id, usado pelos dois lados

```ts
// lib/ronda/field-anchor.ts (novo)
export function fieldDomId(findingId: string, field: MissingField): string {
  return `campo-${findingId}-${field}`;
}
```

`finding-card.tsx` usa isso para o `id` do input. O aviso usa isso para o alvo. **Nunca
escreva o formato do id à mão em nenhum dos dois.**

Isto não é preciosismo. É a lição do bug da foto, aplicada antes: lá, `fotos[]` e
`fotoIds[]` viraram dois campos independentes, um consumidor continuou lendo o antigo e
o resultado foi indistinguível de "não tem foto". Aqui, se o card e o aviso montarem o
id separadamente, o link quebra e **falha exatamente igual a um campo já preenchido** —
clica e não acontece nada. Um gerador só torna a divergência impossível.

### Quatro armadilhas desta tela especificamente

**1. O documento não rola.** A correção de viewport de 16/08 prendeu a rolagem na
`<main>`, não no documento. `scrollIntoView` usa o ancestral rolável mais próximo e
funciona — mas confirme na tela real, não no teste.

**2. O cabeçalho é fixo.** Sem `scroll-margin-top` nos campos, o input alvo para
**embaixo** do cabeçalho: a página rolou, o campo está lá, e você não vê. Parece que o
link não funcionou. Use `scroll-margin-top` compatível com a altura real do cabeçalho.

**3. O achado pode estar em outra etapa ou recolhido.** O link precisa, nesta ordem:
ir para a etapa certa → expandir o cartão do achado → só então rolar e focar. Rolar
antes de expandir mira um elemento que ainda não tem posição.

**4. No celular, o teclado abre e empurra.** Foque primeiro, role depois — ou role de
novo após o `focus`, quando a viewport já encolheu. `focus({ preventScroll: true })`
seguido de rolagem explícita dá controle sobre a ordem.

**Movimento:** `smooth` por padrão, `auto` sob `prefers-reduced-motion`. E um realce
temporário no campo alvo — a mesma marcação âmbar que `fieldNotice` já usa, não uma
cor nova.

---

## 4. O botão desabilitado — recomendação, decisão sua

Hoje "Concluir" fica desabilitado quando falta campo. Funciona, mas em campo tem um
custo real: **botão desabilitado não explica nada.** Com luva, no pátio, a pessoa
aperta, não acontece nada, e precisa descobrir sozinha que a resposta está mais acima
na tela.

**Recomendo:** o botão continua clicável, com `aria-disabled="true"` em vez do atributo
`disabled`, e ao ser tocado **não envia — rola até o primeiro campo faltando e o
foca.**

Vantagens: o toque vira a resposta em vez do silêncio; leitor de tela ainda anuncia que
está indisponível; e o botão continua alcançável por teclado, o que `disabled` impede.

**Contra:** um botão que parece ativo e não envia pode ser lido como travado. Mitigue
mantendo a diferença visual clara e trocando o rótulo quando incompleto — algo como
"Faltam 3 campos" no lugar de "Concluir ronda". Aí o botão **é** o aviso, e continua
levando ao lugar certo.

Se preferir manter `disabled`, mantenha — mas então o aviso com os links precisa estar
sempre visível junto do botão, não só no topo da etapa.

---

## 5. Verificação

`pnpm typecheck`, `pnpm test` (**75 hoje — não pode cair, nenhum existente alterado**),
`pnpm run test:constitution`, `pnpm build`.

Testes novos, em função pura:

- `fieldDomId` é estável e o mesmo id sai da detecção do cliente e do
  `parseIssuePath` do servidor, para o mesmo achado e campo
- `enqueueRonda` recusa submissão com campo obrigatório faltando
- Gate do editor devolve a mesma lista que o do wizard, para a mesma entrada

Ponta a ponta, com Playwright, no padrão que as sessões anteriores já usaram:

- Achado incompleto na Etapa C → o aviso lista um link por campo
- Clicar no link → o campo certo fica focado **e visível** (verificar que o retângulo
  do elemento não está sob o cabeçalho — não basta `document.activeElement`)
- Achado em cartão recolhido → o link expande antes de rolar
- Editor: salvar com campo faltando não enfileira

**Portão real:** o Arquiteto, no celular, numa ronda com dois achados incompletos,
toca no link e cai no campo — visível, focado, teclado aberto, sem precisar procurar.

**Regressão a vigiar:** foto continua nunca obrigatória, em nenhum estado. Já foi
corrigido uma vez em campo. Se algum caminho novo exigir foto para avançar, está
errado.

---

## 6. Ordem

Depois do pacote da foto (`GENESIS_2026-08-17_foto-nao-lida-camada2.md`) — aquele é um
recurso inteiro desligado em silêncio; este é uma melhoria sobre algo que já funciona.

Os dois tocam `finding-card.tsx` e `ronda-wizard.tsx`. **Em série, com o segundo
rebaseando no primeiro.** E ambos depois de o gate urgente sair do PR #28 para branch
própria, senão os três disputam os mesmos arquivos.

---

## 7. O que este pacote não resolve

- **Campos obrigatórios além dos quatro.** Se o servidor passar a exigir outra coisa,
  a divergência volta. A defesa definitiva é o contrato de validação ser compartilhado
  entre `luna-core` e `luna-frontend` em vez de espelhado à mão — ADR próprio
- **Metadados da ronda.** Título, data, local, responsável e turno têm gate próprio
  (`metadataComplete`) e ficam fora daqui
- **Achado em estado `nao_avaliado`.** Já coberto por `pendingFindings`; a lista de
  links trata só de campo faltando em achado identificado
