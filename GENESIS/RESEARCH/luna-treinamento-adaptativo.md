# Treinamento Adaptativo com Captura de Conhecimento Tácito — Research Hypothesis

Status: Research Hypothesis pronta para promoção a Theory, com resultado
de campo real confirmando a teoria (não é hipótese não-testada — o
método já rodou fora da arquitetura LUNA, com resultado positivo
mensurado) e com os dois pontos pedagógicos centrais já esclarecidos
pelo Originador (ver "Pontos que estavam em aberto — resolvidos"). Não
implementado no Convergia/Cognitive Engine ainda. Registrado a partir de
relato direto do Originador (2026-07-23), Engineer presente na sessão
que extraiu e organizou o método, sem ter presenciado a execução
original (que ocorreu numa sessão de ChatGPT, fora desta conversa).

## Origem

O Originador (técnico de segurança do trabalho, Manserv/Sylvamo) já
conduziu, em pelo menos uma ocasião real, um treinamento em que a IA
(ChatGPT, não a LUNA) ministrou a parte teórica de um treinamento de
segurança do trabalho, enquanto o Originador conduziu a parte prática
presencialmente. O material de entrada incluía documentos reais do
próprio acervo de trabalho: apostila de treinamento, APR, material de
integração de segurança, entre outros.

## O método (como relatado, passo a passo)

1. Upload dos materiais reais de treinamento (apostila, APR, integração
   de segurança, outros documentos já existentes).
2. A IA explica a matéria, tópico por tópico.
3. Para cada tópico abordado, a IA faz 3 perguntas de verificação.
4. Ao final de todos os tópicos, a IA faz uma rodada de revisão
   consolidada: 1 pergunta por tópico.
5. Critério de aprovação na revisão: o aluno precisa acertar pelo menos
   80% das questões.
   5.1. Reforço por tópico, durante a explicação inicial (passo 3): se
        o aluno erra 2 das 3 perguntas de um tópico, a IA explica a
        matéria daquele tópico novamente e questiona sobre o
        entendimento de forma socrática (perguntas que levam o aluno a
        articular o raciocínio, não repetição direta da mesma
        pergunta).
   5.2. Reforço na revisão final (passo 4), se o aluno não atinge 80%:
        a IA separa as questões que o aluno respondeu incorretamente,
        explica novamente a matéria referente a cada questão, e
        esclarece a questão em si reformulando-a de 2 a 3 maneiras
        diferentes, em linguagem coloquial e menos técnica — o
        objetivo explícito é distinguir erro por não saber a resposta
        de erro por não ter entendido a pergunta.
6. Captura de conhecimento tácito (o elemento mais novo do método):
   quando a IA identifica uma lacuna ou tem dúvida sobre como um assunto
   é tratado na prática real (não coberto, ou coberto de forma
   incompleta, pelo material de origem), ela pergunta ao aluno como ele
   trata aquele assunto no dia a dia da operação — não é o aluno
   perguntando à IA, é o inverso.
7. A resposta do aluno é tratada como candidata a conhecimento, não como
   fato aceito de imediato. Validação por um de dois caminhos:
   a. Confere contra o material/documento já existente, ou
   b. Fica pendente de esclarecimento posterior com o Originador
      (instrutor humano).
8. Depois da sessão teórica: prova teórica escrita e prova prática
   presencial, ambas aplicadas pelo Originador.

## Resultado de campo

Aplicação real confirmada: os alunos foram aprovados tanto na prova
teórica escrita quanto na prova prática presencial. Este é o dado que
eleva o método de "ideia" para "hipótese com evidência de campo" — mas a
evidência existe fora da arquitetura LUNA (rodou com ChatGPT, sem
Convergia, sem Cognitive Engine, sem Guardian/Hipocampo envolvidos).

## Por que isto importa para o Convergia e para a LUNA como um todo

O Convergia já tem uma aba "Conhecimento" (`/api/convergia/training`) que
alimenta o Guardian/Hipocampo com conteúdo consolidado — o caminho de
ingestão do material de treinamento (passo 1 do método) já tem um lugar
natural na arquitetura existente, sem inventar nada novo.

A condução da teoria em si (passos 2 a 7) pertenceria ao Cognitive Engine
(o motor de chat), não ao Convergia — são rotas irmãs em `luna-core`
(`/api/convergia/*` e `/api/chat`), não o mesmo sistema. Isto sugere que
o "MVP de treinamento adaptativo" não é uma capability nova isolada, é
uma composição de duas capacidades que já existem em esqueleto (Convergia
para ingestão + Cognitive Engine para condução), mais um mecanismo novo
(o loop de pergunta-ao-aluno → validação → promoção a conhecimento) que
não existe em nenhum dos dois hoje.

## Disciplina de proveniência (extensão por analogia, não decisão nova)

Esse mecanismo de captura (passo 6-7) tem disciplina de proveniência
compatível com o que já existe na Constituição para outros casos
(ADR-014 Emenda 1, aplicado também a CONV-009/leitura de foto no
Roadmap): a resposta do aluno nasceria como `unverified` e só seria
promovida a `corroborated` após validação contra documento real ou
confirmação do Originador — nunca aceita direto na palavra do aluno.
Isto é extensão por analogia de um princípio já ratificado, não uma
decisão nova sendo tomada aqui.

## Pontos que estavam em aberto — resolvidos (2026-07-23)

**O que a IA faz com a resposta do aluno enquanto a validação não
chega:** não infere o conhecimento — fica em estado de espera explícito
("como numa fila de framework", nas palavras do Originador). A resposta
do aluno não é usada como fato em nenhuma outra conversa, com nenhum
outro aluno, até ser validada por um dos dois caminhos do passo 7. Isto
é o mesmo comportamento de `unverified` já usado em CONV-009/ADR-014
Emenda 1 — não promove a `corroborated` sem confirmação, e enquanto
isso, não propaga.

**O que acontece se o aluno não atinge 80% na revisão final:** não é
loop de mastery learning que insiste indefinidamente, nem é só
relatório de diagnóstico sem ação — é uma combinação: a IA identifica
exatamente quais questões o aluno errou, reensina a matéria
correspondente, e reformula a própria pergunta de 2-3 formas diferentes
em linguagem mais simples — porque o Originador quer isolar se o erro é
de conteúdo (aluno não sabe) ou de formulação (aluno não entendeu o que
foi perguntado). Isto é distinto do reforço socrático do passo 5.1 (que
acontece durante a explicação inicial, tópico a tópico) — aqui o foco é
reformulação de linguagem, não apenas reexplicação de conteúdo.

## O que ainda não está definido (não fabricado, sinalizado como aberto)

- Nenhuma decisão de arquitetura (ADR) foi tomada ainda sobre como ligar
  Convergia → Cognitive Engine → Guardian neste fluxo específico. Este
  documento é o registro do método e do resultado de campo — a
  especificação técnica (que capability, que contrato, que rota) é passo
  seguinte, não coberto aqui.
- Não especificado: depois de quantas rodadas de reforço (5.1 ou 5.2)
  sem sucesso a IA para de insistir e escala para o Originador
  presencialmente — o método, como relatado, não menciona um limite.

## Próximo passo sugerido

Os dois pontos pedagógicos centrais já estão resolvidos — este documento
está pronto para promoção a Theory (segundo passo do pipeline
Hypothesis → Research → Theory → Architecture (ADR) → Implementation).
O único ponto remanescente (limite de rodadas de reforço) pode ser
resolvido na própria Theory, não bloqueia a promoção.
