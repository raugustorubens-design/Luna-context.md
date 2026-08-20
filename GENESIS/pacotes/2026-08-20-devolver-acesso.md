# URGENTE — devolver o acesso, e o Convergia no celular

**Caminho:** `GENESIS/pacotes/2026-08-20-devolver-acesso.md`
**Estado:** pronto · **prioridade máxima**

> ## REPOSITÓRIO-ALVO
>
> **`raugustorubens-design/luna-frontend`** — exclusivamente.
> Escopo: `lib/forge/allowed-email.ts` ou `middleware.ts`, `auth.ts`,
> `components/forge/convergia-panel*`.

---

## O que está acontecendo

O Arquiteto está **trancado fora do Safety Walk**, com dois pedidos de senha do Google e
nenhuma entrada.

A sequência, e são dois defeitos se somando:

1. Ele abre `/ronda` → sem sessão → vai para o login
2. O Google aprova. O `signIn` do `auth.ts` autoriza, porque o e-mail **está** no
   `FORGE_ALLOWED_EMAIL`
3. Sem o callback `redirect`, o Auth.js devolve a raiz — **o site antigo**
4. Ele volta ao `/ronda`. Agora há sessão, mas o middleware exige
   `RONDA_ALLOWED_EMAILS`, que **não existe no ambiente** — e `isAllowedEmail` devolve
   `false` quando a variável falta
5. Barrado. Tenta de novo, segunda senha, mesmo fim

---

## Etapa 1 · O acesso de volta — e é a que importa agora

**O problema de desenho:** falhar fechado quando a variável não existe protege contra
estranho e **tranca o dono**. Numa ferramenta operada por uma pessoa, variável esquecida
vira perda de acesso ao trabalho de campo.

**Correção:** quando `RONDA_ALLOWED_EMAILS` não estiver definida, o `/ronda` **recai no
`FORGE_ALLOWED_EMAIL`**.

Não é afrouxar: continua fechado para quem não está em lista nenhuma. Só garante que **quem
administra o Forge nunca perde o acesso à ronda por variável faltando**.

Quando a variável for definida, ela manda — e aí os técnicos entram sem precisar do
`FORGE_ALLOWED_EMAIL`.

**Registre no código o motivo**, com uma linha: recaída existe para o dono não se trancar
fora, não para relaxar o portão.

## Etapa 2 · O callback `redirect`

Sem ele, o `callbackUrl` que o middleware monta com cuidado é ignorado, e todo login cai na
raiz.

Três regras, no `auth.ts`:

- Relativo → `baseUrl + url`
- Mesma origem → o próprio `url`
- Origem diferente → `baseUrl`

A terceira evita redirecionamento aberto por `callbackUrl` forjado.

**Junto com a etapa 1, isso encerra o problema:** entra pelo `/ronda`, volta ao `/ronda`, e
entra.

## Etapa 3 · O Convergia no celular

Mesma família do Forge: grade pensada para tela larga, espremida em 390 pixels.

O painel do Convergia é **lista**, não grade — e lista cabe no celular. Em tela estreita:
uma coluna, cartões empilhados, sem tabela lado a lado, sem largura fixa.

Os quatro blocos do `2026-08-20-tudo-novo.md` — em andamento, gerar, documentos recentes,
modelos — funcionam empilhados sem perder nada.

**A escolha de formato, orientação e papel** precisa caber também: três seletores em coluna,
não em linha.

---

## Pré-respostas

| Se encontrar | Faça |
|---|---|
| `RONDA_ALLOWED_EMAILS` já definida no ambiente | A recaída fica assim mesmo, para o futuro; ela só age quando falta |
| `redirect` já existir | Confira as três regras — a de origem externa é a que costuma faltar |
| O Convergia depender de largura fixa | Troque por largura fluida; **não** role horizontal |
| Tabela que não cabe no celular | Vira lista de cartões, um por linha |

## Condições de parada

- A recaída exigir mudar o comportamento do `/forge`
- Adaptar o Convergia exigir refazer o painel — nesse caso, só o essencial cabe agora, e o
  redesenho fica para o pacote `tudo-novo`

## Autorização de merge

**Etapas 1 e 2: mergeie assim que verde.** O Arquiteto está sem acesso à ferramenta de
campo, e as duas são pequenas e reversíveis.

Etapa 3: abra o PR e reporte.

---

## Critério de pronto

**1 e 2** — entrar pelo `/ronda` num aparelho sem sessão, **um único login**, e cair no
`/ronda`. Não na raiz, não numa segunda senha.

**3** — abrir o Convergia num celular e conseguir gerar um relatório sem rolagem lateral.

---

## Memórias geradas

- Falhar fechado por variável ausente protege contra estranho e tranca o dono; numa
  ferramenta de um operador só, isso é perda de acesso ao trabalho
- `callbackUrl` montado no middleware não vale nada sem o callback `redirect` no `auth.ts`
- Duas senhas seguidas sem entrar é sinal de sessão válida numa área e recusada em outra,
  não de credencial errada
