# Curadoria antes de gerar — os dois modelos

**19/08/2026 · desenho**

---

## Os dois modelos, e o que cada um permite

| | **Visual · político** | **Técnico** |
|---|---|---|
| Para quem | o cliente | você, auditoria |
| O que é | apresentação | registro |
| Selecionar o que entra | **sim** — caixa de seleção por achado | não · entra tudo |
| Editar comentário | **sim** | **sim** |
| Excluir achado | pela seleção | **sim**, mas com registro |
| Padrão inicial | nada marcado, ou tudo? *(ver pergunta no fim)* | tudo dentro |

A diferença não é de recurso — é de natureza. **No Visual você escolhe o que mostrar; no
Técnico você só corrige o que ficou errado.** Por isso a seleção existe num e não no outro.

---

## A tela de curadoria

Uma lista de achados, na ordem da ronda. Cada linha traz:

- **Caixa de seleção** — só no Visual
- **Miniaturas das fotos**, com o selo de classificação em cada uma
- **Descrição**, editável ali mesmo
- **Ação recomendada**, editável
- **Classificação e gravidade**, visíveis e **não editáveis** — mudá-las é mudar o achado,
  não o relatório

No Técnico, a caixa de seleção dá lugar a um **excluir** por achado, com confirmação e
campo de motivo.

No rodapé: contagem do que vai entrar, botão **Gerar**, e — no Visual — um aviso quando
alguma **não conformidade** estiver desmarcada. Não impede: avisa.

---

## Onde a edição mora — e esta é a decisão que importa

> **A ronda não muda. O relatório carrega a versão curada.**

A ronda é constatação: o que foi visto naquele dia, naquele lugar. Editar o registro depois
reescreve prova. Num documento que pode ser questionado em auditoria ou processo, isso não
se faz.

Então a curadoria vira um registro próprio, ligado à ronda:

```
convergia_relatorio_curadoria
  ronda_id · modelo · gerado_em
  achados_incluidos[]
  edicoes[]      { achado_id, campo, texto_original, texto_final }
  exclusoes[]    { achado_id, motivo }
```

**O original fica sempre.** É a mesma regra que vale para o resto do projeto — nunca
sobrescrever, sempre registrar com contexto.

E isso resolve um problema prático: gerar o mesmo relatório de novo, seis meses depois,
devolve o mesmo documento. Se a edição tivesse alterado a ronda, você não saberia mais o
que foi registrado em campo e o que foi ajustado na revisão.

---

## Exclusão no Técnico — com rastro

Excluir do Técnico é raro e deve ser difícil de fazer por engano: é o documento de registro.

Casos legítimos: achado duplicado, foto do lugar errado, item lançado por engano no
aparelho.

Por isso o motivo é obrigatório, e o achado excluído **não some da ronda** — só não entra
naquele relatório. Se alguém perguntar depois por que o relatório tem doze achados e a
ronda tem treze, a resposta existe.

---

## O que a curadoria devolve para a LUNA

Aqui está o ganho que não é óbvio.

**O que você tira é dado tão bom quanto o que você mantém.** Um achado registrado em campo e
desmarcado na revisão diz que a leitura estava errada — e diz isso sem ambiguidade nenhuma.
Um texto que você reescreve mostra a diferença entre o que a IA sugeriu e o que você
considera correto, agora com calma, não com o sol na tela.

Pelo critério do `ADR-014 Emenda 1`, **este é o sinal mais forte da cadeia inteira**: mais
que a correção em campo, muito mais que a sugestão aceita em silêncio.

A curadoria é o momento da ratificação. É de lá que sai o melhor material de aprendizado —
e é por isso que construir o relatório serve ao seu objetivo primário, não ao secundário.

---

## Duas perguntas antes do pacote

**1 · No Visual, o que vem marcado por padrão?**

Tudo marcado, e você desmarca o que não quer — mais rápido quando a ronda é boa. Ou nada
marcado, e você escolhe — mais deliberado, e evita mandar ao cliente algo que passou
batido.

Minha inclinação: **tudo marcado, menos os Positivos.** O cliente quer ver o que precisa de
ação; o Positivo entra se você quiser mostrar cobertura.

**2 · O Positivo entra no Visual?**

Ontem eu sugeri seção separada no fim. Com a caixa de seleção, isso deixa de precisar de
regra: você marca quando fizer sentido.

---

## Escopo da primeira etapa

Tela de curadoria + geração do **Técnico**, que é o mais simples: sem seleção, só editar e
excluir.

O Visual entra depois e reusa a mesma tela, acrescentando a caixa de seleção — e o mesmo
adaptador, com outro template.
