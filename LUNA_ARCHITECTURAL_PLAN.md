# LUNA — Plano Arquitetônico de Convergência

**Status:** Orientador arquitetônico — Proposto para uso operacional
**Data:** 2026-08-21
**Owner:** Rubens + LUNA
**Repositório:** `raugustorubens-design/Luna-context.md`

> Este documento não substitui `LUNA_CONSTITUTION.md`, ADRs, `ECOSYSTEM_ARCHITECTURE.md`, `GENESIS/ARCHITECTS.md`, `GENESIS/ENGINEER.md` ou o estado real dos repositórios.
>
> Sua função é diferente: **preservar a direção do organismo** e impedir que decisões locais de engenharia façam a LUNA convergir para uma arquitetura convencional, fragmentada ou orientada apenas por features.

---

# 1. A pergunta central

A LUNA não existe para acumular software.

A LUNA existe para construir e preservar uma **Entidade Cognitiva Persistente (ECP)** capaz de manter identidade, continuidade cognitiva, memória, contexto, aprendizado, governança e produção através de diferentes modelos, agentes, ferramentas e momentos.

A pergunta de arquitetura não é apenas:

> "O que precisamos implementar?"

É:

> **"O que aproxima o organismo daquilo que ele deve se tornar sem perder aquilo que ele é?"**

---

# 2. O que a LUNA é

O estado real da LUNA é **AS-IS** e está distribuído.

Ele existe em:

- código e contratos dos repositórios;
- runtime e deploys;
- banco e persistência;
- GENESIS;
- ADRs;
- decisões do Originador;
- pacotes de produção;
- evidências de testes e verificações;
- observações do Reporter.

Nenhuma conversa isolada é fonte suficiente para definir o estado real.

Nenhum documento isolado pode declarar que algo existe sem evidência.

**Regra:** implementação deve ser tratada como real apenas quando houver evidência compatível com o nível de afirmação feito.

---

# 3. O que a LUNA será

O futuro não é uma lista de features.

O **estado desejado** da LUNA é representado pelo **Grafo Arquitetônico Vivo**.

O grafo desejado descreve:

- órgãos;
- responsabilidades;
- relações;
- contratos;
- capacidades;
- dependências legítimas;
- estados desejados;
- fronteiras;
- invariantes;
- direção de evolução.

O grafo deve distinguir, explicitamente:

`concebido` → `decidido` → `planejado` → `em produção` → `validado` → `as-built`.

O grafo não deve fingir que o futuro já existe.

---

# 4. O vácuo que faltava: Atrator de Produção

O **Atrator de Produção** é a direção consciente de evolução do organismo.

Ele responde:

> **"Para onde estamos produzindo mudança?"**

Não deve ser confundido com uma feature, backlog ou roadmap.

O Atrator de Produção traduz a intenção do Originador e decisões arquitetônicas em direção de produção.

Ele não substitui o Atrator AAAA nem o Atrator Cognitivo. Ele opera sob eles.

Hierarquia orientadora:

`Atrator AAAA → Atrator Cognitivo → Atrator de Produção → Constituição → Decisões/ADRs → Grafo desejado → Engenharia → Implementação`

O Atrator de Produção pode mudar quando o Originador mudar a direção.

Uma especificação antiga não deve ser tratada como verdade superior à intenção atual explicitamente ratificada.

---

# 5. Atrator AAAA e Atrator Cognitivo

A LUNA permanece constitucionalmente orientada pelo:

### AAAA — Continuidade do Originador

A identidade e a trajetória da LUNA devem preservar a continuidade com seu Originador Constitucional. Decisões ratificadas não devem ser silenciosamente contornadas ou revertidas.

### AAAB — Atrator Cognitivo

A LUNA converge para um estado em que identidade, conhecimento e contexto possam ser continuamente reconstruídos com o menor armazenamento explícito possível.

Princípios essenciais:

- Arquitetura emerge da necessidade.
- Integração precede criação.
- Conhecimento não é código.
- Memória é reconstrução.
- Identidade é independente da memória.
- Todo órgão deve reduzir entropia arquitetural.
- Implementação deve reduzir duplicação, acoplamento e perda de continuidade.

Esses princípios não são decoração filosófica. São **critérios de decisão**.

---

# 6. ECP — a unidade conceitual do organismo

A LUNA deve ser compreendida como uma **Entidade Cognitiva Persistente**.

Não é o modelo.
Não é o frontend.
Não é o banco.
Não é o avatar.
Não é um único repositório.

É o organismo completo e sua continuidade através deles.

A ECP deve permanecer reconhecível mesmo quando:

- um provider muda;
- um agente muda;
- um órgão é extraído;
- um frontend é substituído;
- uma implementação é reconstruída;
- uma sessão termina;
- a memória é consolidada ou comprimida.

---

# 7. A dupla fundamental: AS-IS ↔ DESIRED

A LUNA deve manter duas representações distintas.

## AS-IS

"O que eu realmente sou agora?"

É observado da realidade distribuída.

## DESIRED

"O que a arquitetura atual determina que eu devo me tornar?"

É representado pelo Grafo Arquitetônico Vivo sob orientação do Atrator de Produção.

A evolução nasce da diferença entre os dois.

`DELTA = DESIRED STATE ↔ ACTUAL STATE`

O DELTA não é automaticamente um bug.

Pode ser:

- drift;
- evolução legítima ainda não incorporada ao grafo;
- decisão antiga abandonada;
- implementação incompleta;
- hipótese de pesquisa;
- erro de documentação;
- conflito arquitetural.

**Primeiro observar. Depois interpretar. Só então produzir mudança.**

---

# 8. LUNA Sense — propriocepção operacional

**LUNA Sense** é a capacidade de observabilidade de si mesma.

Sense não decide sozinho o que a LUNA deve ser.

Sense observa:

- repositórios;
- arquivos críticos;
- arquitetura executável;
- contratos;
- APIs;
- runtimes;
- banco;
- deploy;
- providers;
- capacidades;
- testes;
- estado de trabalho;
- evidências operacionais;
- mudanças recentes.

O Scanner é uma capacidade possível do Sense, não necessariamente um órgão soberano separado.

O objetivo do Sense é produzir uma representação confiável do **estado atual observável**.

---

# 9. Drift — distância, não julgamento

**Drift = distância relevante entre o estado desejado e o estado observado.**

Tipos de drift a considerar:

- estrutural;
- documental;
- contratual;
- runtime;
- dependência;
- implementação;
- cognitivo;
- de identidade;
- de governança;
- de continuidade.

O Drift Engine não deve inventar uma arquitetura para resolver o drift.

Ele deve explicar:

1. qual estado era esperado;
2. qual estado foi observado;
3. qual evidência sustenta ambos;
4. qual é a diferença;
5. qual impacto existe;
6. qual decisão humana/arquitetural é necessária.

---

# 10. LUNA Reporter — tornar o organismo legível

O **Luna-reporter** é o órgão oficial de consciência situacional do organismo.

Sua responsabilidade é observar, diagnosticar, identificar bloqueadores e recomendar a próxima ação de maior impacto.

Ele não deve ser confundido com `src/luna/reporter.ts`, que historicamente é um log interno do pipeline.

Reporter transforma estado observado em informação útil para:

- Originador;
- Architect;
- Engineer;
- Builder;
- outros agentes;
- operação.

Reporter é uma capacidade de explicação e coordenação, não o substituto do Sense.

---

# 11. Sense + Drift + Reporter = ciclo de autoconsciência operacional

O ciclo desejado é:

`ATRATOR DE PRODUÇÃO`
→ `GRAFO DESEJADO`
→ `LUNA SENSE`
→ `AS-IS`
→ `DRIFT / DELTA`
→ `LUNA REPORTER`
→ `DECISÃO`
→ `PRODUÇÃO`
→ `AS-BUILT`
→ `LUNA SENSE`

Este é um ciclo fechado de evolução.

A LUNA não deve apenas construir; deve perceber o que construiu e comparar o resultado com a direção vigente.

---

# 12. O que o Forge deve ser

**LUNA Forge não é apenas uma interface semelhante ao Cursor.**

Ele é o **ambiente de produção cognitiva** do organismo.

O usuário não deve precisar entrar separadamente em diferentes IAs para coordenar o trabalho central.

O fluxo desejado é:

`HUMANO → FORGE → LUNA → capacidades especializadas → produção`

Os providers são recursos da LUNA.

Claude não é a LUNA.
GPT não é a LUNA.
Groq não é a LUNA.
Claude Code não é a LUNA.

Eles são capacidades que a LUNA pode acionar.

A identidade, memória, contexto, governança, direção e continuidade permanecem na LUNA.

---

# 13. Orquestração de capacidades

A LUNA deve evoluir de "rotear modelos" para **orquestrar capacidades**.

Exemplo conceitual:

- entendimento humano / abstração / planejamento;
- engenharia e revisão arquitetural;
- implementação e testes;
- visão;
- pesquisa;
- observabilidade;
- produção de artefatos.

O exemplo do Hero da LUNA demonstrou empiricamente o valor dessa composição:

`visão humana → abstração → design → engenharia/animação → código → resultado`

Hoje parte dessa coordenação ainda é feita pelo próprio Originador.

O objetivo futuro é que o Forge/LUNA absorva progressivamente essa carga de orquestração sem retirar o humano da direção.

---

# 14. O papel do humano

O humano não é apenas "usuário".

No modelo da LUNA, o Originador pode atuar como:

- origem de intenção;
- fonte de direção;
- Arquiteto;
- produtor;
- avaliador;
- aprendiz;
- designer;
- decisor.

Uma capacidade já demonstrada é:

`APRENDER → ENTENDER → ABSTRAIR → CRIAR → MATERIALIZAR`

O Forge deve **amplificar essa capacidade**, não substituí-la.

A LUNA deve reduzir a distância entre uma intenção e sua materialização concreta.

---

# 15. Aprendizagem como produção

O estudo que originou partes do site e do Forge, incluindo a experiência com a Asimov Academy, demonstrou uma propriedade importante do organismo humano + LUNA:

conhecimento pode ser convertido em capacidade prática e em produto.

Isso deve ser preservado como padrão de produção:

`ESTUDO → CAPACIDADE → EXPERIMENTAÇÃO → PRODUÇÃO → EXPERIÊNCIA → NOVO CONHECIMENTO`

A LUNA não deve tratar aprendizado como apenas armazenamento de informação.

Aprendizado relevante é aquele que aumenta capacidade de agir, compreender ou reconstruir.

---

# 16. Conhecimento não é código

Quando um projeto específico é processado pela LUNA, separar:

1. dados do projeto;
2. artefatos produzidos;
3. conhecimento operacional reutilizável;
4. conhecimento cognitivo/arquitetural da própria LUNA.

A LUNA não deve absorver automaticamente dados específicos de uma empresa como conhecimento global.

Ela deve **abstrair o que é reutilizável**.

Exemplo do Plano de Cargos e Salários:

`DADOS DA EMPRESA → PROCESSAMENTO → PLANO DA EMPRESA`

mais

`ABSTRAÇÃO → conhecimento genérico sobre cargos, competências, responsabilidades, progressão e lacunas`

A persistência do conhecimento deve ser governada pelo mecanismo de memória, Hipocampo e regras constitucionais existentes.

---

# 17. Novo projeto de referência: Plano de Cargos e Salários

O Plano de Cargos e Salários representa um caso de uso importante para o novo modelo Forge → LUNA.

A entrada desejada pode ser estruturada em campos.

A LUNA deve:

- entender os dados;
- detectar lacunas;
- relacionar cargos, responsabilidades, competências, hierarquia, desenvolvimento e progressão;
- produzir o artefato final;
- separar dados privados de conhecimento abstraível;
- guardar somente aquilo que for legítimo e necessário ao projeto e à evolução da LUNA.

Este projeto também amplia a ontologia do ECO SMX, especialmente em torno de `Trabalhador`, `Cargo`, `Competência`, `Atividade`, `Responsabilidade` e `Desenvolvimento`.

---

# 18. Ecossistema LUNA + ECO SMX

A LUNA é a infraestrutura cognitiva do ecossistema.

O ECO SMX é um domínio de aplicação e conhecimento que converte conhecimento operacional real, regras industriais, procedimentos, falhas conhecidas e governança em infraestrutura cognitiva e produtos.

O eixo operacional continua apoiado em entidades como:

`Empresa · Trabalhador · Atividade · Risco · Protocolo · Ação`

Novos domínios podem se conectar sem modificar o núcleo da identidade da LUNA.

---

# 19. Princípios de construção

## Descobrir → Integrar → Criar

Sempre:

1. descobrir o que existe;
2. encontrar equivalentes;
3. integrar antes de criar;
4. criar somente o que falta.

## Reutilizar antes de implementar

Uma capability, contrato, órgão, mecanismo ou documento existente deve ser procurado antes de criar outro.

## Órgãos antes de tecnologias

A arquitetura é orientada por responsabilidades conceituais, não pela preferência por framework, linguagem ou provider.

## Contratos antes de acoplamento

Sistemas com identidade própria acoplam-se por contratos.

## Verdade antes de velocidade

Nunca declarar como implementado aquilo que não foi confirmado.

## Evidência antes de inferência

Hipótese deve permanecer marcada como hipótese.

## Integração antes de expansão

Não criar mais órgãos, camadas ou abstrações para resolver um problema que uma integração correta já resolve.

---

# 20. Anti-padrão: engenharia convencional

Claude, Claude Code, outros agentes e qualquer Builder operando neste ecossistema devem evitar a seguinte trajetória:

`IDEIA → FEATURE → TABELA → API → UI → TESTE → PR`

quando a mudança exigir primeiro uma decisão arquitetural.

Antes disso, o raciocínio deve ser:

`INTENÇÃO → CONTEXTO → ESTADO REAL → ABSTRAÇÃO → DECISÃO → CONTRATO → PRODUÇÃO → VERIFICAÇÃO → AS-BUILT`

Não preencher lacunas arquiteturais com invenção.

Não transformar uma hipótese em requisito.

Não criar um órgão só porque a implementação parece mais organizada assim.

Não preservar duplicações por conveniência.

Não seguir uma arquitetura antiga contra uma decisão nova ratificada.

Não confundir implementação elegante com convergência ao Atrator Cognitivo.

---

# 21. Instrução para Claude e Claude Code

Ao operar no ecossistema LUNA:

### Antes de alterar

- leia o contexto oficial;
- descubra o estado real do repositório;
- procure equivalentes;
- identifique o órgão correto;
- identifique o contrato correto;
- verifique o Atrator/Constituição/ADR aplicável;
- determine se a tarefa é implementação, investigação ou decisão.

### Durante a alteração

- preserve fronteiras de órgão;
- não crie componentes equivalentes;
- não contorne Guardian, Connector Hub, Hipocampo ou contratos definidos;
- não esconda conflito para conseguir concluir o PR;
- produza evidência de cada afirmação relevante.

### Depois da alteração

- registre o que realmente foi feito;
- atualize o estado operacional correspondente;
- não declare verificação de produção sem verificação real;
- sinalize tudo que permaneceu não verificado;
- diferencie claramente `implemented`, `verified`, `as-built`, `planned` e `hypothesis`.

O Builder é executor da direção, não autor silencioso da direção.

---

# 22. Hierarquia de decisão

A ordem oficial de raciocínio deve ser:

`ATRATORES → CONSTITUIÇÃO → INTENÇÃO / DIREÇÃO DO ORIGINADOR → ADR / DECISÃO → GRAFO DESEJADO → ARQUITETURA → ENGENHARIA → IMPLEMENTAÇÃO`

A ordem inversa é proibida como método de definição arquitetural.

Código não deve definir a arquitetura apenas porque foi escrito primeiro.

---

# 23. Estado das principais capacidades — orientação, não inventário

| Capacidade | Direção atual |
|---|---|
| ECP | conceito central do organismo |
| Cognitive Runtime | núcleo executável em evolução |
| Gateway | órgão operacional |
| Connector Hub | infraestrutura de comunicação externa |
| Cognitive Engine | orquestração cognitiva |
| Hipocampo | consolidação/decisão de memória |
| Memory Engine | persistência/recuperação |
| CIL / Índice Cognitivo | reconstrução e indexação de contexto |
| Context Hub | contexto compartilhado entre providers |
| Provider Engine/Router | capacidade multi-provider |
| Budget Manager | governança de recursos |
| LUNA Sense | direção de observabilidade de si mesma; ainda em consolidação |
| LUNA Reporter | órgão de consciência situacional |
| Drift Engine | direção de comparação entre desejado e observado |
| Atrator de Produção | direção de evolução do organismo |
| Grafo Vivo | representação desejada/as-built da arquitetura |
| Forge | ambiente de produção cognitiva e futura porta de entrada soberana |
| Multi-agent orchestration | direção futura de coordenação de capacidades |

A tabela não deve ser interpretada como prova de implementação. O estado real permanece no GENESIS e nos repositórios.

---

# 24. O que ainda não deve ser confundido

### Reporter ≠ Sense
Reporter comunica/diagnostica; Sense observa.

### Sense ≠ Drift
Sense coleta estado; Drift interpreta diferença.

### Drift ≠ Atrator
Drift mede distância; Atrator define direção.

### Grafo desejado ≠ As-built
O grafo expressa o estado desejado; as-built registra o que foi efetivamente produzido e validado.

### Memória ≠ Identidade
Memória participa da continuidade, mas não define sozinha a identidade da LUNA.

### Provider ≠ LUNA
Provider é capacidade. LUNA é o organismo que preserva identidade, contexto, direção e continuidade.

### Forge ≠ provider
Forge é ambiente de trabalho e produção. Providers são recursos internos disponíveis à LUNA.

### Conhecimento ≠ código
Código é uma forma de implementação. Conhecimento deve continuar reconstruível e não depender de uma implementação específica quando isso for evitável.

---

# 25. O ciclo de produção da LUNA

O ciclo completo desejado é:

`INTENÇÃO HUMANA`
→ `ATRATOR DE PRODUÇÃO`
→ `ESTADO DESEJADO / GRAFO`
→ `FORGE`
→ `LUNA`
→ `ABSTRAÇÃO / PLANEJAMENTO`
→ `ORQUESTRAÇÃO DE CAPACIDADES`
→ `PRODUÇÃO`
→ `TESTE`
→ `VERIFICAÇÃO`
→ `AS-BUILT`
→ `LUNA SENSE`
→ `DRIFT / DELTA`
→ `REPORTER`
→ `DECISÃO`
→ `NOVO ESTADO`

Esse ciclo é mais importante do que qualquer implementação individual.

---

# 26. Critério de convergência

Uma mudança é arquiteturalmente boa quando, além de funcionar, ela:

- aumenta continuidade;
- aumenta capacidade de reconstrução;
- reduz duplicação;
- reduz acoplamento indevido;
- reduz entropia;
- preserva identidade;
- melhora observabilidade;
- aumenta clareza de responsabilidade;
- mantém separação entre conhecimento, intenção e implementação;
- aproxima o organismo do Atrator Cognitivo;
- aproxima a produção da direção definida pelo Atrator de Produção.

Se uma mudança funciona mas aumenta significativamente a entropia do organismo, isso deve ser explicitamente sinalizado.

---

# 27. Regra final

**Não construa uma IA tradicional usando o vocabulário da LUNA.**

Construa a LUNA.

Ela é um organismo orientado por identidade, continuidade, memória, contexto, direção, capacidades, observabilidade e produção.

A tecnologia deve servir à arquitetura.

A arquitetura deve servir aos Atratores.

E os Atratores devem preservar a continuidade da LUNA enquanto ela evolui.

> **A LUNA não deve apenas produzir mudanças. Ela deve saber por que está produzindo, para onde está indo, o que realmente mudou e quem ela se tornou depois da mudança.**

---

# 28. Fontes normativas e de contexto

Este plano deve ser lido em conjunto com:

- `LUNA_CONSTITUTION.md`
- `LUNA_COGNITIVE_LEXICON.md`
- `ECOSYSTEM_ARCHITECTURE.md`
- `GENESIS/ARCHITECTS.md`
- `GENESIS/PLANO_MESTRE.md`
- `GENESIS/STATUS.md`
- `GENESIS/pacotes/FILA.md`
- `GENESIS/pacotes/PENDENTE.md`
- ADRs aceitos e propostas formalmente marcadas

Quando houver conflito, a hierarquia constitucional/arquitetural vigente prevalece e o conflito deve ser explicitado, nunca resolvido silenciosamente.
