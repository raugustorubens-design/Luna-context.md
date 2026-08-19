# Canais e a idade da fonte

**19/08/2026**

---

## Os três canais têm trabalhos diferentes

| Canal | Trabalho | O que vai por ele |
|---|---|---|
| **E-mail** | **Formalizar** | Resumo periódico, aviso com prazo, notificação que precisa deixar rastro |
| **WhatsApp** | **Agilizar** | Desvio com prazo curto e ação clara — e só isso |
| **Painel** | **Divulgar** | Panorama, tendência, o que está desligado e por quê |

### O e-mail não é burocracia — é proteção

Em SSMA, **notificação formal tem peso.** O e-mail estabelece que o cliente foi avisado,
com data e conteúdo. Se algo acontecer depois, a diferença entre "eu avisei" e "consta que
foi avisado em 12/03" é a diferença entre palavra e prova.

Isso protege o técnico tanto quanto informa o gestor. É argumento de venda que não parece
argumento de venda.

### O WhatsApp precisa de regra, senão morre

O risco é conhecido: se tudo vai para o WhatsApp, nada é lido em duas semanas.

Regra que eu proporia — e vale travar antes de existir:

> **Só vai por WhatsApp o que tem prazo e tem ação.**
> *"Certificado de espaço confinado do turno B vence em 15 dias — 3 pessoas"* vai.
> *"Sua matriz não é atualizada há 7 meses"* não vai; isso é e-mail.

Se o desvio não tem o que fazer hoje, ele não interrompe ninguém.

### O painel é onde o sinal desligado mora

É a superfície onde o cliente vê o que **não** está sendo percebido, com o motivo. Não
cabe em e-mail nem em mensagem — precisa ser consultável, não empurrado.

---

## Sobre a idade da fonte — eu estava simplificando

Você perguntou se vale questionar a fonte de verdade estar desatualizada. **Vale, mas
idade absoluta é sinal fraco**, e eu propus mal quando sugeri isso como primeiro sinal.

Uma matriz de treinamento parada há sete meses pode estar perfeitamente correta: ninguém
foi contratado, nenhuma atividade mudou, nenhum certificado venceu. **Avisar sobre isso é
cobrança, não percepção** — e o produto que cobra sem evidência é desligado.

### Os três casos em que idade é sinal legítimo

**1 · Prazo normativo — aí idade é a regra, não proxy.** Documento com periodicidade
exigida por norma tem data de revisão obrigatória. Não é suspeita: é obrigação vencendo, e
é aritmética de data pura.

**2 · Idade relativa entre documentos acoplados.** A APR foi revisada em março; o
procedimento que a executa é de outubro do ano passado. **Um mudou, o outro não.** Isso não
é idade — é incoerência entre duas fontes, e é evidência.

**3 · Divergência contra observação.** A matriz lista doze pessoas; a ronda registrou
atividade num setor com nome que não está nela. Aqui nem se fala em idade: **a fonte está
provadamente errada**, não velha.

### O que isso muda no princípio

Os três casos são determinísticos — data, comparação de datas, diferença de conjuntos.
Nenhum precisa de modelo. **Idade sem referência é o único que precisaria de julgamento, e
é exatamente o que sai.**

Isso reforça o que você estabeleceu: o Sense não opina. Se não há regra que sustente o
aviso, não há aviso.

---

## Corrigindo minha sugestão de primeiro sinal

Eu tinha proposto *"sua fonte está velha"* por ser o mais fácil. **Troco por: prazo
normativo vencendo.**

Motivos: funciona no dia um com qualquer cliente, igual ao anterior; é aritmética de data
pura; **é indiscutível** — o prazo é da norma, não nosso; e o cliente reconhece o valor
imediatamente, porque é o tipo de coisa que dá multa.

E ele já demonstra os três canais de uma vez: entra no painel quando falta muito, vira
e-mail quando entra no prazo, e vira WhatsApp quando falta pouco. **O mesmo desvio muda de
canal conforme a urgência** — o que é a melhor demonstração possível do modelo que você
acabou de descrever.

---

## Decisão ratificada — faixas de prazo por sinal

**Ratificada pelo Arquiteto em 19/08/2026.**

Cada sinal declara suas próprias faixas de prazo. **Canal é consequência da faixa, nunca
propriedade do sinal.** O mesmo desvio atravessa painel, e-mail e WhatsApp conforme se
aproxima do vencimento.

### O que define a faixa — e não é o prazo

A faixa não sai do vencimento. Sai do **tempo necessário para agir**.

Um treinamento de oito horas exige agendar com fornecedor, tirar gente do turno e
remanejar escala — precisa de semanas. Atualizar a data de revisão de um documento precisa
de uma tarde. **Avisar os dois com a mesma antecedência erra nos dois sentidos:** cedo
demais vira ruído, tarde demais vira aviso inútil.

Regra: **a primeira faixa começa no tempo de ação mais o dobro dele de folga.** Se agendar
o treinamento leva 15 dias, o aviso começa em 45.

Isso torna o número defensável. Quando alguém perguntar por que 45 e não 30, a resposta é
o tempo de agendamento — não uma escolha nossa.

### Escada padrão, quando o sinal não declara a sua

| Faixa | Canal | Leitura |
|---|---|---|
| Fora do prazo de ação | **Painel** | Está no radar, não exige nada hoje |
| Dentro do prazo de ação | **E-mail** | Precisa entrar na agenda, e fica registrado |
| Menos da metade do prazo de ação | **WhatsApp** | Só se houver ação clara para hoje |
| Vencido | **E-mail**, sempre | O registro formal importa mais que a pressa |

**Vencido volta para e-mail de propósito.** Depois do vencimento o valor não é agilidade —
é constar que foi comunicado, com data.

### O que ainda é seu

O **tempo de ação de cada tipo de pendência** é conhecimento de campo, não de engenharia:
quanto leva, na prática, agendar um treinamento de altura; revisar uma APR; substituir um
controle apontado em ronda.

Com esses números, as faixas saem por conta. **Sem eles, a escada padrão roda com o
tempo de ação declarado como desconhecido — e o sinal fica só no painel**, que é o
comportamento seguro: não interrompe ninguém com base em chute.
