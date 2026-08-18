# ADR-022 — Padronização de Paleta e Redesenho

Status: Etapas 1–4 implementadas e commitadas em `luna-frontend`, branch
`claude/new-session-44hpdu` (ver §Implementação). Etapa 5 (dívida de GENESIS
de 16/08) parcialmente executada — ver §Pendência aberta. Aguardando o
Arquiteto abrir cada superfície nova em produção e aprovar, conforme o
portão descrito no pacote do Engenheiro.
Data: 2026-08-17
Decisor: Architect (Rubens)
Contexto: Engineer — a partir do pacote
`GENESIS_2026-08-17_paleta-e-redesenho-v2.md` e da referência visual
`luna-design-system-v2.html`, ambos produzidos pelo Engenheiro.

## Contexto

Duas frentes, um repositório (`luna-frontend`).

**Paleta.** O aplicativo tinha duas paletas coexistindo: o Modo Usuário e o
Forge usavam `#050816` com violeta e ciano (`tailwind.config.ts`,
namespace `luna.*`); o Safety Walk (`/ronda`) usava Midnight `#1E2761`,
papel `#F4F6FB` e três cores de classificação (`positivo`/`atencao`/
`nao_conformidade`) validadas no protótipo real do relatório
(`components/ronda/finding-card.tsx`) e medidas por contraste (o âmbar de
"Atenção" com texto Midnight, não branco — branco mede 2,16:1 e reprova
AA). A paleta do Safety Walk é a única que passou por campo, por contraste
medido e por relatório impresso — não por ser mais bonita.

**Forge.** `forge-layout.tsx` empilhava três `ResizablePanelGroup`
verticais dentro de `h-screen` — Explorer/Editor em 55% de altura, Chat em
20%, Contexto/Git/Terminal em 25%. Como a soma já fechava a tela, o Chat só
podia crescer roubando altura do editor. Não havia barra de estado,
indicador de saúde, paleta de comandos nem atalhos.

## Decisão

A paleta do Safety Walk vira a paleta do produto inteiro, com tema claro e
escuro — escuro por padrão, como já era em `/ronda`. A gramática de
classificação (conforme / atenção / não conforme, com os mesmos três hex)
vira a identidade visual: usada tanto para classificar achado de ronda
quanto para classificar o próprio estado do sistema na página nova.

O Forge ganha um layout novo, ao lado do antigo — trilha lateral de
painéis reusados, coluna própria para o Chat (em vez de faixa horizontal
de 20%), barra de comandos com paleta (⌘K) e barra de estado.

Em nenhum dos dois casos algo existente é removido, substituído ou movido.
Tudo entra aditivo, ao lado do que já funciona, e o que já funciona
continua sendo o padrão até ser visto funcionando em produção e aprovado.

## Implementação

Quatro etapas, cada uma seu próprio commit em `luna-frontend`, todas com
`pnpm typecheck`, `pnpm test` (56 passando, nenhum teste existente alterado
ou removido) e `pnpm build` verdes, mais verificação visual com Playwright
(tema claro/escuro, desktop/mobile) contra build de produção:

1. **Tokens** (`app/globals.css`, `tailwind.config.ts`, `app/layout.tsx`) —
   bloco `--luna-*` novo depois do `:root` existente, tema claro via
   `[data-theme="light"]`, bloco de religação dos tokens estruturais do
   Forge (`--background`, `--primary` etc.) com o valor anterior comentado
   em cada linha, e as três famílias (Archivo, IBM Plex Sans, IBM Plex
   Mono) carregadas via `next/font/google`, aplicadas só sob `.luna-v2`.
   `--radius` não foi religado — é lido por `rounded-lg` em três telas de
   `/ronda`, e religá-lo mudaria a aparência da ronda.
2. **Tema do site** (`components/theme/site-theme-provider.tsx` +
   `theme-toggle.tsx`) — provider irmão do de `/ronda`, não uma extensão
   dele: mecanismo diferente de propósito (atributo `data-theme` em vez de
   classe `dark`), chave de armazenamento própria (`luna-site-theme`).
   Dívida aceita e registrada abaixo.
3. **Modo Usuário v2** (`app/(site)/v2/page.tsx` + `components/site/*`) —
   página nova em `/v2`; `app/page.tsx` e os componentes atuais (`hero.tsx`,
   `cognitive-dashboard.tsx`, `pipeline-view.tsx`, `chat-terminal.tsx`,
   `observability-panel.tsx`) continuam intocados e `/` continua servindo
   eles. Inclui o razão de estado (`state-ledger.tsx`) com as nove linhas
   do pacote, literais.
4. **Forge v2** (`components/forge/forge-layout-v2.tsx` + sete componentes
   novos) — `forge-layout.tsx` não é alterado; `/forge` continua exatamente
   como hoje, `/forge?layout=v2` abre o novo. `Explorer`, `Editor`, `Chat`,
   `GitPanel`, `ContextPanel`, `Terminal`, `ClaudeCodePanel` e
   `ConvergiaPanel` são reusados sem alteração de assinatura.

Dois bugs reais foram achados testando visualmente e corrigidos antes de
fechar as respectivas etapas — registrados nas mensagens de commit de cada
etapa (`tailwind.config.ts` sem `lib/**` no glob de conteúdo, fazendo o JIT
não gerar as classes de classificação; `terminal.tsx` importado de forma
estática quebrando SSR no v2, quando o layout antigo já isolava isso com
`next/dynamic`).

## Pendência aberta

A etapa 5 do pacote (commitar em `Luna-context.md` os documentos do Gênese
de 16/08 — três achados de campo, uma decisão, uma pendência e três
patches, listados no pacote) **não foi executada**: este documento não tem
acesso ao conteúdo desses arquivos. O pacote afirma que eles "foram
escritos no projeto Claude e nunca commitados" — ou seja, existem numa
sessão/contexto diferente deste, e não vieram junto com o pacote recebido
aqui. Nenhum dos oito caminhos existe hoje em `Luna-context.md` (conferido
antes de escrever este ADR), então não há risco de sobrescrita — só a
ausência do conteúdo em si.

Por serem registro histórico de achados de campo reais (comportamento do
Safety Walk em 16/08), inventar o conteúdo para fechar a etapa violaria a
regra do próprio pacote ("não reescrever conteúdo para 'ficar atualizado'";
"nenhuma linha inventada"). Fica registrado aqui para o Architect decidir:
localizar o conteúdo original (no projeto Claude onde foi escrito) e
enviá-lo para commit, ou tratar a pendência como obsoleta se o conteúdo já
não existir em lugar nenhum.

## Consequências

- Tokens compartilhados pelas três superfícies (`/ronda`, `/v2`,
  `/forge?layout=v2`) — um único lugar de verdade para a paleta, em vez de
  cada superfície reimplementar seus próprios valores.
- Duas chaves de preferência de tema coexistindo (`luna-ronda-theme` e
  `luna-site-theme`), dívida aceita nesta decisão. Unificar exigiria editar
  o provider da ronda, que está escopado de propósito para não alcançar o
  Forge — e é esse escopo que impede um efeito colateral em campo. Fica
  para uma etapa futura, com migração de leitura das duas chaves.
- O razão de estado (`/v2#estado`) vira compromisso público de honestidade:
  como ele expõe não conformidades reais do próprio sistema (autorização do
  Gateway, Reporter), ele precisa ser mantido atualizado à medida que o
  estado muda — inclusive para pior. Suavizar uma classificação ali quebra
  a razão de a página existir.
- O Forge v2 introduz dois indicadores "sem leitura" (cinza) — CommandBar e
  StatusBar — porque este repositório não expõe endpoint de saúde para
  núcleo/guardião nem lista de problemas/diagnóstico agregado. Continuam
  cinza até esses endpoints existirem; verde antes disso seria o "verde
  mentiroso" que o pacote proíbe.
- Os dois layouts do Forge (e as duas páginas do Modo Usuário) coexistem no
  mesmo bundle — custo aceito de propósito, o preço de poder voltar em um
  clique até a aprovação.

## Alternativas descartadas

- **Manter as duas paletas.** Descartado: a inconsistência entre Modo
  Usuário/Forge e Safety Walk já era o problema que motivou este pacote —
  mantê-la não resolve nada.
- **Adotar a paleta atual do Forge (violeta/ciano) como padrão.** Descartado:
  não passou por campo, nem por contraste medido, nem por relatório
  impresso — é a paleta menos validada das duas, não a mais.
- **Página de marketing separada do painel de estado.** Descartado: o
  pacote quer que o Modo Usuário assuma a mesma responsabilidade de
  honestidade que o Safety Walk já tem com achados de campo — separar as
  duas coisas romperia essa continuidade de propósito.
