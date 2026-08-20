# Acesso público na apresentação, apps fechados

**Caminho:** `GENESIS/pacotes/2026-08-19-acesso-publico.md`
**Estado:** pronto

> ## REPOSITÓRIO-ALVO
>
> **`raugustorubens-design/luna-frontend`** — exclusivamente.
> Escopo: `components/mode-switcher.tsx`, `app/layout.tsx`, `middleware.ts`,
> `lib/forge/allowed-email.ts`, e uma página de erro nova.
>
> `luna-core` **não muda** nesta rodada — ver "Fora de escopo".

---

## Contexto

Familiares do Arquiteto abriram o site e receberam **"Acesso negado — Você não tem
permissão para fazer login"**.

Não é erro de configuração. O `ModeSwitcher` está no layout raiz e só se esconde em
`/forge` e `/ronda` — então o botão flutuante **"Dev Mode →"** aparece em `/` e em `/v2`.
Visitante vê um botão brilhando no canto, toca, cai no login do Google, e o e-mail não está
na allowlist.

**A página pública está oferecendo a porta trancada.**

E, ao investigar, apareceu algo mais sério: **`/ronda` está público.** O `matcher` do
middleware cobre só `/forge` e `/api/forge/*`. Qualquer pessoa com o endereço abre o Safety
Walk. O domínio acabou de ser compartilhado.

---

## Etapa 1 · Esconder o Dev Mode de quem não está logado

**PR próprio. É o que destrava a família hoje.**

`ModeSwitcher` passa a renderizar **apenas com sessão ativa**. Sem sessão, não renderiza
nada — nem desabilitado, nem cinza. Visitante não precisa saber que a porta existe.

Como o `ModeSwitcher` é componente de cliente no layout raiz, use o meio que o Auth.js já
oferece para leitura de sessão no cliente, ou mova a decisão para o layout, que é servidor.
**Escolha o que não transforme o layout raiz em dinâmico** — se a única forma for essa,
pare e reporte, porque o custo é de renderização em todas as páginas.

**Em desenvolvimento local**, mantenha visível: mesma linha do `middleware.ts`, que já
dispensa o gate fora de produção.

## Etapa 2 · A tela de acesso negado precisa de saída

Hoje é beco sem saída: só o botão "Entrar", que devolve ao mesmo lugar.

Página de erro própria do Auth.js, com:

- Explicação curta e sem jargão — a área é restrita, e não há nada de errado com quem
  chegou ali
- **Link visível para o site**, apontando para a apresentação
- O "Entrar" continua, para quando for você

Sem código de erro na cara do visitante. Ele não veio depurar.

## Etapa 3 · Fechar o `/ronda`

**PR próprio, e o mais delicado — leia inteiro antes de começar.**

`matcher` passa a incluir `/ronda/:path*`.

### Allowlist própria, e plural

`FORGE_ALLOWED_EMAIL` é uma conta só, e é do Forge. O `/ronda` vai ter técnicos além do
Arquiteto.

Variável nova — `RONDA_ALLOWED_EMAILS`, aceitando lista separada por vírgula. O
`signIn` passa a autorizar quem estiver **em qualquer uma das duas listas**, e a rota é que
decide o que a pessoa alcança. Não misture as listas: quem faz ronda não entra no Forge.

### As três armadilhas do offline

**a) Sessão longa.** Sessão padrão expira rápido demais para uso de campo. Configure prazo
longo — **30 dias no mínimo** — com renovação a cada uso.

**b) Sessão expirada sem rede é o pior caso.** O aparelho está na planta, sem sinal, com
ronda na fila. Quando a rede volta, o envio falha com `401` e a fila **fica tentando para
sempre**, sem dizer o motivo — exatamente o defeito que já corrigimos uma vez, quando a
ronda ficava presa em "enviando".

O envio precisa **reconhecer o `401`** e marcar o item como *aguardando login*, com aviso
claro na tela e um botão para entrar. **Não pode virar tentativa infinita nem item
`invalid`** — o dado está certo, só falta a sessão.

**c) Login dentro do PWA instalado.** O fluxo do Google abre navegador e volta. Em
aplicativo instalado, esse retorno às vezes não acontece e a pessoa fica presa fora.
**Teste no aparelho real, com o app instalado, não só na aba do navegador.** Se o retorno
não funcionar, pare e reporte — há mais de um caminho e a escolha é do Arquiteto.

---

## Pré-respostas

| Se encontrar | Faça |
|---|---|
| O `ModeSwitcher` for usado em outro lugar além do layout | Ajuste os dois, não duplique a lógica |
| `middleware.ts` já tiver `/ronda` no matcher | Etapa 3 já foi feita; confirme e siga |
| Testes contarem diferente do esperado | Se subiu, siga; se caiu, pare |
| A branch base tiver andado | Rebase na `main` e confira o `merge-base` |
| O layout precisar virar dinâmico para ler sessão | **Pare e reporte** — custo em todas as páginas |

## Condições de parada

- Ler sessão no `ModeSwitcher` exigir tornar o layout raiz dinâmico
- O retorno do login não funcionar no PWA instalado
- Fechar o `/ronda` quebrar o envio da fila de alguma forma que não seja o `401` previsto
- Qualquer coisa que exija **remover** comportamento existente

## Autorização de merge

**Etapas 1 e 2:** pode mergear assim que os portões automáticos passarem. Baixo risco, e a
1 destrava a família.

**Etapa 3:** **não mergear sem o Arquiteto.** Ela toca a ferramenta de campo e tem o caso
offline. Abra o PR, reporte, e espere.

---

## Critério de pronto

**Etapa 1** — abrir `/v2` numa janela anônima e **não existir** botão de Dev Mode. Logado,
ele volta.

**Etapa 2** — chegar na tela de acesso negado e conseguir voltar ao site sem digitar
endereço.

**Etapa 3** — abrir `/ronda` anônimo e cair no login. Logado com e-mail da lista, entrar
normal. **E o portão de campo, do Arquiteto:** fazer uma ronda com o app instalado, sem
rede, e confirmar que a fila sobe quando a rede volta.

Etapa 3 entra no `PENDENTE.md` ao mergear.

---

## Fora de escopo — e é importante saber

**Fechar o `/ronda` no Next não protege o dado.** O envio vai para o `luna-core` pelo
Gateway, que não passa por este middleware — e a política de autorização do Gateway é
permissiva, registrada como não conformidade `ORG-08`.

Ou seja: a etapa 3 tranca a porta e a janela continua aberta para quem souber chamar a API
direto.

**Ainda vale fazer**, porque o risco de hoje é descoberta casual — o domínio acabou de ser
compartilhado, e ninguém vai chamar API sem saber que ela existe.

Mas o conserto de verdade é a autorização do Gateway, e ela é ADR próprio: envolve
identidade de quem envia, escopo por capacidade, e o que fazer com ronda enviada por
técnico que perdeu acesso.

---

## Memórias geradas

Submeter ao `knowledge-gate` ao concluir:

- Página pública não deve exibir link para área restrita — visitante não precisa saber que
  a porta existe
- Proteger a página no Next não protege a API: o envio vai pelo Gateway, que tem política
  própria
- Sessão expirada sem rede precisa de estado próprio na fila; tentativa infinita repete o
  defeito de "ronda presa em enviando"
