# ADR-005 — Gestão de Segredos: Nome no Código, Valor Nunca no GitHub

**Status:** Proposto

**Data:** 2026-07-11

**Relacionado a:**
- ADR-002 — Gateway e Connector Hub como órgãos distintos, coabitando o `luna-core`
- ADR-004 — Portar o Gateway para o `luna-core` e migrar seu runtime de Python para Node/TypeScript
- Sanitização de credenciais no Railway (Fase 1 desta linha de trabalho — o bug de boot `Missing SUPABASE_URL and/or SUPABASE_KEY` em `luna-core`/honest-joy)

## Contexto

Durante a revisão da migração do GitHub e dos adapters de IA para o Connector Hub (`luna-core` PR #7), ficou explícita uma confusão de modelo mental que valia a pena corrigir formalmente: a expectativa de que o valor real de uma API key pudesse viver "dentro do código, no GitHub", e que os ambientes Railway "espelhassem" automaticamente essas chaves entre si.

Nenhuma das duas coisas é verdade, e o próprio bug de boot do `luna-core` (`Missing SUPABASE_URL and/or SUPABASE_KEY`, resolvido na Fase 1 desta linha de trabalho) já era sintoma direto dessa confusão: a variável existia em outro ambiente Railway (`sunny-quietude`), mas não havia nenhuma replicação automática entre ambientes — cada um é isolado por padrão.

## Decisão

1. **O nome de uma variável de ambiente pode e deve aparecer no código** (ex.: `process.env.OPENROUTER_API_KEY`) — isso é apenas um rótulo, sem informação sensível.

2. **O valor real de qualquer credencial (API key, token, senha, connection string) nunca é commitado no GitHub**, em nenhuma hipótese, mesmo em repositório privado. Histórico de Git é permanente e amplia a superfície de vazamento (colaboradores, repositório tornado público por engano, ferramentas de terceiros com acesso ao repo).

3. **Não existe replicação automática de variáveis entre ambientes Railway.** Cada ambiente (`honest-joy`, `outstanding-learning`, `sunny-quietude`, e quaisquer futuros) mantém seu próprio conjunto de variáveis, isolado por padrão. Uma variável definida em um ambiente não existe em outro até ser colada manualmente ali, ou até ser centralizada por um mecanismo explícito (o próprio Connector Hub, quando maduro, é candidato a esse papel).

4. **Fluxo de responsabilidade ao introduzir uma nova credencial:**
   - Quem escreve código (Claude Code ou qualquer IA orquestradora) declara o nome da variável, implementa a leitura (`process.env.X`), garante que a ausência dela não derruba o serviço inteiro quando a credencial é opcional (ex.: `GITHUB_TOKEN` ausente deve permitir requisições não autenticadas, não crashar o boot), e entrega ao usuário a lista exata de nomes de variáveis novas e em qual serviço/ambiente cada uma é necessária.
   - O usuário (Rubens) cola o valor real diretamente no painel de Variables do Railway, no ambiente correspondente. Nenhuma IA gera, inventa ou manuseia o valor de uma credencial real — inclui não escrever placeholders de valor (ex.: comentários do tipo "cole sua API key aqui") dentro de arquivos de código; o nome da variável já é autoexplicativo o suficiente.

## Justificativa

- **Segurança básica**: separar nome (público, estrutural) de valor (secreto) é prática padrão de engenharia, não uma peculiaridade da LUNA.
- **Evita repetição do bug já visto**: o crash de boot por variável ausente não era falha de código nem do Railway — era expectativa equivocada sobre como variáveis se propagam entre ambientes. Registrar isso formalmente evita que a mesma suposição errada gere o mesmo tipo de bug em um quarto, quinto, sexto serviço no futuro.
- **Sustenta a Constitution**: o mesmo princípio de auditoria/rastreabilidade que já rege ADRs e checkpoints se aplica aqui — cada credencial nova deve ser rastreável (qual serviço, qual variável, por que existe), não simplesmente colada ad-hoc sem registro de onde ela é necessária.

## Consequências

- Toda PR que introduz uma nova variável de ambiente deve incluir, na descrição ou no comentário de fechamento, a lista exata de nomes de variáveis novas e o(s) serviço(s)/ambiente(s) Railway onde cada uma precisa ser configurada — nunca o valor. (Precedente já seguido em `luna-core` PR #7, antes mesmo deste ADR ser formalizado.)
- Nenhuma IA (Claude Code, GPT, ou qualquer futuro provider no Connector Hub) deve gerar placeholders de valor real de credencial dentro de arquivos de código — apenas nomes de variável e pontos de leitura.
- Quando o Connector Hub amadurecer o suficiente para centralizar gestão de credenciais entre ambientes, essa centralização deve ser tratada como evolução deste ADR, não como violação dele — o princípio "valor nunca no GitHub" permanece; muda apenas onde o valor passa a ser gerido (um cofre de segredos único, em vez de colado ambiente por ambiente).
