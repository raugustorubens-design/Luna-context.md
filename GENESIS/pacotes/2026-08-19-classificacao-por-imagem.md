# Classificação por imagem — o que muda, e a decisão que precisa vir antes

**18/08/2026 · proposta do Arquiteto**

---

## O problema que isso resolve, e ele já existe

Hoje a classificação vive no **achado**. Toda foto daquele achado herda o mesmo rótulo.

Numa não conformidade típica você tira duas ou três fotos: uma panorâmica para situar a
área, um detalhe mostrando o problema, às vezes o entorno. **Todas ficam marcadas como
Não Conformidade** — inclusive a panorâmica, que não mostra irregularidade nenhuma.

Isso não incomoda no relatório. Incomoda no acervo: quando essas imagens virarem fonte de
exemplo para LUP e material normativo, a panorâmica entra rotulada como exemplo do errado.
Um acervo com rótulo errado é pior que acervo nenhum — ensina errado.

---

## A decisão que precisa vir antes de tudo: soma ou substitui?

Interpretei que **soma**, e explico por que a substituição quebraria coisas:

| Nível | O que significa | Quem usa |
|---|---|---|
| **Achado** | O **veredito** — o que você concluiu sobre aquela situação | Relatório, gravidade, validação do servidor |
| **Imagem** | O que **aquela imagem mostra** | Acervo de exemplo, borda colorida no relatório |

São perguntas diferentes. O achado responde *"isto está conforme?"*; a imagem responde
*"esta foto mostra o quê?"*.

Se a classificação sair do achado, três coisas quebram: o servidor exige `classificacao`
em todo achado identificado, o par com `gravidade` perde a metade, e o relatório perde o
veredito por achado — que é o que o cliente lê.

**E os dois níveis podem legitimamente divergir.** Um achado de Não Conformidade pode
incluir uma foto Positivo, mostrando o equipamento ao lado feito do jeito certo. Isso não
é inconsistência — **é uma LUP inteira dentro de um achado só.**

**Confirme isso antes de eu escrever o pacote**, porque muda o trabalho por completo.

---

## Os quatro valores — e uma ressalva de nome

Positivo · Atenção · Não Conformidade · **Não Aplicável (somente para registro)**

Os três primeiros são os que já existem, com os hex validados.

O quarto é o que faltava, e é o que salva a panorâmica. Mas o nome me preocupa, e é do seu
domínio, não do meu:

Em auditoria, **"não aplicável" costuma significar que o requisito não se aplica àquele
escopo** — o item não vale ali. O que você está descrevendo é outra coisa: a imagem existe
para situar, não para julgar. Ela se aplica; só não é veredito.

E há um segundo risco de confusão: a ronda já tem o estado "Considerado inexistente" no
achado. Duas negações parecidas em níveis diferentes confundem em campo.

Alternativas que não carregam o outro sentido: **Registro** · **Contexto** ·
**Sem julgamento**.

Não decido — só sinalizo antes de virar rótulo em tela e coluna em banco, porque depois
custa caro trocar.

---

## O padrão de entrada, e uma regra que sai de graça

**O que uma foto nova recebe por padrão?** Duas opções, com efeitos opostos:

- Padrão **herda o achado** — a maioria das fotos realmente mostra o achado, então acerta
  quase sempre; a panorâmica erra até alguém corrigir
- Padrão **Registro** — nunca rotula errado, mas obriga um toque a mais em toda foto de
  verdade, em campo, com luva

Recomendo **herdar**, com uma regra que resolve o resto:

> **Só imagem com classificação escolhida explicitamente entra no acervo de exemplo.**
> A herdada serve de prova no relatório, mas não vira exemplo em LUP nem em normativo.

Assim o campo não ganha fricção, e o acervo só recebe imagem que alguém olhou e decidiu.
**O ato deliberado é o que qualifica** — não o valor do rótulo.

---

## O que custa

| Onde | O quê |
|---|---|
| `convergia_ronda_fotos` | Coluna nova de classificação e uma de origem (herdada ou explícita). Migration em arquivo **antes** de aplicar — `ENG-036`/`DRIFT-001` |
| Contrato do achado | `fotoIds` é `string[]` hoje. **Não troque por objeto** — quebra item já na fila. Campo novo opcional, chaveado por `fotoId` |
| Wizard | Seletor por miniatura. Em 64px, com luva, ciclar entre quatro estados erra — toque abre escolha, não alterna |
| Relatório | Borda ou selo por foto, com as cores sólidas já validadas |
| Servidor | `requiredWhenIdentified` **não muda** — classificação de imagem nunca é obrigatória, mesma disciplina da foto |

Nada aqui é grande. O maior cuidado é o contrato: um campo novo opcional mantém item
antigo da fila válido, e um item sem o campo simplesmente herda.

---

## O que isso destrava

**Acervo limpo para LUP.** A panorâmica para de virar exemplo do errado, e cada metade da
LUP vem de imagem que alguém marcou de propósito.

**Relatório mais legível.** Hoje as fotos de um achado aparecem iguais. Com borda por
classificação, quem lê vê na hora qual foto é o problema e qual é o contexto.

**E a comparação ganha os dois lados.** Um Positivo explícito é o padrão visual contra o
qual a próxima ronda compara — a metade que faltava para o mecanismo de comparação de
imagem que ainda não existe.

---

## Duas perguntas antes do pacote

1. **Soma ou substitui?** Interpretei que soma — achado mantém o veredito, imagem ganha o
   dela. Confirme
2. **O nome do quarto valor** — "Não Aplicável" ou algo sem o outro sentido de auditoria

Com as duas, escrevo o pacote. Ele entra depois da correção da câmera, que ainda bloqueia
o uso — mas antes de qualquer coisa de LUP, porque é ele que produz o acervo que a LUP vai
consumir.
