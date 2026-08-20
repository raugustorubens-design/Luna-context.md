# Modo demonstração do Safety Walk

**Caminho:** `GENESIS/pacotes/2026-08-19-ronda-demo.md`
**Estado:** pronto · **depende de** `2026-08-19-acesso-publico.md` etapa 3

> ## REPOSITÓRIO-ALVO
>
> **`raugustorubens-design/luna-frontend`** — exclusivamente.
> `luna-core` **não muda**: o modo demonstração nunca chega ao servidor.

---

## O que é

Uma rota pública onde qualquer visitante monta uma ronda inteira — flags, achados,
classificação, fotos, o gate de conclusão — e vê o relatório que sairia. **Sem nada sair do
aparelho dele.**

Faz sentido junto com o fechamento do `/ronda`: a ferramenta real fica trancada, e a
demonstração fica aberta.

---

## A regra que governa o pacote

> **O bloqueio é na origem, não na interface.**

Esconder o botão de enviar não basta. Se a ronda de demonstração entrar na mesma fila local,
ela **sobe depois** — quando o Arquiteto abrir o aplicativo no aparelho dele, ou quando o
próprio visitante voltar ao site. Dado de estranho no banco de produção, sem ninguém ter
clicado em nada errado.

Duas travas independentes, e as duas precisam existir:

**a) Armazenamento separado.** Banco IndexedDB com nome próprio — `luna-ronda-demo` — e não
o mesmo com uma marcação. Nome diferente torna a mistura impossível, não improvável.

**b) Nenhuma chamada de escrita, no cliente de rede.** O módulo que fala com o servidor
recusa qualquer escrita em modo demonstração — no ponto onde a requisição é montada, não
onde o botão é desenhado. Se alguém acrescentar um botão novo daqui a seis meses, ele já
nasce bloqueado.

---

## Etapa 1 · A rota

**`/demo`**, pública. Não `/ronda/demo` — o `matcher` do middleware cobre `/ronda/:path*` e
pegaria a demonstração junto.

Reusa os componentes do wizard. Não duplique tela: uma cópia divergiria em duas semanas.

O modo entra por **propriedade explícita** repassada aos componentes, não por leitura de
rota lá dentro. Componente que descobre sozinho onde está é componente que erra quando
alguém o move.

## Etapa 2 · Isolamento

Ao entrar em `/demo`:

- Abrir `luna-ronda-demo`, **apagando o que houver** — cada visita começa limpa
- Nunca tocar no banco real, nem para ler
- Ao sair ou recarregar, descartar

**O service worker não deve cachear `/demo` como aplicativo instalável.** Ele não é o
produto; é a vitrine.

## Etapa 3 · Bloqueio de rede

No cliente de rede, em modo demonstração:

| Chamada | Comportamento |
|---|---|
| Envio da ronda | recusa local, sem requisição |
| Upload de foto | recusa local, sem requisição |
| Sugestão por IA sobre a foto | **decisão pendente — ver abaixo** |
| Leitura de flags e biblioteca | permitida, é só leitura |

A recusa é **silenciosa para o fluxo** e explícita na tela: o visitante conclui a ronda
normalmente e recebe a prévia, sem erro vermelho.

## Etapa 4 · A prévia do relatório

Ao concluir, mostrar **na tela** como o relatório ficaria: cabeçalho, achados, fotos,
classificação com as cores sólidas.

**Sem download.** Prévia em tela é melhor demonstração que arquivo baixado — a pessoa vê na
hora, sem abrir outro aplicativo, e não fica com um documento solto que parece oficial.

No fim da prévia, um convite discreto para falar com você.

## Etapa 5 · Sinalização que não dá para confundir

Alguém vai fazer uma ronda de verdade achando que salvou. Isso não pode acontecer por
distração.

- **Faixa fixa no topo**, visível em todas as etapas: *demonstração — nada é salvo nem enviado*
- **Aviso na entrada**, antes da primeira etapa, dizendo que as fotos não saem do aparelho
- **Aviso no fim**, junto da prévia, repetindo que nada foi enviado
- Ao sair, avisar que os dados serão descartados

Se o visitante levar um susto ao descobrir que nada foi salvo, a sinalização falhou.

---

## Decisão pendente do Arquiteto

**A sugestão por IA sobre a foto entra na demonstração?**

É a parte mais impressionante — a pessoa fotografa e a descrição vem preenchida. Mas cada
leitura consome cota do Groq, que já foi registrada perto da saturação, e uma demonstração
pública é chamada por gente que você não controla.

| Opção | Efeito |
|---|---|
| **Desligada** | Zero custo. A demonstração mostra o fluxo, não a inteligência |
| **Ligada com teto** | Impressiona de verdade. Precisa de limite por sessão e por dia, e de degradar em silêncio ao estourar |

Minha inclinação: **ligada, com teto de três leituras por sessão**, e degradação silenciosa —
sem sugestão é o comportamento normal do produto, então ninguém percebe o limite.

Mas isso é decisão sua: envolve custo e exposição.

---

## Pré-respostas

| Se encontrar | Faça |
|---|---|
| O componente do wizard ler a rota internamente | Extraia para propriedade; não replique a tela |
| O cliente de rede tiver mais chamadas de escrita que as listadas | Bloqueie todas; a lista é mínimo, não teto |
| A fila local for compartilhada por nome fixo | É exatamente o risco — nome próprio para a demonstração |
| A prévia exigir o renderizador do `luna-core` | **Pare e reporte** — a demonstração não chama o servidor |

## Condições de parada

- Isolar o armazenamento exigir mudar o banco real
- A prévia não ser possível sem chamada ao servidor
- O modo demonstração exigir alterar comportamento do `/ronda` real

## Autorização de merge

**Não mergear sem o Arquiteto.** Toca o mesmo código da ferramenta de campo, e o risco de
contaminar a fila real é o mais caro do pacote.

## Critério de pronto

1. Numa janela anônima, fazer uma ronda em `/demo` do começo ao fim, **com fotos**, e ver a
   prévia
2. Confirmar, nas ferramentas do navegador, que **nenhuma requisição de escrita saiu**
3. Recarregar e a ronda de demonstração ter sumido
4. **Portão do Arquiteto:** abrir o `/ronda` real no aparelho e confirmar que a fila
   continua intacta, sem nada da demonstração

O item 4 é o que prova o isolamento. Sem ele, o pacote não fecha.

---

## Fora de escopo

**Ronda de exemplo pré-preenchida.** Melhoraria a demonstração para quem não é da área, mas
é conteúdo, não código — e o conteúdo é seu.

**Métrica de uso da demonstração.** Quantas pessoas concluíram é sinal comercial legítimo,
mas é assunto do Sense.

---

## Memórias geradas

- Modo demonstração precisa de bloqueio na origem, não na interface: botão escondido com
  fila compartilhada envia depois
- Armazenamento isolado por **nome de banco**, não por marcação em registro
- Prévia em tela é melhor demonstração que arquivo baixado, e evita documento solto com cara
  de oficial
