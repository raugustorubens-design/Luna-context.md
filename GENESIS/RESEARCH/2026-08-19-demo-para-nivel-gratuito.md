# Do demo ao nível gratuito

**19/08/2026 · nota de desenho, antes de virar pacote**

---

## O que muda

O pacote anterior garantia uma coisa forte: **nada sai do aparelho**. Com o relatório
gratuito, o dado precisa chegar ao servidor — o renderizador está no `luna-core`.

Então passam a existir dois momentos distintos, e a fronteira entre eles é o que importa:

| Momento | O que acontece |
|---|---|
| **Montar a ronda** | Tudo local. Nada sai. Como no pacote anterior |
| **Pedir o relatório** | O visitante decide entregar o dado. Aí sobe |

**Manter o local-first até esse instante é o que preserva a promessa.** A pessoa explora
sem compromisso, e o envio acontece por escolha dela, não por padrão.

---

## O limite de "um relatório" não se sustenta sozinho

Qualquer trava anônima — armazenamento do navegador, endereço de rede, impressão digital do
aparelho — cai em trinta segundos: apagar dados do site, aba anônima, outro aparelho.

**Mas isso importa menos do que parece**, por dois motivos.

Primeiro: quem contorna a trava não ia comprar de qualquer forma.

Segundo, e é o que muda o desenho: **o relatório gratuito não é para bloquear — é para
capturar.** Pedir o e-mail antes de gerar te dá um contato qualificado, de alguém que
montou uma ronda inteira e quer o documento. Isso vale mais que impedir o décimo relatório
de um curioso.

O limite vira efeito colateral da conta, não um mecanismo próprio.

---

## O risco que você não perguntou

**Ronda de estranho no seu banco significa dado de terceiro sob sua guarda.**

Fotos de planta industrial de outra empresa, achados de segurança, possivelmente pessoas
enquadradas. No Brasil isso te coloca na posição de quem responde pelo dado — com dever de
guarda, de exclusão quando pedirem, e de não misturar com o seu.

Consequências práticas, e nenhuma é cara **se for feita desde o começo**:

- Dado de nível gratuito **em separado** do seu — outra tabela ou marcação de origem, nunca
  no mesmo balaio
- **Prazo de descarte** declarado e cumprido. Trinta dias é razoável, e é o mesmo mecanismo
  dos sete dias do relatório
- Aviso de privacidade curto e honesto, antes do envio
- Dado de nível gratuito **nunca** alimenta o Hipocampo. É de outra pessoa

Fazer depois custa dez vezes mais, porque implica separar o que já se misturou.

---

## A versão mínima — e ela não tem cobrança

**Não construa pagamento para descobrir se alguém paga.**

O primeiro passo que eu faria:

1. A demonstração continua **inteiramente local**, como no pacote anterior
2. No fim, junto da prévia: *"quer este relatório em documento?"*
3. Um campo de e-mail e uma frase sobre o que acontece com o dado
4. **Você recebe o aviso e gera manualmente**, com o gerador que já existe

Zero código de cobrança, zero código de limite, zero conta de usuário. E você descobre a
coisa que importa: **quantas pessoas chegam ao fim e pedem.**

Se ninguém pedir, você economizou o sistema de pagamento inteiro. Se muita gente pedir,
você tem os contatos e um número para dimensionar o resto.

**Manual até doer.** Quando gerar à mão virar incômodo, aí vale automatizar — e aí você já
sabe o volume, o perfil e o que essas pessoas perguntam.

---

## O que precisa de decisão antes de virar código

Nenhuma delas é técnica:

| Decisão | Por que trava o desenho |
|---|---|
| **O que é gratuito e o que é pago** | Um relatório é o gratuito? Ou uma ronda por mês? Muda o que a conta guarda |
| **Assinatura ou por documento** | Muda o modelo de dados inteiro |
| **Nota fiscal** | Você vai emitir? Isso decide o meio de pagamento |
| **Quem é o cliente** | Técnico autônomo ou empresa? Muda preço, contrato e quem assina |
| **Retenção do dado gratuito** | Quanto tempo, e o que acontece se a pessoa virar cliente |

A quarta é a que mais muda tudo. Técnico autônomo compra sozinho, no cartão, e quer preço
baixo. Empresa quer proposta, nota e contrato — e aí o site precisa de outra conversa, não
de um botão.

---

## Recomendação de sequência

1. **Demonstração local**, como está no pacote — sem envio, sem download, com prévia
2. **Campo de e-mail** no fim, com aviso de privacidade. Você gera manual
3. *(esperar)* — medir quantos pedem e quem são
4. Só então: conta, limite, cobrança

O passo 2 é uma tela e um e-mail. Os passos 3 e 4 dependem do que o 2 mostrar.

**E a separação do dado de terceiro entra já no passo 2**, não depois. É o único item desta
nota que não pode esperar, porque desfazer mistura custa muito mais que evitá-la.

---

## O que eu escreveria como pacote agora

Só o passo 2, acrescentado ao pacote da demonstração:

- Campo de e-mail na prévia, com aviso curto de privacidade
- O pedido chega até você — e-mail ou uma linha em tabela própria
- **Nenhuma foto sobe nesse momento.** Você gera a partir do que a pessoa descrever, ou
  pede as fotos por outro canal

Isso mantém a promessa de que nada sai do aparelho, te dá o contato, e não constrói nada que
possa virar desperdício se o modelo mudar.

Se preferir que a foto suba junto para você gerar sem depender da pessoa, dá — mas aí o
aviso de privacidade e a separação do dado passam a ser obrigatórios no mesmo pacote, não
depois.
