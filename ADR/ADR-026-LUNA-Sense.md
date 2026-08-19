# ADR-026 (proposta) — LUNA Sense

**Status:** Proposto — aguardando ratificação do Arquiteto
**Repositório-alvo do documento:** `raugustorubens-design/Luna-context.md`
**Órgão vive em:** `raugustorubens-design/Luna-reporter`

---

## Contexto

A LUNA acumula estado em quatro lugares — repositórios, Supabase, Railway e a própria
memória — e **ninguém percebe mudança neles.** Todo defeito dos últimos dois dias foi
descoberto por uma pessoa olhando o celular. Nenhum por instrumento.

Do lado do cliente, o mesmo vazio: matriz de treinamento vence, achado se repete, APR é
revisada e o procedimento não acompanha — e isso só aparece na auditoria ou no acidente.

O Reporter existe, varre GitHub, e está registrado como **não conforme** por não ter
consumidor.

---

## Decisão

Criar o **LUNA Sense**: órgão de observabilidade, e **produto**, na mesma linha do Safety
Walk, do Convergia e do Forge.

> **O Sense detecta desvio entre o que é e o que deveria ser, e avisa quem precisa saber.**
> Ele percebe. Não decide, não grava, não opina.

Ele nasce dentro do `Luna-reporter`, completando-o em vez de criar um segundo observador
pela metade — o `ENG-020` já registra o custo de repositório duplicado neste projeto.

---

## D1 · O contrato de sinal — é o que torna tudo escalável

**Um sinal é sempre a mesma estrutura.** Acrescentar sinal novo passa a ser dado, não
arquitetura:

| Campo | O que é |
|---|---|
| `invariante` | A afirmação sobre como deveria ser |
| `fonte` | De onde vem o dado, e a data dele |
| `desvio` | A diferença medida entre o real e o invariante |
| `evidência` | Os registros concretos que sustentam — sempre citáveis |
| `severidade` | Derivada de faixa de prazo declarada |
| `sujeito` | A própria LUNA, ou um cliente |
| `cobertura` | Determinístico ou resolvido com IA |

Se um sinal não consegue preencher `evidência`, ele não é emitido. **Suspeita não vira
aviso.**

## D2 · Núcleo determinístico, IA na borda

A lógica é Python e determinística. A IA entra **só onde a entrada é suja** — normalizar
nome de treinamento, extrair estrutura de APR em PDF, ligar item de norma a questão
existente, ler foto.

**A IA compreende; ela não conclui.** Depois que a entrada está limpa, o raciocínio volta a
ser data, comparação e conjunto.

Motivo que não é técnico: aviso de SSMA precisa ser defensável. *"O certificado venceu em
12/03 e a atividade consta na matriz"* se sustenta em auditoria. *"O modelo achou que"*
não.

## D3 · Todo recurso à IA é dívida declarada

```
determinístico não cobre  →  registra o vazio
IA resolve aquele caso    →  resposta nasce não ratificada
humano confirma           →  vira regra
caso seguinte             →  não chama IA
```

**Regra aprendida tem escopo** — global quando vem da norma, por cliente quando vem do
jargão dele. *"PT"* é Permissão de Trabalho num cliente e Passivo Trabalhista noutro.
**Promoção de por-cliente para global é decisão do Arquiteto, nunca contagem.**

## D4 · Observa mudança, não estado — e o silêncio é resultado

Estado repetido é ruído. Só desvio vira sinal, e isso exige linha de base persistida em
banco — não em memória de processo, senão todo reinício parece novidade.

**Ciclo sem desvio não produz registro.** É o que separa percepção de relatório periódico.

## D5 · O Sense propõe, nunca grava

A porta do conhecimento continua sendo o `knowledge-gate`, com a tranca do
`architecture-check`. O Sense submete candidato pelo Gateway; o Hipocampo decide.

Observador autônomo com direito de escrita transforma o Hipocampo de filtro em depósito.

**E o Sense não corrobora a si mesmo:** registrar que uma memória existe não faz a memória
valer mais. Mesmo princípio do ADR-014 Emenda 1.

## D6 · Canal por urgência, não por tipo

| Canal | Trabalho |
|---|---|
| **Painel** | Divulgar — panorama, tendência, e o que está desligado |
| **E-mail** | Formalizar — deixa rastro com data; em SSMA isso tem peso |
| **WhatsApp** | Agilizar — **só o que tem prazo e tem ação** |

O mesmo desvio muda de canal conforme se aproxima do prazo. **Canal é consequência da
faixa, nunca propriedade do sinal** — ratificado em 19/08.

E a faixa não sai do vencimento: sai do **tempo necessário para agir**. Agendar um
treinamento de oito horas leva semanas; corrigir a data de revisão de um documento leva
uma tarde. A primeira faixa começa no tempo de ação mais o dobro dele de folga — o que
torna o número defensável, porque responde a "por que 45 e não 30" com o prazo de
agendamento, e não com uma preferência nossa.

**Vencido volta para e-mail**, sempre: passado o prazo, o que importa é constar que foi
comunicado, com data — não a pressa.

Sinal sem tempo de ação declarado **fica só no painel**. É o comportamento seguro: não
interrompe ninguém com base em estimativa.

## D7 · Vendável sozinho, mais forte acoplado

Sozinho ele **percebe**; com Safety Walk percebe **cedo**; com Convergia percebe cedo e
**resolve**.

Isso exige: entrada própria de dados, lendo o que o cliente já tem; modelo de identidade
próprio; e **degradação por sinal, não do produto**.

**O sinal desligado declara o motivo** — *"Achado recorrente: depende de rondas
registradas. Nenhuma fonte conectada."* Não é anúncio; é o estado real do produto dele. É a
mesma disciplina do razão de estado: mostrar a não conformidade em vez de escondê-la.

---

## Escopo agora — um sinal só

**Prazo normativo vencendo.**

Escolhido porque funciona no dia um com qualquer cliente, é aritmética de data pura, é
indiscutível — o prazo é da norma, não nosso — e exercita **os três canais de uma vez**,
mudando de canal conforme a urgência.

Junto vem o mínimo estrutural: o contrato de sinal, a linha de base persistida, o
registro de cobertura, e a submissão pelo Gateway.

**Um sinal, a estrutura inteira.** Os outros quatro viram dado.

### Explicitamente fora de escopo agora

Achado recorrente, cobertura de cargo, APR versus procedimento, controle nunca verificado —
todos dependem de dado que ainda não existe. Ficam **desligados e declarados**, que é o
próprio D7 funcionando desde o primeiro dia.

---

## Pré-requisito que não é negociável

**Os vetores.** Tudo em `memoria_luna` de julho para cá está com `embedding` nulo.

Candidato que o Sense produza nesse estado some do mesmo jeito que as três correções de
sugestão sumiram — fica no banco, invisível à busca semântica. **Órgão de percepção sem
ninguém ouvindo é a não conformidade que o Reporter carrega hoje.** Não vale repetir com
nome novo.

---

## A direção — e é aqui que os seus dois projetos se encontram

O Sense começa percebendo desvio. A escala está em **quem consome o que ele percebe**.

### Sense como gatilho de aprendizado

Hoje: detecta vazio de regra → IA resolve → humano ratifica → vira regra.
**O mesmo mecanismo, apontado para fora:** detecta vazio de *conhecimento* → dispara
pesquisa → o material volta pelo `knowledge-gate`.

É o seu projeto de a LUNA pesquisar na internet o que precisa aprender. **Ele não é outro
sistema — é o D3 com o alcance ampliado.** E resolve a pergunta que a pesquisa autônoma
sempre esbarra: *pesquisar o quê?* A resposta passa a ser: o que o Sense percebeu que falta.

### A bolsa como bancada de teste do Hipocampo

A escolha é boa por um motivo específico, e não é o óbvio: **o mercado devolve verdade com
relógio.** Em SSMA você descobre que errou em meses, ou nunca. Ali você descobre amanhã.

Mas vale fixar o que se está testando, senão o teste se perde:

**O que se mede é calibração, não acerto.** A pergunta não é *"ela ganhou?"* — é *"quando
ela esteve confiante, ela estava certa?"*. Isso testa exatamente o que o ADR-014 Emenda 1
estabeleceu: os níveis de confiança significam alguma coisa? Memória `corroborated` produz
inferência melhor que `unverified`?

**Só assim o resultado transfere.** Uma calibração validada ali vale para o julgamento de
risco em SSMA; um lucro, não.

Três travas que eu registraria:

- **Sem dinheiro real.** Previsão registrada antes, resultado conferido depois. Dinheiro
  troca o que está sendo medido
- **Previsão gravada com carimbo de tempo**, antes do fato. Sem isso, não é teste — é
  narrativa
- **Mercado é adversarial.** Um sistema que parece aprender ali pode estar decorando ruído.
  Por isso a métrica é calibração ao longo do tempo, não sequência de acertos

*Isto é desenho de bancada de teste, não recomendação de investimento — não sou consultor
financeiro e não avalio o mérito da operação em si.*

---

## Consequências

**Boas.** O Reporter deixa de ser não conformidade. As três gerações do banco ganham
consumidor — era a pergunta em aberto sobre quem leria as tabelas vazias. E cada chamada
de IA vira dívida medida, com a cobertura determinística subindo como indicador de saúde.

**A vigiar.** Volume — teto por ciclo é obrigatório. Autorreferência — escopo declarado,
com o Sense fora dele. Falso sinal por reinício — linha de base no banco. E qualidade da
fonte do cliente: aviso errado desgasta mais rápido que aviso nenhum.

**Descartado.** Criar repositório novo ao lado do Reporter. Sense escrevendo direto na
memória. Idade absoluta de fonte como sinal — sem prazo normativo, sem documento acoplado
e sem divergência observada, idade é suspeita, e suspeita não vira aviso.

---

## Para ratificar

1. **O contrato de sinal** como unidade — sinal novo vira dado, não código
2. **Prazo normativo vencendo** como único sinal do escopo inicial
3. ~~As faixas de prazo por canal~~ — **ratificado em 19/08.** Pendente apenas o **tempo de
   ação** de cada tipo de pendência: quanto leva, na prática, agendar um treinamento de
   altura, revisar uma APR, substituir um controle apontado em ronda
4. **Sense como gatilho da pesquisa autônoma**, em vez de organismo separado
5. **Calibração, não retorno**, como métrica da bancada de bolsa
