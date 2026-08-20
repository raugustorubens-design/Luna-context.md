# A IA que mora no Forge

**19/08/2026 · nota de desenho**

Duas metades independentes: **o que ela enxerga** e **o que ela pode fazer**. E uma terceira
coisa que amarra as duas — o contrato de plugin.

---

## Metade 1 · O que ela enxerga

A diferença entre um painel de chat e o que você viu no Cursor não é o modelo. **É o
contexto montado.** Hoje o chat do Forge não sabe nem qual arquivo está aberto.

O que existe no Forge para ser sabido:

| Fonte | O que contribui |
|---|---|
| **Editor** | Arquivo aberto, trecho selecionado, posição do cursor, o que ainda não foi salvo |
| **Explorer** | Estrutura do projeto, caminho atual |
| **Terminal** | Últimas linhas de saída, código de saída do último comando |
| **Git** | Branch, arquivos modificados, o diff |
| **Reporter** | Estado dos órgãos, o que está em atenção |
| **Convergia** | Ronda aberta, documento em curadoria |
| **Chat** | O que já foi dito nesta sessão |

### O erro que eu evitaria

**Mandar tudo isso a cada mensagem.** É o mesmo problema da memória truncada: o contexto
estoura, o modelo perde o que importa no meio do que não importa, e a conta cresce sem
melhorar a resposta.

Três camadas, e só a primeira é automática:

**Sempre, e pequeno:** arquivo aberto com o nome e a linguagem, trecho selecionado, branch,
resultado do último comando. Isso é barato e resolve a maioria das perguntas.

**Sob referência explícita:** `@arquivo`, `@terminal`, `@ronda`, `@diff`. Você diz o que
trazer, como no Cursor. Previsível, e você controla o custo.

**Por busca:** quando a pergunta pede algo que não está aberto, a IA pede — *"quer que eu
leia `report.ts`?"* — em vez de varrer o projeto sozinha.

**A primeira camada sozinha já muda a experiência.** Perguntar *"por que isso está
falhando?"* com o arquivo e o erro do terminal em mãos é outra conversa.

---

## Metade 2 · O que ela pode fazer

Aqui a sua própria regra resolve o desenho, e é a mesma da ronda:

> **A IA propõe. Você ratifica.**

Ela nunca escreve no arquivo. Ela devolve um **diff**, você vê o que muda, e aceita ou
recusa. É exatamente o modelo do Cursor, e é o mesmo laço da sugestão de foto — só que agora
o que se ratifica é código.

E tem o mesmo ganho de aprendizado: **o que você recusa é dado tão bom quanto o que você
aceita.**

Três ações, em ordem de esforço:

**Propor edição no arquivo aberto** — diff em tela, botão de aceitar. É a mais valiosa.

**Preencher campo** — na curadoria do relatório, na ronda, no formulário do Convergia.
Mesmo padrão: preenche marcado como sugestão, você confirma.

**Rodar comando no terminal** — a mais delicada. Deve **sempre** pedir confirmação, mostrando
o comando antes. Nunca executar por conta.

---

## O contrato de plugin

Você quer o padrão do Connector Hub: cada um com a chave do usuário, ligado quando ele
quiser. Concordo — e a peça que falta é declarar que **um plugin contribui duas coisas**:

```
plugin
  nome, ícone
  chave: qual variável, e onde o usuário informa
  capacidades: o que a IA passa a poder fazer
  contexto: o que ele passa a saber
  estado: ligado · sem chave · com erro
```

**Um exemplo torna claro.** O plugin do GitHub contribui:

- **Capacidade:** abrir Issue, comentar em PR, ler diff
- **Contexto:** PRs abertos, Issues com rótulo `duvida`, estado do CI

Com ele ligado, *"o que está esperando resposta minha?"* passa a ter resposta. Sem ele,
a IA responde que não tem acesso — **não inventa**.

### Regras que evitam o pior

**Sem chave, o plugin aparece desligado, com o motivo.** É o mesmo desenho do sinal
desligado do Sense: o que falta se anuncia sozinho, sem virar propaganda.

**A chave é do usuário e fica com ele.** Nunca no repositório, nunca compartilhada entre
plugins.

**Contexto de plugin não vaza para outro.** O que o plugin do Supabase enxerga não entra no
prompt quando você está conversando sobre código, a menos que você chame.

**Plugin declara custo.** Se ele traz muito contexto, isso conta no orçamento e você
precisa ver.

---

## O que já existe e serve

| Peça | Onde |
|---|---|
| Conector com chave por usuário | Connector Hub, no `luna-core` |
| Capacidades registradas | Gateway, 17 hoje |
| Chat com escolha de agente | Painel do Forge, funcionando |
| Contexto montado e priorizado | Recém-construído no `#46` — a Constituição chegando ao prompt |

**O `#46` é a fundação.** Ele resolveu o problema de montar contexto com orçamento e
prioridade declarada. O que falta é acrescentar as fontes do Forge nessa montagem — não
construir montagem nova.

---

## Riscos que eu vigiaria

**Custo por mensagem.** Contexto rico é caro. Sem a divisão em três camadas, cada pergunta
vira uma conta. A medição que o `#46` introduziu — contexto montado contra enviado —
passa a valer aqui também.

**Confiança falsa.** Uma IA que parece saber tudo, mas cuja visão está desatualizada, é pior
que uma que admite não saber. O contexto precisa dizer **de quando é**: *"arquivo lido às
20:14"*.

**Comando destrutivo.** A ação de terminal é a única com poder de estrago. Confirmação
sempre, e nunca em lote.

**Chave de usuário.** Se o Forge um dia tiver mais de um usuário, chave de um não pode
alcançar contexto de outro.

---

## Ordem que eu sugiro

**1 · Contexto automático mínimo.** Arquivo aberto, seleção, branch, último comando. É
metade do valor, e reusa o que o `#46` construiu.

**2 · Referência explícita** — `@arquivo`, `@terminal`, `@diff`. Você controla o que entra.

**3 · Edição proposta como diff**, com aceitar e recusar. É o que faz parecer o Cursor.

**4 · Contrato de plugin**, com o do GitHub como primeiro. É o que você mais usa.

**5 · Preencher campo** na curadoria e na ronda.

**6 · Comando no terminal**, com confirmação. Por último, porque é o de maior risco.

Os passos 1 a 3 já entregam a sensação que você descreveu. Os 4 a 6 são o que torna o Forge
diferente de um editor com chat — porque aí a IA passa a saber da **LUNA**, não só do
código.

---

## Uma decisão sua antes do pacote

**Quem é o usuário do Forge?**

Se for só você, plugin com chave própria é conveniência. Se o Forge for produto — alguém
comprando um cockpit —, então chave por usuário, isolamento de contexto e limite de custo
deixam de ser detalhe e viram requisito.

A resposta muda o passo 4 inteiro, e é melhor decidir antes de construir.
