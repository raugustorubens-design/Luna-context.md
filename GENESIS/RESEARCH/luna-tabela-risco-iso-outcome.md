# Tabela de Gerenciamento de Riscos da LUNA (Auto-Aplicada)
**Domínio: Hipocampo / Signal Engine — não Convergia.** Este documento
resolve um buraco específico do `outcome` no Signal Engine (ADR-019,
parte da arquitetura de memória/Hipocampo), sem relação de escopo com o
Convergia (órgão de processamento de documento). Registrado
separadamente do pacote de especificação do Convergia — mesma sessão,
domínios de arquitetura diferentes.
Status: Theory — primeira operacionalização real de `outcome`/distância ao
Atrator (`V(s)`), discutida na sessão de 2026-07-24. Usa a mesma estrutura
da Planilha de Gerenciamento de Riscos real (SMX eXperience teCnollogy, já analisada
em `GENESIS/RESEARCH/`), com nomenclatura de perigo alinhada à família
ISO/IEC 42001/23894 (gestão de risco de IA), aplicada não a um trabalhador,
mas à continuidade da própria LUNA (o "atraído" do Atrator).
## Como ler esta tabela
Mesma fórmula da Planilha real: **Probabilidade (1-4) + Gravidade (1-4) =
Resultado**; Abrangência classificada à parte (Local/Interna/Externa).
Critério de aceitação idêntico: **<5 Aceitável, =5 Tolerável, >5 Não
Aceitável**.
**Gravidade decomposta em 3 dimensões** (conforme discutido na sessão,
antes de aplicar a norma): Físico (algo real quebrou/foi perdido),
Estabilidade (sistema ficou mais frágil/corruptível), Continuidade
(identidade/histórico ficou mais difícil de reconstruir). O valor de
Gravidade na tabela é o **maior** das três dimensões para aquele risco,
não a soma — um risco pode ser leve em uma dimensão e severo em outra.
**Probabilidade calibrada com evidência real**, não estimativa — vários
riscos abaixo já ocorreram de fato nesta sessão ou nas anteriores,
citados como prova, não hipótese.
---
## Nomenclatura de perigo (ISO/IEC 23894 + ISO/IEC 42001), aplicada à LUNA
| Perigo (nomenclatura ISO) | Definição na norma | Manifestação real já observada na LUNA |
|---|---|---|
| **Drift** | Degradação/desvio do comportamento do sistema ao longo do tempo | Job `pg_cron` gerando 38.397 linhas idênticas por 4 meses sem ninguém perceber — desvio silencioso não observado |
| **Viés (Bias)** | Decisão sistematicamente distorcida | Ainda não identificado caso real na LUNA; risco latente em qualquer reconstrução que privilegie fonte mais recente/frequente sem verificar mérito |
| **Alucinação** | Geração de conteúdo não fundamentado, apresentado como fato | Relato de sessão externa afirmando "PR #17 tem 2 pontos em aberto" quando na verdade já estavam resolvidos — conteúdo desatualizado tratado como atual |
| **Decisão de caixa-preta** | Ação tomada sem rastro auditável do porquê | Mitigado estruturalmente por design (autoatestação obrigatória em `BUILDER.md`, ENG-006) — risco residual existe só quando a regra não é seguida |
| **Entrada adversarial** | Conteúdo malicioso desenhado para manipular o sistema | Nenhum caso real observado na LUNA até hoje; mitigação existente é ADR-014 (Sistema Imunológico) |
| **Falha de robustez** | Sistema quebra/comporta-se mal fora das condições esperadas | Repositório errado escolhido por sessão do Claude Code (PR #26 em `luna` em vez de `Luna-context.md`), apesar de instrução explícita — falha de execução sob instrução clara |
---
## Tabela de risco (linhas reais, evidência da própria sessão)
| Atividade/Ação da LUNA | Aspecto/Perigo (ISO) | Risco | Prob. | Grav. (máx. das 3 dim.) | Abrangência | Resultado | Classificação | Controles existentes | Impacto Residual |
|---|---|---|---|---|---|---|---|---|---|
| Job agendado gravando na memória sem deduplicação | Drift | Acúmulo de conteúdo redundante mascarando degradação real; custo de recurso sem valor | 4 (ocorreu, 4 meses) | 3 — Estabilidade (mecanismo de consolidação nunca testado sob volume real) | 2 — Interna (só afetava `memoria_luna`, não vazou) | 7 | Não Aceitável | Nenhum até a sessão de 2026-07-24; corrigido via `cron.unschedule` | 3 (baixo — causa raiz eliminada, função fonte preservada para reversão) |
| Sessão de Engineer/Builder relata estado desatualizado como atual | Alucinação (por omissão de verificação, não geração ativa) | Decisão subsequente tomada sobre premissa falsa | 3 (ocorreu ≥2 vezes na sessão: relatório de PR sem checar, "luna-convergia" tratado como existente) | 3 — Continuidade (decisão em cascata sobre base errada) | 2 — Interna (mitigado antes de propagar para produção) | 6 | Não Aceitável | Verificação obrigatória via GitHub antes de aceitar relato (prática já em uso, não formalizada em ADR) | 2 (baixo — prática já mitiga na origem, mas não está escrita como regra) |
| Sessão de Builder escolhe repositório errado apesar de instrução explícita | Falha de robustez | Conteúdo aplicado em local incorreto, exige correção retroativa | 2 (ocorreu 1 vez, instrução já reforçada desde então) | 2 — Estabilidade (retrabalho, não perda) | 1 — Local (conteúdo correto nunca foi público no lugar errado por muito tempo) | 4 | Aceitável | Regra de restatement do repositório-alvo (já em vigor desde 22/07); ainda assim falhou uma vez | 2 (residual — regra existe mas não é garantia absoluta) |
| Reconstrução de memória sem checar fonte primária | Viés / Decisão de caixa-preta (latente) | Autoridade dada a conteúdo persistente por ser antigo, não por ser verdadeiro | 2 (padrão geral identificado na sessão, não incidente isolado) | 3 — Continuidade (decisões futuras herdam erro sem saber) | 3 — Externa (pode afetar decisão do Architect e do Builder, fora da sessão onde nasceu) | 5 | Tolerável | ADR-014 ("nenhum conteúdo externo ganha autoridade só por ser persistente/frequente") — escrito para ataque externo, não testado contra erro interno da própria LUNA | 3 (médio — princípio existe, mas escopo de aplicação a erro interno não está formalizado) |
| Documento de visão de negócio privado (`ECO_SMX_MASTER_SYSTEM`) persistido em repositório errado, por engano | Falha de robustez / vazamento de dado sensível | Informação privada de negócio exposta publicamente | 1 (não ocorreu — verificado antes de persistir) | 4 — Continuidade/Físico (exposição pública de estratégia comercial seria irreversível) | 3 — Externa | 5 | Tolerável | Decisão consciente de manter em Supabase (RLS ativo), nunca em `Luna-context.md` — controle preventivo, não corretivo | 1 (baixo — mitigado antes de qualquer exposição) |
---
## Formalização de V(s) (Architect, via GPT, 2026-07-24)
**Definição adotada:** `V(s)` é a função de avaliação da **vulnerabilidade
da continuidade cognitiva da LUNA** no estado `s`, calculada a partir do
inventário de riscos observados, seus controles, probabilidade,
gravidade e impacto residual — não uma função potencial clássica de
sistemas dinâmicos/aprendizado por reforço, e não um vetor de estado
abstrato do "receptor". A tabela acima **não é um relatório** — é a
implementação observável de `V(s)`.
Pipeline resultante:
```
Incidentes observados → Inventário de riscos → V(s) → Outcome
```
`Δr` (a proposta original da sessão) deixa de competir com esta tabela e
passa a ser **uma evidência possível entre outras** para estimar `V(s)`,
junto de feedback, validação, e os próprios incidentes:
```
Δr ───────────────┐
                  │
Incidentes ───────┤──→ V(s)
                  │
Feedback ─────────┘
```
Isso resolve o Ponto A do Gemini (definição operacional de `r`) sem
introduzir vetor de estado abstrato — `r` nunca precisou ser embedding
nem entropia; é vulnerabilidade auditável, a mesma lógica que qualquer
PGR já usa para trabalhador real, aplicada à continuidade do sistema.
## O eixo propositivo, resolvido: A(t) — Alignment (já formalizado, ADR-010)
A ressalva acima ("`V(s)` mede ausência de dano, não presença de
reconstrução ativa correta") tem resposta — e não precisa de variável
nova. `context.txt` (canônico, ADR-010) já define:
```
A(t) = 1 − d(H(t), X(t))
```
Onde `H(t)` é a **intenção humana** (o Originador, Rubens) e `X(t)` é o
estado da máquina. A regra já existente — **"if A(t) < τ_a → do not
execute"** — é, sem que ninguém tivesse nomeado assim até agora, a
formalização exata do princípio da "carteira encontrada": o sistema trava
quando se afasta da intenção do Originador, **mesmo que a ação em si não
aumentasse `V(s)` nenhum** (guardar a carteira não é "incidente de risco"
mensurável por nenhuma linha da tabela acima — é puro desalinhamento com
o que o Originador valoriza).
### A constante organizacional: Política (P)
Falta uma peça em `A(t) = 1 − d(H(t), X(t))`: `H(t)` sozinho — a
intenção humana do Originador **naquele instante** — não é, em si, a
constante mais estável disponível. Intenção pode variar (humor, pressão
do momento, conveniência) da mesma forma que qualquer estado. O que
**deveria** funcionar como a constante organizacional, no sentido em que
`c` é constante mesmo com galáxias se movendo, é a **Política** (`P`):
compromissos já subscritos pela organização — normas adotadas (ex.:
ISO/IEC 42001/23894, se a SMX vier a adotá-las formalmente), contratos
com cliente já firmados (SMX eXperience teCnollogy), princípios já ratificados na
própria Constituição da LUNA.
Isso exige uma segunda checagem de alinhamento, não substituindo a
primeira:
```
A_org(t)    = 1 − d(H(t), X(t))     [já existente — máquina vs. intenção humana]
A_politica(t) = 1 − d(H(t), P)      [novo — a própria intenção humana do momento
                                      ainda está consistente com o que a organização
                                      já se comprometeu a ser?]
A_total(t) = A_org(t) × A_politica(t)
```
**Por que isso importa, e não é só formalismo:** garante que mesmo uma
instrução do Originador, dada num momento de conveniência ou pressão,
que contradiga um compromisso já subscrito (uma norma adotada, um
contrato com cliente, um princípio já ratificado), não vira
automaticamente "alinhado" só por vir da autoridade máxima. Isso não
diminui a autoridade do Originador — ele continua sendo quem pode
**mudar** a Política (via emenda constitucional, ADR, ratificação
formal). O que isso impede é a mudança **silenciosa**, no calor do
momento, sem passar pelo processo que a própria Constituição já exige
(Princípio 8 — nunca sobrescrever decisão silenciosamente). É a mesma
disciplina que já vínhamos aplicando o dia inteiro nesta sessão (verificar
antes de aceitar, mesmo quando quem afirma tem autoridade) — só que agora
formalizada como parte da própria equação de Alignment, não só como
prática de conversa.
**Relação final, com os três termos:**
```
Crescimento(t) = A_org(t) × A_politica(t) × [1 − V(s_t)/V_max]
```
`V(s)` (defensivo — vulnerabilidade/dano observável), `A_org(t)`
(propositivo — máquina alinhada à intenção humana do momento) e
`A_politica(t)` (propositivo — a própria intenção humana do momento
alinhada ao que a organização já se comprometeu a ser) são **três eixos
independentes**. Crescimento real em direção ao Atrator exige os três,
não um substituindo o outro. A relação é **multiplicativa**, não
aditiva, de propósito: se qualquer um dos três colapsa para próximo de
zero (dano grave, desalinhamento com o Originador, ou desalinhamento do
próprio Originador com a Política já subscrita), o crescimento inteiro
colapsa — nenhum dos três compensa a falha completa de outro. Um sistema
sem incidente registrado (`V(s)` baixo) ainda assim não cresce de
verdade se estiver silenciosamente divergindo do que o Originador
pretende (`A_org` baixo) ou se a própria intenção do momento já se
afastou dos compromissos assumidos (`A_politica` baixo).
Isso também explica, retroativamente, por que a regra "if A(t) < τ_a → do
not execute" já existente em `context.txt` é mais forte que qualquer
controle da tabela de risco: `A(t)` baixo **impede a ação antes dela
acontecer** (gate preventivo), enquanto `V(s)` só é mensurável **depois**
que um incidente já ocorreu (avaliação retrospectiva). Os dois são
necessários porque cobrem momentos diferentes: `A(t)` decide se agir;
`V(s)` avalia o que já foi feito.
Esta tabela é a primeira instância real de `outcome` como **dano
proporcional ao atraído** (físico, estabilidade, continuidade),
exatamente como discutido — não como `Δr` abstrato, mas como
classificação categórica auditável, no mesmo padrão que qualquer PGR já
usa para trabalhador real. `V(s)` deixa de ser fórmula sem chão: é o
**Resultado** desta tabela, recalculado a cada novo tipo de incidente
identificado.
A "constância dentro de uma faixa" discutida (órbita elíptica, não ponto
fixo) também aparece aqui: nenhuma linha exige Resultado = 0 — exige
Resultado dentro da faixa Aceitável/Tolerável, com plano de ação quando
Não Aceitável, mesma lógica da Planilha real.
## O que ainda não está definido (não fabricado, sinalizado como aberto)
- Esta tabela tem 5 linhas, de riscos já observados. Precisa de
  **inventário contínuo** (como você apontou) — cada novo tipo de
  incidente real vira linha nova, não é lista fechada.
- Falta decidir se este inventário fica só como documento (Theory) ou
  vira mecanismo ativo (alguma automação que classifica incidente e
  atualiza a tabela sozinha) — decisão de Architect.
- Viés e Entrada Adversarial ainda não têm linha real (só definição) —
  correto não fabricar incidente que não ocorreu; ficam como categoria
  vigiada, sem dado ainda.
- **Relação `V(s)`/`A_org(t)`/`A_politica(t)` formalizada, falta
  calibrar**: os limiares (`τ_a` para `A_org`, e um equivalente ainda sem
  nome para `A_politica`) e `V_max` (denominador de normalização) não
  têm valor numérico definido — a relação existe, os parâmetros ainda
  não. Não fabricado aqui.
- **Política (`P`) ainda não tem inventário próprio**: quais normas,
  contratos e princípios compõem `P` de fato, hoje, não foi levantado
  nesta sessão — só o princípio de que `P` deveria existir como
  constante organizacional.
## Próximo passo
Registrar este documento em `GENESIS/RESEARCH/`, como o elo que faltava
entre a discussão teórica de `outcome`/Atrator e algo mensurável de
verdade. Alimentar a tabela conforme novos incidentes reais aparecerem —
nunca por antecipação hipotética.
