# ADR-025 (proposta) — Leitura de foto acumulativa, com pergunta ao técnico

**Status:** Proposto — aguardando ratificação do Arquiteto
**Emenda a:** ADR-021 (Convergia Mobile — Ronda Fotográfica), Decisões 6 e 9
**Repositório-alvo do documento:** `raugustorubens-design/Luna-context.md`

---

## Contexto

Hoje a leitura por IA acontece uma vez, sobre **a primeira foto** do achado, e devolve
uma sugestão fechada. O Arquiteto pediu, em campo, 18/08:

> *"O ideal é a cada foto e a partir da segunda, ele soma ao contexto da primeira. O
> ideal seria questionar até."*

São duas mudanças, e a segunda é maior que parece: a leitura deixa de ser um palpite
entregue e passa a ser **uma leitura que se constrói** enquanto a pessoa caminha — com a
LUNA podendo perguntar o que não consegue ver.

---

## D1 — Contexto acumulado por achado, mantido no cliente

Cada foto nova é lida **junto do que já foi entendido** naquele achado. Foto 2 não é uma
segunda leitura: é a mesma leitura, mais informada.

O acúmulo vive no cliente, por achado, e morre com ele. Sem sessão no servidor —
mesmo padrão sem estado que o Convergia já usa, e que evita ter de limpar sessão órfã
quando alguém remove um achado no meio da ronda.

## D2 — Imagem já lida nunca é reenviada

**Esta é a decisão que torna o resto viável.**

O caminho ingênuo — mandar todas as fotos de novo a cada foto nova — faz o custo crescer
ao quadrado. Cinco fotos custariam quinze leituras de imagem. A cota do Groq foi
registrada em 10/08 **perto da saturação em 8000 TPM**; isso a estoura na primeira ronda
séria.

O caminho certo: a cada foto nova, envia-se **a imagem nova mais o texto do que já foi
entendido**. Texto é barato; imagem não. O modelo recebe o resumo do que viu antes e a
foto que ainda não viu.

Custo passa de quadrático a linear, e o resultado é melhor — o resumo é o julgamento já
consolidado, não pixels para reinterpretar.

## D3 — A LUNA pode perguntar. A pergunta nunca bloqueia

A resposta do modelo ganha um campo de **pergunta ao técnico**, para o que a foto não
resolve sozinha: altura de um guarda-corpo, se o cilindro estava em uso ou armazenado,
qual atividade estava em curso.

Regras, herdadas da mesma disciplina que fez a foto nunca ser obrigatória:

- **Zero ou uma pergunta por leitura.** Duas viram formulário
- **Ignorável.** Continuar sem responder é sempre possível, sem aviso, sem penalidade
- **Nunca bloqueia concluir a ronda.** Não entra em `requiredWhenIdentified`
- Resposta, quando vem, entra no contexto acumulado da D1

**Isto não depende de tool-calling.** A pergunta é um campo da resposta estruturada, não
uma ação que o modelo decide tomar — então não esbarra na limitação registrada em
ENG-038, que pausou `A(t)` esperando `FORGE-WORKSPACE-001`. Vale registrar explicitamente,
porque alguém vai levantar isso.

## D4 — Pergunta e resposta são o melhor dado de aprendizado que existe hoje

O laço de correção humana (10/08) aprende comparando sugerido com salvo — inferência
sobre o que a pessoa mudou e por quê.

Um par pergunta-resposta é **explícito**: a LUNA declara o que não sabia, e a pessoa
responde exatamente aquilo. Não precisa inferir intenção.

Vai para o Hipocampo pelo mesmo caminho já existente, sob a mesma regra de dado sensível
do ADR-021: **nunca nome de pessoa**, departamento e local tokenizados, achado de EPI e
comportamental mais estrito que estrutural.

## D5 — Degradação é silenciosa, mas contada

Cota estourada, rede caída, modelo fora do ar: a sugestão simplesmente não aparece, como
hoje. **Mas passa a existir um contador de leituras pedidas contra bem-sucedidas** — sem
ele, "a IA parou de ler" e "a IA não tinha nada a dizer" continuam indistinguíveis, que
é exatamente o buraco que levou uma investigação inteira ao lugar errado nesta semana.

---

## O que fica de fora, e por quê

**A comparação com APR e controles reais não entra nesta proposta.** É a Decisão 9 do
ADR-021 — percepção separada de julgamento — e continua bloqueada por uma pergunta que
ninguém respondeu:

> Existem dois schemas no Supabase: `biblioteca_*`, populado (114 riscos, 262 controles,
> 358 vínculos), e `risco`/`atividade`/`treinamento`, com chave estrangeira real e quase
> vazio. **Qual é o canônico?** ENG-037 registrou que a decisão ficaria para quando a
> Fase 4 virasse tarefa de Builder.

Esta proposta é **pré-requisito** daquela: sem contexto acumulado, não há o que comparar
com a APR. Fazer nesta ordem é mais barato do que fazer as duas juntas.

**Segunda pergunta ainda aberta:** "aprendizado da LUNA" é o laço que já existe aplicado
também às perguntas, ou é memória nova, com outra estrutura? A D4 assume o primeiro. Se
for o segundo, a D4 muda.

---

## Consequências

**Boas.** A leitura melhora conforme a pessoa fotografa mais, em vez de depender de a
primeira foto ser a certa. A pergunta transforma o que a IA não sabe em dado, em vez de
palpite. E o custo cresce de forma linear, não quadrática.

**A vigiar.** Uma pergunta a cada foto vira ruído — se acontecer, o teto passa a ser uma
pergunta por achado, não por foto. Latência acumulada em rede de planta precisa ser
medida em campo, não estimada aqui. E o contexto acumulado morre se o app for despejado —
o que hoje ainda acontece, e é motivo a mais para o defeito de despejo vir antes.

**Descartado.** Reenviar todas as imagens a cada leitura, pelo custo. Sessão de contexto
no servidor, por criar estado órfão. Pergunta obrigatória, por contrariar a disciplina de
não travar quem está em campo.

---

## Ordem de implementação

| # | O quê | Depende de |
|---|---|---|
| 1 | Dois botões de foto — câmera e escolher | nada · pacote já escrito |
| 2 | Despejo pela câmera | nada · bloqueia uso |
| 3 | `createImageBitmap` | panorâmica |
| 4 | **D1 + D2** — contexto acumulado, sem reenviar imagem | ratificação desta proposta |
| 5 | **D3 + D4** — pergunta e aprendizado | item 4 |
| 6 | Decisão 9 — comparação com APR | schema canônico decidido |

Nada disto entra antes do item 2. Contexto acumulado que se perde a cada foto porque o
app fechou é pior que sugestão simples.

---

## Próximo passo

Ratificação do Arquiteto. Três coisas para dizer sim ou não:

1. **Contexto acumulado por achado, com o texto viajando e a imagem não** (D1 e D2)
2. **Pergunta opcional, no máximo uma por leitura** (D3)
3. **Par pergunta-resposta indo para o Hipocampo pelo laço que já existe** (D4)

E a que continua pendente desde 05/08: **qual dos dois schemas é o canônico.**
