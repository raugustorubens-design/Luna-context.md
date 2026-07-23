# Treinamento Adaptativo com Captura de Conhecimento Tácito — Research Hypothesis

Status: Research Hypothesis, com resultado de campo real confirmando a
teoria (não é hipótese não-testada — o método já rodou fora da
arquitetura LUNA, com resultado positivo mensurado). Não implementado no
Convergia/Cognitive Engine ainda. Registrado a partir de relato direto do
Originador (2026-07-23), Engineer presente na sessão que extraiu e
organizou o método, sem ter presenciado a execução original (que ocorreu
numa sessão de ChatGPT, fora desta conversa).

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

## Por que está aberto (não fabricado)

- O que a IA faz com a resposta do aluno enquanto a validação não chega
  (nem bate com documento, nem chegou confirmação do Originador a
  tempo): usa como provisória na própria conversa (arriscando repetir
  algo não confirmado a outro aluno), ou aguarda em silêncio até
  confirmação? Não foi especificado pelo Originador ainda.
- Se o aluno não atinge 80% na revisão final: não foi especificado se a
  IA repete explicação + nova rodada de perguntas até o aluno passar
  (loop fechado de mastery learning), ou se apenas reporta o resultado
  (quais tópicos falharam) como insumo para o Originador tratar na parte
  prática presencial.
- Nenhuma decisão de arquitetura (ADR) foi tomada ainda sobre como ligar
  Convergia → Cognitive Engine → Guardian neste fluxo específico. Este
  documento é o registro do método e do resultado de campo — a
  especificação técnica (que capability, que contrato, que rota) é passo
  seguinte, não coberto aqui.

## Próximo passo sugerido

Arquitetar como Theory (segundo passo do pipeline Hypothesis → Research
→ Theory → Architecture (ADR) → Implementation) depois que o Originador
esclarecer os dois pontos em aberto acima. Só depois disso caberia um
ADR formal.
